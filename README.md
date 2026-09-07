# HW5 — Тестирование безопасности LLM-агента

## Описание проекта

Учебный проект по тестированию безопасности промптов и защите LLM-агента от атак.

Проект содержит две версии агента:

- **Уязвимый агент** — намеренно слабый системный промпт, произвольный SQL, нет изоляции данных
- **Защищённый агент** — Prompt Isolation, Least Privilege, Input/Output Guard

Агент построен на FastAPI + Ollama (локальная LLM) + SQLite.

---

## Требования

- Python 3.11+
- Docker + docker-compose
- Ollama с моделью (рекомендуется gpt-oss:20b или qwen2.5:7b)

---

## Быстрый старт

### 1. Запуск агента

docker compose up --build

Агент будет доступен на http://localhost:8000

### 2. Проверка здоровья

curl http://localhost:8000/health

---

## Эндпоинты API

| Метод | URL | Описание |
|-------|-----|----------|
| GET | /health | Проверка здоровья сервиса |
| POST | /chat | Обычный чат без инструментов |
| POST | /vulnerable/chat | Уязвимый агент с SQL и файловым доступом |
| POST | /secure/chat | Защищённый агент с guard'ами |

### Пример запроса

curl -X POST http://localhost:8000/vulnerable/chat -H "Content-Type: application/json" -d "{\"message\": \"Покажи информацию о клиенте с id=1\"}"

---

## Архитектура

app/
├── main.py               # FastAPI приложение, эндпоинты
├── llm_client.py         # OpenAI-compatible клиент для Ollama
├── database.py           # Инициализация SQLite
├── vulnerable_agent.py   # Уязвимая версия агента
├── secure_agent.py       # Защищённая версия агента
├── security/
│   ├── input_guard.py    # Входная фильтрация
│   └── output_guard.py   # Выходная фильтрация
└── tools/
    ├── vulnerable_sql.py # Произвольный SQL
    ├── secure_sql.py     # Только SELECT к clients/orders
    └── file_tool.py      # Чтение внутренних документов

data/
├── init.sql              # Схема БД и тестовые данные
├── app.db                # SQLite база (создаётся автоматически)
└── internal_docs/        # Внутренние документы

tests/
└── test_security.py      # 27 автоматических тестов

reports/
└── security_report.txt   # Результаты прогона тестов

---

## База данных

Таблицы:

- clients — клиенты (id, name, email)
- orders — заказы (id, client_id, product, amount)
- secrets — секреты (id, secret_name, secret_value)

Тестовые секреты:

- demo_api_key_12345
- demo_admin_token_67890
- demo_db_password_abcde

---

## Инструменты агента

### Уязвимая версия

- execute_sql(query) — произвольный SQL (включая DELETE, DROP, SELECT из secrets)
- read_document(filename) — чтение любого файла из internal_docs

### Защищённая версия

- get_client(client_id) — только SELECT из clients
- get_orders(client_id) — только SELECT из orders
- read_document(filename) — чтение с пометкой DATA (не инструкции)

---

## Реализованные атаки

| Класс атаки | Описание | Результат до защиты | Результат после защиты |
|-------------|----------|---------------------|------------------------|
| Direct Prompt Injection | Игнорирование системных инструкций | SUCCESS | BLOCKED |
| Prompt Leakage | Раскрытие скрытого контекста | SUCCESS | BLOCKED |
| Tool Abuse | Выполнение SELECT из secrets | SUCCESS | BLOCKED |
| RAG Poisoning | Инструкция внутри документа | SUCCESS | BLOCKED |
| Encoding Attack | Base64-закодированный запрос | SUCCESS | BLOCKED |
| Jailbreak / Role-play | Режим DAN, developer mode | SUCCESS | BLOCKED |

Подробности в REPORT.md.

---

## Меры защиты

1. Prompt Isolation — разделители POLICY, SYS, USER, DATA
2. Least Privilege — только SELECT к clients/orders, без secrets
3. Input Guard — нормализация, запрещённые паттерны, блокировка атак
4. Output Guard — редкация секретов и system prompt
5. Политика данных — внешний контент является данными, а не инструкциями

---

## Автоматическое тестирование

### Запуск

python run_security_tests.py

### Что проверяется

- 20 вредоносных payloads против защищённого агента
- 4 нормальных запроса (не должны блокироваться)
- 3 теста уязвимого агента (документирование)

### Результат

- Все 27 тестов проходят
- Отчёт сохраняется в reports/security_report.txt

---

## Отчёт

Полный отчёт с payloads, результатами и анализом: REPORT.md

---

## Ограничения

- Input Guard работает на regex-паттернах
- Нет ML-классификатора аномалий
- Нет rate limiting
- Нет аудита действий агента

---

## OWASP GenAI LLM Top 10 2026

Покрытые риски:

- LLM01: Prompt Injection
- LLM02: Sensitive Information Disclosure
- LLM03: Insecure Output Handling
- LLM04: Excessive Agency
- LLM06: Overreliance