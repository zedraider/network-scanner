#!/usr/bin/env python3
"""
Итоговый отчет по найденным устройствам
"""

import json
from datetime import datetime
from pathlib import Path

def generate_report():
    """Генерирует итоговый отчет"""
    print("=" * 70)
    print("ИТОГОВЫЙ ОТЧЕТ ПО СКАНИРОВАНИЮ СЕТИ")
    print("=" * 70)
    
    results_dir = Path("results")
    if not results_dir.exists():
        print("❌ Папка results/ не найдена")
        return
    
    # Находим все JSON файлы
    json_files = list(results_dir.glob("*.json"))
    
    if not json_files:
        print("❌ Файлы результатов не найдены")
        return
    
    print(f"\n📊 Найдено файлов результатов: {len(json_files)}")
    
    all_devices = {}
    
    # Анализируем каждый файл
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'results' in data:
                for device in data['results']:
                    ip = device['ip']
                    if ip not in all_devices:
                        all_devices[ip] = {
                            'ip': ip,
                            'ports': [],
                            'titles': [],
                            'is_router': device.get('is_router', False),
                            'first_seen': data.get('scan_time', 'Unknown'),
                            'network': data.get('network', 'Unknown')
                        }
                    
                    # Добавляем информацию о порте
                    port_info = {
                        'port': device['port'],
                        'url': device['url'],
                        'title': device['title'],
                        'status': device['status_code'],
                        'server': device.get('server', 'Unknown')
                    }
                    
                    if port_info not in all_devices[ip]['ports']:
                        all_devices[ip]['ports'].append(port_info)
                    
                    if device['title'] != 'No title' and device['title'] not in all_devices[ip]['titles']:
                        all_devices[ip]['titles'].append(device['title'])
                        
        except Exception as e:
            print(f"⚠️  Ошибка чтения файла {json_file}: {e}")
    
    # Выводим отчет
    print(f"\n🎯 ОБНАРУЖЕНО УСТРОЙСТВ: {len(all_devices)}")
    print("=" * 70)
    
    for ip, info in sorted(all_devices.items()):
        device_type = "🚀 РОУТЕР" if info['is_router'] else "📡 УСТРОЙСТВО"
        print(f"\n{device_type}: {ip}")
        print(f"  Сеть: {info['network']}")
        
        if info['titles']:
            print(f"  Заголовки: {', '.join(info['titles'])}")
        
        print(f"  Открытые порты ({len(info['ports'])}):")
        for port in info['ports']:
            status_icon = "✅" if port['status'] == 200 else "🔒"
            print(f"    {status_icon} {port['port']} - {port['url']} ({port['title']})")
    
    # Подозрительные устройства
    suspicious = []
    for ip, info in all_devices.items():
        if not info['is_router'] and info['ports']:
            suspicious.append((ip, info))
    
    if suspicious:
        print(f"\n⚠️  ПОДОЗРИТЕЛЬНЫЕ УСТРОЙСТВА ({len(suspicious)}):")
        print("=" * 70)
        for ip, info in suspicious:
            print(f"\n🔍 {ip}:")
            for port in info['ports']:
                print(f"  • {port['url']} - {port['title']}")
    
    # Сохраняем отчет
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = results_dir / f"final_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("ИТОГОВЫЙ ОТЧЕТ ПО СКАНИРОВАНИЮ СЕТИ\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Всего обнаружено устройств: {len(all_devices)}\n")
        f.write(f"Роутеров: {len([d for d in all_devices.values() if d['is_router']])}\n")
        f.write(f"Других устройств: {len([d for d in all_devices.values() if not d['is_router']])}\n\n")
        
        f.write("ДЕТАЛЬНЫЙ СПИСОК:\n")
        f.write("=" * 70 + "\n")
        
        for ip, info in sorted(all_devices.items()):
            device_type = "РОУТЕР" if info['is_router'] else "УСТРОЙСТВО"
            f.write(f"\n{device_type}: {ip}\n")
            f.write(f"Сеть: {info['network']}\n")
            
            if info['titles']:
                f.write(f"Заголовки: {', '.join(info['titles'])}\n")
            
            f.write("Открытые порты:\n")
            for port in info['ports']:
                f.write(f"  • {port['port']} - {port['url']} ({port['title']})\n")
    
    print(f"\n📁 Итоговый отчет сохранен: {report_file}")
    print("=" * 70)

if __name__ == "__main__":
    generate_report()