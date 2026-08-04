from app.sandbox.scanner import scan_code


def test_allows_a_simple_plugin():
    assert scan_code("print('hello')") == []


def test_blocks_filesystem_imports():
    violations = scan_code("import os\nos.listdir('.')")
    assert any("Blocked import 'os'" in violation for violation in violations)


def test_blocks_network_imports():
    violations = scan_code("import socket\nsocket.socket()")
    assert any("Blocked import 'socket'" in violation for violation in violations)


def test_blocks_object_graph_escape():
    violations = scan_code("print((()).__class__.__base__)")
    assert any("__class__" in violation for violation in violations)


def test_reports_syntax_errors():
    violations = scan_code("def broken(")
    assert violations[0].startswith("SyntaxError:")
