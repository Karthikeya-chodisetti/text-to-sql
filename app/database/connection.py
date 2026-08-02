from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

# def test_connection():
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             print("Database connection successful:", result.scalar())

#     except Exception as e:
#         print("Database connection failed:")
#         print(e)


# if __name__ == "__main__":
#     test_connection()