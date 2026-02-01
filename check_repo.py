#!/usr/bin/env python3
"""
Проверка структуры репозитория перед публикацией
"""

import os
import sys
from pathlib import Path

REQUIRED_FILES = {
    'pyproject.toml': 'Конфигурация проекта',
    'README.md': 'Документация',
    'LICENSE': 'Лицензия',
    'src/network_scanner/__init__.py': 'Пакет Python',
    'src/network_scanner/scanner.py': 'Основной код',
    'src/network_scanner/cli.py': 'CLI интерфейс',
    'tests/__init__.py': 'Тесты',
    'tests/test_scanner.py': 'Тесты сканера',
    'tests/test_cli.py': 'Тесты CLI',
    '.github/workflows/python-tests.yml': 'GitHub Actions',
}

OPTIONAL_FILES = {
    'requirements-dev.txt': 'Dev зависимости (рекомендуется)',
    'examples/': 'Примеры использования',
    'docs/': 'Документация',
    'scripts/': 'Вспомогательные скрипты',
}

def check_repository():
    print("🔍 Проверка структуры репозитория network-scanner")
    print("=" * 60)
    
    root = Path(".")
    
    # Проверка обязательных файлов
    print("\n✅ Обязательные файлы:")
    missing = []
    
    for file_path, description in REQUIRED_FILES.items():
        if (root / file_path).exists():
            print(f"  ✓ {file_path} - {description}")
        else:
            print(f"  ✗ {file_path} - {description} (ОТСУТСТВУЕТ!)")
            missing.append(file_path)
    
    # Проверка опциональных файлов
    print("\n📦 Опциональные файлы:")
    for file_path, description in OPTIONAL_FILES.items():
        if (root / file_path).exists():
            print(f"  ✓ {file_path} - {description}")
        else:
            print(f"  ○ {file_path} - {description} (необязательно)")
    
    # Проверка содержимого pyproject.toml
    print("\n📄 Проверка pyproject.toml:")
    pyproject_path = root / "pyproject.toml"
    if pyproject_path.exists():
        try:
            import tomli
            with open(pyproject_path, 'rb') as f:
                data = tomli.load(f)
            
            required_fields = ['project.name', 'project.version', 'project.description']
            for field in required_fields:
                keys = field.split('.')
                value = data
                for key in keys:
                    value = value.get(key, {})
                if value and value != {}:
                    print(f"  ✓ {field} = {value}")
                else:
                    print(f"  ✗ {field} - отсутствует")
                    missing.append(f"pyproject.toml:{field}")
        
        except ImportError:
            print("  ⚠️  tomli не установлен, пропускаем детальную проверку")
        except Exception as e:
            print(f"  ⚠️  Ошибка чтения pyproject.toml: {e}")
    
    # Итог
    print("\n" + "=" * 60)
    if missing:
        print(f"❌ Найдено {len(missing)} проблем:")
        for item in missing:
            print(f"  - {item}")
        return False
    else:
        print("✅ Все проверки пройдены! Репозиторий готов.")
        return True

if __name__ == "__main__":
    success = check_repository()
    sys.exit(0 if success else 1)