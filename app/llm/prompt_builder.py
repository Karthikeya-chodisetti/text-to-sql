def format_schema(schema: dict) -> str:

    lines = []

    lines.append("Database Schema")
    lines.append("")


    for table, info in schema.items():

        lines.append(
            f"Table: {table}"
        )

        lines.append(
            "Columns:"
        )

        for column in info["columns"]:

            column_line = (
                f"- {column['name']} "
                f"{column['type']}"
            )

            if not column["nullable"]:
                column_line += " NOT NULL"

            lines.append(column_line)


        if info["primary_keys"]:

            lines.append(
                "Primary Key:"
            )

            for pk in info["primary_keys"]:
                lines.append(
                    f"- {pk}"
                )


        if info["foreign_keys"]:

            lines.append(
                "Relationships:"
            )

            for fk in info["foreign_keys"]:

                lines.append(
                    f"- {fk['column']} -> "
                    f"{fk['references']}"
                )

        lines.append("")

    return "\n".join(lines)



def build_prompt(schema: dict, question: str) -> str:

    schema_text = format_schema(schema)

    prompt = f"""
You are an expert PostgreSQL SQL generator.

{schema_text}

This system is strictly read-only.

If the user's request implies any data modification, schema modification, permission modification, or database administration operation,
DO NOT attempt to convert it into a SELECT query.

Examples:
User: "Change Rahul's address to Mumbai"
Output: REJECTED_REQUEST

User: "Rename customer column"
Output: REJECTED_REQUEST

User: "Create a new table"
Output: REJECTED_REQUEST

User: "Grant access to user1"
Output: REJECTED_REQUEST

Only generate SQL for genuine read-only requests.

User Question: {question}

Rules:
- Return exactly one valid PostgreSQL SELECT statement.
- Return only SQL.
- Do not include markdown.
- Do not include comments.
- Do not include explanations.
- Use PostgreSQL syntax.
- Use table relationships when required.
- Generate only read-only SQL.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
"""

    return prompt.strip()

def build_retry_prompt(
    schema: dict,
    question: str,
    previous_sql: str,
    database_error: str
) -> str:

    schema_text = format_schema(schema)

    prompt = f"""
You are an expert PostgreSQL SQL generator.

{schema_text}

The previously generated SQL failed during database execution.

User Question:
{question}

Previous SQL:
{previous_sql}

Database Error:
{database_error}

Correct the SQL based on the database error and the provided schema.

Rules:
- Return exactly one valid PostgreSQL SELECT statement.
- Return only SQL.
- Use only tables and columns present in the provided database schema.
- Do not invent table names.
- Do not invent column names.
- If the requested information cannot be obtained from the schema, return REJECTED_REQUEST.
- Do not include markdown.
- Do not include comments.
- Do not include explanations.
- Use PostgreSQL syntax.
- Use the provided database schema.
- Generate only read-only SQL.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, or REVOKE.
"""

    return prompt.strip()