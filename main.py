from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.database.schema_loader import get_database_schema
from app.services.text_to_sql_service import answer_question
from app.services.validation_errors import AppError

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
        res = answer_question(request.question)

        return {
            "success": True,
            **res
        }

    except AppError as e:
        
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "error": e.message
            }
        )
    
    except Exception as e:

        print("UNEXPECTED ERROR:", repr(e))

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "An unexpected internal error occurred."
            }
        )