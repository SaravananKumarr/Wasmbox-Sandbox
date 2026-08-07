"""Helper to start the backend development server reliably from the
`backend/` directory. It ensures the project root is on `sys.path` so
`import backend` works when the current working directory is `backend/`.

Usage (from project root):
  python backend/start_server.py

Or (from inside `backend/`):
  python start_server.py
"""
from pathlib import Path
import sys
import uvicorn


def main() -> None:
    # Project root is the parent of the folder containing this file
    project_root = Path(__file__).resolve().parent
    # If executed from inside backend/, project_root is backend/; parent is repository root
    repo_root = project_root.parent

    # Ensure repo root is on sys.path so `import backend` resolves to the package
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)

    # Start uvicorn pointing to the package entrypoint
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
