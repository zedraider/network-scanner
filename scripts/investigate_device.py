#!/usr/bin/env python3
"""
Детальное исследование найденного устройства
"""

import requests
import socket
import json
from datetime import datetime
import urllib3

# Отключаем SSL предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def investigate_device(ip):
    """Исследует устройство на всех возможных портах"""
    print(f"\n🔍 ИССЛЕДУЮ УСТРОЙСТВО: {ip}")
    print("=" * 60)
    
    # Список портов для проверки
    ports_to_check = [
        80, 81, 82, 443, 8080, 8081, 8443, 8888, 
        8000, 8001, 7547, 5000, 9999, 9000, 8088,
        21, 22, 23, 25, 53, 110, 143, 161, 162, 443
    ]
    
    results = []
    
    for port in ports_to_check:
        # Проверяем открыт ли порт
        if check_port(ip, port):
            # Проверяем веб-сервис
            web_info = check_web_service(ip, port)
            if web_info:
                results.append(web_info)
                print_result(web_info)
    
    # Сохраняем результаты
    if results:
        save_investigation_results(ip, results)
    
    return results

def check_port(ip, port, timeout=2):
    """Проверяет, открыт ли порт"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def check_web_service(ip, port):
    """Проверяет веб-сервис на порту"""
    schemes = ['http', 'https'] if port in [443, 8443] else ['http']
    
    for scheme in schemes:
        url = f"{scheme}://{ip}:{port}"
        
        try:
            response = requests.get(
                url,
                timeout=3,
                allow_redirects=True,
                verify=False,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                }
            )
            
            # Получаем заголовок
            title = extract_title(response.text)
            
            return {
                'ip': ip,
                'port': port,
                'url': url,
                'status_code': response.status_code,
                'title': title,
                'server': response.headers.get('Server', 'Unknown'),
                'content_type': response.headers.get('Content-Type', ''),
                'headers': dict(response.headers),
                'content_preview': response.text[:500],
            }
            
        except requests.exceptions.SSLError:
            # Пробуем другой протокол
            continue
        except Exception as e:
            continue
    
    return None

def extract_title(html):
    """Извлекает title из HTML"""
    try:
        start = html.find('<title>')
        end = html.find('</title>')
        if start != -1 and end != -1:
            title = html[start+7:end].strip()
            if title:
                return title
    except:
        pass
    return "No title"

def print_result(result):
    """Выводит результат"""
    if result['status_code'] == 200:
        color = "\033[92m"
    else:
        color = "\033[93m"
    
    print(f"{color}✅ Найден: {result['ip']}:{result['port']}\033[0m")
    print(f"   URL: {result['url']}")
    print(f"   Статус: {result['status_code']}")
    
    if result['title'] != 'No title':
        print(f"   Заголовок: {result['title']}")
    
    if result['server'] != 'Unknown':
        print(f"   Сервер: {result['server']}")
    
    print(f"   Тип: {result.get('content_type', 'N/A')}")
    print()

def save_investigation_results(ip, results):
    """Сохраняет результаты исследования"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"device_investigation_{ip}_{timestamp}.json"
    
    output = {
        'device_ip': ip,
        'investigation_time': datetime.now().isoformat(),
        'total_ports_found': len(results),
        'results': results
    }
    
    with open(f"results/{filename}", 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 Результаты сохранены в: results/{filename}")

def main():
    print("=" * 60)
    print("ИНСТРУМЕНТ ДЛЯ ИССЛЕДОВАНИЯ СЕТЕВЫХ УСТРОЙСТВ")
    print("=" * 60)
    
    # Устройство для исследования
    device_ip = "192.168.3.86"
    
    # Исследуем устройство
    results = investigate_device(device_ip)
    
    if results:
        print(f"\n🎯 Устройство {device_ip} имеет {len(results)} открытых веб-интерфейсов:")
        for result in results:
            print(f"  • {result['url']} - {result['title']}")
    else:
        print(f"\n⚠️  На устройстве {device_ip} не найдено веб-интерфейсов")
    
    print("\n" + "=" * 60)
    print("ИССЛЕДОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)

if __name__ == "__main__":
    main()