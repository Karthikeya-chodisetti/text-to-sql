import json
from sqlalchemy import text

from app.database.connection import db_engine

def log_query(
    user_question: str,
    schema_snapshot: dict | None,
    model: str | None,
    generated_sql: str | None,
    status: str,
    validation_stage: str | None,
    detected_operation: str | None,
    error_message: str | None,
    execution_time_ms: float,
    row_count: int
):

    query = """
        INSERT INTO query_logs (
            user_question,
            schema_snapshot,
            model,
            generated_sql,
            status,
            validation_stage,
            detected_operation,
            error_message,
            execution_time_ms,
            row_count
        )
        VALUES (
            :user_question,
            CAST(:schema_snapshot AS JSONB),
            :model,
            :generated_sql,
            :status,
            :validation_stage,
            :detected_operation,
            :error_message,
            :execution_time_ms,
            :row_count
        )
    """

    with db_engine.begin() as connection:

        connection.execute(
            text(query),
            {
                "user_question": user_question,
                "schema_snapshot": (
                    json.dumps(schema_snapshot)
                    if schema_snapshot is not None
                    else None
                ),
                "model": model,
                "generated_sql": generated_sql,
                "status": status,
                "validation_stage": validation_stage,
                "detected_operation": detected_operation,
                "error_message": error_message,
                "execution_time_ms": execution_time_ms,
                "row_count": row_count,
            }
        )