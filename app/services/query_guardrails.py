import re

from app.services.validation_errors import QueryGuardrailError


def validate_query_guardrails(sql: str):

    sql_upper = sql.upper()

    if re.search(r"\bCROSS\s+JOIN\b", sql_upper):

        raise QueryGuardrailError(
            guardrail="CROSS_JOIN",
            message=(
                "Query contains a potentially expensive CROSS JOIN. "
                "Queries with CROSS JOIN are not allowed."
            )
        )

    return True