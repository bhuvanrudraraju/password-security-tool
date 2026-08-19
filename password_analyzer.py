"""Local-only password-strength analysis.

This module intentionally never writes a password to disk or prints it. It is
an educational heuristic, not a guarantee that a password is safe.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# A deliberately small list keeps the project understandable. In a production
# tool this would be replaced with a maintained breached-password service.
COMMON_PASSWORDS = {
    "password", "password1", "123456", "12345678", "123456789",
    "qwerty", "abc123", "letmein", "welcome", "admin", "iloveyou",
}

KEYBOARD_SEQUENCES = ("qwerty", "asdf", "zxcv", "12345", "23456", "34567")


@dataclass
class AnalysisResult:
    """A password assessment that deliberately excludes the password itself."""

    rating: str
    score: int
    reasons: list[str]
    recommendations: list[str]


def _has_repeated_characters(password: str) -> bool:
    """Return True for a run of three or more identical characters, e.g. aaa."""
    return bool(re.search(r"(.)\1{2,}", password, re.IGNORECASE))


def _has_sequence(password: str) -> bool:
    """Detect common keyboard and ascending/descending number sequences."""
    lower_password = password.lower()
    if any(sequence in lower_password for sequence in KEYBOARD_SEQUENCES):
        return True

    digits = "0123456789"
    return any(
        digits[index : index + 4] in password
        or digits[index : index + 4][::-1] in password
        for index in range(len(digits) - 3)
    )


def analyze_password(password: str) -> AnalysisResult:
    """Assess one password in memory and return non-sensitive feedback.

    The score begins at zero. Good traits add points and predictable traits
    subtract points. The final value is limited to 0--10 for a simple rating.
    """
    score = 0
    reasons: list[str] = []
    recommendations: list[str] = []
    password_lower = password.lower()

    if len(password) >= 20:
        score += 5
        reasons.append("It has 20 or more characters.")
    elif len(password) >= 16:
        score += 4
        reasons.append("It has 16 or more characters.")
    elif len(password) >= 12:
        score += 3
        reasons.append("It has at least 12 characters.")
    elif len(password) >= 8:
        score += 1
        reasons.append("It has at least 8 characters, but a longer passphrase is safer.")
        recommendations.append("Use at least 12 characters; 16 or more is even better.")
    else:
        reasons.append("It is shorter than 8 characters.")
        recommendations.append("Use at least 12 characters; 16 or more is even better.")

    character_checks = {
        "uppercase letters": any(char.isupper() for char in password),
        "lowercase letters": any(char.islower() for char in password),
        "numbers": any(char.isdigit() for char in password),
        "symbols": any(not char.isalnum() for char in password),
    }
    diversity = sum(character_checks.values())
    score += diversity
    reasons.append(f"It uses {diversity} of 4 character types.")
    missing_types = [name for name, present in character_checks.items() if not present]
    if missing_types:
        recommendations.append("Add " + ", ".join(missing_types) + ".")

    if password_lower in COMMON_PASSWORDS:
        score -= 7
        reasons.append("It matches a commonly used password.")
        recommendations.append("Do not use common or previously used passwords.")

    if _has_repeated_characters(password):
        score -= 2
        reasons.append("It contains a run of repeated characters.")
        recommendations.append("Avoid repeated runs such as 'aaa' or '111'.")

    if _has_sequence(password):
        score -= 2
        reasons.append("It contains a predictable keyboard or number sequence.")
        recommendations.append("Avoid sequences such as '1234' and 'qwerty'.")

    score = max(0, min(10, score))
    if score <= 2:
        rating = "Very Weak"
    elif score <= 4:
        rating = "Weak"
    elif score <= 6:
        rating = "Moderate"
    elif score <= 8:
        rating = "Strong"
    else:
        rating = "Very Strong"

    if not recommendations:
        recommendations.append("Keep it unique for every account and store it in a password manager.")

    return AnalysisResult(rating, score, reasons, recommendations)
