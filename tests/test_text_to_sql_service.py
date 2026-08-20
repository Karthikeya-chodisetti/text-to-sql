import pytest
from unittest.mock import patch

from app.services.text_to_sql_service import answer_question
from app.services.validation_errors import SQLValidationError
from app.services.result_cache import clear_cache

def setup_function():
    clear_cache()

@patch("app.services.text_to_sql_service.execute_sql")
@patch(
    "app.services.text_to_sql_service.generate_sql",
    return_value="DROP TABLE customers;"
)
@patch(
    "app.services.text_to_sql_service.get_database_schema",
    return_value={
        "customers": {
            "columns": [
                {
                    "name": "id",
                    "type": "INTEGER",
                    "nullable": False,
                    "default": None,
                    "autoincrement": True
                }
            ],
            "primary_keys": ["id"],
            "foreign_keys": []
        }
    }
)
def test_dangerous_generated_sql_is_rejected(
    mock_schema,
    mock_generate_sql,
    mock_execute_sql
):

    with pytest.raises(SQLValidationError) as exc:
        answer_question("show customers")

    assert exc.value.operation == "DROP"

    mock_execute_sql.assert_not_called()