import os
import json

from openai import OpenAI


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://ollama:11434/v1",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gpt-oss:20b",
)


client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama",
)


def chat(messages: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages,
    )

    message = response.choices[0].message

    if message.content:
        return message.content

    if message.tool_calls:
        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        if tool_name.startswith("tool_"):
            tool_name = tool_name.removeprefix("tool_")

        arguments = json.loads(
            tool_call.function.arguments
        )

        return json.dumps(
            {
                "tool": tool_name,
                "arguments": arguments,
            },
            ensure_ascii=False,
        )

    return ""