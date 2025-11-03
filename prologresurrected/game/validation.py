"""
Prolog Validation Utilities

This module provides validation functionality for Prolog facts and queries,
including syntax checking, component parsing, and error message generation
for the Hello World Prolog tutorial.
"""

import re
import random
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class ValidationResult:
    """
    Structured validation response for Prolog syntax checking.

    Attributes:
        is_valid: Whether the input is syntactically correct
        error_message: Human-readable error description if invalid
        hint: Helpful suggestion for fixing the error
        parsed_components: Dictionary of parsed syntax components
    """

    is_valid: bool
    error_message: Optional[str] = None
    hint: Optional[str] = None
    parsed_components: Optional[Dict[str, str]] = None


class PrologValidator:
    """
    Static utility class for validating Prolog facts and queries.

    Provides comprehensive syntax validation with detailed error messages
    and hints for common mistakes made by beginners.
    """

    # Regex patterns for Prolog syntax components
    ATOM_PATTERN = r"[a-z][a-zA-Z0-9_]*"
    VARIABLE_PATTERN = r"[A-Z][a-zA-Z0-9_]*"
    NUMBER_PATTERN = r"\d+"
    ARGUMENT_PATTERN = rf"({ATOM_PATTERN}|{VARIABLE_PATTERN}|{NUMBER_PATTERN})"

    # Fact pattern: predicate(arg1, arg2, ...).
    FACT_PATTERN = (
        rf"^({ATOM_PATTERN})\(({ARGUMENT_PATTERN}(?:\s*,\s*{ARGUMENT_PATTERN})*)\)\.$"
    )

    # Query pattern: ?- predicate(arg1, arg2, ...).
    QUERY_PATTERN = rf"^\?\-\s+({ATOM_PATTERN})\(({ARGUMENT_PATTERN}(?:\s*,\s*{ARGUMENT_PATTERN})*)\)\.$"

    @staticmethod
    def validate_fact(user_input: str) -> ValidationResult:
        """
        Validate a Prolog fact for correct syntax.

        Args:
            user_input: The user's input string to validate

        Returns:
            ValidationResult with validation status and feedback
        """
        if not user_input or not user_input.strip():
            return ValidationResult(
                is_valid=False,
                error_message="Empty input - please enter a Prolog fact.",
                hint="A fact should look like: predicate(argument1, argument2).",
            )

        user_input = user_input.strip()

        # Check if it looks like a query instead of a fact
        if user_input.startswith("?-"):
            return ValidationResult(
                is_valid=False,
                error_message="This looks like a query, not a fact.",
                hint="Facts don't start with '?-'. Try: predicate(argument1, argument2).",
            )

        # Check for missing period
        if not user_input.endswith("."):
            return ValidationResult(
                is_valid=False,
                error_message="Missing period at the end.",
                hint="All Prolog facts must end with a period (.).",
            )

        # Check basic structure with parentheses
        if "(" not in user_input or ")" not in user_input:
            return ValidationResult(
                is_valid=False,
                error_message="Missing parentheses around arguments.",
                hint="Facts need parentheses: predicate(argument1, argument2).",
            )

        # Validate against the complete pattern
        match = re.match(PrologValidator.FACT_PATTERN, user_input)
        if not match:
            return PrologValidator._analyze_fact_error(user_input)

        # Extract components
        predicate = match.group(1)
        arguments_str = match.group(2)
        arguments = [arg.strip() for arg in arguments_str.split(",")]

        return ValidationResult(
            is_valid=True,
            parsed_components={
                "predicate": predicate,
                "arguments": arguments,
                "full_fact": user_input,
            },
        )

    @staticmethod
    def validate_query(user_input: str) -> ValidationResult:
        """
        Validate a Prolog query for correct syntax.

        Args:
            user_input: The user's input string to validate

        Returns:
            ValidationResult with validation status and feedback
        """
        if not user_input or not user_input.strip():
            return ValidationResult(
                is_valid=False,
                error_message="Empty input - please enter a Prolog query.",
                hint="A query should look like: ?- predicate(argument1, argument2).",
            )

        user_input = user_input.strip()

        # Check for missing query prefix
        if not user_input.startswith("?-"):
            return ValidationResult(
                is_valid=False,
                error_message="Missing query prefix '?-'.",
                hint="All Prolog queries must start with '?-'. Try: ?- predicate(arguments).",
            )

        # Check for missing period
        if not user_input.endswith("."):
            return ValidationResult(
                is_valid=False,
                error_message="Missing period at the end.",
                hint="All Prolog queries must end with a period (.).",
            )

        # Check basic structure with parentheses
        if "(" not in user_input or ")" not in user_input:
            return ValidationResult(
                is_valid=False,
                error_message="Missing parentheses around arguments.",
                hint="Queries need parentheses: ?- predicate(argument1, argument2).",
            )

        # Validate against the complete pattern
        match = re.match(PrologValidator.QUERY_PATTERN, user_input)
        if not match:
            return PrologValidator._analyze_query_error(user_input)

        # Extract components
        predicate = match.group(1)
        arguments_str = match.group(2)
        arguments = [arg.strip() for arg in arguments_str.split(",")]

        return ValidationResult(
            is_valid=True,
            parsed_components={
                "predicate": predicate,
                "arguments": arguments,
                "full_query": user_input,
            },
        )

    @staticmethod
    def _analyze_fact_error(user_input: str) -> ValidationResult:
        """
        Analyze a malformed fact and provide specific error feedback.

        Args:
            user_input: The malformed fact string

        Returns:
            ValidationResult with specific error analysis
        """
        # Check for common predicate name errors
        if user_input[0].isupper():
            return ValidationResult(
                is_valid=False,
                error_message="Predicate names must start with a lowercase letter.",
                hint="Try changing the first letter to lowercase. Example: 'likes' not 'Likes'.",
            )

        # Check for spaces in predicate name
        paren_pos = user_input.find("(")
        if paren_pos > 0:
            predicate_part = user_input[:paren_pos]
            if " " in predicate_part:
                return ValidationResult(
                    is_valid=False,
                    error_message="Predicate names cannot contain spaces.",
                    hint="Use underscores instead of spaces: 'likes_food' not 'likes food'.",
                )

        # Check for mismatched parentheses
        open_count = user_input.count("(")
        close_count = user_input.count(")")
        if open_count != close_count:
            return ValidationResult(
                is_valid=False,
                error_message="Mismatched parentheses.",
                hint="Make sure you have exactly one '(' and one ')' around the arguments.",
            )

        # Check for invalid characters in arguments
        if re.search(r"[^a-zA-Z0-9_(),.\s]", user_input):
            return ValidationResult(
                is_valid=False,
                error_message="Invalid characters in fact.",
                hint="Use only letters, numbers, underscores, commas, parentheses, and periods.",
            )

        # Generic syntax error
        return ValidationResult(
            is_valid=False,
            error_message="Invalid fact syntax.",
            hint="Facts should follow the pattern: predicate(argument1, argument2).",
        )

    @staticmethod
    def _analyze_query_error(user_input: str) -> ValidationResult:
        """
        Analyze a malformed query and provide specific error feedback.

        Args:
            user_input: The malformed query string

        Returns:
            ValidationResult with specific error analysis
        """
        # Check for space after ?-
        if user_input.startswith("?-") and len(user_input) > 2 and user_input[2] != " ":
            return ValidationResult(
                is_valid=False,
                error_message="Missing space after '?-'.",
                hint="Put a space after the query prefix: '?- predicate(arguments)'.",
            )

        # Remove the ?- prefix for further analysis
        query_body = (
            user_input[2:].strip() if user_input.startswith("?-") else user_input
        )

        # Check for common predicate name errors
        if query_body and query_body[0].isupper():
            return ValidationResult(
                is_valid=False,
                error_message="Predicate names must start with a lowercase letter.",
                hint="Try changing the first letter to lowercase. Example: '?- likes(...)' not '?- Likes(...)'.",
            )

        # Check for mismatched parentheses
        open_count = user_input.count("(")
        close_count = user_input.count(")")
        if open_count != close_count:
            return ValidationResult(
                is_valid=False,
                error_message="Mismatched parentheses.",
                hint="Make sure you have exactly one '(' and one ')' around the arguments.",
            )

        # Check for invalid characters
        if re.search(r"[^a-zA-Z0-9_(),.?\-\s]", user_input):
            return ValidationResult(
                is_valid=False,
                error_message="Invalid characters in query.",
                hint="Use only letters, numbers, underscores, commas, parentheses, '?-', and periods.",
            )

        # Generic syntax error
        return ValidationResult(
            is_valid=False,
            error_message="Invalid query syntax.",
            hint="Queries should follow the pattern: ?- predicate(argument1, argument2).",
        )

    @staticmethod
    def extract_components(prolog_statement: str) -> Dict[str, str]:
        """
        Extract predicate and arguments from a valid Prolog statement.

        Args:
            prolog_statement: A valid fact or query string

        Returns:
            Dictionary containing parsed components
        """
        # Try fact pattern first
        fact_match = re.match(PrologValidator.FACT_PATTERN, prolog_statement.strip())
        if fact_match:
            predicate = fact_match.group(1)
            arguments_str = fact_match.group(2)
            arguments = [arg.strip() for arg in arguments_str.split(",")]
            return {
                "type": "fact",
                "predicate": predicate,
                "arguments": arguments,
                "argument_count": len(arguments),
            }

        # Try query pattern
        query_match = re.match(PrologValidator.QUERY_PATTERN, prolog_statement.strip())
        if query_match:
            predicate = query_match.group(1)
            arguments_str = query_match.group(2)
            arguments = [arg.strip() for arg in arguments_str.split(",")]
            return {
                "type": "query",
                "predicate": predicate,
                "arguments": arguments,
                "argument_count": len(arguments),
            }

        return {"type": "invalid", "error": "Could not parse statement"}


# Common error messages for tutorial use
COMMON_ERRORS = {
    "missing_period": "Don't forget the period (.) at the end!",
    "uppercase_predicate": "Predicate names start with lowercase letters.",
    "missing_parentheses": "Arguments go inside parentheses: predicate(arg1, arg2).",
    "missing_query_prefix": "Queries start with '?-': ?- predicate(arguments).",
    "spaces_in_predicate": "Use underscores instead of spaces in predicate names.",
    "empty_input": "Please enter something! Don't be shy.",
    "mismatched_parens": "Check your parentheses - you need exactly one '(' and one ')'.",
}


def get_encouraging_message() -> str:
    """
    Get a random encouraging message for when users make mistakes.

    Returns:
        A supportive message to keep users motivated
    """
    messages = [
        "No worries! Even experienced programmers make syntax errors.",
        "You're learning! Each mistake brings you closer to mastery.",
        "That's okay! Prolog syntax takes some getting used to.",
        "Don't give up! You're doing great so far.",
        "Almost there! Just a small syntax adjustment needed.",
        "Good attempt! Let's fix this together.",
        "Learning is a process - you're on the right track!",
    ]
    return random.choice(messages)
