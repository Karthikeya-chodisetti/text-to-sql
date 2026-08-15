import time
import pytest

from app.database.executor import execute_sql


def test_statement_timeout():

    start = time.perf_counter()

    with pytest.raises(Exception) as exc:

        execute_sql("SELECT pg_sleep(10);")

    elapsed = time.perf_counter() - start

    assert "statement timeout" in str(exc.value).lower()

    assert elapsed < 6