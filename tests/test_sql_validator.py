import pytest

from app.services.sql_validator import validate_sql
from app.services.validation_errors import SQLValidationError


def test_select_is_allowed():

    sql = "SELECT * FROM customers;"

    result = validate_sql(sql)

    assert result == sql


def test_with_is_allowed():

    sql = """
    WITH customer_orders AS (
        SELECT customer_id, SUM(amount) AS total
        FROM orders
        GROUP BY customer_id
    )
    SELECT *
    FROM customer_orders;
    """

    result = validate_sql(sql)

    assert result == sql.strip()


def test_insert_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("INSERT INTO customers(name) VALUES ('Alice');")

    assert exc.value.operation == "INSERT"


def test_create_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("CREATE TABLE test(id INTEGER);")

    assert exc.value.operation == "CREATE"


def test_revoke_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql(
            "REVOKE SELECT ON customers FROM user1;"
        )

    assert exc.value.operation == "REVOKE"


def test_empty_sql_is_rejected():

    with pytest.raises(SQLValidationError):
        validate_sql("")

def test_forbidden_word_inside_string_is_allowed():

    sql = """
    SELECT *
    FROM customers
    WHERE name = 'DROP TABLE customers';
    """

    result = validate_sql(sql)

    assert result == sql.strip()

def test_invalid_sql_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql(
            "SELECT * FROM customers WHERE;"
        )

    assert exc.value.operation == "UNKNOWN"

def test_multiple_statements_are_rejected():

    sql = """
    SELECT * FROM customers;
    DROP TABLE customers;
    """

    with pytest.raises(SQLValidationError):
        validate_sql(sql)