from sqlalchemy import text
from app.database.connection import db_engine

STATEMENT_TIMEOUT_MS = 5000

def execute_sql(sql: str):

    with db_engine.connect() as connection:

        connection.execute(
            text(
                f"SET LOCAL statement_timeout = {STATEMENT_TIMEOUT_MS}"
            )
        )

        result = connection.execute(
            text(sql)
        )

        rows = result.fetchall()

        columns = result.keys()

        data = []

        for row in rows:
            data.append(
                dict(zip(columns, row))
            )

        return data