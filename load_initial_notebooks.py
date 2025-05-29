import os
import nbformat
from urllib.parse import urlparse

ContentsManager = None # Initialize to None

print("Attempting to import ContentsManager from pgcontents.api...")
try:
    from pgcontents.api import ContentsManager as CM_api
    ContentsManager = CM_api
    print("Successfully imported ContentsManager from pgcontents.api")
except ImportError as e_api:
    print(f"Failed to import from pgcontents.api: {e_api}")
    print("Attempting to import ContentsManager directly from pgcontents...")
    try:
        from pgcontents import ContentsManager as CM_direct
        ContentsManager = CM_direct
        print("Successfully imported ContentsManager directly from pgcontents")
    except ImportError as e_direct:
        print(f"Failed to import directly from pgcontents: {e_direct}")
        print("CRITICAL: Could not import ContentsManager. Exiting notebook load script.")
        # exit(1) # Optionally exit if it's critical and no other action can be taken

if ContentsManager is None:
    print("Aborting notebook load: ContentsManager could not be imported.")
    # We might want to exit here if this is a hard requirement for the script to run
else:
    def load_notebook():
        notebook_path_in_repo = "notebooks/main.ipynb" # Assuming your notebook is here
        notebook_path_in_jupyter = "main.ipynb"      # How it will appear in Jupyter root

        if not os.path.exists(notebook_path_in_repo):
            print(f"Notebook file not found at {notebook_path_in_repo}. Skipping initial load.")
            return

        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            print("DATABASE_URL not set. Skipping initial notebook load.")
            return

        # pgcontents expects postgresql://, Heroku provides postgres://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        print(f"Attempting to load {notebook_path_in_repo} into pgcontents...")

        try:
            cm = ContentsManager(db_url=db_url)

            with open(notebook_path_in_repo, "r", encoding="utf-8") as f:
                notebook_content = nbformat.read(f, as_version=4)

            # Create a model for saving
            # Path is the path in Jupyter's file system, including the notebook name
            # Content is the notebook object itself
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