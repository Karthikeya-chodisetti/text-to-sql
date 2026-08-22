from app.services.sql_parser import parse_sql
from app.services.validation_errors import SQLValidationError

ALLOWED_OPERATIONS = { "SELECT", "WITH", "EXPLAIN", }

def validate_sql(sql: str):

    tree = parse_sql(sql)

    operation = tree.key.upper()

    if operation not in ALLOWED_OPERATIONS:

        raise SQLValidationError(
            operation=operation,
            message=(
                f"SQL operation '{operation}' is not allowed. "
                "Only SELECT, WITH, and EXPLAIN statements are allowed."
            )
        )

    return sql.strip()