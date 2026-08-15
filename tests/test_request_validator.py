import pytest

from app.services.request_validator import validate_request
from app.services.validation_errors import RequestValidationError


def test_read_only_request_is_allowed():

    result = validate_request(
        "Show all customers"
    )

    assert result is True


def test_drop_request_is_rejected():

    with pytest.raises(RequestValidationError):
        validate_request(
            "Drop all customers"
        )


def test_update_request_is_rejected():

    with pytest.raises(RequestValidationError):
        validate_request(
            "Update customer city to Delhi"
        )


def test_forbidden_operation_is_case_insensitive():

    with pytest.raises(RequestValidationError):
        validate_request(
            "dElEtE all customers"
        )