"""
Tests for the comprehensive error handling system in Hello World Prolog tutorial.

Tests the progressive hint system, specific error messages, encouraging tone,
recovery mechanisms, and integration with the tutorial flow.
"""

import pytest
from prologresurrected.game.error_handling import (
    ProgressiveHintSystem, RecoveryMechanisms, ErrorContext, 
    ErrorCategory, HintLevel, create_comprehensive_error_handler
)
from prologresurrected.game.validation import ValidationResult, PrologValidator


class TestProgressiveHintSystem:
    """Test the progressive hint system with escalating help levels."""
    
    def test_hint_level_progression(self):
        """Test that hint levels escalate appropriately with attempt count."""
        assert ProgressiveHintSystem.determine_hint_level(1) == HintLevel.GENTLE
        assert ProgressiveHintSystem.determine_hint_level(2) == HintLevel.SPECIFIC
        assert ProgressiveHintSystem.determine_hint_level(3) == HintLevel.DETAILED
        assert ProgressiveHintSystem.determine_hint_level(4) == HintLevel.EXPLICIT
        assert ProgressiveHintSystem.determine_hint_level(5) == HintLevel.SHOW_ANSWER
        assert ProgressiveHintSystem.determine_hint_level(10) == HintLevel.SHOW_ANSWER
    
    def test_encouraging_messages(self):
        """Test that encouraging messages are provided for different situations."""
        first_msg = ProgressiveHintSystem.get_encouraging_message("first_attempt")
        assert isinstance(first_msg, str)
        assert len(first_msg) > 0
        
        multiple_msg = ProgressiveHintSystem.get_encouraging_message("multiple_attempts")
        assert isinstance(multiple_msg, str)
        assert len(multiple_msg) > 0
        
        stuck_msg = ProgressiveHintSystem.get_encouraging_message("stuck_user")
        assert isinstance(stuck_msg, str)
        assert len(stuck_msg) > 0
    
    def test_error_categorization_missing_period(self):
        """Test categorization of missing period errors."""
        context = ErrorContext(
            user_input="likes(bob, pizza)",
            expected_answer="likes(bob, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.GENERIC_SYNTAX,
            exercise_type="fact"
        )
        
        category = ProgressiveHintSystem.categorize_error(context)
        assert category == ErrorCategory.MISSING_PERIOD
    
    def test_error_categorization_uppercase_predicate(self):
        """Test categorization of uppercase predicate errors."""
        context = ErrorContext(
            user_input="Likes(bob, pizza).",
            expected_answer="likes(bob, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.GENERIC_SYNTAX,
            exercise_type="fact"
        )
        
        category = ProgressiveHintSystem.categorize_error(context)
        assert category == ErrorCategory.UPPERCASE_PREDICATE
    
    def test_error_categorization_missing_parentheses(self):
        """Test categorization of missing parentheses errors."""
        context = ErrorContext(
            user_input="likes bob, pizza.",
            expected_answer="likes(bob, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.GENERIC_SYNTAX,
            exercise_type="fact"
        )
        
        category = ProgressiveHintSystem.categorize_error(context)
        assert category == ErrorCategory.MISSING_PARENTHESES
    
    def test_error_categorization_missing_query_prefix(self):
        """Test categorization of missing query prefix errors."""
        context = ErrorContext(
            user_input="likes(bob, pizza).",
            expected_answer="?- likes(bob, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.GENERIC_SYNTAX,
            exercise_type="query"
        )
        
        category = ProgressiveHintSystem.categorize_error(context)
        assert category == ErrorCategory.MISSING_QUERY_PREFIX
    
    def test_error_categorization_lowercase_variable(self):
        """Test categorization of lowercase variable errors."""
        context = ErrorContext(
            user_input="?- likes(x, pizza).",
            expected_answer="?- likes(X, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.GENERIC_SYNTAX,
            exercise_type="variable_query"
        )
        
        category = ProgressiveHintSystem.categorize_error(context)
        assert category == ErrorCategory.LOWERCASE_VARIABLE
    
    def test_error_categorization_empty_input(self):
        """Test categorization of empty input errors."""
        context = ErrorContext(
            user_input="",
            expected_answer="likes(bob, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.GENERIC_SYNTAX,
            exercise_type="fact"
        )
        
        category = ProgressiveHintSystem.categorize_error(context)
        assert category == ErrorCategory.EMPTY_INPUT
    
    def test_generate_error_response_gentle_level(self):
        """Test error response generation for gentle hint level."""
        validation_result = ValidationResult(
            is_valid=False,
            error_message="Missing period at the end.",
            hint="All Prolog facts must end with a period (.)."
        )
        
        context = ErrorContext(
            user_input="likes(bob, pizza)",
            expected_answer="likes(bob, pizza).",
            attempt_count=1,
            error_category=ErrorCategory.MISSING_PERIOD,
            validation_result=validation_result,
            exercise_type="fact"
        )
        
        response = ProgressiveHintSystem.generate_error_response(context)
        
        assert response.hint_level == HintLevel.GENTLE
        assert len(response.message_lines) > 0
        assert any("Missing period" in line for line in response.message_lines)
        assert response.color == "yellow"
        assert not response.show_answer
    
    def test_generate_error_response_show_answer_level(self):
        """Test error response generation for show answer level."""
        validation_result = ValidationResult(
            is_valid=False,
            error_message="Missing period at the end.",
            hint="All Prolog facts must end with a period (.)."
        )
        
        context = ErrorContext(
            user_input="likes(bob, pizza)",
            expected_answer="likes(bob, pizza).",
            attempt_count=5,
            error_category=ErrorCategory.MISSING_PERIOD,
            validation_result=validation_result,
            exercise_type="fact"
        )
        
        response = ProgressiveHintSystem.generate_error_response(context)
        
        assert response.hint_level == HintLevel.SHOW_ANSWER
        assert len(response.message_lines) > 0
        assert any("likes(bob, pizza)." in line for line in response.message_lines)
        assert response.color == "green"
        assert response.show_answer
    
    def test_pattern_examples(self):
        """Test that appropriate pattern examples are provided."""
        fact_pattern = ProgressiveHintSystem._get_pattern_example("fact")
        assert "predicate(argument1, argument2)." in fact_pattern
        
        query_pattern = ProgressiveHintSystem._get_pattern_example("query")
        assert "?- predicate(argument1, argument2)." in query_pattern
        
        variable_pattern = ProgressiveHintSystem._get_pattern_example("variable_query")
        assert "?- predicate(Variable, argument)." in variable_pattern
    
    def test_detailed_checklist(self):
        """Test that detailed checklists are provided for each exercise type."""
        fact_checklist = ProgressiveHintSystem._get_detailed_checklist("fact")
        assert len(fact_checklist) > 0
        assert any("lowercase predicate" in item for item in fact_checklist)
        assert any("period" in item for item in fact_checklist)
        
        query_checklist = ProgressiveHintSystem._get_detailed_checklist("query")
        assert len(query_checklist) > 0
        assert any("?-" in item for item in query_checklist)
        
        variable_checklist = ProgressiveHintSystem._get_detailed_checklist("variable_query")
        assert len(variable_checklist) > 0
        assert any("UPPERCASE" in item for item in variable_checklist)


