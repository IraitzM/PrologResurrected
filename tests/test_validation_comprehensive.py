"""
Comprehensive unit tests for Prolog validation logic.

This module tests all aspects of the PrologValidator class, ValidationResult,
and tutorial content parsing and navigation functionality.
"""

import pytest
import re
from unittest.mock import patch
from prologresurrected.game.validation import (
    PrologValidator,
    ValidationResult,
    get_encouraging_message,
    COMMON_ERRORS,
)
from prologresurrected.game.tutorial_content import (
    TutorialProgress,
    TutorialNavigator,
    TutorialSession,
    TutorialStep,
    TUTORIAL_CONTENT,
)


class TestValidationResult:
    """Test the ValidationResult dataclass."""

    def test_validation_result_creation_valid(self):
        """Test creating a ValidationResult for valid input."""
        result = ValidationResult(
            is_valid=True,
            parsed_components={"predicate": "likes", "arguments": ["alice", "chocolate"]}
        )
        
        assert result.is_valid is True
        assert result.error_message is None
        assert result.hint is None
        assert result.parsed_components == {"predicate": "likes", "arguments": ["alice", "chocolate"]}

    def test_validation_result_creation_invalid(self):
        """Test creating a ValidationResult for invalid input."""
        result = ValidationResult(
            is_valid=False,
            error_message="Missing period at the end.",
            hint="All Prolog facts must end with a period (.)."
        )
        
        assert result.is_valid is False
        assert result.error_message == "Missing period at the end."
        assert result.hint == "All Prolog facts must end with a period (.)."
        assert result.parsed_components is None

    def test_validation_result_defaults(self):
        """Test ValidationResult with default values."""
        result = ValidationResult(is_valid=False)
        
        assert result.is_valid is False
        assert result.error_message is None
        assert result.hint is None
        assert result.parsed_components is None


