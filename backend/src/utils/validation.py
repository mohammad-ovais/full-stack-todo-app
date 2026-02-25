from typing import Optional
import re


def validate_email_format(email: str) -> bool:
    """
    Validate email format using regex
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    if len(password.encode('utf-8')) > 71:
        return False, "Password is too long (maximum 71 bytes)"

    return True, ""


def sanitize_input(text: str) -> str:
    """
    Basic input sanitization to prevent common injection attacks
    """
    # Remove null bytes
    sanitized = text.replace('\x00', '')

    # Remove common SQL injection patterns
    sql_patterns = [
        r"(?i)(union\s+select)",
        r"(?i)(drop\s+table)",
        r"(?i)(exec\s*\()",
        r"(?i)(script)",
    ]

    for pattern in sql_patterns:
        sanitized = re.sub(pattern, "", sanitized)

    return sanitized.strip()


def validate_todo_title(title: str) -> tuple[bool, str]:
    """
    Validate todo title
    Returns (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Title is required"

    if len(title.strip()) > 255:
        return False, "Title must be 255 characters or less"

    return True, ""


def validate_todo_description(description: Optional[str]) -> tuple[bool, str]:
    """
    Validate todo description
    Returns (is_valid, error_message)
    """
    if description is None:
        return True, ""

    if len(description) > 1000:  # Limit description length
        return False, "Description must be 1000 characters or less"

    return True, ""