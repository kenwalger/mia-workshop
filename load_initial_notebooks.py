import os
import nbformat
from urllib.parse import urlparse

ActualContentsManager = None # Initialize to None

print("Attempting to import PostgresContentsManager directly from pgcontents...")
try:
    from pgcontents import PostgresContentsManager as PCM_direct
    ActualContentsManager = PCM_direct
    print("Successfully imported PostgresContentsManager directly from pgcontents")
except ImportError as e_direct:
    print(f"Failed to import PostgresContentsManager directly from pgcontents: {e_direct}")
    print("Attempting to import PostgresContentsManager from pgcontents.postgres...")
    try:
        from pgcontents.postgres import PostgresContentsManager as PCM_postgres
        ActualContentsManager = PCM_postgres
        print("Successfully imported PostgresContentsManager from pgcontents.postgres")
    except ImportError as e_postgres:
        print(f"Failed to import from pgcontents.postgres: {e_postgres}")
        print("Attempting to import PostgresContentsManager from pgcontents.core...")
        try:
            from pgcontents.core import PostgresContentsManager as PCM_core
            ActualContentsManager = PCM_core
            print("Successfully imported PostgresContentsManager from pgcontents.core")
        except ImportError as e_core:
            print(f"Failed to import from pgcontents.core: {e_core}")
            print("CRITICAL: Could not import PostgresContentsManager. Exiting notebook load script.")

if ActualContentsManager is None:
    print("Aborting notebook load: PostgresContentsManager could not be imported.")
else:
    def load_notebook():
        notebook_path_in_repo = "notebooks/main.ipynb"
        notebook_path_in_jupyter = "main.ipynb"

        if not os.path.exists(notebook_path_in_repo):
            print(f"Notebook file not found at {notebook_path_in_repo}. Skipping initial load.")
            return

        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            print("DATABASE_URL not set. Skipping initial notebook load.")
            return

        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        print(f"Attempting to load {notebook_path_in_repo} into pgcontents using {ActualContentsManager.__name__}...")

        try:
            cm = ActualContentsManager(db_url=db_url)
            with open(notebook_path_in_repo, "r", encoding="utf-8") as f:
                notebook_content = nbformat.read(f, as_version=4)
            model = {
                "type": "notebook",
                "content": notebook_content,
            }
            cm.save(model, path=notebook_path_in_jupyter)
            print(f"Successfully loaded {notebook_path_in_repo} as {notebook_path_in_jupyter} in pgcontents.")
        except Exception as e:
            print(f"Error loading notebook into pgcontents: {e}")

    if __name__ == "__main__":
        load_notebook() 