class TestRecoveryMechanisms:
    """Test recovery mechanisms for stuck users."""
    
    def test_help_options_basic(self):
        """Test basic help options for early attempts."""
        options = RecoveryMechanisms.offer_help_options(2, "fact")
        
        assert "continue" in options
        assert "hint" in options
        assert "example" in options
        assert "answer" in options
        assert "skip" not in options  # Should not appear for early attempts
    
    def test_help_options_many_attempts(self):
        """Test help options for many attempts."""
        options = RecoveryMechanisms.offer_help_options(4, "fact")
        
        assert "continue" in options
        assert "hint" in options
        assert "example" in options
        assert "answer" in options
        assert "skip" in options  # Should appear after 3+ attempts
    
    def test_help_options_excessive_attempts(self):
        """Test help options for excessive attempts."""
        options = RecoveryMechanisms.offer_help_options(6, "fact")
        
        assert "continue" in options
        assert "hint" in options
        assert "example" in options
        assert "answer" in options
        assert "skip" in options
        assert "review" in options  # Should appear after 5+ attempts
    
    def test_help_menu_generation(self):
        """Test help menu generation."""
        menu = RecoveryMechanisms.generate_help_menu(3, "fact")
        
        assert len(menu) > 0
        assert any("several attempts" in line for line in menu)
        assert any("1." in line for line in menu)  # Should have numbered options
    
    def test_alternative_explanations(self):
        """Test alternative explanations for different exercise types."""
        fact_explanation = RecoveryMechanisms.provide_alternative_explanation("fact", "syntax")
        assert len(fact_explanation) > 0
        assert any("database" in line.lower() or "relationship" in line.lower() for line in fact_explanation)
        
        query_explanation = RecoveryMechanisms.provide_alternative_explanation("query", "syntax")
        assert len(query_explanation) > 0
        assert any("question" in line.lower() for line in query_explanation)
        
        variable_explanation = RecoveryMechanisms.provide_alternative_explanation("variable_query", "syntax")
        assert len(variable_explanation) > 0
        assert any("blank" in line.lower() or "uppercase" in line.lower() for line in variable_explanation)


