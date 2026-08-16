import pytest

import app.database.schema_loader as schema_loader


def test_schema_cache_miss_loads_schema(monkeypatch):

    schema_loader._schema_cache = None

    inspect_calls = 0

    class FakeInspector:

        def get_table_names(self):
            nonlocal inspect_calls
            inspect_calls += 1
            return ["customers"]

        def get_columns(self, table):
            return [
                {
                    "name": "id",
                    "type": "INTEGER",
                    "nullable": False,
                    "default": None,
                    "autoincrement": True
                }
            ]

        def get_pk_constraint(self, table):
            return {
                "constrained_columns": ["id"]
            }

        def get_foreign_keys(self, table):
            return []

    monkeypatch.setattr(
        schema_loader,
        "inspect",
        lambda engine: FakeInspector()
    )

    schema = schema_loader.get_database_schema()

    assert "customers" in schema
    assert schema["customers"]["columns"][0]["name"] == "id"
    assert inspect_calls == 1

def test_schema_cache_hit_does_not_inspect_database(monkeypatch):

    schema_loader._schema_cache = {
        "customers": {
            "columns": [
                {
                    "name": "id",
                    "type": "INTEGER",
                    "nullable": False,
                    "default": None,
                    "autoincrement": True
                }
            ],
            "primary_keys": ["id"],
            "foreign_keys": []
        }
    }

    def fail_if_called(engine):
        pytest.fail("Database inspection should not happen when cache exists.")

    monkeypatch.setattr(
        schema_loader,
        "inspect",
        fail_if_called
    )

    schema = schema_loader.get_database_schema()

    assert "customers" in schema
    assert schema["customers"]["primary_keys"] == ["id"]


def test_refresh_replaces_existing_cache(monkeypatch):

    old_schema = {
        "old_table": {
            "columns": [],
            "primary_keys": [],
            "foreign_keys": []
        }
    }

    schema_loader._schema_cache = old_schema

    class FakeInspector:

        def get_table_names(self):
            return ["new_table"]

        def get_columns(self, table):
            return []

        def get_pk_constraint(self, table):
            return {
                "constrained_columns": []
            }

        def get_foreign_keys(self, table):
            return []

    monkeypatch.setattr(
        schema_loader,
        "inspect",
        lambda engine: FakeInspector()
    )

    new_schema = schema_loader.refresh_schema_cache()

    assert new_schema != old_schema
    assert "old_table" not in new_schema
    assert "new_table" in new_schema

    assert schema_loader._schema_cache == new_schema
