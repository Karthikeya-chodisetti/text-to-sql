from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database.schema_loader import get_database_schema
from app.services.text_to_sql_service import answer_question
from app.services.validation_errors import (
    RequestValidationError, SQLValidationError, SQLExecutionError, QueryGuardrailError
)

app = FastAPI(
    title="Text-to-SQL API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Text-to-SQL API is running"}

@app.get("/schema")
def get_schema():
    return { "tables": get_database_schema() }

class QueryRequest(BaseModel):
    question: str

@app.post("/generate-sql")
def generate(request: QueryRequest):

    try:
        return answer_question(request.question)

    except ( RequestValidationError, SQLValidationError, SQLExecutionError, QueryGuardrailError) as e:
        raise HTTPException(
            status_code=400,
            detail=e.message
        )
    