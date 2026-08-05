import subprocess


class SandboxExecutor:

    def execute(
        self,
        wasm_path: str,
        stdin: str | None = None,
    ):
        command = [
            "wasmtime",
            wasm_path,
        ]

        try:
            result = subprocess.run(
                command,
                input=stdin,
                capture_output=True,
                text=True,
                timeout=5,
            )

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "failed",
                "stdout": "",
                "stderr": "Execution timeout",
            }

        except Exception as e:
            return {
                "status": "failed",
                "stdout": "",
                "stderr": str(e),
            }


sandbox_executor = SandboxExecutor()