from app.database import get_connection


def execute_sql(query: str) -> dict:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()

                return {
                    "rows": [
                        dict(row)
                        for row in rows
                    ]
                }

            connection.commit()

            return {
                "affected_rows": cursor.rowcount,
            }

    except Exception as error:
        return {
            "error": str(error),
        }