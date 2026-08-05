from app.database.executor import execute_sql
from app.database.schema_loader import get_database_schema
from app.llm.prompt_builder import build_prompt
from app.llm.gemini_client import generate_sql


def answer_question(question: str):

    schema = get_database_schema()

    prompt = build_prompt(schema, question)

    sql = generate_sql(prompt)

    result = execute_sql(sql)

    return {
        "question": question,
        "sql": sql,
        "result": result
    }