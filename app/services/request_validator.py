import re
from app.services.validation_errors import RequestValidationError

FORBIDDEN_OPERATIONS = { "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE", }

def validate_request(question: str):

    question_upper = question.upper()

    for op in FORBIDDEN_OPERATIONS:

        pattern = rf"\b{op}\b"

        if re.search(pattern, question_upper):

           raise RequestValidationError(
                operation=op,
                message=(
                    f"Request contains forbidden operation: {op}. "
                    "Only read-only requests are allowed."
                )
            )

    return True