class TestErrorHandlerIntegration:
    """Test integration of the comprehensive error handling system."""
    
    def test_create_comprehensive_error_handler(self):
        """Test creation of comprehensive error handler."""
        handler = create_comprehensive_error_handler()
        
        assert "hint_system" in handler
        assert "recovery" in handler
        assert "max_attempts" in handler
        assert "show_answer_threshold" in handler
        assert "offer_help_threshold" in handler
        
        assert isinstance(handler["hint_system"], ProgressiveHintSystem)
        assert isinstance(handler["recovery"], RecoveryMechanisms)
        assert handler["max_attempts"] >= 5
        assert handler["show_answer_threshold"] >= 3
        assert handler["offer_help_threshold"] >= 2
    
    def test_error_context_creation(self):
        """Test creation of error context objects."""
        context = ErrorContext(
            user_input="likes(bob, pizza)",
            expected_answer="likes(bob, pizza).",
            attempt_count=2,
            error_category=ErrorCategory.MISSING_PERIOD,
            exercise_type="fact"
        )
        
        assert context.user_input == "likes(bob, pizza)"
        assert context.expected_answer == "likes(bob, pizza)."
        assert context.attempt_count == 2
        assert context.error_category == ErrorCategory.MISSING_PERIOD
        assert context.exercise_type == "fact"
    
    def test_validation_integration(self):
        """Test integration with PrologValidator."""
        # Test fact validation
        fact_result = PrologValidator.validate_fact("likes(bob, pizza)")
        assert not fact_result.is_valid
        assert "period" in fact_result.error_message.lower()
        
        # Test query validation
        query_result = PrologValidator.validate_query("likes(bob, pizza).")
        assert not query_result.is_valid
        assert "?-" in query_result.error_message or "query prefix" in query_result.error_message.lower()
        
        # Test valid inputs
        valid_fact = PrologValidator.validate_fact("likes(bob, pizza).")
        assert valid_fact.is_valid
        
        valid_query = PrologValidator.validate_query("?- likes(bob, pizza).")
        assert valid_query.is_valid


