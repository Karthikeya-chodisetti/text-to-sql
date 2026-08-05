from app.database.executor import execute_sql


def test_execute_sql():

    result = execute_sql("SELECT 1 AS value")

    assert result == [
        {
            "value": 1
        }
    ]