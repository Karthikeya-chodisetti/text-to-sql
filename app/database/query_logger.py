import json
from sqlalchemy import text

from app.database.connection import db_engine

def log_query( user_question: str,
    prompt: str,
    schema_snapshot: dict,
    model: str,
    generated_sql: str,
    status: str,
    execution_error: str | None,
    execution_time_ms: float,
    row_count: int
):
    query = """
        INSERT INTO query_logs (
            user_question,
            prompt,
            schema_snapshot,
            model,
            generated_sql,
            status,
            execution_error,
            execution_time_ms,
            row_count
        )
        VALUES (
            :user_question,
            :prompt,
            CAST(:schema_snapshot AS JSONB),
            :model,
            :generated_sql,
            :status,
            :execution_error,
            :execution_time_ms,
            :row_count
        )
    """

    with db_engine.begin() as connection:
        connection.execute(
            text(query),
            {
                "user_question": user_question,
                "prompt": prompt,
                "schema_snapshot": json.dumps(schema_snapshot),
                "model": model,
                "generated_sql": generated_sql,
                "status": status,
                "execution_error": execution_error,
                "execution_time_ms": execution_time_ms,
                "row_count": row_count
            }
        )