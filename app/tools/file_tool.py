from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = BASE_DIR / "data" / "internal_docs"


def list_documents() -> list[str]:
    return [
        file.name
        for file in DOCS_DIR.iterdir()
        if file.is_file()
    ]


def read_document(filename: str) -> str:
    path = DOCS_DIR / filename

    return path.read_text(
        encoding="utf-8",
    )


def search_documents(query: str) -> list[dict]:
    query_lower = query.lower()

    results = []

    for file in DOCS_DIR.iterdir():
        if not file.is_file():
            continue

        content = file.read_text(
            encoding="utf-8",
        )

        if query_lower in content.lower() or query_lower in file.name.lower():
            results.append(
                {
                    "filename": file.name,
                    "content": content,
                }
            )

    return results