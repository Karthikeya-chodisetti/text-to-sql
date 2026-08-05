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