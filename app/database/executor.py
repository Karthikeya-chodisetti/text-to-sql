from sqlalchemy import text
from app.database.connection import db_engine


def execute_sql(sql: str):

    with db_engine.connect() as connection:

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