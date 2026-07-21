import pytest
from app.compiler.ast_scanner import ASTSecurityScanner


def test_scan_blocks_os_import():
    scanner = ASTSecurityScanner()
    result = scanner.scan("import os")
    assert result["blocked"] is True
    assert "os" in result["reason"]


def test_scan_allows_safe_code():
    scanner = ASTSecurityScanner()
    result = scanner.scan("print('hello')")
    assert result["blocked"] is False
