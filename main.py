from fastapi import FastAPI
from pydantic import BaseModel

from app.database.schema_loader import get_database_schema
from app.services.text_to_sql_service import answer_question


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
    return answer_question(request.question)