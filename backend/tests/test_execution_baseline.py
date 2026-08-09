"""Baseline behavior tests for the Week 1-2 execution flow."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.sandbox.engine import execute_plugin


class ExecutionBaselineTests(unittest.TestCase):
    def test_printed_output_is_returned(self):
        result = execute_plugin("print('Hello from WasmBox!')")

        self.assertEqual(result["status"], "Success")
        self.assertEqual(result["return_code"], 0)
        self.assertEqual(result["output"], "Hello from WasmBox!")

    def test_input_payload_is_available_to_the_plugin(self):
        result = execute_plugin("print(INPUT)", '{"event": "baseline"}')

        self.assertEqual(result["status"], "Success")
        self.assertEqual(result["output"], '{"event": "baseline"}')

    def test_invalid_syntax_returns_a_failure_response(self):
        result = execute_plugin("print(")

        self.assertEqual(result["status"], "Failed")
        self.assertEqual(result["return_code"], 126)
        self.assertIn("SyntaxError", result["output"])

    def test_blocked_import_is_rejected_before_execution(self):
        result = execute_plugin("import os\nprint(os.getcwd())")

        self.assertEqual(result["status"], "Failed")
        self.assertEqual(result["return_code"], 126)
        self.assertIn("Blocked import 'os'", result["output"])

    def test_infinite_loop_returns_a_timeout_failure(self):
        with patch("app.sandbox.engine.settings.SANDBOX_TIMEOUT_SECONDS", 0.05):
            result = execute_plugin("while True:\n    pass")

        self.assertEqual(result["status"], "Failed")
        self.assertEqual(result["return_code"], 124)
        self.assertEqual(result["error_message"], "Execution timed out")


if __name__ == "__main__":
    unittest.main()
