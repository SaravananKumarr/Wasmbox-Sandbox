import os
import uuid


PLUGIN_DIR = "storage/plugins"

os.makedirs(PLUGIN_DIR, exist_ok=True)


def save_source_code(source_code: str, extension: str = "py") -> str:
    """
    Save plugin source code to disk.
    Returns the saved file path.
    """

    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(PLUGIN_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(source_code)

    return filepath