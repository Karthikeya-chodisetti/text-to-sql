from app.database.query_logger import log_query


def test_log_query():

    log_query(
        user_question="Show all customers",
        prompt="Generate SQL for: Show all customers",
        schema_snapshot={
            "customers": {
                "columns": [
                    {
                        "name": "id",
                        "type": "INTEGER"
                    }
                ]
            }
        },
        model="gemini-000-turbo-lite",
        generated_sql="SELECT * FROM customers;",
        status="SUCCESS",
        execution_error=None,
        execution_time_ms=4.55,
        row_count=3
    )