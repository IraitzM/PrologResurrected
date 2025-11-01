#!/usr/bin/env python3
"""
Comprehensive test suite for Prolog validation utilities.
"""

from game.validation import PrologValidator, ValidationResult, get_encouraging_message


def test_basic_validation():
    """Test basic validation functionality."""
    # Test valid fact
    result = PrologValidator.validate_fact("likes(alice, chocolate).")
    assert result.is_valid, "Valid fact should pass validation"

    # Test invalid fact (missing period)
    result = PrologValidator.validate_fact("likes(alice, chocolate)")
    assert not result.is_valid, "Invalid fact should fail validation"
    assert "period" in result.error_message.lower(), "Should mention missing period"

    # Test valid query
    result = PrologValidator.validate_query("?- likes(alice, X).")
    assert result.is_valid, "Valid query should pass validation"

    # Test invalid query (missing prefix)
    result = PrologValidator.validate_query("likes(alice, X).")
    assert not result.is_valid, "Invalid query should fail validation"

    print("✓ All basic validation tests passed")


def test_fact_validation_comprehensive():
    """Test comprehensive fact validation scenarios."""
    # Valid facts
    valid_facts = [
        "likes(alice, chocolate).",
        "parent(tom, bob).",
        "employee(john, cyberdyne).",
        "age(sarah, 25).",
        "works_at(employee123, company_xyz).",
    ]

    for fact in valid_facts:
        result = PrologValidator.validate_fact(fact)
        assert result.is_valid, f"Valid fact '{fact}' should pass validation"
        assert result.parsed_components is not None
        assert "predicate" in result.parsed_components
        assert "arguments" in result.parsed_components

    # Invalid facts with specific error checking
    invalid_cases = [
        ("likes(alice, chocolate)", "period"),  # Missing period
        ("Likes(alice, chocolate).", "lowercase"),  # Uppercase predicate
        ("likes alice chocolate.", "parentheses"),  # Missing parentheses
        ("?- likes(alice, chocolate).", "query"),  # Query syntax
        ("", "empty"),  # Empty input
        ("likes(alice chocolate).", "syntax"),  # Missing comma
    ]

    for fact, expected_error_type in invalid_cases:
        result = PrologValidator.validate_fact(fact)
        assert not result.is_valid, f"Invalid fact '{fact}' should fail validation"
        assert result.error_message is not None
        assert result.hint is not None


def test_query_validation_comprehensive():
    """Test comprehensive query validation scenarios."""
    # Valid queries
    valid_queries = [
        "?- likes(alice, chocolate).",
        "?- parent(tom, X).",
        "?- employee(john, Company).",
        "?- age(Person, 25).",
        "?- works_at(Employee, cyberdyne).",
    ]

    for query in valid_queries:
        result = PrologValidator.validate_query(query)
        assert result.is_valid, f"Valid query '{query}' should pass validation"
        assert result.parsed_components is not None
        assert "predicate" in result.parsed_components
        assert "arguments" in result.parsed_components

    # Invalid queries with specific error checking
    invalid_cases = [
        ("likes(alice, chocolate).", "prefix"),  # Missing query prefix
        ("?-likes(alice, chocolate).", "space"),  # Missing space after ?-
        ("?- likes(alice, chocolate)", "period"),  # Missing period
        ("?- Likes(alice, chocolate).", "lowercase"),  # Uppercase predicate
        ("", "empty"),  # Empty input
        ("?- likes alice chocolate.", "parentheses"),  # Missing parentheses
    ]

    for query, expected_error_type in invalid_cases:
        result = PrologValidator.validate_query(query)
        assert not result.is_valid, f"Invalid query '{query}' should fail validation"
        assert result.error_message is not None
        assert result.hint is not None


def test_component_extraction():
    """Test component extraction functionality."""
    # Test fact extraction
    fact_result = PrologValidator.extract_components("likes(alice, chocolate).")
    assert fact_result["type"] == "fact"
    assert fact_result["predicate"] == "likes"
    assert fact_result["arguments"] == ["alice", "chocolate"]
    assert fact_result["argument_count"] == 2

    # Test query extraction
    query_result = PrologValidator.extract_components("?- parent(tom, X).")
    assert query_result["type"] == "query"
    assert query_result["predicate"] == "parent"
    assert query_result["arguments"] == ["tom", "X"]
    assert query_result["argument_count"] == 2

    # Test invalid statement
    invalid_result = PrologValidator.extract_components("invalid syntax")
    assert invalid_result["type"] == "invalid"
    assert "error" in invalid_result


def test_encouraging_messages():
    """Test that encouraging messages are generated."""
    message = get_encouraging_message()
    assert isinstance(message, str)
    assert len(message) > 0

    # Test that we get different messages (run multiple times)
    messages = [get_encouraging_message() for _ in range(10)]
    assert len(set(messages)) > 1, "Should generate different encouraging messages"


def test_validation_result_structure():
    """Test ValidationResult dataclass structure."""
    # Test valid result
    valid_result = ValidationResult(
        is_valid=True,
        parsed_components={"predicate": "likes", "arguments": ["alice", "chocolate"]},
    )
    assert valid_result.is_valid
    assert valid_result.error_message is None
    assert valid_result.hint is None
    assert valid_result.parsed_components is not None

    # Test invalid result
    invalid_result = ValidationResult(
        is_valid=False, error_message="Test error", hint="Test hint"
    )
    assert not invalid_result.is_valid
    assert invalid_result.error_message == "Test error"
    assert invalid_result.hint == "Test hint"
    assert invalid_result.parsed_components is None


if __name__ == "__main__":
    test_basic_validation()
    test_fact_validation_comprehensive()
    test_query_validation_comprehensive()
    test_component_extraction()
    test_encouraging_messages()
    test_validation_result_structure()
    print("✓ All comprehensive validation tests passed")
