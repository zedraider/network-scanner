"""
Тесты для функций определения кодировки
"""

import pytest
from src.network_scanner.scanner import NetworkScanner

def test_encoding_detection():
    """Тест определения кодировки"""
    scanner = NetworkScanner()
    
    # Тест с китайским текстом (GBK encoding)
    chinese_text = "小米路由器".encode('gbk')
    
    # Создаем mock response
    class MockResponse:
        def __init__(self, content, headers=None):
            self.content = content
            self.headers = headers or {'Content-Type': 'text/html'}
            self.text = ""
            self.encoding = None
    
    response = MockResponse(chinese_text)
    
    # Тестируем detect_encoding
    encoding = scanner.detect_encoding(response)
    assert encoding in ['gbk', 'gb2312', 'gb18030']
    
def test_fix_encoding_issues():
    """Тест исправления проблем с кодировкой"""
    scanner = NetworkScanner()
    
    # Тест нашего конкретного случая
    garbled = "å°ç±³è·¯ç±å¨"
    fixed = scanner.fix_common_encoding_issues(garbled)
    assert fixed == "小米路由器"
    
    # Тест других распространенных проблем
    test_cases = [
        ("cafÃ©", "café"),
        ("niÃ±o", "niño"),
        ("naÃ¯ve", "naïve"),
    ]
    
    for input_text, expected in test_cases:
        result = scanner.fix_common_encoding_issues(input_text)
        assert result == expected

def test_has_garbled_text():
    """Тест обнаружения испорченного текста"""
    scanner = NetworkScanner()
    
    # Должно обнаружить кракозябры
    assert scanner.has_garbled_text("å°ç±³è·¯ç±å¨") == True
    assert scanner.has_garbled_text("cafÃ©") == True
    assert scanner.has_garbled_text("正常文本") == False  # Нормальный китайский
    assert scanner.has_garbled_text("Normal text") == False