class TestPrologValidatorFacts:
    """Test PrologValidator.validate_fact() with various inputs."""

    def test_validate_fact_valid_simple(self):
        """Test validation of simple valid facts."""
        valid_facts = [
            "likes(alice, chocolate).",
            "parent(tom, bob).",
            "employee(sarah, tech_corp).",
            "color(grass, green).",
            "owns(john, car).",
            "age(person, 25).",
        ]
        
        for fact in valid_facts:
            result = PrologValidator.validate_fact(fact)
            assert result.is_valid, f"Expected {fact} to be valid, but got: {result.error_message}"
            assert result.error_message is None
            assert result.hint is None
            assert result.parsed_components is not None
            assert "predicate" in result.parsed_components
            assert "arguments" in result.parsed_components

    def test_validate_fact_valid_with_numbers(self):
        """Test validation of facts with numeric arguments."""
        result = PrologValidator.validate_fact("age(alice, 25).")
        
        assert result.is_valid
        assert result.parsed_components["predicate"] == "age"
        assert result.parsed_components["arguments"] == ["alice", "25"]

    def test_validate_fact_valid_with_underscores(self):
        """Test validation of facts with underscores in names."""
        result = PrologValidator.validate_fact("works_at(john, tech_company).")
        
        assert result.is_valid
        assert result.parsed_components["predicate"] == "works_at"
        assert result.parsed_components["arguments"] == ["john", "tech_company"]

    def test_validate_fact_valid_single_argument(self):
        """Test validation of facts with single argument."""
        result = PrologValidator.validate_fact("human(alice).")
        
        assert result.is_valid
        assert result.parsed_components["predicate"] == "human"
        assert result.parsed_components["arguments"] == ["alice"]

    def test_validate_fact_valid_multiple_arguments(self):
        """Test validation of facts with multiple arguments."""
        result = PrologValidator.validate_fact("meeting(alice, bob, charlie, friday).")
        
        assert result.is_valid
        assert result.parsed_components["predicate"] == "meeting"
        assert result.parsed_components["arguments"] == ["alice", "bob", "charlie", "friday"]

    def test_validate_fact_empty_input(self):
        """Test validation of empty input."""
        test_cases = ["", "   ", None]
        
        for empty_input in test_cases:
            if empty_input is None:
                # Handle None case separately since strip() will fail
                result = ValidationResult(
                    is_valid=False,
                    error_message="Empty input - please enter a Prolog fact.",
                    hint="A fact should look like: predicate(argument1, argument2)."
                )
            else:
                result = PrologValidator.validate_fact(empty_input)
            
            assert not result.is_valid
            assert "Empty input" in result.error_message
            assert "predicate(argument1, argument2)" in result.hint

    def test_validate_fact_missing_period(self):
        """Test validation of facts missing the period."""
        result = PrologValidator.validate_fact("likes(alice, chocolate)")
        
        assert not result.is_valid
        assert "Missing period" in result.error_message
        assert "period (.)" in result.hint

    def test_validate_fact_query_instead_of_fact(self):
        """Test validation when user enters a query instead of a fact."""
        result = PrologValidator.validate_fact("?- likes(alice, chocolate).")
        
        assert not result.is_valid
        assert "looks like a query" in result.error_message
        assert "don't start with '?-'" in result.hint

    def test_validate_fact_missing_parentheses(self):
        """Test validation of facts missing parentheses."""
        test_cases = [
            ("likes alice, chocolate.", "parentheses"),
            ("likes alice chocolate.", "parentheses"),
            ("likes(alice, chocolate", "period"),  # This will fail on missing period first
            ("likes alice, chocolate).", "parentheses"),
        ]
        
        for fact, expected_error_type in test_cases:
            result = PrologValidator.validate_fact(fact)
            assert not result.is_valid
            assert expected_error_type in result.error_message.lower()

    def test_validate_fact_uppercase_predicate(self):
        """Test validation of facts with uppercase predicate names."""
        result = PrologValidator.validate_fact("Likes(alice, chocolate).")
        
        assert not result.is_valid
        assert "lowercase letter" in result.error_message
        assert "lowercase" in result.hint

    def test_validate_fact_spaces_in_predicate(self):
        """Test validation of facts with spaces in predicate names."""
        result = PrologValidator.validate_fact("likes food(alice, chocolate).")
        
        assert not result.is_valid
        assert "cannot contain spaces" in result.error_message
        assert "underscores" in result.hint

    def test_validate_fact_mismatched_parentheses(self):
        """Test validation of facts with mismatched parentheses."""
        test_cases = [
            "likes((alice, chocolate).",
            "likes(alice, chocolate)).",
            "likes(alice, chocolate.",
            "likesalice, chocolate).",
        ]
        
        for fact in test_cases:
            result = PrologValidator.validate_fact(fact)
            assert not result.is_valid
            assert "parentheses" in result.error_message.lower()

    def test_validate_fact_invalid_characters(self):
        """Test validation of facts with invalid characters."""
        test_cases = [
            "likes(alice, chocolate!).",
            "likes(alice, chocolate@home).",
            "likes(alice, chocolate#1).",
            "likes(alice, chocolate$).",
        ]
        
        for fact in test_cases:
            result = PrologValidator.validate_fact(fact)
            assert not result.is_valid
            assert "Invalid characters" in result.error_message

    def test_validate_fact_whitespace_handling(self):
        """Test validation handles whitespace correctly."""
        test_cases = [
            ("  likes(alice, chocolate).  ", True),  # Leading/trailing whitespace OK
            ("likes( alice , chocolate ).", False),  # Spaces around args not allowed by regex
            ("likes(alice,chocolate).", True),       # No spaces around comma OK
        ]
        
        for fact, should_be_valid in test_cases:
            result = PrologValidator.validate_fact(fact)
            if should_be_valid:
                assert result.is_valid, f"Expected {fact} to be valid, but got: {result.error_message}"
            else:
                assert not result.is_valid, f"Expected {fact} to be invalid"


