from app.database.query_logger import log_query


def test_log_query():

    log_query(
        user_question="Show all customers",
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
        validation_stage=None,
        detected_operation=None,
        error_message=None,
        execution_time_ms=4.1234567,
        row_count=0,
        retry_count=0,
    )