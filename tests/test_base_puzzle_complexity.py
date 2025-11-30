"""
Unit tests for BasePuzzle complexity awareness functionality.

Tests the complexity-aware methods added to BasePuzzle class including
hint adaptation, feedback adaptation, and complexity parameter handling.
"""

import pytest
from prologresurrected.game.puzzles import BasePuzzle, SimpleFactPuzzle, PuzzleResult, PuzzleDifficulty
from prologresurrected.game.complexity import ComplexityLevel, HintFrequency, ExplanationDepth
from prologresurrected.game.validation import ValidationResult


class TestBasePuzzleComplexity:
    """Test complexity-aware functionality in BasePuzzle."""

    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle = SimpleFactPuzzle()

    def test_default_complexity_level(self):
        """Test that puzzles start with BEGINNER complexity level."""
        assert self.puzzle.get_complexity_level() == ComplexityLevel.BEGINNER

    def test_set_complexity_level(self):
        """Test setting complexity level."""
        self.puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.puzzle.get_complexity_level() == ComplexityLevel.ADVANCED

    def test_get_complexity_parameters(self):
        """Test getting complexity parameters."""
        # Test beginner parameters
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        params = self.puzzle.get_complexity_parameters()
        assert params["provide_templates"] is True
        assert params["show_examples"] is True
        assert params["max_variables"] == 2

        # Test expert parameters
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        params = self.puzzle.get_complexity_parameters()
        assert params["provide_templates"] is False
        assert params["require_optimization"] is True
        assert params["include_edge_cases"] is True

    def test_should_provide_template(self):
        """Test template provision based on complexity level."""
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert self.puzzle.should_provide_template() is True

        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert self.puzzle.should_provide_template() is False

    def test_should_show_examples(self):
        """Test example showing based on complexity level."""
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert self.puzzle.should_show_examples() is True

        self.puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.puzzle.should_show_examples() is False

    def test_complexity_adapted_hints_beginner(self):
        """Test hint adaptation for beginner level."""
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        hint = self.puzzle.get_complexity_adapted_hint(1)
        
        # Should contain the base hint plus additional encouragement
        assert "Think about the relationship" in hint
        assert "💡 Remember:" in hint

    def test_complexity_adapted_hints_expert(self):
        """Test hint adaptation for expert level."""
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        hint = self.puzzle.get_complexity_adapted_hint(1)
        
        # Should deny hints at expert level
        assert "Hints are not available at Expert level" in hint

    def test_complexity_adapted_hints_advanced_after_attempts(self):
        """Test hint availability after attempts for advanced level."""
        self.puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Should require attempts before giving hints
        hint = self.puzzle.get_complexity_adapted_hint(1)
        assert "Try a few more times" in hint
        
        # After attempts, should provide hints
        self.puzzle.attempts = 2
        hint = self.puzzle.get_complexity_adapted_hint(1)
        assert "Think about the problem structure" in hint

    def test_complexity_adapted_feedback_detailed(self):
        """Test detailed feedback for beginner level."""
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        validation_result = ValidationResult(
            is_valid=False,
            error_message="Syntax error",
            hint="Check your parentheses"
        )
        
        feedback = self.puzzle.get_complexity_adapted_feedback(validation_result)
        assert "Syntax error" in feedback
        assert "💡 Hint:" in feedback
        assert "🔍 Take a moment" in feedback

    def test_complexity_adapted_feedback_minimal(self):
        """Test minimal feedback for expert level."""
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        validation_result = ValidationResult(
            is_valid=False,
            error_message="Syntax error",
            hint="Check your parentheses"
        )
        
        feedback = self.puzzle.get_complexity_adapted_feedback(validation_result)
        assert feedback == "Incorrect. Try again."

    def test_complexity_adapted_success_feedback(self):
        """Test success feedback adaptation."""
        # Beginner level - detailed success feedback
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        self.puzzle.attempts = 1
        self.puzzle.hints_used = 0
        
        validation_result = ValidationResult(is_valid=True)
        feedback = self.puzzle.get_complexity_adapted_feedback(validation_result)
        assert "🎉" in feedback
        assert "✨" in feedback

        # Expert level - minimal success feedback
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        feedback = self.puzzle.get_complexity_adapted_feedback(validation_result)
        assert feedback == "Correct."

    def test_scoring_with_complexity_multiplier(self):
        """Test that scoring includes complexity multiplier."""
        # Test beginner scoring (1.0x multiplier)
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        self.puzzle.attempts = 1
        self.puzzle.hints_used = 0
        score = self.puzzle._calculate_score()
        assert score == 100  # Base score with 1.0x multiplier

        # Test expert scoring (2.0x multiplier)
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        self.puzzle.attempts = 1
        self.puzzle.hints_used = 0
        score = self.puzzle._calculate_score()
        assert score == 200  # Base score with 2.0x multiplier

    def test_complexity_aware_description(self):
        """Test that puzzle description adapts to complexity level."""
        # Beginner level should include examples and templates
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        description = self.puzzle.get_description()
        assert "Template:" in description
        assert "facts follow the pattern" in description

        # Expert level should be more minimal
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        description = self.puzzle.get_description()
        assert "Template:" not in description

    def test_complexity_aware_initial_context(self):
        """Test that initial context adapts to complexity level."""
        # Beginner level should include examples
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        context = self.puzzle.get_initial_context()
        assert "examples" in context
        assert len(context["examples"]) > 0

        # Expert level should not include examples
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        context = self.puzzle.get_initial_context()
        assert "examples" not in context

    def test_attempt_solution_uses_complexity_feedback(self):
        """Test that attempt_solution uses complexity-adapted feedback."""
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Test incorrect solution
        result = self.puzzle.attempt_solution("invalid_syntax")
        assert "🔍 Take a moment" in result.feedback

        # Test correct solution
        result = self.puzzle.attempt_solution("likes(alice, chocolate).")
        assert result.success is True
        assert "🎉" in result.feedback

    def test_request_hint_uses_complexity_adaptation(self):
        """Test that request_hint uses complexity-adapted hints."""
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        hint = self.puzzle.request_hint()
        assert "Hints are not available at Expert level" in hint
        assert self.puzzle.hints_used == 1

    def test_complexity_parameter_methods(self):
        """Test individual complexity parameter methods."""
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert self.puzzle.get_max_variables_allowed() == 2
        assert self.puzzle.get_max_predicates_allowed() == 3
        assert self.puzzle.allows_complex_syntax() is False
        assert self.puzzle.requires_optimization() is False
        assert self.puzzle.includes_edge_cases() is False

        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert self.puzzle.get_max_variables_allowed() == 8
        assert self.puzzle.get_max_predicates_allowed() == 12
        assert self.puzzle.allows_complex_syntax() is True
        assert self.puzzle.requires_optimization() is True
        assert self.puzzle.includes_edge_cases() is True


class TestSimpleFactPuzzleComplexity:
    """Test complexity awareness in SimpleFactPuzzle implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle = SimpleFactPuzzle()

    def test_validation_error_messages_adapt_to_complexity(self):
        """Test that validation error messages adapt to complexity level."""
        # Test detailed error message for beginners
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        result = self.puzzle.validate_solution("likes(bob, pizza).")
        assert "syntactically correct but doesn't match" in result.error_message
        assert "exact format" in result.error_message

        # Test brief error message for experts
        self.puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        result = self.puzzle.validate_solution("likes(bob, pizza).")
        assert result.error_message == "Incorrect fact."

    def test_hint_messages_adapt_to_complexity(self):
        """Test that hint messages are properly adapted."""
        # Base hint should be adapted by complexity level
        self.puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        hint = self.puzzle.get_complexity_adapted_hint(1)
        assert "💡 Remember:" in hint

        self.puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        self.puzzle.attempts = 3  # Ensure hints are allowed
        hint = self.puzzle.get_complexity_adapted_hint(1)
        assert hint == "Think about the problem structure."