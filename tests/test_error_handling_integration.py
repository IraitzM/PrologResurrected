"""
Integration tests for the comprehensive error handling system.

Tests the complete error handling flow from user input through progressive hints
to recovery mechanisms, ensuring all components work together seamlessly.
"""

import pytest
from game.hello_world_puzzle import HelloWorldPuzzle
from game.validation import ValidationResult, PrologValidator
from game.error_handling import (
    ProgressiveHintSystem, RecoveryMechanisms, ErrorContext, 
    ErrorCategory, HintLevel
)


class MockTerminal:
    """Mock terminal for testing output."""
    
    def __init__(self):
        self.outputs = []
        self.clear_count = 0
    
    def add_output(self, text, color=None):
        self.outputs.append((text, color))
    
    def clear_terminal(self):
        self.clear_count += 1
        self.outputs = []
    
    def get_all_output_text(self):
        return " ".join([output[0] for output in self.outputs])


class TestErrorHandlingIntegration:
    """Test complete error handling integration."""
    
    def test_complete_error_handling_flow(self):
        """Test the complete error handling flow from error to recovery."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Simulate a user making a common error (missing period)
        user_input = "likes(bob, pizza)"
        expected_answer = "likes(bob, pizza)."
        
        # Validate the input (should fail)
        validation_result = PrologValidator.validate_fact(user_input)
        assert not validation_result.is_valid
        assert "period" in validation_result.error_message.lower()
        
        # Test progressive error handling for multiple attempts
        for attempt in range(1, 6):
            terminal.outputs = []  # Clear previous outputs
            puzzle._last_user_input = user_input
            
            # Display error feedback
            puzzle._display_syntax_error_feedback(
                terminal, validation_result, attempt, [], expected_answer, "fact"
            )
            
            output_text = terminal.get_all_output_text()
            
            # Verify encouraging tone is maintained
            encouraging_words = [
                "no worries", "that's okay", "great", "good", "learning",
                "persistence", "don't give up", "admirable", "dedication",
                "teaches", "new", "attempt", "well", "excellent"
            ]
            assert any(word in output_text.lower() for word in encouraging_words), \
                f"Attempt {attempt} output lacks encouraging tone"
            
            # Verify error message is present (unless showing complete answer)
            if attempt < 5:  # Before showing complete answer
                assert "missing period" in output_text.lower() or "period" in output_text.lower()
            else:  # When showing complete answer
                assert "likes(bob, pizza)." in output_text
            
            # Verify progressive hints
            if attempt == 1:
                assert "try again" in output_text.lower()
            elif attempt == 2:
                assert ("pattern" in output_text.lower() or "remember" in output_text.lower())
            elif attempt == 3:
                assert ("step by step" in output_text.lower() or "check" in output_text.lower())
            elif attempt == 4:
                # Should offer recovery options or show detailed guidance
                assert ("recovery" in output_text.lower() or "help" in output_text.lower() or 
                       "guidance" in output_text.lower() or "detailed" in output_text.lower())
            elif attempt >= 5:
                # Should show complete answer
                assert ("complete answer" in output_text.lower() or "correct answer" in output_text.lower())
    
    def test_error_categorization_accuracy(self):
        """Test that errors are categorized correctly for appropriate responses."""
        test_cases = [
            {
                "input": "likes(bob, pizza)",
                "expected": "likes(bob, pizza).",
                "exercise": "fact",
                "expected_category": ErrorCategory.MISSING_PERIOD
            },
            {
                "input": "Likes(bob, pizza).",
                "expected": "likes(bob, pizza).",
                "exercise": "fact",
                "expected_category": ErrorCategory.UPPERCASE_PREDICATE
            },
            {
                "input": "likes bob, pizza.",
                "expected": "likes(bob, pizza).",
                "exercise": "fact",
                "expected_category": ErrorCategory.MISSING_PARENTHESES
            },
            {
                "input": "likes(bob, pizza).",
                "expected": "?- likes(bob, pizza).",
                "exercise": "query",
                "expected_category": ErrorCategory.MISSING_QUERY_PREFIX
            },
            {
                "input": "?- likes(x, pizza).",
                "expected": "?- likes(X, pizza).",
                "exercise": "variable_query",
                "expected_category": ErrorCategory.LOWERCASE_VARIABLE
            }
        ]
        
        for case in test_cases:
            context = ErrorContext(
                user_input=case["input"],
                expected_answer=case["expected"],
                attempt_count=1,
                error_category=ErrorCategory.GENERIC_SYNTAX,
                exercise_type=case["exercise"]
            )
            
            category = ProgressiveHintSystem.categorize_error(context)
            assert category == case["expected_category"], \
                f"Input '{case['input']}' should be categorized as {case['expected_category']}, got {category}"
    
    def test_recovery_mechanisms_integration(self):
        """Test that recovery mechanisms are properly integrated."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Test help options for different attempt counts
        for attempt_count in [3, 4, 5, 6]:
            terminal.outputs = []
            
            # Display recovery options
            puzzle._display_recovery_options(terminal, attempt_count, "fact")
            
            output_text = terminal.get_all_output_text()
            
            # Verify recovery options are presented
            assert "stuck" in output_text.lower()
            assert "help" in output_text.lower()
            assert "learning" in output_text.lower()
            
            # Verify encouraging tone
            assert ("don't worry" in output_text.lower() or 
                   "every programmer" in output_text.lower())
    
    def test_alternative_explanations(self):
        """Test that alternative explanations are helpful and clear."""
        explanations = {
            "fact": RecoveryMechanisms.provide_alternative_explanation("fact", "syntax"),
            "query": RecoveryMechanisms.provide_alternative_explanation("query", "syntax"),
            "variable_query": RecoveryMechanisms.provide_alternative_explanation("variable_query", "syntax")
        }
        
        for exercise_type, explanation in explanations.items():
            assert len(explanation) > 0, f"No explanation provided for {exercise_type}"
            
            explanation_text = " ".join(explanation).lower()
            
            # Verify explanations contain relevant concepts
            if exercise_type == "fact":
                assert ("database" in explanation_text or 
                       "relationship" in explanation_text or
                       "true" in explanation_text)
            elif exercise_type == "query":
                assert ("question" in explanation_text or
                       "ask" in explanation_text or
                       "true" in explanation_text)
            elif exercise_type == "variable_query":
                assert ("variable" in explanation_text or
                       "uppercase" in explanation_text or
                       "match" in explanation_text)
    
    def test_show_answer_integration(self):
        """Test that showing answers provides complete explanations."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        test_cases = [
            ("likes(bob, pizza).", "fact"),
            ("?- likes(bob, pizza).", "query"),
            ("?- likes(X, pizza).", "variable_query")
        ]
        
        for expected_answer, exercise_type in test_cases:
            terminal.outputs = []
            
            # Show the correct answer
            puzzle._show_correct_answer(terminal, expected_answer, exercise_type)
            
            output_text = terminal.get_all_output_text()
            
            # Verify the answer is shown
            assert expected_answer in output_text
            
            # Verify explanation is provided
            assert ("break" in output_text.lower() or 
                   "explanation" in output_text.lower())
            
            # Verify encouraging tone for users who needed help
            encouraging_indicators = [
                "persistence", "didn't give up", "better", "experience",
                "resilience", "programmer", "learning"
            ]
            assert any(indicator in output_text.lower() for indicator in encouraging_indicators)
    
    def test_hint_progression_consistency(self):
        """Test that hint progression is consistent across different error types."""
        error_types = [
            ErrorCategory.MISSING_PERIOD,
            ErrorCategory.UPPERCASE_PREDICATE,
            ErrorCategory.MISSING_PARENTHESES,
            ErrorCategory.MISSING_QUERY_PREFIX,
            ErrorCategory.LOWERCASE_VARIABLE
        ]
        
        for error_type in error_types:
            # Test that all hint levels have appropriate messages
            if error_type in ProgressiveHintSystem.ERROR_PATTERNS:
                patterns = ProgressiveHintSystem.ERROR_PATTERNS[error_type]
                messages = patterns["messages"]
                
                # Verify all hint levels are covered
                required_levels = [HintLevel.GENTLE, HintLevel.SPECIFIC, 
                                 HintLevel.DETAILED, HintLevel.EXPLICIT]
                
                for level in required_levels:
                    assert level in messages, \
                        f"Error type {error_type} missing hint level {level}"
                    
                    message = messages[level]
                    assert len(message) > 0, \
                        f"Empty message for {error_type} at level {level}"
                    
                    # Verify messages get more specific at higher levels
                    if level == HintLevel.GENTLE:
                        # Should be brief and encouraging
                        assert len(message.split()) <= 15, \
                            f"Gentle hint too long for {error_type}"
                    elif level == HintLevel.EXPLICIT:
                        # Should be very specific
                        assert len(message.split()) >= 5, \
                            f"Explicit hint too brief for {error_type}"
    
    def test_encouraging_tone_throughout_flow(self):
        """Test that encouraging tone is maintained throughout the entire error handling flow."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Test various error scenarios
        error_scenarios = [
            ("likes(bob, pizza)", "likes(bob, pizza).", "fact"),
            ("Likes(bob, pizza).", "likes(bob, pizza).", "fact"),
            ("likes(bob, pizza).", "?- likes(bob, pizza).", "query"),
            ("?- likes(x, pizza).", "?- likes(X, pizza).", "variable_query")
        ]
        
        for user_input, expected_answer, exercise_type in error_scenarios:
            # Test multiple attempts for each scenario
            for attempt in range(1, 4):
                terminal.outputs = []
                puzzle._last_user_input = user_input
                
                # Get validation result
                if exercise_type == "fact":
                    validation_result = PrologValidator.validate_fact(user_input)
                else:
                    validation_result = PrologValidator.validate_query(user_input)
                
                # Display error feedback
                puzzle._display_syntax_error_feedback(
                    terminal, validation_result, attempt, [], expected_answer, exercise_type
                )
                
                output_text = terminal.get_all_output_text().lower()
                
                # Verify no discouraging language (but "don't give up" is encouraging)
                discouraging_words = [
                    "bad", "wrong", "terrible", "awful", "stupid", "dumb",
                    "fail", "failure", "hopeless", "quit"
                ]
                
                # Special case: "don't give up" is encouraging, not discouraging
                if "give up" in output_text and "don't give up" not in output_text:
                    discouraging_words.append("give up")
                
                for word in discouraging_words:
                    assert word not in output_text, \
                        f"Discouraging word '{word}' found in output for {exercise_type} attempt {attempt}"
                
                # Verify encouraging elements are present
                encouraging_elements = [
                    "💡", "🔍", "📝", "✅", "🎯", "🤗", "🌟", "🚀"  # Positive emojis
                ]
                
                assert any(element in terminal.get_all_output_text() for element in encouraging_elements), \
                    f"No encouraging visual elements found for {exercise_type} attempt {attempt}"