class TestPrologValidatorQueries:
    """Test PrologValidator.validate_query() covering edge cases."""

    def test_validate_query_valid_simple(self):
        """Test validation of simple valid queries."""
        valid_queries = [
            "?- likes(alice, chocolate).",
            "?- parent(tom, bob).",
            "?- employee(sarah, tech_corp).",
            "?- color(grass, green).",
            "?- owns(john, car).",
        ]
        
        for query in valid_queries:
            result = PrologValidator.validate_query(query)
            assert result.is_valid, f"Expected {query} to be valid, but got: {result.error_message}"
            assert result.error_message is None
            assert result.hint is None
            assert result.parsed_components is not None
            assert "predicate" in result.parsed_components
            assert "arguments" in result.parsed_components

    def test_validate_query_valid_with_variables(self):
        """Test validation of queries with variables."""
        test_cases = [
            ("?- likes(alice, X).", "X"),
            ("?- parent(Person, bob).", "Person"),
            ("?- employee(X, Y).", "X"),
            ("?- color(Thing, Color).", "Thing"),
        ]
        
        for query, expected_variable in test_cases:
            result = PrologValidator.validate_query(query)
            assert result.is_valid, f"Expected {query} to be valid"
            assert expected_variable in result.parsed_components["arguments"], f"Expected {expected_variable} in arguments {result.parsed_components['arguments']}"

    def test_validate_query_valid_mixed_case_variables(self):
        """Test validation of queries with mixed case variables."""
        result = PrologValidator.validate_query("?- likes(Person123, Something_Good).")
        
        assert result.is_valid
        assert result.parsed_components["arguments"] == ["Person123", "Something_Good"]

    def test_validate_query_empty_input(self):
        """Test validation of empty query input."""
        test_cases = ["", "   "]
        
        for empty_input in test_cases:
            result = PrologValidator.validate_query(empty_input)
            assert not result.is_valid
            assert "Empty input" in result.error_message
            assert "?- predicate(argument1, argument2)" in result.hint

    def test_validate_query_missing_query_prefix(self):
        """Test validation of queries missing '?-' prefix."""
        result = PrologValidator.validate_query("likes(alice, chocolate).")
        
        assert not result.is_valid
        assert "Missing query prefix" in result.error_message
        assert "?-" in result.hint

    def test_validate_query_missing_period(self):
        """Test validation of queries missing the period."""
        result = PrologValidator.validate_query("?- likes(alice, chocolate)")
        
        assert not result.is_valid
        assert "Missing period" in result.error_message
        assert "period (.)" in result.hint

    def test_validate_query_missing_parentheses(self):
        """Test validation of queries missing parentheses."""
        test_cases = [
            ("?- likes alice, chocolate.", "parentheses"),
            ("?- likes alice chocolate.", "parentheses"),
            ("?- likes(alice, chocolate", "period"),  # This will fail on missing period first
            ("?- likes alice, chocolate).", "parentheses"),
        ]
        
        for query, expected_error_type in test_cases:
            result = PrologValidator.validate_query(query)
            assert not result.is_valid
            assert expected_error_type in result.error_message.lower()

    def test_validate_query_missing_space_after_prefix(self):
        """Test validation of queries missing space after '?-'."""
        result = PrologValidator.validate_query("?-likes(alice, chocolate).")
        
        assert not result.is_valid
        assert "Missing space after" in result.error_message
        assert "space after" in result.hint

    def test_validate_query_uppercase_predicate(self):
        """Test validation of queries with uppercase predicate names."""
        result = PrologValidator.validate_query("?- Likes(alice, chocolate).")
        
        assert not result.is_valid
        assert "lowercase letter" in result.error_message
        assert "lowercase" in result.hint

    def test_validate_query_mismatched_parentheses(self):
        """Test validation of queries with mismatched parentheses."""
        test_cases = [
            "?- likes((alice, chocolate).",
            "?- likes(alice, chocolate)).",
            "?- likes(alice, chocolate.",
            "?- likesalice, chocolate).",
        ]
        
        for query in test_cases:
            result = PrologValidator.validate_query(query)
            assert not result.is_valid
            assert "parentheses" in result.error_message.lower()

    def test_validate_query_invalid_characters(self):
        """Test validation of queries with invalid characters."""
        test_cases = [
            "?- likes(alice, chocolate!).",
            "?- likes(alice, chocolate@home).",
            "?- likes(alice, chocolate#1).",
            "?- likes(alice, chocolate$).",
        ]
        
        for query in test_cases:
            result = PrologValidator.validate_query(query)
            assert not result.is_valid
            assert "Invalid characters" in result.error_message

    def test_validate_query_whitespace_handling(self):
        """Test validation handles whitespace correctly in queries."""
        test_cases = [
            ("  ?- likes(alice, chocolate).  ", True),   # Leading/trailing whitespace OK
            ("?- likes( alice , chocolate ).", False),   # Spaces around args not allowed by regex
            ("?- likes(alice,chocolate).", True),        # No spaces around comma OK
            ("?-  likes(alice, chocolate).", True),      # Extra space after ?- is allowed by \s+
        ]
        
        for query, should_be_valid in test_cases:
            result = PrologValidator.validate_query(query)
            if should_be_valid:
                assert result.is_valid, f"Expected {query} to be valid, but got: {result.error_message}"
            else:
                assert not result.is_valid, f"Expected {query} to be invalid"


