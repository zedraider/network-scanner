#!/usr/bin/env python3
"""
Сканирование всех возможных сетей для поиска повторителя
"""

import subprocess
import sys
import os

def scan_network(network, ports=None):
    """Сканирует одну сеть"""
    print(f"\n🔍 Сканирую сеть {network}...")
    
    cmd = [sys.executable, "-m", "network_scanner.cli", "--network", network, "--save"]
    
    if ports:
        cmd.extend(["--ports", ports])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.stderr:
            print(f"Ошибки: {result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"⚠️  Таймаут при сканировании сети {network}")

def main():
    """Основная функция"""
    print("=" * 60)
    print("ПОИСК WIFI ПОВТОРИТЕЛЯ ВО ВСЕХ СЕТЯХ")
    print("=" * 60)
    
    # Список сетей для сканирования
    networks = [
        "192.168.1.0/24",
        "192.168.0.0/24", 
        "192.168.2.0/24",
        "192.168.100.0/24",
        "10.0.0.0/24",
        "10.1.1.0/24",
        "172.16.0.0/24",
        "172.16.1.0/24",
    ]
    
    # Порты для проверки
    ports = "80,81,82,443,8080,8081,8443,8888,8000,8001,9000"
    
    for network in networks:
        scan_network(network, ports)
    
    print("\n" + "=" * 60)
    print("СКАНИРОВАНИЕ ЗАВЕРШЕНО!")
    print("Проверьте папку results/ для просмотра результатов")
    print("=" * 60)

if __name__ == "__main__":
    main()