class TestSpecificErrorMessages:
    """Test specific error messages for common Prolog syntax mistakes."""
    
    def test_missing_period_messages(self):
        """Test specific messages for missing period errors."""
        patterns = ProgressiveHintSystem.ERROR_PATTERNS[ErrorCategory.MISSING_PERIOD]
        
        assert HintLevel.GENTLE in patterns["messages"]
        assert HintLevel.SPECIFIC in patterns["messages"]
        assert HintLevel.DETAILED in patterns["messages"]
        assert HintLevel.EXPLICIT in patterns["messages"]
        
        gentle_msg = patterns["messages"][HintLevel.GENTLE]
        assert "period" in gentle_msg.lower()
        assert "." in gentle_msg
    
    def test_uppercase_predicate_messages(self):
        """Test specific messages for uppercase predicate errors."""
        patterns = ProgressiveHintSystem.ERROR_PATTERNS[ErrorCategory.UPPERCASE_PREDICATE]
        
        gentle_msg = patterns["messages"][HintLevel.GENTLE]
        assert "lowercase" in gentle_msg.lower()
        
        detailed_msg = patterns["messages"][HintLevel.DETAILED]
        assert "first letter" in detailed_msg.lower()
    
    def test_missing_parentheses_messages(self):
        """Test specific messages for missing parentheses errors."""
        patterns = ProgressiveHintSystem.ERROR_PATTERNS[ErrorCategory.MISSING_PARENTHESES]
        
        gentle_msg = patterns["messages"][HintLevel.GENTLE]
        assert "parenthes" in gentle_msg.lower()
        assert "(" in gentle_msg and ")" in gentle_msg
    
    def test_missing_query_prefix_messages(self):
        """Test specific messages for missing query prefix errors."""
        patterns = ProgressiveHintSystem.ERROR_PATTERNS[ErrorCategory.MISSING_QUERY_PREFIX]
        
        gentle_msg = patterns["messages"][HintLevel.GENTLE]
        assert "?-" in gentle_msg
        
        specific_msg = patterns["messages"][HintLevel.SPECIFIC]
        assert "?-" in specific_msg  # The message contains ?- even if not the word "query"
    
    def test_lowercase_variable_messages(self):
        """Test specific messages for lowercase variable errors."""
        patterns = ProgressiveHintSystem.ERROR_PATTERNS[ErrorCategory.LOWERCASE_VARIABLE]
        
        gentle_msg = patterns["messages"][HintLevel.GENTLE]
        assert "UPPERCASE" in gentle_msg
        
        detailed_msg = patterns["messages"][HintLevel.DETAILED]
        assert "capital" in detailed_msg.lower() or "uppercase" in detailed_msg.lower()


class TestEncouragingTone:
    """Test that all error messages maintain an encouraging tone."""
    
    def test_encouraging_message_tone(self):
        """Test that encouraging messages are positive and supportive."""
        situations = ["first_attempt", "multiple_attempts", "stuck_user", "success_after_struggle"]
        
        for situation in situations:
            msg = ProgressiveHintSystem.get_encouraging_message(situation)
            
            # Check for positive words
            positive_indicators = [
                "great", "good", "well", "excellent", "perfect", "amazing",
                "learning", "progress", "better", "success", "persistence",
                "don't worry", "no worries", "that's okay", "almost there",
                "teaches", "learn", "new", "attempt", "dedication", "admirable",
                "resilience", "built", "matters", "didn't give up"
            ]
            
            assert any(indicator in msg.lower() for indicator in positive_indicators), \
                f"Message '{msg}' doesn't seem encouraging enough"
            
            # Check that there are no discouraging words
            discouraging_words = ["bad", "wrong", "terrible", "awful", "stupid", "dumb"]
            assert not any(word in msg.lower() for word in discouraging_words), \
                f"Message '{msg}' contains discouraging language"
    
    def test_error_response_tone(self):
        """Test that error responses maintain encouraging tone."""
        validation_result = ValidationResult(
            is_valid=False,
            error_message="Missing period at the end.",
            hint="All Prolog facts must end with a period (.)."
        )
        
        context = ErrorContext(
            user_input="likes(bob, pizza)",
            expected_answer="likes(bob, pizza).",
            attempt_count=2,
            error_category=ErrorCategory.MISSING_PERIOD,
            validation_result=validation_result,
            exercise_type="fact"
        )
        
        response = ProgressiveHintSystem.generate_error_response(context)
        
        # Check that the response starts with encouragement
        first_line = response.message_lines[0] if response.message_lines else ""
        positive_indicators = [
            "no worries", "that's okay", "good attempt", "you're learning",
            "almost there", "don't give up", "great", "well", "teaches",
            "learn", "new", "attempt", "dedication", "admirable"
        ]
        
        assert any(indicator in first_line.lower() for indicator in positive_indicators), \
            f"First line '{first_line}' is not encouraging enough"


if __name__ == "__main__":
    pytest.main([__file__])