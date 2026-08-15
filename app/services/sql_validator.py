import re

from app.services.validation_errors import SQLValidationError

FORBIDDEN_OPERATIONS = { "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE", }

ALLOWED_OPERATIONS = { "SELECT", "WITH", "EXPLAIN" }


def validate_sql(sql: str):

    cleaned_sql = sql.strip()

    if not cleaned_sql:
        raise SQLValidationError(
            operation="UNKNOWN",
            message="Generated SQL is empty."
        )

    sql_upper = cleaned_sql.upper()

    for op in FORBIDDEN_OPERATIONS:

        pattern = rf"\b{op}\b"

        if re.search(pattern, sql_upper):

            raise SQLValidationError(
                operation=op,
                message=(
                    f"Generated SQL contains forbidden operation: "
                    f"{op}. Only read-only SQL is allowed."
                )
            )

    first_keyword_match = re.match( r"^\s*(\w+)", sql_upper)

    if not first_keyword_match:

        raise SQLValidationError(
            operation="UNKNOWN",
            message="Unable to determine SQL operation."
        )

    first_keyword = first_keyword_match.group(1)

    if first_keyword not in ALLOWED_OPERATIONS:

        raise SQLValidationError(
            operation=first_keyword,
            message=(
                f"SQL operation '{first_keyword}' is not allowed. "
                "Only SELECT, WITH, and EXPLAIN statements are allowed."
            )
        )

    return cleaned_sql