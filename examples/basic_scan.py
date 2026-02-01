#!/usr/bin/env python3
"""
Пример базового использования Network Scanner
"""

import sys
import os

# Добавляем путь к src для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.network_scanner import NetworkScanner

def main():
    print("=== Basic Network Scanner Example ===")
    
    # Создаем сканер
    scanner = NetworkScanner(
        network="192.168.1.0/24",
        timeout=2,
        threads=50
    )
    
    # Запускаем сканирование
    results = scanner.scan_network()
    
    # Выводим результаты
    print(f"\nFound {len(results)} web interfaces:")
    for result in results:
        if result.get('is_router'):
            print(f"🔥 ROUTER: {result['ip']}:{result['port']} - {result['title']}")
        else:
            print(f"  Device: {result['ip']}:{result['port']} - {result['title']}")
    
    # Сохраняем результаты
    scanner.save_results()

if __name__ == "__main__":
    main()