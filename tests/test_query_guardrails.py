import pytest

from app.services.query_guardrails import validate_query_guardrails
from app.services.validation_errors import QueryGuardrailError


def test_normal_select_is_allowed():

    sql = "SELECT * FROM customers;"

    assert validate_query_guardrails(sql) is True


def test_join_is_allowed():

    sql = """
    SELECT *
    FROM orders
    JOIN customers
        ON orders.customer_id = customers.id;
    """

    assert validate_query_guardrails(sql) is True


def test_cross_join_is_rejected():

    sql = """
    SELECT *
    FROM orders
    CROSS JOIN customers;
    """

    with pytest.raises(QueryGuardrailError) as exc:

        validate_query_guardrails(sql)

    assert exc.value.guardrail == "CROSS_JOIN"


def test_cross_join_case_insensitive():

    sql = """
    SELECT *
    FROM orders
    cross join customers;
    """

    with pytest.raises(QueryGuardrailError):

        validate_query_guardrails(sql)