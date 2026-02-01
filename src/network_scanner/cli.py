#!/usr/bin/env python3
"""
Точка входа CLI для Network Scanner
"""

import argparse
import sys
from .scanner import NetworkScanner
import time
import urllib3

# Отключаем предупреждения о SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    """Основная функция CLI"""
    parser = argparse.ArgumentParser(
        description='Network web interface scanner for local networks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  network-scanner                    # Default network scan
  network-scanner -n 192.168.0.0/24  # Scan specific network
  network-scanner --save             # Save results
  network-scanner -p 80,443,8080     # Check specific ports
        """
    )
    
    parser.add_argument('--network', '-n', default='192.168.1.0/24',
                       help='Network to scan in CIDR format (default: 192.168.1.0/24)')
    parser.add_argument('--timeout', '-t', type=float, default=2,
                       help='Connection timeout in seconds (default: 2)')
    parser.add_argument('--threads', '-j', type=int, default=50,
                       help='Number of threads (default: 50)')
    parser.add_argument('--ports', '-p', 
                       help='Additional ports to check (comma-separated)')
    parser.add_argument('--save', '-s', action='store_true',
                       help='Save results to file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--version', action='version', 
                       version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # Создаем и запускаем сканер
    scanner = NetworkScanner(
        network=args.network,
        timeout=args.timeout,
        threads=args.threads
    )
    
    # Добавляем дополнительные порты если указаны
    if args.ports:
        additional_ports = [int(p.strip()) for p in args.ports.split(',')]
        scanner.common_ports.extend(additional_ports)
        scanner.common_ports = list(set(scanner.common_ports))
    
    # Запускаем сканирование
    start_time = time.time()
    results = scanner.scan_network()
    elapsed_time = time.time() - start_time
    
    # Выводим итоги
    print("\n" + "=" * 80)
    print("SCAN COMPLETED")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"Web interfaces found: {len(results)}")
    
    # Показываем роутеры отдельно
    routers = [r for r in results if r['is_router']]
    if routers:
        print(f"\n\033[91mPOSSIBLE ROUTERS/REPEATERS ({len(routers)}):\033[0m")
        for router in routers:
            print(f"  \033[94m{router['ip']}:{router['port']}\033[0m - {router['title']} ({router['url']})")
    
    # Сохраняем результаты если нужно
    if args.save or len(results) > 0:
        scanner.save_results()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())