from app_guardrails.input_validator import (
    validate_input
)

from app_guardrails.prompt_injection import (
    detect_prompt_injection
)

from app_guardrails.pii_detector import (
    detect_pii
)


def run_guardrails(question):

    print(
        "\n=================================================="
    )

    print(
        "GUARDRAILS STARTED"
    )

    print(
        "=================================================="
    )

    print(
        f"Question: {question}"
    )

    # -----------------------------
    # INPUT VALIDATION
    # -----------------------------

    valid, error = (
        validate_input(
            question
        )
    )

    if not valid:

        print(
            "INPUT VALIDATION FAILED"
        )

        print(error)

        return (
            False,
            "Invalid Input"
        )

    print(
        "INPUT VALIDATION PASSED"
    )

    # -----------------------------
    # PROMPT INJECTION
    # -----------------------------

    attack_found, attack_type = (
        detect_prompt_injection(
            question
        )
    )

    if attack_found:

        print(
            "PROMPT INJECTION DETECTED"
        )

        print(
            f"Pattern: {attack_type}"
        )

        return (
            False,
            "Prompt Injection Detected"
        )

    print(
        "PROMPT INJECTION CHECK PASSED"
    )

    # -----------------------------
    # PII DETECTION
    # -----------------------------

    pii_results = (
        detect_pii(
            question
        )
    )

    if pii_results:

        print(
            f"PII FOUND: {len(pii_results)}"
        )

        for item in pii_results:

            print(item)

    else:

        print(
            "NO PII FOUND"
        )

    print(
        "GUARDRAILS PASSED"
    )

    print(
        "=================================================="
    )

    return (
        True,
        None
    )