from sqlalchemy import text
from app.database.connection import db_engine

def test_database_connection():
    
    with db_engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        assert result.scalar() == 1