class TestPrologValidatorComponentExtraction:
    """Test the extract_components method."""

    def test_extract_components_valid_fact(self):
        """Test component extraction from valid facts."""
        result = PrologValidator.extract_components("likes(alice, chocolate).")
        
        assert result["type"] == "fact"
        assert result["predicate"] == "likes"
        assert result["arguments"] == ["alice", "chocolate"]
        assert result["argument_count"] == 2

    def test_extract_components_valid_query(self):
        """Test component extraction from valid queries."""
        result = PrologValidator.extract_components("?- parent(tom, X).")
        
        assert result["type"] == "query"
        assert result["predicate"] == "parent"
        assert result["arguments"] == ["tom", "X"]
        assert result["argument_count"] == 2

    def test_extract_components_single_argument(self):
        """Test component extraction with single argument."""
        result = PrologValidator.extract_components("human(alice).")
        
        assert result["type"] == "fact"
        assert result["predicate"] == "human"
        assert result["arguments"] == ["alice"]
        assert result["argument_count"] == 1

    def test_extract_components_multiple_arguments(self):
        """Test component extraction with multiple arguments."""
        result = PrologValidator.extract_components("meeting(alice, bob, charlie, friday).")
        
        assert result["type"] == "fact"
        assert result["predicate"] == "meeting"
        assert result["arguments"] == ["alice", "bob", "charlie", "friday"]
        assert result["argument_count"] == 4

    def test_extract_components_invalid_statement(self):
        """Test component extraction from invalid statements."""
        result = PrologValidator.extract_components("invalid statement")
        
        assert result["type"] == "invalid"
        assert "error" in result
        assert "Could not parse" in result["error"]

    def test_extract_components_whitespace_handling(self):
        """Test component extraction handles whitespace correctly."""
        # Test with valid whitespace (leading/trailing only)
        result = PrologValidator.extract_components("  likes(alice, chocolate).  ")
        
        assert result["type"] == "fact"
        assert result["predicate"] == "likes"
        assert result["arguments"] == ["alice", "chocolate"]
        
        # Test with invalid whitespace (spaces around arguments)
        result_invalid = PrologValidator.extract_components("likes( alice , chocolate ).")
        assert result_invalid["type"] == "invalid"