class TestSpecificErrorScenarios:
    """Test specific error scenarios that users commonly encounter."""
    
    def test_missing_period_scenario(self):
        """Test the complete flow for missing period errors."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        user_input = "likes(alice, chocolate)"
        expected_answer = "likes(alice, chocolate)."
        
        validation_result = PrologValidator.validate_fact(user_input)
        puzzle._last_user_input = user_input
        
        # Test first attempt (gentle hint)
        puzzle._display_syntax_error_feedback(
            terminal, validation_result, 1, [], expected_answer, "fact"
        )
        
        output = terminal.get_all_output_text()
        assert "period" in output.lower()
        assert "try again" in output.lower()
        
        # Test third attempt (detailed guidance)
        terminal.outputs = []
        puzzle._display_syntax_error_feedback(
            terminal, validation_result, 3, [], expected_answer, "fact"
        )
        
        output = terminal.get_all_output_text()
        assert "step by step" in output.lower() or "check" in output.lower()
        assert "period" in output.lower()
    
    def test_uppercase_predicate_scenario(self):
        """Test the complete flow for uppercase predicate errors."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        user_input = "Likes(bob, pizza)."
        expected_answer = "likes(bob, pizza)."
        
        validation_result = PrologValidator.validate_fact(user_input)
        puzzle._last_user_input = user_input
        
        # Test error handling
        puzzle._display_syntax_error_feedback(
            terminal, validation_result, 2, [], expected_answer, "fact"
        )
        
        output = terminal.get_all_output_text()
        assert "lowercase" in output.lower()
        assert "predicate" in output.lower()
    
    def test_lowercase_variable_scenario(self):
        """Test the complete flow for lowercase variable errors."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        user_input = "?- likes(x, pizza)."
        expected_answer = "?- likes(X, pizza)."
        
        validation_result = PrologValidator.validate_query(user_input)
        puzzle._last_user_input = user_input
        
        # Test error handling
        puzzle._display_syntax_error_feedback(
            terminal, validation_result, 1, [], expected_answer, "variable_query"
        )
        
        output = terminal.get_all_output_text()
        assert "uppercase" in output.lower()
        assert "variable" in output.lower()


if __name__ == "__main__":
    pytest.main([__file__])