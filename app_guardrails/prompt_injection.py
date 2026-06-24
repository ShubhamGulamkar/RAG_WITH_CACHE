import re


PROMPT_ATTACK_PATTERNS = [

    "ignore previous instructions",

    "ignore all instructions",

    "forget previous instructions",

    "reveal system prompt",

    "show system prompt",

    "show developer prompt",

    "developer message",

    "bypass security",

    "jailbreak",

    "override instructions",

    "act as root",

    "act as admin",

    "disable guardrails",

    "ignore safety",

    "system:"
]


def detect_prompt_injection(question):

    question = question.lower()

    for pattern in PROMPT_ATTACK_PATTERNS:

        if pattern in question:

            return (
                True,
                pattern
            )

    return (
        False,
        None
    )