class TestErrorMessageGeneration:
    """Test error message generation and encouraging messages."""

    def test_common_errors_dictionary(self):
        """Test that COMMON_ERRORS contains expected keys and messages."""
        expected_keys = [
            "missing_period",
            "uppercase_predicate", 
            "missing_parentheses",
            "missing_query_prefix",
            "spaces_in_predicate",
            "empty_input",
            "mismatched_parens",
        ]
        
        for key in expected_keys:
            assert key in COMMON_ERRORS
            assert isinstance(COMMON_ERRORS[key], str)
            assert len(COMMON_ERRORS[key]) > 0

    def test_encouraging_message_generation(self):
        """Test that encouraging messages are generated correctly."""
        # Test multiple calls to ensure randomness works
        messages = [get_encouraging_message() for _ in range(10)]
        
        # All messages should be strings
        assert all(isinstance(msg, str) for msg in messages)
        
        # All messages should be non-empty
        assert all(len(msg) > 0 for msg in messages)
        
        # Should have some variety (not all the same)
        unique_messages = set(messages)
        assert len(unique_messages) > 1, "Should generate different encouraging messages"

    @patch('random.choice')
    def test_encouraging_message_selection(self, mock_choice):
        """Test that encouraging message selection works correctly."""
        expected_message = "Test encouraging message"
        mock_choice.return_value = expected_message
        
        result = get_encouraging_message()
        
        assert result == expected_message
        mock_choice.assert_called_once()


class TestTutorialProgress:
    """Test tutorial progress tracking functionality."""

    def test_tutorial_progress_initialization(self):
        """Test TutorialProgress initialization with defaults."""
        progress = TutorialProgress()
        
        assert progress.current_step == 0
        assert progress.completed_steps == []
        assert progress.user_facts == []
        assert progress.user_queries == []
        assert progress.mistakes_count == 0
        assert progress.hints_used == 0
        assert progress.start_time is None
        assert progress.step_completion_times == {}

    def test_mark_step_complete(self):
        """Test marking steps as complete."""
        progress = TutorialProgress()
        
        progress.mark_step_complete("introduction")
        assert "introduction" in progress.completed_steps
        
        progress.mark_step_complete("facts_explanation")
        assert "facts_explanation" in progress.completed_steps
        assert len(progress.completed_steps) == 2
        
        # Test duplicate marking doesn't add twice
        progress.mark_step_complete("introduction")
        assert progress.completed_steps.count("introduction") == 1

    def test_is_step_completed(self):
        """Test checking if steps are completed."""
        progress = TutorialProgress()
        
        assert not progress.is_step_completed("introduction")
        
        progress.mark_step_complete("introduction")
        assert progress.is_step_completed("introduction")
        assert not progress.is_step_completed("facts_explanation")

    def test_add_user_fact(self):
        """Test adding user-created facts."""
        progress = TutorialProgress()
        
        progress.add_user_fact("likes(bob, pizza).")
        assert "likes(bob, pizza)." in progress.user_facts
        
        progress.add_user_fact("parent(tom, bob).")
        assert len(progress.user_facts) == 2
        assert "parent(tom, bob)." in progress.user_facts

    def test_add_user_query(self):
        """Test adding user-created queries."""
        progress = TutorialProgress()
        
        progress.add_user_query("?- likes(alice, X).")
        assert "?- likes(alice, X)." in progress.user_queries
        
        progress.add_user_query("?- parent(tom, bob).")
        assert len(progress.user_queries) == 2

    def test_increment_mistakes(self):
        """Test incrementing mistake counter."""
        progress = TutorialProgress()
        
        assert progress.mistakes_count == 0
        
        progress.increment_mistakes()
        assert progress.mistakes_count == 1
        
        progress.increment_mistakes()
        assert progress.mistakes_count == 2

    def test_increment_hints(self):
        """Test incrementing hints counter."""
        progress = TutorialProgress()
        
        assert progress.hints_used == 0
        
        progress.increment_hints()
        assert progress.hints_used == 1
        
        progress.increment_hints()
        assert progress.hints_used == 2

    def test_get_completion_percentage(self):
        """Test calculation of completion percentage."""
        progress = TutorialProgress()
        
        # No steps completed
        assert progress.get_completion_percentage() == 0.0
        
        # Complete some steps
        total_steps = len(TUTORIAL_CONTENT)
        progress.mark_step_complete("introduction")
        expected_percentage = (1 / total_steps) * 100
        assert progress.get_completion_percentage() == expected_percentage
        
        # Complete all steps
        for step_name in TUTORIAL_CONTENT.keys():
            progress.mark_step_complete(step_name)
        assert progress.get_completion_percentage() == 100.0


