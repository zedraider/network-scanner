"""
Тесты для Network Scanner
"""

import pytest
from src.network_scanner import NetworkScanner

def test_scanner_initialization():
    """Тест инициализации сканера"""
    scanner = NetworkScanner()
    assert scanner.network == "192.168.1.0/24"
    assert scanner.timeout == 2
    assert scanner.threads == 50
    
def test_scanner_custom_params():
    """Тест сканера с кастомными параметрами"""
    scanner = NetworkScanner(
        network="192.168.0.0/24",
        timeout=1,
        threads=10
    )
    assert scanner.network == "192.168.0.0/24"
    assert scanner.timeout == 1
    assert scanner.threads == 10

def test_port_check():
    """Тест проверки портов"""
    scanner = NetworkScanner()
    
    # Локальные тесты (не пытаемся реально подключиться)
    assert 80 in scanner.common_ports
    assert 443 in scanner.common_ports
    assert 8080 in scanner.common_ports