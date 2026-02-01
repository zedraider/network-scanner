"""
Тесты для CLI интерфейса (использует argparse, не click)
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

class TestCLI:
    """Тесты командной строки с argparse"""
    
    def test_cli_help(self):
        """Тест вывода справки"""
        from src.network_scanner.cli import main
        
        # Захватываем stdout
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('sys.argv', ['network-scanner', '--help']):
                try:
                    main()
                except SystemExit:
                    pass  # argparse вызывает SystemExit при --help
        
        output = mock_stdout.getvalue()
        assert 'usage:' in output
        assert 'Network web interface scanner' in output
    
    def test_cli_version(self):
        """Тест вывода версии"""
        from src.network_scanner.cli import main
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with patch('sys.argv', ['network-scanner', '--version']):
                try:
                    main()
                except SystemExit:
                    pass
        
        output = mock_stdout.getvalue()
        assert 'network-scanner' in output
        assert '1.0.0' in output
    
    def test_cli_default_parameters(self):
        """Тест запуска с параметрами по умолчанию"""
        from src.network_scanner.cli import main
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            mock_scanner.save_results.return_value = None
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner']):
                main()
            
            MockScanner.assert_called_once_with(
                network="192.168.1.0/24",
                timeout=2,
                threads=50
            )
    
    def test_cli_custom_network(self):
        """Тест запуска с кастомной сетью"""
        from src.network_scanner.cli import main
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner', '--network', '192.168.0.0/24']):
                main()
            
            MockScanner.assert_called_once_with(
                network="192.168.0.0/24",
                timeout=2,
                threads=50
            )
    
    def test_cli_custom_timeout_and_threads(self):
        """Тест запуска с кастомными timeout и threads"""
        from src.network_scanner.cli import main
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner', '--timeout', '5', '--threads', '10']):
                main()
            
            MockScanner.assert_called_once_with(
                network="192.168.1.0/24",
                timeout=5,
                threads=10
            )
    
    def test_cli_with_ports(self):
        """Тест запуска с дополнительными портами"""
        from src.network_scanner.cli import main
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            mock_scanner.common_ports = [80, 443, 8080, 8443, 8888, 8000, 8081]
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner', '--ports', '81,82,8001']):
                main()
            
            # Проверяем что порты были добавлены
            assert 81 in mock_scanner.common_ports
            assert 82 in mock_scanner.common_ports
            assert 8001 in mock_scanner.common_ports
    
    def test_cli_save_results(self):
        """Тест сохранения результатов"""
        from src.network_scanner.cli import main
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner', '--save']):
                main()
            
            mock_scanner.save_results.assert_called_once()
    
    def test_cli_with_results(self):
        """Тест CLI с найденными результатами"""
        from src.network_scanner.cli import main
        
        mock_results = [
            {
                'ip': '192.168.1.1',
                'port': 80,
                'url': 'http://192.168.1.1:80',
                'status_code': 200,
                'title': 'Router Admin',
                'server': 'nginx',
                'is_router': True,
                'content_length': 1000
            }
        ]
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = mock_results
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner']):
                main()
            
            output = mock_stdout.getvalue()
            assert 'SCAN COMPLETED' in output
            assert 'Web interfaces found: 1' in output
    
    def test_cli_verbose_mode(self):
        """Тест verbose режима"""
        from src.network_scanner.cli import main
        
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            MockScanner.return_value = mock_scanner
            
            with patch('sys.argv', ['network-scanner', '--verbose']):
                main()
            
            # Должен нормально завершиться
    
    def test_cli_main_function_direct(self):
        """Тест прямой вызов main() функции"""
        from src.network_scanner.cli import main
        
        # Тестируем через mock чтобы не запускать реальное сканирование
        with patch('src.network_scanner.cli.NetworkScanner') as MockScanner, \
             patch('sys.stdout', new_callable=StringIO):
            
            mock_scanner = MagicMock()
            mock_scanner.scan_network.return_value = []
            MockScanner.return_value = mock_scanner
            
            # Имитируем аргументы командной строки
            with patch('sys.argv', ['network-scanner', '--save']):
                try:
                    main()
                    # Если не было исключений - тест пройден
                    assert True
                except SystemExit as e:
                    # SystemExit с кодом 0 - нормальное завершение
                    if e.code == 0:
                        assert True
                    else:
                        raise