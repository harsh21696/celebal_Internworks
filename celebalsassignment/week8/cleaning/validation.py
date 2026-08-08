"""
validation.py
==============
Thin wrapper module exposing the two validation-focused functions
(validate_emails, check_referential_integrity) separately from the
cleaning transformations in clean_data.py, matching the project's
folder structure. Both are re-used directly from clean_data.py so
there is a single source of truth for the logic.

Usage:
    from validation import validate_emails, check_referential_integrity
"""

from clean_data import validate_emails, check_referential_integrity  # noqa: F401

__all__ = ["validate_emails", "check_referential_integrity"]
