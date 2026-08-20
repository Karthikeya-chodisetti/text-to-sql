import time

from app.services.result_cache import ( get_cached_result, set_cached_result, clear_cache )


def setup_function():
    clear_cache()


def test_cache_miss():

    result = get_cached_result("show customers")

    assert result is None


def test_cache_hit():

    set_cached_result(
        question="show customers",
        generated_sql="SELECT id, name, city FROM customers;",
        result=[
            {
                "id": 1,
                "name": "Rahul",
                "city": "Mysore"
            }
        ]
    )

    cached = get_cached_result("show customers")

    assert cached is not None
    assert cached["question"] == "show customers"
    assert cached["generated_sql"] == (
        "SELECT id, name, city FROM customers;"
    )
    assert cached["result"][0]["name"] == "Rahul"


def test_cache_question_normalization():

    set_cached_result(
        question="show customers",
        generated_sql="SELECT * FROM customers;",
        result=[]
    )

    cached = get_cached_result("  SHOW CUSTOMERS  ")

    assert cached is not None
    assert cached["generated_sql"] == (
        "SELECT * FROM customers;"
    )


def test_expired_cache():

    set_cached_result(
        question="show customers",
        generated_sql="SELECT * FROM customers;",
        result=[]
    )

    import app.services.result_cache as result_cache

    cache_key = result_cache._generate_cache_key(
        "show customers"
    )

    result_cache._cache[cache_key]["expires_at"] = (
        time.time() - 1
    )

    cached = get_cached_result("show customers")

    assert cached is None

    assert cache_key not in result_cache._cache


def test_clear_cache():

    set_cached_result(
        question="show customers",
        generated_sql="SELECT * FROM customers;",
        result=[]
    )

    assert get_cached_result("show customers") is not None

    clear_cache()

    assert get_cached_result("show customers") is None