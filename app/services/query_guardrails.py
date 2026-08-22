from sqlglot import exp
from app.services.sql_parser import parse_sql
from app.services.validation_errors import QueryGuardrailError

MAX_JOINS = 5
MAX_SUBQUERY_DEPTH = 3


def validate_query_guardrails(sql: str):

    tree = parse_sql(sql)

    _check_cross_join(tree)
    _check_cartesian_product(tree)
    _check_max_joins(tree)
    _check_subquery_depth(tree)

    return True


def _check_cross_join(tree):

    for join in tree.find_all(exp.Join):

        if join.args.get("kind") == "CROSS":

            raise QueryGuardrailError(
                guardrail="CROSS_JOIN",
                message=(
                    "Query contains a potentially expensive CROSS JOIN. "
                    "Queries with CROSS JOIN are not allowed."
                )
            )


def _check_cartesian_product(tree):

    for join in tree.find_all(exp.Join):

        if ( join.args.get("on") is None and join.args.get("using") is None ):

            if join.args.get("kind") == "CROSS":
                continue

            raise QueryGuardrailError(
                guardrail="CARTESIAN_PRODUCT",
                message=(
                    "Query contains a JOIN without a join condition. "
                    "This may produce a Cartesian product."
                )
            )


def _check_max_joins(tree):

    join_count = sum(
        1 for _ in tree.find_all(exp.Join)
    )

    if join_count > MAX_JOINS:

        raise QueryGuardrailError(
            guardrail="MAX_JOINS",
            message=(
                f"Query contains {join_count} JOINs. "
                f"The maximum allowed is {MAX_JOINS}."
            )
        )


def _check_subquery_depth(tree):

    def calculate_depth(node, current_depth=0):

        if isinstance(node, exp.Subquery):
            current_depth += 1

        max_depth = current_depth

        for child in node.iter_expressions():

            child_depth = calculate_depth(child, current_depth )

            max_depth = max( max_depth, child_depth)

        return max_depth

    depth = calculate_depth(tree)

    if depth > MAX_SUBQUERY_DEPTH:

        raise QueryGuardrailError(
            guardrail="SUBQUERY_DEPTH",
            message=(
                f"Query contains subquery nesting depth {depth}. "
                f"The maximum allowed is {MAX_SUBQUERY_DEPTH}."
            )
        )