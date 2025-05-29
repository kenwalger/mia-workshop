import os
import nbformat
# Try to import ContentsManager from pgcontents.api, then directly from pgcontents
try:
    from pgcontents.api import ContentsManager
except ImportError:
    from pgcontents import ContentsManager # Fallback import
from urllib.parse import urlparse

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