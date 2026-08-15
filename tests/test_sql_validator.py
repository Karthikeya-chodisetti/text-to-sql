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


def test_update_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("UPDATE customers SET city = 'Delhi';")

    assert exc.value.operation == "UPDATE"


def test_delete_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("DELETE FROM customers;")

    assert exc.value.operation == "DELETE"


def test_drop_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("DROP TABLE customers;")

    assert exc.value.operation == "DROP"


def test_alter_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql(
            "ALTER TABLE customers ADD COLUMN age INTEGER;"
        )

    assert exc.value.operation == "ALTER"


def test_truncate_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("TRUNCATE TABLE customers;")

    assert exc.value.operation == "TRUNCATE"


def test_create_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql("CREATE TABLE test(id INTEGER);")

    assert exc.value.operation == "CREATE"


def test_grant_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql(
            "GRANT SELECT ON customers TO user1;"
        )

    assert exc.value.operation == "GRANT"


def test_revoke_is_rejected():

    with pytest.raises(SQLValidationError) as exc:
        validate_sql(
            "REVOKE SELECT ON customers FROM user1;"
        )

    assert exc.value.operation == "REVOKE"


def test_empty_sql_is_rejected():

    with pytest.raises(SQLValidationError):
        validate_sql("")