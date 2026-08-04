def build_prompt(schema: dict, question: str) -> str:
    schema_text = ""

    for table, info in schema.items():
        schema_text += f"Table: {table}\n"

        for column in info["columns"]:
            schema_text += (
                f"  - {column['name']} ({column['type']})\n"
            )

        if info["foreign_keys"]:
            schema_text += "Foreign Keys:\n"

            for fk in info["foreign_keys"]:
                schema_text += (
                    f"  - {fk['constrained_columns']} "
                    f"references "
                    f"{fk['referred_table']}."
                    f"{fk['referred_columns']}\n"
                )

        schema_text += "\n"

    prompt = f"""
        You are an expert PostgreSQL SQL generator.

        Database schema: {schema_text}

        Generate ONLY SQL query.

        User Question: {question} 

        Rules:
            - Return only SQL.
            - No markdown.
            - No explanations.
            - Use PostgreSQL syntax.
            - Use table relationships when required.
        
        """

    return prompt