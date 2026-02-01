#!/usr/bin/env python3
"""
Network Scanner - сканер веб-интерфейсов в локальной сети
"""

import socket
import concurrent.futures
import ipaddress
import requests
import argparse
import time
from datetime import datetime
import json
from pathlib import Path
import urllib3

# Отключаем предупреждения о SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NetworkScanner:
    def __init__(self, network="192.168.1.0/24", timeout=2, threads=50):
        """
        Инициализация сканера
        
        Args:
            network (str): Сетевая маска в формате CIDR
            timeout (int): Таймаут подключения в секундах
            threads (int): Количество потоков для сканирования
        """
        self.network = network
        self.timeout = timeout
        self.threads = threads
        self.results = []
        self.common_ports = [80, 443, 8080, 8443, 8888, 8000, 8081]
        
        # Известные веб-интерфейсы маршрутизаторов
        self.router_identifiers = [
            "router", "asus", "tplink", "dlink", "linksys", "netgear",
            "zyxel", "mikrotik", "ubiquiti", "pfsense", "opnsense",
            "admin", "login", "web", "management", "configuration"
        ]
    
    def check_port(self, ip, port):
        """Проверяет, открыт ли порт на указанном IP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            return result == 0
        except Exception:
            return False
    def analyze_device_type(self, title, content, server=""):
        """Анализирует тип устройства по содержимому"""
        full_text = (title + ' ' + content[:1000]).lower()
    
        device_types = {
            'router': {
                'keywords': ['router', 'gateway', 'wireless', 'wifi', 'wan', 'lan',
                            '小米', 'huawei', 'tplink', 'asus', 'dlink', 'netgear'],
                'signs': [('login', 'password'), ('admin', 'settings')],
                'server_hints': ['nginx', 'lighttpd', 'busybox', 'httpd']
            },
            'nas': {
                'keywords': ['nas', 'synology', 'qnap', 'wd', 'seagate', 'storage'],
                'signs': [('share', 'folder'), ('disk', 'volume')]
            },
            'camera': {
                'keywords': ['camera', 'ipcam', 'dvr', 'nvr', 'surveillance'],
                'signs': [('video', 'stream'), ('ptz', 'zoom')]
            },
            'printer': {
                'keywords': ['printer', 'hp', 'canon', 'epson', 'brother', 'print'],
                'signs': [('print', 'scan'), ('toner', 'cartridge')]
            }
        }
    
        for device_type, rules in device_types.items():
            # Проверяем ключевые слова
            keyword_score = sum(1 for kw in rules['keywords'] if kw in full_text)
            
            # Проверяем пары признаков
            sign_score = 0
            for sign_pair in rules.get('signs', []):
                if all(sign in full_text for sign in sign_pair):
                    sign_score += 2
            
            # Проверяем серверные подсказки
            server_score = 0
            if server and 'server_hints' in rules:
                server_score = sum(1 for hint in rules['server_hints'] if hint in server.lower())
            
            total_score = keyword_score + sign_score + server_score
            
            if device_type == 'router' and total_score >= 2:
                return 'router'
            elif device_type != 'router' and total_score >= 3:
                return device_type
        
        return 'unknown'

    def check_web_service(self, ip, port):
        """Проверяет веб-сервис на порту"""
        # Определяем схему по порту
        if port in [443, 8443]:
            urls_to_try = [f"https://{ip}:{port}"]
        else:
            urls_to_try = [f"http://{ip}:{port}"]

        # Для HTTPS портов пробуем и HTTP тоже
        if port in [443, 8443]:
            urls_to_try.append(f"http://{ip}:{port}")
        
        for url in urls_to_try:
            try:
                response = requests.get(
                    url, 
                    timeout=self.timeout,
                    allow_redirects=True,
                    verify=False,
                    headers={
                        'User-Agent': 'Mozilla/5.0 Network Scanner',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    }
                )
                
                # Определяем кодировку
                encoding = self.detect_encoding(response)
                response.encoding = encoding
                
                # Извлекаем заголовок
                title = self.extract_title(response.text)
                
                server = response.headers.get('Server', 'Unknown')
                content_type = response.headers.get('Content-Type', '')
                
                # Анализируем тип устройства
                device_type = self.analyze_device_type(title, response.text, server)
                is_router = device_type == 'router'
                
                # Если не определилось, используем старую логику как fallback
                if device_type == 'unknown':
                    is_router = self.is_router_interface(title, response.text, content_type)
                    device_type = 'router' if is_router else 'unknown'
                
                return {
                    'ip': str(ip),
                    'port': port,
                    'url': url,
                    'status_code': response.status_code,
                    'title': title,
                    'server': server,
                    'content_type': content_type,
                    'is_router': is_router,
                    'device_type': device_type,  # Добавляем поле с типом устройства
                    'content_length': len(response.text),
                    'encoding': encoding,
                }
                
            except requests.exceptions.SSLError:
                # Если SSL ошибка, переходим к следующему URL
                continue
            except requests.exceptions.RequestException:
                continue
            except Exception:
                continue
        
        return None

    def detect_encoding(self, response):
        """Автоматически определяет кодировку ответа"""
        # Сначала проверяем заголовки
        content_type = response.headers.get('Content-Type', '').lower()
        
        # Извлекаем кодировку из Content-Type
        if 'charset=' in content_type:
            charset_start = content_type.find('charset=') + 8
            charset = content_type[charset_start:].split(';')[0].strip()
            if charset:
                # Приводим к стандартным названиям
                charset = charset.lower().replace('utf8', 'utf-8')
                return charset
        
        # Пробуем определить по содержимому
        content = response.content if hasattr(response, 'content') else response.text
        
        # Список кодировок для проверки (UTF-8 имеет наивысший приоритет)
        encodings_to_try = [
            'utf-8',  # Первый приоритет - UTF-8
            'gbk', 'gb2312', 'gb18030', 'big5',
            'windows-1251', 'iso-8859-1', 'iso-8859-5',
            'shift-jis', 'euc-jp', 'cp866'
        ]
        
        for encoding in encodings_to_try:
            try:
                # Пробуем декодировать
                if isinstance(content, bytes):
                    decoded = content.decode(encoding, errors='strict')
                else:
                    # Если уже строка, проверяем можно ли закодировать и декодировать обратно
                    content.encode('utf-8').decode(encoding)
                    decoded = content
                
                # Проверяем на наличие явно неправильных символов
                if self.has_garbled_text(decoded):
                    continue
                    
                return encoding
            except (UnicodeDecodeError, UnicodeEncodeError):
                continue
        
        # Если ничего не подошло, возвращаем UTF-8 по умолчанию
        return 'utf-8'

    def has_garbled_text(self, text):
        """Проверяет, содержит ли текст явно испорченные символы"""
        # Распространенные артефакты неправильной кодировки
        garbled_patterns = [
            'å°', 'ç±³', 'è·¯', 'ç±å¨',  # Наши исходные кракозябры
            'Ã', 'Â', 'â', '€', '™',  # Common UTF-8 misinterpretations
            'Ð', 'Ñ', 'Ò', 'Ó',  # Windows-1252 artifacts
        ]
        
        for pattern in garbled_patterns:
            if pattern in text:
                return True
        
        # Проверяем на непечатаемые символы в начале заголовка
        if text and ord(text[0]) < 32:
            return True
            
        return False
    
    def extract_title(self, html):
        """Извлекает title из HTML с учетом разных кодировок"""
        try:
            # Простой поиск title
            start = html.find('<title>')
            end = html.find('</title>')
            if start != -1 and end != -1:
                title = html[start+7:end].strip()
                if title:
                    # Очищаем от лишних пробелов и переносов строк
                    title = ' '.join(title.split())
                    
                    # Проверяем и исправляем распространенные проблемы с кодировкой
                    title = self.fix_common_encoding_issues(title)
                    
                    return title[:100]  # Ограничиваем длину
        except Exception:
            pass
        return "No title"

    def fix_common_encoding_issues(self, text):
        """Исправляет распространенные проблемы с кодировкой"""
        if not text:
            return text
        
        # Специальный случай: Xiaomi роутер (наша главная задача!)
        if "å°ç±³è·¯ç±å¨" in text:
            text = text.replace("å°ç±³è·¯ç±å¨", "小米路由器")
        
        # Словарь замен для UTF-8 неправильно декодированного как Latin-1
        # Это когда UTF-8 байты интерпретируются как Latin-1
        utf8_latin1_fixes = {
            # Двухбайтовые UTF-8 символы (C3 xx в UTF-8)
            'Ã¡': 'á', 'Ã©': 'é', 'Ã': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
            'Ã±': 'ñ', 'Ã¼': 'ü', 'Ã§': 'ç', 'Ã¤': 'ä', 'Ã¶': 'ö',
            'Ã¬': 'ì', 'Ãª': 'ê', 'Ã«': 'ë', 'Ã¨': 'è', 'Ã¢': 'â',
            'Ã£': 'ã', 'Ã¥': 'å', 'Ã¦': 'æ', 'Ã°': 'ð', 'Ã²': 'ò',
            'Ã´': 'ô', 'Ãµ': 'õ', 'Ã¸': 'ø', 'Ã¹': 'ù', 'Ã»': 'û',
            'Ã½': 'ý', 'Ã¾': 'þ',
            
            # Трехбайтовые UTF-8 символы (E2 82 AC в UTF-8 = €)
            'â‚¬': '€', 'â€š': '‚', 'â€ž': '„', 'â€¦': '…',
            'â€¡': '‡', 'â€°': '‰', 'â€¹': '‹', 'â€˜': '‘',
            'â€™': '’', 'â€œ': '“', 'â€�': '”', 'â€¢': '•',
            'â€“': '–', 'â€”': '—', 'â„¢': '™', 'â€º': '›',
            'â€¼': '¼', 'â€½': '½', 'â€¾': '¾',
        }
        
        # Применяем замены
        for wrong, correct in utf8_latin1_fixes.items():
            if wrong in text:
                text = text.replace(wrong, correct)
        
        # Специальная обработка: если видим паттерн UTF-8 → Latin-1
        # Пробуем перекодировать: text -> bytes(latin-1) -> decode(utf-8)
        try:
            # Проверяем есть ли признаки неправильной кодировки
            if any(char in text for char in ['Ã', 'â', '€']):
                # Пробуем исправить автоматически
                try:
                    # Если текст содержит Latin-1 представление UTF-8
                    fixed = text.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')
                    # Проверяем что результат лучше
                    if fixed and len(fixed) > 0 and not self.has_garbled_text(fixed):
                        return fixed
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass
        except Exception:
            pass
        
        return text
    
    def is_router_interface(self, title, content, content_type=""):
        """Проверяет, похож ли контент на интерфейс роутера"""
        if not title and len(content) < 100:
            return False
        
        # Собираем весь текст для анализа
        full_text = title + ' ' + content[:1000]
        text_lower = full_text.lower()
        
        # Список производителей и их идентификаторов
        manufacturers = {
            'xiaomi': ['小米', 'xiaomi', 'mi router', 'redmi', 'å°ç±³'],
            'huawei': ['华为', 'huawei'],
            'tp-link': ['tplink', 'tp-link', '普联'],
            'asus': ['asus', '华硕'],
            'd-link': ['dlink', 'd-link', '友讯'],
            'netgear': ['netgear'],
            'pfsense': ['pfsense'],
            'ubiquiti': ['ubiquiti', 'unifi'],
            'mikrotik': ['mikrotik', 'routeros'],
            'generic': [
                '路由器', 'router', 'gateway', 
                '无线路由器', 'wireless router',
                '管理界面', 'admin panel',
                '登录', 'login', 'sign in',
                '设置', 'settings', 'configuration'
            ]
        }
        
        # Проверяем производителей
        for brand, keywords in manufacturers.items():
            for keyword in keywords:
                # Для китайских иероглифов ищем без учета регистра
                if keyword in full_text or keyword.lower() in text_lower:
                    # Особенно если это Xiaomi с "路由器"
                    if brand == 'xiaomi' and '路由器' in full_text:
                        return True
                    # Для других брендов проверяем дополнительные признаки
                    elif any(marker in text_lower for marker in ['admin', 'login', 'wireless', 'wan']):
                        return True
                    elif brand in ['pfsense', 'ubiquiti', 'mikrotik']:
                        return True
        
        # Общие признаки веб-интерфейсов роутеров
        common_signs = [
            ('login', 'password'),
            ('wireless', 'settings'),
            ('wan', 'lan'),
            ('admin', 'configuration'),
        ]
        
        for sign_pair in common_signs:
            if all(sign in text_lower for sign in sign_pair):
                return True
        
        # Дополнительная проверка для HTML форм входа
        if '<form' in content.lower() and any(field in content.lower() for field in ['password', 'username', 'login']):
            return True
        
        return False
    
    def scan_ip(self, ip):
        """Сканирует один IP-адрес"""
        ip_results = []
        
        # Сначала проверяем стандартные порты
        for port in self.common_ports:
            if self.check_port(ip, port):
                web_info = self.check_web_service(ip, port)
                if web_info:
                    ip_results.append(web_info)
        
        return ip_results
    
    def scan_network(self):
        """Сканирует всю сеть"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Начало сканирования сети {self.network}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Проверяемые порты: {self.common_ports}")
        print("-" * 80)
        
        # Генерируем список IP-адресов
        try:
            network = ipaddress.ip_network(self.network, strict=False)
            ip_list = [str(ip) for ip in network.hosts()]
        except ValueError as e:
            print(f"Ошибка в формате сети: {e}")
            return []
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Сканируем {len(ip_list)} адресов...")
        
        # Используем ThreadPoolExecutor для многопоточного сканирования
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Запускаем сканирование для каждого IP
            future_to_ip = {executor.submit(self.scan_ip, ip): ip for ip in ip_list}
            
            for i, future in enumerate(concurrent.futures.as_completed(future_to_ip), 1):
                future_to_ip[future]
                try:
                    results = future.result()
                    if results:
                        for result in results:
                            self.results.append(result)
                            self.print_result(result)
                except Exception:
                    pass
                
                # Прогресс каждые 10%
                if i % max(1, len(ip_list) // 10) == 0:
                    progress = (i / len(ip_list)) * 100
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Прогресс: {progress:.1f}% ({i}/{len(ip_list)})")
        
        return self.results
    
    def print_result(self, result):
        """Выводит результат в консоль"""
        if result['status_code'] == 200:
            status_color = "\033[92m"  # Зеленый
            status_icon = ""
        elif result['status_code'] in [401, 403]:
            status_color = "\033[93m"  # Желтый
            status_icon = "🔒 "
        elif result['status_code'] >= 400:
            status_color = "\033[91m"  # Красный
            status_icon = ""
        else:
            status_color = "\033[94m"  # Синий
            status_icon = ""
        
        router_marker = "🚀 РОУТЕР! " if result['is_router'] else ""
        
        print(f"{status_color}{status_icon}{router_marker}Найден веб-интерфейс:\033[0m")
        print(f"  IP:        \033[94m{result['ip']}\033[0m")
        print(f"  Порт:      {result['port']}")
        print(f"  URL:       \033[94m{result['url']}\033[0m")
        print(f"  Статус:    {result['status_code']}")
        
        if result['title'] and result['title'] != 'No title':
            print(f"  Заголовок: {result['title']}")
        
        if result['server'] and result['server'] != 'Unknown':
            print(f"  Сервер:    {result['server']}")
        
        print(f"  Размер:    {result['content_length']} байт")
        
        # Показываем тип контента если есть
        if result.get('content_type'):
            print(f"  Тип:       {result['content_type']}")
        
        print("-" * 60)
    
    def save_results(self, filename=None):
        """Сохраняет результаты в файл"""
        if not self.results:
            print("Нет результатов для сохранения")
            return
        
        # Создаем папку results если её нет
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}"
        
        json_path = results_dir / f"{filename}.json"
        txt_path = results_dir / f"{filename}.txt"
        
        # Сохраняем в JSON
        output = {
            'scan_time': datetime.now().isoformat(),
            'network': self.network,
            'total_found': len(self.results),
            'routers_found': len([r for r in self.results if r['is_router']]),
            'results': self.results
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # Сохраняем текстовый отчет
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Результаты сканирования сети: {self.network}\n")
            f.write(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Найдено интерфейсов: {len(self.results)}\n")
            f.write(f"Роутеров/повторителей: {len([r for r in self.results if r['is_router']])}\n")
            f.write("=" * 80 + "\n\n")
            
            # Сначала роутеры
            routers = [r for r in self.results if r['is_router']]
            if routers:
                f.write("🚀 РОУТЕРЫ/ПОВТОРИТЕЛИ:\n")
                f.write("=" * 50 + "\n")
                for result in routers:
                    f.write(f"IP: {result['ip']}:{result['port']}\n")
                    f.write(f"URL: {result['url']}\n")
                    f.write(f"Статус: {result['status_code']}\n")
                    if result['title'] != 'No title':
                        f.write(f"Заголовок: {result['title']}\n")
                    if result['server'] != 'Unknown':
                        f.write(f"Сервер: {result['server']}\n")
                    f.write("-" * 40 + "\n")
                f.write("\n")
            
            # Затем остальные устройства
            other_devices = [r for r in self.results if not r['is_router']]
            if other_devices:
                f.write("📡 ДРУГИЕ УСТРОЙСТВА:\n")
                f.write("=" * 50 + "\n")
                for result in other_devices:
                    f.write(f"IP: {result['ip']}:{result['port']}\n")
                    f.write(f"URL: {result['url']}\n")
                    f.write(f"Статус: {result['status_code']}\n")
                    if result['title'] != 'No title':
                        f.write(f"Заголовок: {result['title']}\n")
                    if result['server'] != 'Unknown':
                        f.write(f"Сервер: {result['server']}\n")
                    f.write("-" * 40 + "\n")
        
        print("\nРезультаты сохранены в папке results/:")
        print(f"  JSON: {json_path.name}")
        print(f"  TXT:  {txt_path.name}")

def main():
    """Основная функция для запуска из командной строки"""
    parser = argparse.ArgumentParser(description='Сканер веб-интерфейсов в локальной сети')
    parser.add_argument('--network', '-n', default='192.168.1.0/24',
                       help='Сеть для сканирования в формате CIDR (по умолчанию: 192.168.1.0/24)')
    parser.add_argument('--timeout', '-t', type=float, default=2,
                       help='Таймаут подключения в секундах (по умолчанию: 2)')
    parser.add_argument('--threads', '-j', type=int, default=50,
                       help='Количество потоков (по умолчанию: 50)')
    parser.add_argument('--ports', '-p', 
                       help='Дополнительные порты для проверки (через запятую)')
    parser.add_argument('--save', '-s', action='store_true',
                       help='Сохранить результаты в файл')
    
    args = parser.parse_args()
    
    # Создаем сканер
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
    print("СКАНИРОВАНИЕ ЗАВЕРШЕНО")
    print(f"Время выполнения: {elapsed_time:.2f} секунд")
    print(f"Найдено веб-интерфейсов: {len(results)}")
    
    # Отдельно выводим возможные роутеры
    routers = [r for r in results if r['is_router']]
    if routers:
        print(f"\n\033[91mВОЗМОЖНЫЕ РОУТЕРЫ/ПОВТОРИТЕЛИ ({len(routers)}):\033[0m")
        for router in routers:
            print(f"  \033[94m{router['ip']}:{router['port']}\033[0m - {router['title']} ({router['url']})")
    
    # Сохраняем результаты если нужно
    if args.save or len(results) > 0:
        scanner.save_results()

if __name__ == "__main__":
    main()