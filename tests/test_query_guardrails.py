import pytest

from app.services.query_guardrails import validate_query_guardrails
from app.services.validation_errors import QueryGuardrailError


def test_normal_join_is_allowed():

    sql = """
    SELECT c.id, o.amount
    FROM customers c
    JOIN orders o
        ON c.id = o.customer_id;
    """

    assert validate_query_guardrails(sql) is True


def test_cross_join_is_rejected():

    sql = """
    SELECT *
    FROM customers
    CROSS JOIN orders;
    """

    with pytest.raises(QueryGuardrailError) as exc:

        validate_query_guardrails(sql)

    assert exc.value.guardrail == "CROSS_JOIN"


def test_cartesian_product_is_rejected():

    sql = """
    SELECT *
    FROM customers c
    JOIN orders o;
    """

    with pytest.raises(QueryGuardrailError) as exc:

        validate_query_guardrails(sql)

    assert exc.value.guardrail == "CARTESIAN_PRODUCT"


def test_max_joins_is_rejected():

    sql = """
    SELECT *
    FROM a
    JOIN b ON a.id = b.a_id
    JOIN c ON b.id = c.b_id
    JOIN d ON c.id = d.c_id
    JOIN e ON d.id = e.d_id
    JOIN f ON e.id = f.e_id
    JOIN g ON f.id = g.f_id;
    """

    with pytest.raises(QueryGuardrailError) as exc:

        validate_query_guardrails(sql)

    assert exc.value.guardrail == "MAX_JOINS"


def test_subquery_depth_exceeded_is_rejected():

    sql = """
    SELECT *
    FROM (
        SELECT *
        FROM (
            SELECT *
            FROM (
                SELECT *
                FROM (
                    SELECT *
                    customers
                ) a
            ) b
        ) c
    ) d;
    """

    with pytest.raises(QueryGuardrailError) as exc:

        validate_query_guardrails(sql)

    assert exc.value.guardrail == "SUBQUERY_DEPTH"