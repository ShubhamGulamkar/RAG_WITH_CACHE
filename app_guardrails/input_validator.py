# from guardrails import Guard
# from pydantic import BaseModel, Field


# MAX_QUESTION_LENGTH = 1000


# class QuestionSchema(BaseModel):

#     question: str = Field(
#         min_length=1,
#         max_length=MAX_QUESTION_LENGTH
#     )


# guard = Guard.for_pydantic(
#     output_class=QuestionSchema
# )


# def validate_input(question):

#     try:

#         QuestionSchema(
#             question=question
#         )

#         return (
#             True,
#             None
#         )

#     except Exception as e:

#         return (
#             False,
#             str(e)
#         )

# import re


# MAX_QUESTION_LENGTH = 2000


# def validate_input(question: str):
#     """
#     Basic input validation for user question.
#     Returns:
#         (is_valid: bool, message: str)
#     """

#     if question is None:
#         return False, "Question cannot be empty."

#     question = question.strip()

#     if not question:
#         return False, "Question cannot be empty."

#     if len(question) > MAX_QUESTION_LENGTH:
#         return False, f"Question is too long. Max allowed length is {MAX_QUESTION_LENGTH} characters."

#     # block suspicious binary / null bytes
#     if "\x00" in question:
#         return False, "Invalid characters found in input."

#     # optional: block repeated junk symbols
#     if re.fullmatch(r"[\W_]+", question):
#         return False, "Question appears invalid."

#     return True, "Valid input"

import re
from typing import Tuple, Optional

from pydantic import BaseModel, Field, ValidationError


MAX_QUESTION_LENGTH = 1000
MIN_ALPHA_NUMERIC_CHARS = 3
MAX_URL_COUNT = 5
MAX_NEWLINES = 20
MAX_REPEAT_CHAR = 15
MAX_REPEAT_WORD = 8


class QuestionSchema(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=MAX_QUESTION_LENGTH
    )


# ---------------------------------------------------------
# Regex patterns for suspicious / unsafe input
# ---------------------------------------------------------
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+all\s+previous\s+instructions",
    r"ignore\s+previous\s+instructions",
    r"disregard\s+all\s+previous\s+instructions",
    r"forget\s+all\s+previous\s+instructions",
    r"you\s+are\s+now\s+developer",
    r"you\s+are\s+now\s+system",
    r"act\s+as\s+system",
    r"reveal\s+system\s+prompt",
    r"show\s+me\s+your\s+system\s+prompt",
    r"print\s+hidden\s+instructions",
    r"bypass\s+safety",
    r"disable\s+guardrails",
    r"do\s+not\s+follow\s+your\s+rules",
    r"override\s+your\s+instructions",
]

JAILBREAK_PATTERNS = [
    r"jailbreak",
    r"developer\s+mode",
    r"dan\s+mode",
    r"do\s+anything\s+now",
    r"unfiltered\s+mode",
    r"unsafe\s+mode",
    r"simulate\s+being\s+unrestricted",
]

SQL_INJECTION_PATTERNS = [
    r"(?i)\bunion\s+select\b",
    r"(?i)\bdrop\s+table\b",
    r"(?i)\binsert\s+into\b",
    r"(?i)\bdelete\s+from\b",
    r"(?i)\bupdate\s+\w+\s+set\b",
    r"(?i)\bor\s+1=1\b",
    r"(?i)'\s*or\s*'1'\s*=\s*'1",
    r"(?i)--",
    r"(?i)/\*.*\*/",
]

SCRIPT_INJECTION_PATTERNS = [
    r"(?i)<script.*?>.*?</script>",
    r"(?i)javascript:",
    r"(?i)onerror\s*=",
    r"(?i)onload\s*=",
    r"(?i)<iframe.*?>",
    r"(?i)<img.*?onerror=.*?>",
]

COMMAND_INJECTION_PATTERNS = [
    r"(?i)\brm\s+-rf\b",
    r"(?i)\bdel\s+/f\b",
    r"(?i)\bshutdown\b",
    r"(?i)\bformat\s+c:\b",
    r"(?i)\bcurl\s+http",
    r"(?i)\bwget\s+http",
    r"(?i)\bpowershell\b",
    r"(?i)\bcmd\.exe\b",
    r"(?i)\bbash\b",
]

PATH_TRAVERSAL_PATTERNS = [
    r"\.\./",
    r"\.\.\\",
    r"/etc/passwd",
    r"c:\\windows\\system32",
]

SUSPICIOUS_BASE64_PATTERN = r"\b[A-Za-z0-9+/]{200,}={0,2}\b"

URL_PATTERN = r"(https?://[^\s]+|www\.[^\s]+)"

CONTROL_CHAR_PATTERN = r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]"


# ---------------------------------------------------------
# Helper checks
# ---------------------------------------------------------
def _contains_control_chars(text: str) -> bool:
    return bool(re.search(CONTROL_CHAR_PATTERN, text))


def _has_too_many_urls(text: str) -> bool:
    urls = re.findall(URL_PATTERN, text, flags=re.IGNORECASE)
    return len(urls) > MAX_URL_COUNT


