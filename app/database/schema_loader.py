from sqlalchemy import inspect
from app.database.connection import engine


def load_schema():
    inspector = inspect(engine)

    schema = {}

    tables = inspector.get_table_names()

    for table in tables:
        columns = inspector.get_columns(table)
        primary_keys = inspector.get_pk_constraint(table)
        foreign_keys = inspector.get_foreign_keys(table)

        schema[table] = {
            "columns": [],
            "primary_keys": primary_keys["constrained_columns"],
            "foreign_keys": foreign_keys
        }

        for column in columns:
            schema[table]["columns"].append(
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"]
                }
            )

    return schema


if __name__ == "__main__":
    import pprint

    result = load_schema()
    pprint.pprint(result)