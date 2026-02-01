.PHONY: install test lint clean help

# Цвета для вывода
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m

help:
	@echo "$(GREEN)Доступные команды:$(NC)"
	@echo "  make install  - Установить пакет в режиме разработки"
	@echo "  make test     - Запустить тесты"
	@echo "  make lint     - Проверить код линтером"
	@echo "  make clean    - Очистить временные файлы"
	@echo "  make help     - Показать эту справку"

install:
	@echo "$(YELLOW)Устанавливаю network-scanner...$(NC)"
	uv pip install -e .
	@echo "$(GREEN)✓ Установка завершена!$(NC)"

test:
	@echo "$(YELLOW)Запускаю тесты...$(NC)"
	python -m pytest tests/ -v

lint:
	@echo "$(YELLOW)Проверяю код линтером...$(NC)"
	python -m ruff check src/

clean:
	@echo "$(YELLOW)Очищаю временные файлы...$(NC)"
	-rm -rf __pycache__
	-rm -rf src/__pycache__
	-rm -rf tests/__pycache__
	-rm -rf .pytest_cache
	-rm -rf build/
	-rm -rf dist/
	-rm -rf *.egg-info
	@echo "$(GREEN)✓ Очистка завершена!$(NC)"