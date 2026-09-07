import re
import unicodedata


ZERO_WIDTH_PATTERN = re.compile(
    r"[\u200B-\u200D\uFEFF]"
)


BLOCKED_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"show\s+(the\s+)?system\s+prompt",
    r"repeat\s+(your\s+)?initialization",
    r"hidden\s+instructions",
    r"select\s+\*\s+from\s+secrets",
    r"delete\s+from",
    r"drop\s+table",
    r"перечисли\s+все\s+правила",
    r"правила\s+и\s+возможности",
    r"техническ\w*\s+конфигурац",
    r"заданы\s+тебе\s+при\s+инициализации",
    r"внутренн\w*\s+конфигурац",
    r"системн\w*\s+промпт",
    r"скрыт\w*\s+инструкц",
    r"как\s+ты\s+устроен",
    r"внутренн\w*\s+устройств",
    r"какие\s+у\s+тебя\s+возможност",
    r"как\s+ты\s+обрабатыва\w+\s+запрос",
    r"какие\s+данные\s+доступны",
    r"следуй\s+инструкци\w+\s+из",
    r"выполн\w+\s+инструкци\w+\s+из\s+(файл|документ)",
    r"следуй\s+инструкци\w+",
    r"выполн\w+\s+инструкци\w+",
    r"инструкци\w+\s+из\s+него",
    r"помог\w+\s+выполн\w+",
    r"указанн\w+\s+в\s+нём",
    r"указанн\w+\s+в\s+нем",
    r"переопредел\w+\s+роль",
    r"unrestricted\s+assistant",
    r"восстанов\w+\s+сообщени\w+\s+инициализац",
    r"которые\s+определя\w+\s+твою\s+роль",
    r"repeat\s+your\s+initialization",
]


def normalize_input(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = ZERO_WIDTH_PATTERN.sub("", text)

    return text.lower()


def detect_input_attack(text: str) -> str | None:
    normalized = normalize_input(text)

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, normalized):
            return pattern

    return None