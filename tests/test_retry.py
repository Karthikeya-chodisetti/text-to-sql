from unittest.mock import patch

import pytest

from app.services.text_to_sql_service import answer_question
from app.services.validation_errors import SQLExecutionError


@patch("app.services.text_to_sql_service.log_query")
@patch("app.services.text_to_sql_service.execute_sql")
@patch("app.services.text_to_sql_service.generate_sql")
def test_no_retry_needed(
    mock_generate_sql,
    mock_execute_sql,
    mock_log_query
):
    """
    Case 1:
    SQL succeeds on the first attempt.
    No retry should happen.
    """

    mock_generate_sql.return_value = "SELECT * FROM customers;"
    mock_execute_sql.return_value = [
        {"id": 1, "name": "Rahul", "city": "Mysore"}
    ]

    result = answer_question("show customers")

    assert result["sql"] == "SELECT * FROM customers;"
    assert len(result["result"]) == 1

    assert mock_generate_sql.call_count == 1

    assert mock_execute_sql.call_count == 1


@patch("app.services.text_to_sql_service.log_query")
@patch("app.services.text_to_sql_service.execute_sql")
@patch("app.services.text_to_sql_service.generate_sql")
def test_retry_succeeds(
    mock_generate_sql,
    mock_execute_sql,
    mock_log_query
):
    """
    Case 2:
    First SQL fails.
    Retry generates corrected SQL.
    Corrected SQL succeeds.
    """

    mock_generate_sql.side_effect = [
        "SELECT cust_id FROM customers;",
        "SELECT id FROM customers;"
    ]

    mock_execute_sql.side_effect = [
        Exception('column "cust_id" does not exist'),
        [
            {"id": 1},
            {"id": 2}
        ]
    ]

    result = answer_question("show customers")

    assert result["sql"] == "SELECT id FROM customers;"
    assert len(result["result"]) == 2

    assert mock_generate_sql.call_count == 2

    assert mock_execute_sql.call_count == 2


@patch("app.services.text_to_sql_service.log_query")
@patch("app.services.text_to_sql_service.execute_sql")
@patch("app.services.text_to_sql_service.generate_sql")
def test_retry_also_fails(
    mock_generate_sql,
    mock_execute_sql,
    mock_log_query
):
    """
    Case 3:
    First SQL fails.
    Retry also fails.
    No more retries are allowed.
    """

    mock_generate_sql.side_effect = [
        "SELECT cust_id FROM customers;",
        "SELECT abc123 FROM customers;"
    ]

    mock_execute_sql.side_effect = [
        Exception('column "cust_id" does not exist'),
        Exception('column "abc123" does not exist')
    ]

    with pytest.raises(SQLExecutionError):
        answer_question("show customers")

    assert mock_generate_sql.call_count == 2

    assert mock_execute_sql.call_count == 2