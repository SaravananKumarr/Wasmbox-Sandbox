from app.compiler.ast_scanner import ASTSecurityScanner


def test_malicious_subprocess():
    scanner = ASTSecurityScanner()
    result = scanner.scan("import subprocess; subprocess.run(['ls'])")
    assert result["blocked"] is True


def test_malicious_socket():
    scanner = ASTSecurityScanner()
    result = scanner.scan("import socket; s = socket.socket()")
    assert result["blocked"] is True