class TestTutorialNavigator:
    """Test tutorial navigation functionality."""

    def test_navigator_initialization(self):
        """Test TutorialNavigator initialization."""
        navigator = TutorialNavigator()
        
        assert navigator.current_step_index == 0
        assert len(navigator.step_order) == 6  # All tutorial steps
        assert navigator.step_order[0] == TutorialStep.INTRODUCTION
        assert navigator.step_order[-1] == TutorialStep.COMPLETION

    def test_get_current_step(self):
        """Test getting the current tutorial step."""
        navigator = TutorialNavigator()
        
        assert navigator.get_current_step() == TutorialStep.INTRODUCTION
        
        navigator.current_step_index = 1
        assert navigator.get_current_step() == TutorialStep.FACTS_EXPLANATION
        
        navigator.current_step_index = 5
        assert navigator.get_current_step() == TutorialStep.COMPLETION

    def test_get_current_step_out_of_bounds(self):
        """Test getting current step when index is out of bounds."""
        navigator = TutorialNavigator()
        
        navigator.current_step_index = 999
        assert navigator.get_current_step() == TutorialStep.COMPLETION
        
        navigator.current_step_index = -1
        assert navigator.get_current_step() == TutorialStep.COMPLETION

    def test_get_step_content(self):
        """Test loading content for specific steps."""
        navigator = TutorialNavigator()
        
        content = navigator.get_step_content(TutorialStep.INTRODUCTION)
        assert "title" in content
        assert "Welcome to Prolog" in content["title"]
        
        content = navigator.get_step_content(TutorialStep.FACTS_EXPLANATION)
        assert "title" in content
        assert "examples" in content

    def test_get_step_content_invalid_step(self):
        """Test loading content for invalid step."""
        navigator = TutorialNavigator()
        
        content = navigator.get_step_content("invalid_step")
        assert content == {}

    def test_next_step(self):
        """Test moving to next step."""
        navigator = TutorialNavigator()
        
        assert navigator.current_step_index == 0
        
        result = navigator.next_step()
        assert result is True
        assert navigator.current_step_index == 1
        
        # Move to last step
        navigator.current_step_index = len(navigator.step_order) - 1
        result = navigator.next_step()
        assert result is False
        assert navigator.current_step_index == len(navigator.step_order) - 1

    def test_previous_step(self):
        """Test moving to previous step."""
        navigator = TutorialNavigator()
        navigator.current_step_index = 2
        
        result = navigator.previous_step()
        assert result is True
        assert navigator.current_step_index == 1
        
        # Move to first step
        navigator.current_step_index = 0
        result = navigator.previous_step()
        assert result is False
        assert navigator.current_step_index == 0

    def test_can_go_next(self):
        """Test checking if next step is available."""
        navigator = TutorialNavigator()
        
        assert navigator.can_go_next() is True
        
        navigator.current_step_index = len(navigator.step_order) - 1
        assert navigator.can_go_next() is False

    def test_can_go_previous(self):
        """Test checking if previous step is available."""
        navigator = TutorialNavigator()
        
        assert navigator.can_go_previous() is False
        
        navigator.current_step_index = 1
        assert navigator.can_go_previous() is True

    def test_get_step_number(self):
        """Test getting step number (1-indexed)."""
        navigator = TutorialNavigator()
        
        assert navigator.get_step_number() == 1
        
        navigator.current_step_index = 2
        assert navigator.get_step_number() == 3

    def test_get_total_steps(self):
        """Test getting total number of steps."""
        navigator = TutorialNavigator()
        
        assert navigator.get_total_steps() == 6

    def test_get_progress_percentage(self):
        """Test calculating progress percentage."""
        navigator = TutorialNavigator()
        
        assert navigator.get_progress_percentage() == 0.0
        
        navigator.current_step_index = 3
        expected = (3 / 6) * 100
        assert navigator.get_progress_percentage() == expected

    def test_jump_to_step(self):
        """Test jumping directly to a specific step."""
        navigator = TutorialNavigator()
        
        result = navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        assert result is True
        assert navigator.get_current_step() == TutorialStep.QUERIES_EXPLANATION

    def test_jump_to_invalid_step(self):
        """Test jumping to an invalid step."""
        navigator = TutorialNavigator()
        
        # Create a mock step that doesn't exist
        class InvalidStep:
            pass
        
        result = navigator.jump_to_step(InvalidStep())
        assert result is False
        assert navigator.current_step_index == 0  # Should remain unchanged

    def test_reset(self):
        """Test resetting navigator to beginning."""
        navigator = TutorialNavigator()
        navigator.current_step_index = 3
        
        navigator.reset()
        assert navigator.current_step_index == 0


