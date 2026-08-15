from sqlalchemy import inspect
from app.database.connection import db_engine

EXCLUDED_TABLES = { "query_logs" }

def get_database_schema():

    try:
        inspector = inspect(db_engine)

        schema = {}

        tables = inspector.get_table_names()

        for table in tables:

            if table in EXCLUDED_TABLES:
                continue
                
            columns = inspector.get_columns(table)
            primary_keys = inspector.get_pk_constraint(table)
            foreign_keys = inspector.get_foreign_keys(table)

            column_data = []

            for column in columns:

                column_data.append(
                    {
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column["nullable"],
                        "default": column["default"],
                        "autoincrement": column.get(
                            "autoincrement",
                            False
                        )
                    }
                )


            foreign_key_data = []

            for fk in foreign_keys:

                constrained_columns = fk["constrained_columns"]

                referred_table = fk["referred_table"]

                referred_columns = fk["referred_columns"]
                
                for column, ref_column in zip(constrained_columns, referred_columns):

                    foreign_key_data.append(
                        {
                            "column": column,
                            "references": ( f"{referred_table}.{ref_column}" )
                        }
                    )

            schema[table] = {

                "columns": column_data,

                "primary_keys": (
                    primary_keys[
                        "constrained_columns"
                    ]
                ),

                "foreign_keys": foreign_key_data
            }


        return schema


    except Exception as e:

        raise Exception(
            f"Unable to inspect database schema: {e}"
        )


if __name__ == "__main__":
    import pprint

    result = get_database_schema()
    pprint.pprint(result)