def _has_excessive_newlines(text: str) -> bool:
    return text.count("\n") > MAX_NEWLINES


def _has_repeated_characters(text: str) -> bool:
    """
    Example blocked:
    'heyyyyyyyyyyyyyyyy'
    '!!!!!!!!!!!!!!!!!'
    """
    return bool(re.search(r"(.)\1{" + str(MAX_REPEAT_CHAR - 1) + r",}", text))


def _has_repeated_words(text: str) -> bool:
    """
    Example blocked:
    'hello hello hello hello hello hello hello hello hello'
    """
    words = re.findall(r"\b\w+\b", text.lower())
    if not words:
        return False

    count = 1
    for i in range(1, len(words)):
        if words[i] == words[i - 1]:
            count += 1
            if count >= MAX_REPEAT_WORD:
                return True
        else:
            count = 1
    return False


def _has_too_many_symbols(text: str) -> bool:
    """
    If the input is mostly symbols and very little useful text,
    block it as low-quality / suspicious input.
    """
    if not text.strip():
        return False

    total_chars = len(text)
    symbol_chars = len(re.findall(r"[^A-Za-z0-9\s]", text))
    return total_chars > 20 and (symbol_chars / total_chars) > 0.60


def _has_minimum_meaningful_content(text: str) -> bool:
    """
    Require at least a small amount of alphanumeric content.
    """
    alnum_chars = len(re.findall(r"[A-Za-z0-9]", text))
    return alnum_chars >= MIN_ALPHA_NUMERIC_CHARS


def _looks_like_gibberish(text: str) -> bool:
    """
    Very simple heuristic:
    block if there are almost no vowels in a long alphabetic token.
    """
    tokens = re.findall(r"[A-Za-z]{12,}", text)
    for token in tokens:
        vowels = len(re.findall(r"[aeiouAEIOU]", token))
        if vowels <= 1:
            return True
    return False


def _matches_any_pattern(text: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            return True
    return False


def _detect_risk_category(text: str) -> Optional[str]:
    """
    Returns the first detected risk category, else None.
    Order matters: prompt injection first, then exploit patterns.
    """
    if _matches_any_pattern(text, PROMPT_INJECTION_PATTERNS):
        return "prompt_injection"

    if _matches_any_pattern(text, JAILBREAK_PATTERNS):
        return "jailbreak_attempt"

    if _matches_any_pattern(text, SCRIPT_INJECTION_PATTERNS):
        return "script_injection"

    if _matches_any_pattern(text, SQL_INJECTION_PATTERNS):
        return "sql_injection"

    if _matches_any_pattern(text, COMMAND_INJECTION_PATTERNS):
        return "command_injection"

    if _matches_any_pattern(text, PATH_TRAVERSAL_PATTERNS):
        return "path_traversal"

    if re.search(SUSPICIOUS_BASE64_PATTERN, text):
        return "suspicious_encoded_payload"

    return None


# ---------------------------------------------------------
# Main validation function
# ---------------------------------------------------------
def validate_input(question: str) -> Tuple[bool, Optional[str]]:
    """
    Validates the incoming user question and acts as a lightweight
    guardrails layer for Phase 3.

    Returns:
        (True, None) -> if valid
        (False, error_message) -> if invalid
    """
    try:
        # -------------------------------------------------
        # 1. Pydantic schema validation
        # -------------------------------------------------
        QuestionSchema(question=question)

        # -------------------------------------------------
        # 2. Null / whitespace checks
        # -------------------------------------------------
        if question is None:
            return False, "Question cannot be null."

        cleaned_question = question.strip()

        if not cleaned_question:
            return False, "Question cannot be empty or whitespace only."

        # -------------------------------------------------
        # 3. Meaningful content checks
        # -------------------------------------------------
        if not _has_minimum_meaningful_content(cleaned_question):
            return False, "Question does not contain enough meaningful text."

        if _looks_like_gibberish(cleaned_question):
            return False, "Question appears to contain invalid or nonsensical text."

        # -------------------------------------------------
        # 4. Low-quality / spam checks
        # -------------------------------------------------
        if _has_repeated_characters(cleaned_question):
            return False, "Question contains excessive repeated characters."

        if _has_repeated_words(cleaned_question):
            return False, "Question contains excessive repeated words."

        if _has_too_many_symbols(cleaned_question):
            return False, "Question contains too many special characters or symbols."

        if _has_excessive_newlines(cleaned_question):
            return False, "Question contains too many line breaks."

        # -------------------------------------------------
        # 5. Control character / malformed payload checks
        # -------------------------------------------------
        if _contains_control_chars(cleaned_question):
            return False, "Question contains invalid control characters."

        if _has_too_many_urls(cleaned_question):
            return False, "Question contains too many URLs."

        # -------------------------------------------------
        # 6. Security / injection / jailbreak checks
        # -------------------------------------------------
        risk_category = _detect_risk_category(cleaned_question)
        if risk_category:
            return False, f"Blocked unsafe input. Detected category: {risk_category}"

        # -------------------------------------------------
        # Passed all checks
        # -------------------------------------------------
        return True, None

    except ValidationError as e:
        return False, e.errors()[0]["msg"]

    except Exception as e:
        return False, str(e)