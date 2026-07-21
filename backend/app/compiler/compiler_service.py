import os

from app.compiler.storage import save_source_code


class CompilerService:
    """
    Handles plugin source storage and compilation.
    """

    def save_plugin(self, source_code: str, language: str) -> str:
        extension = {
            "python": "py",
            "rust": "rs",
            "c": "c",
            "cpp": "cpp",
        }.get(language, "txt")

        return save_source_code(source_code, extension)

    def compile(self, filepath: str) -> str:
        """
        Placeholder for WebAssembly compilation.
        """

        wasm_path = os.path.splitext(filepath)[0] + ".wasm"

        # Real compilation will be added later.
        with open(wasm_path, "w", encoding="utf-8") as file:
            file.write("WASM PLACEHOLDER")

        return wasm_path


compiler_service = CompilerService()