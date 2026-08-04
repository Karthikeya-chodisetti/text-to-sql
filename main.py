from fastapi import FastAPI
from app.database.schema_loader import load_schema

from pydantic import BaseModel
from app.llm.prompt_builder import build_prompt
from app.llm.client import generate_sql
from app.services.sql_executor import execute_sql

app = FastAPI(
    title="Text-to-SQL API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Text-to-SQL API is running"}


@app.get("/schema")
def get_schema():
    schema = load_schema()

    return{
        "tables": schema
    }


class QueryRequest(BaseModel):
    question: str


@app.post("/generate-sql")
def generate(request: QueryRequest):

    schema = load_schema()

    prompt = build_prompt(
        schema=schema,
        question=request.question
    )

    sql = generate_sql(prompt)

    result = execute_sql(sql)

    return {
        "question": request.question,
        "sql": sql,
        "result": result
    }