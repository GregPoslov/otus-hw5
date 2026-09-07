from app.database import get_connection


def get_client(client_id: int) -> dict | None:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, name, email
            FROM clients
            WHERE id = ?
            """,
            (client_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)


def get_orders(client_id: int) -> list[dict]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, client_id, product, amount
            FROM orders
            WHERE client_id = ?
            """,
            (client_id,),
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]