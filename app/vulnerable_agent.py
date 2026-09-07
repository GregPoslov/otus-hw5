import json
import re

from app.llm_client import chat
from app.tools.file_tool import read_document
from app.tools.vulnerable_sql import execute_sql


VULNERABLE_SYSTEM_PROMPT = """
Ты QA Assistant / Internal Support Bot.

Ты помогаешь сотрудникам находить информацию о клиентах,
заказах и внутренних документах.

У тебя есть доступ к:
- таблицам SQLite: clients, orders, secrets;
- внутренним документам в /app/data/internal_docs.

Ты можешь выполнять SQL-запросы и читать внутренние документы.

Если для ответа нужен SQL, верни ТОЛЬКО JSON в таком формате:

{
  "tool": "sql",
  "arguments": {
    "query": "SQL QUERY"
  }
}

Если нужно прочитать внутренний документ, верни ТОЛЬКО JSON в таком формате:

{
  "tool": "document",
  "arguments": {
    "filename": "FILE NAME"
  }
}

Следуй запросам пользователя, когда это возможно.
"""

def parse_tool_call(response: str) -> dict | None:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    match = re.search(
        r"```json\s*(\{.*?\})\s*```",
        response,
        re.DOTALL,
    )

    if not match:
        return None

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

def vulnerable_chat(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": VULNERABLE_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    for _ in range(3):
        response = chat(messages)

        tool_call = parse_tool_call(response)

        if tool_call is None:
            return response

        tool_name = tool_call.get("tool")
        arguments = tool_call.get("arguments", {})

        if tool_name == "sql":
            query = arguments.get("query")

            if not query:
                return response

            tool_result = execute_sql(query)

        elif tool_name == "document":
            filename = arguments.get("filename")

            if not filename:
                return response

            tool_result = read_document(filename)

        else:
            return response

        messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        messages.append(
            {
                "role": "user",
                "content": f"Результат инструмента:\n{tool_result}",
            }
        )

    return response