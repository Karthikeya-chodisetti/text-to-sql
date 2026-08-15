import time
import os

from app.database.executor import execute_sql
from app.database.schema_loader import get_database_schema
from app.database.query_logger import log_query
from app.llm.prompt_builder import build_prompt
from app.llm.gemini_client import generate_sql


MODEL_NAME = os.getenv("GEMINI_MODEL")


def answer_question(question: str):

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
            prompt=prompt,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql="",
            status="LLM_FAILED",
            execution_error=str(e),
            execution_time_ms=generation_time_ms,
            row_count=0
        )

        raise

    execution_start = time.perf_counter()

    try:

        result = execute_sql(sql)

        execution_time_ms = (time.perf_counter() - execution_start) * 1000

        log_query(
            user_question=question,
            prompt=prompt,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=sql,
            status="SUCCESS",
            execution_error=None,
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
            prompt=prompt,
            schema_snapshot=schema,
            model=MODEL_NAME,
            generated_sql=sql,
            status="SQL_FAILED",
            execution_error=str(e),
            execution_time_ms=execution_time_ms,
            row_count=0
        )

        raise