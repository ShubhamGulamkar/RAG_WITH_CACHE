def generate_answer(
    question,
    context
):

    return f"""
Question:
{question}

Context:
{context}

Generated Answer:
This answer was generated
using retrieved chunks.
"""