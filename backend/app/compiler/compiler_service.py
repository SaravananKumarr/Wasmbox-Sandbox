import os
import uuid
import subprocess
from pathlib import Path

PLUGIN_DIR = "storage/plugins"
BUILD_DIR = "storage/build"

os.makedirs(PLUGIN_DIR, exist_ok=True)
os.makedirs(BUILD_DIR, exist_ok=True)


class CompilerService:

    EXTENSIONS = {
        "python": ".py",
        "rust": ".rs",
        "c": ".c",
        "cpp": ".cpp"
    }

    def save_plugin(self, source_code: str, language: str):

        extension = self.EXTENSIONS.get(language.lower())

        if not extension:
            raise Exception("Unsupported language")

        filename = f"{uuid.uuid4()}{extension}"

        filepath = os.path.join(PLUGIN_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(source_code)

        return filepath

    def compile(self, filepath: str):

        extension = Path(filepath).suffix

        if extension == ".rs":
            return self.compile_rust(filepath)

        raise Exception("Compilation not supported for this language")

    def compile_rust(self, filepath: str):

        output_file = os.path.join(
            BUILD_DIR,
            f"{uuid.uuid4()}.wasm"
        )

        command = [
            "rustc",
            "--target",
            "wasm32-wasip1",
            filepath,
            "-O",
            "-o",
            output_file,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        return output_file


compiler_service = CompilerService()