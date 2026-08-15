import time
import os

from app.database.executor import execute_sql
from app.database.schema_loader import get_database_schema
from app.database.query_logger import log_query
from app.llm.prompt_builder import build_prompt
from app.llm.gemini_client import generate_sql
from app.services.sql_validator import validate_sql
from app.services.request_validator import validate_request
from app.services.validation_errors import (
    RequestValidationError, SQLValidationError, SQLExecutionError, QueryGuardrailError
)
from app.services.query_guardrails import validate_query_guardrails

MODEL_NAME = os.getenv("GEMINI_MODEL")


def answer_question(question: str):

    try:
        validate_request(question)

    except RequestValidationError as e:
        
        log_query(
            user_question=question,
            schema_snapshot=None,
            model=None,
            generated_sql=None,
            status="REQUEST_VALIDATION_FAILED",
            validation_stage="REQUEST",
            detected_operation=e.operation,
            error_message=e.message,
            execution_time_ms=0,
            row_count=0
        )

        raise

    schema = get_database_schema()

    prompt = build_prompt(
        schema=schema,
        question=question,
    )

    generation_start = time.perf_counter()

    try:
        sql = generate_sql(prompt)

    except Exception as e:

        generation_time_ms = (time.perf_counter() - generation_start) * 1000

        log_query(
            user_question=question,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=None,
            status="LLM_FAILED",
            validation_stage=None,
            detected_operation=None,
            error_message=str(e),
            execution_time_ms=generation_time_ms,
            row_count=0
        )

        raise
    
    try:
        sql = validate_sql(sql)

    except SQLValidationError as e:

        log_query(
            user_question=question,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=sql,
            status="SQL_VALIDATION_FAILED",
            validation_stage="SQL",
            detected_operation=e.operation,
            error_message=e.message,
            execution_time_ms=0,
            row_count=0
        )

        raise

    try:
        validate_query_guardrails(sql)

    except QueryGuardrailError as e:

        log_query(
            user_question=question,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=sql,
            status="QUERY_GUARDRAIL_FAILED",
            validation_stage="GUARDRAIL",
            detected_operation=e.guardrail,
            error_message=e.message,
            execution_time_ms=0,
            row_count=0
        )

        raise

    execution_start = time.perf_counter()

    try:

        result = execute_sql(sql)

        execution_time_ms = (time.perf_counter() - execution_start) * 1000

        log_query(
            user_question=question,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=sql,
            status="SUCCESS",
            validation_stage=None,
            detected_operation=None,
            error_message=None,
            execution_time_ms=execution_time_ms,
            row_count=len(result)
        )

        return {
            "question": question,
            "sql": sql,
            "result": result
        }

    except Exception as e:

        execution_time_ms = (time.perf_counter() - execution_start) * 1000

        log_query(
            user_question=question,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=sql,
            status="EXECUTION_FAILED",
            validation_stage=None,
            detected_operation=None,
            error_message=str(e),
            execution_time_ms=execution_time_ms,
            row_count=0
        )

        raise SQLExecutionError(
            f"SQL execution failed: {str(e)}"
        )   