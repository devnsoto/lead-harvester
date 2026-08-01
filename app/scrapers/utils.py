"""
Shared Scraper Utilities

Common functions used across all platform scrapers.

Provides:
- extract_email() — regex-based email extraction from text
- extract_phone() — phone number extraction from text
- parse_abbreviated_number() — converts "11.5K", "2.3M" to integers
"""

import re
from typing import List, Optional

# A single, correct email regex used by helpers here. It's intentionally simple
# and not fully RFC-complete, but works well for typical profile scraping.
_EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", re.IGNORECASE)


def extract_email(text: str) -> str:
    """Extract the first email address from text.

    Returns an empty string if none found. The returned email is stripped of
    surrounding punctuation and normalized to lower-case to reduce duplicates.
    """
    if not text:
        return ''
    matches = _EMAIL_PATTERN.findall(text)
    if not matches:
        return ''
    # Normalize and strip common trailing punctuation
    email = matches[0].strip("'\".,;:()[]{} ")
    return email.lower()


def extract_phone(text: str) -> str:
    """Extract the first phone number (10+ digits) from text.

    The function will return a digits-only string, prefixed with '+' if a
    leading plus sign was present. It aims to be forgiving for different
    formatting but requires at least 10 digits to consider it a phone.
    """
    if not text:
        return ''

    # Common phone patterns to capture various formats
    patterns = [
        r"\+?[\d\s().-]{10,}",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Clean the match to digits, keep leading + if present
            raw = matches[0].strip()
            leading_plus = raw.startswith('+')
            digits = re.sub(r'[^0-9]', '', raw)
            if len(digits) >= 10:
                return ('+' if leading_plus else '') + digits

    return ''


def parse_abbreviated_number(s: str) -> int:
    """Parse abbreviated numbers like 11M, 7.5K, 1.2B into integers."""
    if not s:
        return 0
    s = s.strip().replace(',', '')
    multipliers = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000}

    for suffix, mult in multipliers.items():
        if s.upper().endswith(suffix):
            try:
                return int(float(s[:-1]) * mult)
            except (ValueError, IndexError):
                return 0

    try:
        return int(float(s))
    except ValueError:
        return 0