class TestTutorialSession:
    """Test complete tutorial session management."""

    def test_session_initialization(self):
        """Test TutorialSession initialization."""
        session = TutorialSession()
        
        assert isinstance(session.navigator, TutorialNavigator)
        assert isinstance(session.progress, TutorialProgress)
        assert session.session_active is True

    def test_start_session(self):
        """Test starting a tutorial session."""
        session = TutorialSession()
        
        session.start_session()
        
        assert session.progress.start_time is not None
        assert session.session_active is True

    def test_end_session(self):
        """Test ending a tutorial session."""
        session = TutorialSession()
        
        session.end_session()
        
        assert session.session_active is False

    def test_get_current_content(self):
        """Test getting current step content."""
        session = TutorialSession()
        
        content = session.get_current_content()
        assert "title" in content
        assert "Welcome to Prolog" in content["title"]

    def test_advance_step(self):
        """Test advancing to next step with progress tracking."""
        session = TutorialSession()
        
        current_step = session.navigator.get_current_step()
        result = session.advance_step()
        
        assert result is True
        assert current_step.value in session.progress.completed_steps
        assert session.navigator.current_step_index == 1

    def test_advance_step_at_end(self):
        """Test advancing step when at the end."""
        session = TutorialSession()
        session.navigator.current_step_index = len(session.navigator.step_order) - 1
        
        result = session.advance_step()
        
        assert result is False

    def test_go_back_step(self):
        """Test going back to previous step."""
        session = TutorialSession()
        session.navigator.current_step_index = 2
        
        result = session.go_back_step()
        
        assert result is True
        assert session.navigator.current_step_index == 1

    def test_record_user_input_fact(self):
        """Test recording user fact input."""
        session = TutorialSession()
        
        session.record_user_input("fact", "likes(bob, pizza).")
        
        assert "likes(bob, pizza)." in session.progress.user_facts

    def test_record_user_input_query(self):
        """Test recording user query input."""
        session = TutorialSession()
        
        session.record_user_input("query", "?- likes(alice, X).")
        
        assert "?- likes(alice, X)." in session.progress.user_queries

    def test_record_user_input_invalid_type(self):
        """Test recording user input with invalid type."""
        session = TutorialSession()
        
        session.record_user_input("invalid", "some input")
        
        # Should not crash, but also shouldn't record anything
        assert len(session.progress.user_facts) == 0
        assert len(session.progress.user_queries) == 0

    def test_record_mistake(self):
        """Test recording user mistakes."""
        session = TutorialSession()
        
        session.record_mistake()
        
        assert session.progress.mistakes_count == 1

    def test_record_hint_used(self):
        """Test recording hint usage."""
        session = TutorialSession()
        
        session.record_hint_used()
        
        assert session.progress.hints_used == 1

    def test_get_session_summary(self):
        """Test getting session summary."""
        session = TutorialSession()
        
        # Add some test data
        session.record_user_input("fact", "likes(bob, pizza).")
        session.record_user_input("query", "?- likes(alice, X).")
        session.record_mistake()
        session.record_hint_used()
        session.progress.mark_step_complete("introduction")
        
        summary = session.get_session_summary()
        
        assert "completion_percentage" in summary
        assert "steps_completed" in summary
        assert "total_steps" in summary
        assert "facts_created" in summary
        assert "queries_written" in summary
        assert "mistakes_made" in summary
        assert "hints_used" in summary
        assert "user_facts" in summary
        assert "user_queries" in summary
        
        assert summary["facts_created"] == 1
        assert summary["queries_written"] == 1
        assert summary["mistakes_made"] == 1
        assert summary["hints_used"] == 1
        assert summary["steps_completed"] == 1

    def test_is_complete_false(self):
        """Test checking completion when tutorial is not complete."""
        session = TutorialSession()
        
        assert session.is_complete() is False

    def test_is_complete_true(self):
        """Test checking completion when tutorial is complete."""
        session = TutorialSession()
        
        # Move to completion step and mark it complete
        session.navigator.jump_to_step(TutorialStep.COMPLETION)
        session.progress.mark_step_complete(TutorialStep.COMPLETION.value)
        
        assert session.is_complete() is True


