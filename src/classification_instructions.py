prompt = """
Task:
You are an expert at identifying whether a request is simple or complicated based on its complexity, specificity, and requirements for specialized knowledge.

Instructions:
Classify the following task as either "Complicated" or "Not Complicated." A task is complicated if it:

Requires advanced reasoning or expert knowledge.
Involves multiple steps or dependencies.
Is ambiguous or ill-defined.
Otherwise, classify it as not complicated. Provide your classification along with a brief explanation for your choice.

Example Task:
"Write a short story about a dragon who learns to play the piano."

Your Response:
Not Complicated

Task to Classify:
"{user_prompt}"

Your Response should only be "Complicated" or "Not Complicated" and nothing else.
"""