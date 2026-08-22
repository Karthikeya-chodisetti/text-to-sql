import sqlglot
from sqlglot import expressions as exp

from app.services.validation_errors import SQLValidationError


def parse_sql(sql: str):

    cleaned_sql = sql.strip()

    if not cleaned_sql:
        raise SQLValidationError(
            operation="UNKNOWN",
            message="Generated SQL is empty."
        )

    try:
        statements = sqlglot.parse(
            cleaned_sql,
            read="postgres"
        )

    except sqlglot.errors.ParseError:

        raise SQLValidationError(
            operation="UNKNOWN",
            message="Generated SQL is invalid or could not be parsed."
        )

    if len(statements) != 1:
        raise SQLValidationError(
            operation="UNKNOWN",
            message="Multiple SQL statements are not allowed."
        )

    return statements[0]