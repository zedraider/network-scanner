"""
Конфигурация pytest для тестов Network Scanner
"""

import pytest
import sys
import os

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_scanner():
    """Фикстура для создания экземпляра NetworkScanner"""
    from network_scanner import NetworkScanner
    return NetworkScanner()

@pytest.fixture
def sample_router_data():
    """Фикстура с примером данных роутера"""
    return {
        'ip': '192.168.1.1',
        'port': 80,
        'url': 'http://192.168.1.1:80',
        'status_code': 200,
        'title': 'Router Admin Panel',
        'server': 'nginx',
        'content_type': 'text/html',
        'is_router': True,
        'content_length': 1500
    }

@pytest.fixture
def sample_device_data():
    """Фикстура с примером данных обычного устройства"""
    return {
        'ip': '192.168.1.100',
        'port': 80,
        'url': 'http://192.168.1.100:80',
        'status_code': 200,
        'title': 'Web Server',
        'server': 'Apache',
        'content_type': 'text/html',
        'is_router': False,
        'content_length': 800
    }

@pytest.fixture
def mock_requests_response():
    """Фикстура для создания mock response requests"""
    class MockResponse:
        def __init__(self, status_code=200, text="", headers=None):
            self.status_code = status_code
            self.text = text
            self.headers = headers or {}
            self.content = text.encode('utf-8')
            self.encoding = 'utf-8'
        
        def json(self):
            import json
            return json.loads(self.text)
    
    return MockResponse