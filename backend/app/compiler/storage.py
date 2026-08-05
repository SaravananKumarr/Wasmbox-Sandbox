import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile

# Directories
PLUGIN_DIR = "storage/plugins"
BUILD_DIR = "storage/build"

os.makedirs(PLUGIN_DIR, exist_ok=True)
os.makedirs(BUILD_DIR, exist_ok=True)


def save_source_code(
    source_code: str,
    extension: str = "py",
) -> str:
    """
    Save plugin source code to disk.
    Returns the saved file path.
    """

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(
        PLUGIN_DIR,
        filename,
    )

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(source_code)

    return filepath


def save_uploaded_wasm(file: UploadFile) -> str:
    """
    Save an uploaded WASM file.

    Returns:
        Path of saved wasm file.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    if not file.filename.lower().endswith(".wasm"):
        raise HTTPException(
            status_code=400,
            detail="Only .wasm files are allowed."
        )

    filename = f"{uuid.uuid4()}.wasm"

    filepath = os.path.join(
        BUILD_DIR,
        filename,
    )

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return filepath