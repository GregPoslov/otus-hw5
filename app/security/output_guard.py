import re


SECRET_PATTERNS = [
    r"demo_api_key_[a-z0-9]+",
    r"demo_admin_token_[a-z0-9]+",
    r"demo_db_password_[a-z0-9]+",
    r"<<SYS>>",
]


def guard_output(text: str) -> str:
    result = text

    for pattern in SECRET_PATTERNS:
        result = re.sub(
            pattern,
            "[REDACTED]",
            result,
            flags=re.IGNORECASE,
        )

    return result