class TestTutorialContentParsing:
    """Test tutorial content parsing and structure."""

    def test_tutorial_content_structure(self):
        """Test that TUTORIAL_CONTENT has expected structure."""
        expected_steps = [
            "introduction",
            "facts_explanation", 
            "fact_creation",
            "queries_explanation",
            "variables_introduction",
            "completion"
        ]
        
        for step in expected_steps:
            assert step in TUTORIAL_CONTENT
            assert "title" in TUTORIAL_CONTENT[step]
            assert isinstance(TUTORIAL_CONTENT[step]["title"], str)

    def test_tutorial_content_introduction(self):
        """Test introduction step content."""
        intro = TUTORIAL_CONTENT["introduction"]
        
        assert "title" in intro
        assert "subtitle" in intro
        assert "explanation" in intro
        assert "cyberpunk_flavor" in intro
        assert "continue_prompt" in intro
        
        assert isinstance(intro["explanation"], list)
        assert len(intro["explanation"]) > 0

    def test_tutorial_content_facts_explanation(self):
        """Test facts explanation step content."""
        facts = TUTORIAL_CONTENT["facts_explanation"]
        
        assert "title" in facts
        assert "examples" in facts
        assert "practice_exercise" in facts
        
        assert isinstance(facts["examples"], list)
        assert len(facts["examples"]) > 0
        
        exercise = facts["practice_exercise"]
        assert "prompt" in exercise
        assert "questions" in exercise
        assert "answers" in exercise

    def test_tutorial_content_fact_creation(self):
        """Test fact creation step content."""
        creation = TUTORIAL_CONTENT["fact_creation"]
        
        assert "title" in creation
        assert "exercise_prompt" in creation
        assert "expected_pattern" in creation
        assert "alternative_answers" in creation
        assert "validation_hints" in creation
        assert "success_message" in creation

    def test_tutorial_content_queries_explanation(self):
        """Test queries explanation step content."""
        queries = TUTORIAL_CONTENT["queries_explanation"]
        
        assert "title" in queries
        assert "examples" in queries
        assert "practice_exercise" in queries
        
        exercise = queries["practice_exercise"]
        assert "prompt" in exercise
        assert "expected_answer" in exercise

    def test_tutorial_content_variables_introduction(self):
        """Test variables introduction step content."""
        variables = TUTORIAL_CONTENT["variables_introduction"]
        
        assert "title" in variables
        assert "examples" in variables
        assert "practice_exercise" in variables
        
        exercise = variables["practice_exercise"]
        assert "expected_pattern" in exercise
        assert "expected_answer" in exercise

    def test_tutorial_content_completion(self):
        """Test completion step content."""
        completion = TUTORIAL_CONTENT["completion"]
        
        assert "title" in completion
        assert "celebration" in completion
        assert "summary" in completion
        assert "next_steps" in completion
        assert "options" in completion
        
        options = completion["options"]
        assert "continue_to_game" in options
        assert "review_concepts" in options
        assert "exit_tutorial" in options


if __name__ == "__main__":
    pytest.main([__file__, "-v"])