from fastapi import FastAPI
from app.database.schema_loader import load_schema

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

    return "tables": schema