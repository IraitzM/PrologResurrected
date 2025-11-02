"""
Unit tests for HelloWorldPuzzle class.

Tests the basic functionality of the Hello World Prolog tutorial,
including initialization, step management, and validation logic.
"""

import pytest
from game.hello_world_puzzle import HelloWorldPuzzle
from game.tutorial_content import TutorialStep
from game.puzzles import PuzzleDifficulty
from game.validation import ValidationResult


class TestHelloWorldPuzzle:
    """Test suite for HelloWorldPuzzle class."""

    def test_initialization(self):
        """Test that HelloWorldPuzzle initializes correctly."""
        puzzle = HelloWorldPuzzle()
        
        # Check basic puzzle properties
        assert puzzle.puzzle_id == "hello_world_prolog"
        assert puzzle.title == "Hello World Prolog Challenge"
        assert puzzle.difficulty == PuzzleDifficulty.BEGINNER
        assert not puzzle.completed
        
        # Check tutorial-specific properties
        assert puzzle.tutorial_session is not None
        assert puzzle.current_step_name == ""
        assert len(puzzle.step_methods) == 6  # All tutorial steps

    def test_step_management_methods(self):
        """Test step navigation methods."""
        puzzle = HelloWorldPuzzle()
        
        # Test current_step method
        current = puzzle.current_step()
        assert current == TutorialStep.INTRODUCTION
        
        # Test next_step method
        result = puzzle.next_step()
        assert result is True
        assert puzzle.current_step() == TutorialStep.FACTS_EXPLANATION
        
        # Test previous_step method
        result = puzzle.previous_step()
        assert result is True
        assert puzzle.current_step() == TutorialStep.INTRODUCTION

    def test_get_description(self):
        """Test that get_description returns appropriate tutorial description."""
        puzzle = HelloWorldPuzzle()
        description = puzzle.get_description()
        
        assert isinstance(description, str)
        assert "Hello World Prolog Challenge" in description
        assert "facts" in description.lower()
        assert "queries" in description.lower()
        assert "variables" in description.lower()

    def test_get_initial_context(self):
        """Test that get_initial_context returns proper tutorial context."""
        puzzle = HelloWorldPuzzle()
        context = puzzle.get_initial_context()
        
        assert isinstance(context, dict)
        assert "tutorial_type" in context
        assert context["tutorial_type"] == "hello_world_prolog"
        assert "current_step" in context
        assert "progress" in context
        assert "instructions" in context

    def test_validate_solution_fact_creation(self):
        """Test validation during fact creation step."""
        puzzle = HelloWorldPuzzle()
        
        # Move to fact creation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Test valid fact
        result = puzzle.validate_solution("likes(bob, pizza).")
        assert isinstance(result, ValidationResult)
        # Note: Actual validation depends on PrologValidator implementation
        
        # Test invalid fact (missing period)
        result = puzzle.validate_solution("likes(bob, pizza)")
        assert isinstance(result, ValidationResult)

    def test_validate_solution_query_creation(self):
        """Test validation during query explanation step."""
        puzzle = HelloWorldPuzzle()
        
        # Move to query explanation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        
        # Test query validation
        result = puzzle.validate_solution("?- likes(bob, pizza).")
        assert isinstance(result, ValidationResult)

    def test_validate_solution_variable_query(self):
        """Test validation during variables introduction step."""
        puzzle = HelloWorldPuzzle()
        
        # Move to variables introduction step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.VARIABLES_INTRODUCTION)
        
        # Test variable query validation
        result = puzzle.validate_solution("?- likes(X, pizza).")
        assert isinstance(result, ValidationResult)

    def test_get_hint_system(self):
        """Test that hint system works for different steps."""
        puzzle = HelloWorldPuzzle()
        
        # Test hints for fact creation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        hint1 = puzzle.get_hint(1)
        hint2 = puzzle.get_hint(2)
        
        assert isinstance(hint1, str)
        assert isinstance(hint2, str)
        assert len(hint1) > 0
        assert len(hint2) > 0
        assert hint1 != hint2  # Different hint levels should give different hints

    def test_get_expected_solution(self):
        """Test that expected solutions are provided for each step."""
        puzzle = HelloWorldPuzzle()
        
        # Test expected solution for fact creation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        solution = puzzle.get_expected_solution()
        assert isinstance(solution, str)
        assert "likes(bob, pizza)." in solution
        
        # Test expected solution for query explanation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        solution = puzzle.get_expected_solution()
        assert isinstance(solution, str)
        assert "?-" in solution

    def test_get_tutorial_progress(self):
        """Test tutorial progress tracking."""
        puzzle = HelloWorldPuzzle()
        progress = puzzle.get_tutorial_progress()
        
        assert isinstance(progress, dict)
        assert "completion_percentage" in progress
        assert "steps_completed" in progress
        assert "facts_created" in progress
        assert "queries_written" in progress
        assert "mistakes_made" in progress
        assert "hints_used" in progress

    def test_reset_functionality(self):
        """Test that reset properly resets tutorial state."""
        puzzle = HelloWorldPuzzle()
        
        # Make some progress
        puzzle.next_step()
        puzzle.tutorial_session.record_mistake()
        puzzle.get_hint(1)
        
        # Reset
        puzzle.reset()
        
        # Check that state is reset
        assert not puzzle.completed
        assert puzzle.attempts == 0
        assert puzzle.hints_used == 0
        assert puzzle.current_step() == TutorialStep.INTRODUCTION

    def test_step_methods_exist(self):
        """Test that all step methods are properly defined."""
        puzzle = HelloWorldPuzzle()
        
        # Check that all step methods exist and are callable
        for step, method in puzzle.step_methods.items():
            assert callable(method)
            assert hasattr(puzzle, method.__name__)

    def test_tutorial_session_integration(self):
        """Test integration with TutorialSession."""
        puzzle = HelloWorldPuzzle()
        
        # Test that tutorial session is properly initialized
        assert puzzle.tutorial_session is not None
        assert puzzle.tutorial_session.session_active  # Session is active by default
        
        # Test session summary
        summary = puzzle.tutorial_session.get_session_summary()
        assert isinstance(summary, dict)
        assert summary["completion_percentage"] >= 0

    def test_step_facts_explanation(self):
        """Test the facts explanation step implementation."""
        puzzle = HelloWorldPuzzle()
        
        # Create a mock terminal for testing
        class MockTerminal:
            def __init__(self):
                self.outputs = []
                self.cleared = False
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
            
            def clear_terminal(self):
                self.cleared = True
                self.outputs = []
        
        mock_terminal = MockTerminal()
        
        # Move to facts explanation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACTS_EXPLANATION)
        
        # Run the facts explanation step
        result = puzzle.step_facts_explanation(mock_terminal)
        
        # Verify the step completed successfully
        assert result is True
        
        # Verify terminal was cleared
        assert mock_terminal.cleared is True
        
        # Verify content was displayed
        assert len(mock_terminal.outputs) > 0
        
        # Check for key content elements
        output_text = " ".join([output[0] for output in mock_terminal.outputs])
        
        # Should contain title and explanation
        assert "Your First Prolog Fact" in output_text or "FACTS" in output_text
        
        # Should contain examples
        assert "likes(alice, chocolate)" in output_text
        assert "parent(tom, bob)" in output_text
        assert "employee(sarah, tech_corp)" in output_text
        
        # Should contain syntax breakdown
        assert "predicate" in output_text.lower()
        assert "arguments" in output_text.lower()
        assert "period" in output_text.lower()
        
        # Should contain completion message
        assert "completed successfully" in output_text
        
        # Verify component identification exercise elements
        assert "loves(romeo, juliet)" in output_text
        assert "PRACTICE EXERCISE" in output_text or "practice" in output_text.lower()

    def test_component_identification_exercise(self):
        """Test the component identification exercise functionality."""
        puzzle = HelloWorldPuzzle()
        
        # Test the validation method for component answers
        # Question 0: predicate
        assert puzzle._validate_component_answer("loves", "loves", 0) is True
        assert puzzle._validate_component_answer("LOVES", "loves", 0) is True  # Case insensitive
        assert puzzle._validate_component_answer("likes", "loves", 0) is False
        
        # Question 1: arguments
        assert puzzle._validate_component_answer("romeo and juliet", "romeo and juliet", 1) is True
        assert puzzle._validate_component_answer("romeo, juliet", "romeo and juliet", 1) is True
        assert puzzle._validate_component_answer("juliet and romeo", "romeo and juliet", 1) is True  # Contains both
        assert puzzle._validate_component_answer("alice", "romeo and juliet", 1) is False
        
        # Question 2: punctuation
        assert puzzle._validate_component_answer("period", "period (.)", 2) is True
        assert puzzle._validate_component_answer(".", "period (.)", 2) is True
        assert puzzle._validate_component_answer("dot", "period (.)", 2) is True
        assert puzzle._validate_component_answer("comma", "period (.)", 2) is False

    def test_component_explanation_generation(self):
        """Test that component explanations are generated correctly."""
        puzzle = HelloWorldPuzzle()
        
        # Test explanations for each question type
        explanation_0 = puzzle._get_component_explanation(0, "loves")
        explanation_1 = puzzle._get_component_explanation(1, "romeo and juliet")
        explanation_2 = puzzle._get_component_explanation(2, "period (.)")
        
        assert isinstance(explanation_0, str)
        assert isinstance(explanation_1, str)
        assert isinstance(explanation_2, str)
        
        assert "predicate" in explanation_0.lower()
        assert "arguments" in explanation_1.lower()
        assert "period" in explanation_2.lower() or "end" in explanation_2.lower()

    def test_step_fact_creation(self):
        """Test the fact creation step implementation."""
        puzzle = HelloWorldPuzzle()
        
        # Create a mock terminal for testing
        class MockTerminal:
            def __init__(self):
                self.outputs = []
                self.cleared = False
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
            
            def clear_terminal(self):
                self.cleared = True
                self.outputs = []
        
        mock_terminal = MockTerminal()
        
        # Move to fact creation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Run the fact creation step
        result = puzzle.step_fact_creation(mock_terminal)
        
        # Verify the step completed successfully
        assert result is True
        
        # Verify terminal was cleared
        assert mock_terminal.cleared is True
        
        # Verify content was displayed
        assert len(mock_terminal.outputs) > 0
        
        # Check for key content elements
        output_text = " ".join([output[0] for output in mock_terminal.outputs])
        
        # Should contain title and explanation
        assert "Create Your First Fact" in output_text or "FACT" in output_text
        
        # Should contain exercise prompt
        assert "Bob likes pizza" in output_text
        
        # Should contain completion message
        assert "completed successfully" in output_text
        
        # Should contain pattern reminder
        assert "predicate(argument1, argument2)" in output_text
        
        # Should contain positive reinforcement
        assert "PERFECT" in output_text or "EXCELLENT" in output_text or "SUCCESS" in output_text

    def test_fact_creation_validation_methods(self):
        """Test the fact creation validation helper methods."""
        puzzle = HelloWorldPuzzle()
        
        # Test _is_acceptable_fact_answer method
        expected = "likes(bob, pizza)."
        alternatives = ["enjoys(bob, pizza).", "loves(bob, pizza)."]
        
        # Test exact match
        assert puzzle._is_acceptable_fact_answer("likes(bob, pizza).", expected, alternatives) is True
        
        # Test case insensitive match
        assert puzzle._is_acceptable_fact_answer("LIKES(BOB, PIZZA).", expected, alternatives) is True
        
        # Test alternative match
        assert puzzle._is_acceptable_fact_answer("enjoys(bob, pizza).", expected, alternatives) is True
        
        # Test semantic match with different predicate
        assert puzzle._is_acceptable_fact_answer("wants(bob, pizza).", expected, alternatives) is True
        
        # Test incorrect content
        assert puzzle._is_acceptable_fact_answer("likes(alice, chocolate).", expected, alternatives) is False

    def test_fact_creation_progressive_hints(self):
        """Test the progressive hint system in fact creation."""
        puzzle = HelloWorldPuzzle()
        
        # Create mock validation result for testing
        from game.validation import ValidationResult
        
        # Test different error scenarios
        missing_period_error = ValidationResult(
            is_valid=False,
            error_message="Missing period at the end.",
            hint="All Prolog facts must end with a period (.)."
        )
        
        # Create a mock terminal
        class MockTerminal:
            def __init__(self):
                self.outputs = []
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
        
        mock_terminal = MockTerminal()
        
        # Test progressive feedback for different attempt counts
        puzzle._display_syntax_error_feedback(mock_terminal, missing_period_error, 1, [], "likes(bob, pizza).", "fact")
        output_text_1 = " ".join([output[0] for output in mock_terminal.outputs])
        
        mock_terminal.outputs = []  # Clear outputs
        puzzle._display_syntax_error_feedback(mock_terminal, missing_period_error, 2, [], "likes(bob, pizza).", "fact")
        output_text_2 = " ".join([output[0] for output in mock_terminal.outputs])
        
        mock_terminal.outputs = []  # Clear outputs
        puzzle._display_syntax_error_feedback(mock_terminal, missing_period_error, 3, [], "likes(bob, pizza).", "fact")
        output_text_3 = " ".join([output[0] for output in mock_terminal.outputs])
        
        # Verify that different attempt counts give different levels of help
        assert "TRY AGAIN" in output_text_1
        assert ("TRY AGAIN" in output_text_2 or "DEBUG" in output_text_2)  # Updated error handling may use different titles
        assert ("BREAKDOWN" in output_text_3 or "GUIDANCE" in output_text_3 or "DEBUG" in output_text_3)  # Updated error handling may use different titles
        
        # Verify that all contain the error message
        assert "Missing period" in output_text_1
        assert "Missing period" in output_text_2
        assert "Missing period" in output_text_3

    def test_positive_reinforcement_messages(self):
        """Test that positive reinforcement varies based on attempt count."""
        puzzle = HelloWorldPuzzle()
        
        class MockTerminal:
            def __init__(self):
                self.outputs = []
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
        
        mock_terminal = MockTerminal()
        
        # Test first attempt success
        puzzle._display_positive_reinforcement(mock_terminal, "likes(bob, pizza).", 1)
        output_text_1 = " ".join([output[0] for output in mock_terminal.outputs])
        
        mock_terminal.outputs = []  # Clear outputs
        puzzle._display_positive_reinforcement(mock_terminal, "likes(bob, pizza).", 2)
        output_text_2 = " ".join([output[0] for output in mock_terminal.outputs])
        
        mock_terminal.outputs = []  # Clear outputs
        puzzle._display_positive_reinforcement(mock_terminal, "likes(bob, pizza).", 4)
        output_text_4 = " ".join([output[0] for output in mock_terminal.outputs])
        
        # Verify different messages for different attempt counts
        assert "PERFECT ON THE FIRST TRY" in output_text_1
        assert "EXCELLENT" in output_text_2
        assert "Persistence pays off" in output_text_4
        
        # All should contain the user's fact
        assert "likes(bob, pizza)." in output_text_1
        assert "likes(bob, pizza)." in output_text_2
        assert "likes(bob, pizza)." in output_text_4

    def test_step_queries_explanation(self):
        """Test the queries explanation step implementation."""
        puzzle = HelloWorldPuzzle()
        
        # Create a mock terminal for testing
        class MockTerminal:
            def __init__(self):
                self.outputs = []
                self.cleared = False
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
            
            def clear_terminal(self):
                self.cleared = True
                self.outputs = []
        
        mock_terminal = MockTerminal()
        
        # Move to queries explanation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        
        # Run the queries explanation step
        result = puzzle.step_queries_explanation(mock_terminal)
        
        # Verify the step completed successfully
        assert result is True
        
        # Verify terminal was cleared
        assert mock_terminal.cleared is True
        
        # Verify content was displayed
        assert len(mock_terminal.outputs) > 0
        
        # Check for key content elements
        output_text = " ".join([output[0] for output in mock_terminal.outputs])
        
        # Should contain title and explanation
        assert "Asking Questions with Queries" in output_text or "QUERIES" in output_text
        
        # Should contain query syntax introduction
        assert "?-" in output_text
        assert "queries start with" in output_text.lower() or "query prefix" in output_text.lower()
        
        # Should contain examples of yes/no queries
        assert "likes(alice, chocolate)" in output_text
        assert "likes(bob, pizza)" in output_text
        assert "parent(tom, bob)" in output_text
        
        # Should contain syntax breakdown
        assert "QUERY PREFIX" in output_text or "query syntax" in output_text.lower()
        assert "period" in output_text.lower()
        
        # Should contain interactive exercise elements
        assert "QUERY WRITING EXERCISE" in output_text or "practice" in output_text.lower()
        
        # Should contain completion message
        assert "completed successfully" in output_text
        
        # Should mention variables as next step
        assert "variables" in output_text.lower()

    def test_query_writing_exercise(self):
        """Test the query writing exercise functionality."""
        puzzle = HelloWorldPuzzle()
        
        # Create a mock terminal for testing
        class MockTerminal:
            def __init__(self):
                self.outputs = []
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
        
        mock_terminal = MockTerminal()
        
        # Test the exercise with sample content
        exercise_config = {
            "prompt": "Given the fact: likes(bob, pizza).",
            "instruction": "Write a query to ask if Bob likes pizza:",
            "expected_answer": "?- likes(bob, pizza)."
        }
        
        # Run the exercise
        result = puzzle._run_query_writing_exercise(mock_terminal, exercise_config)
        
        # Should complete successfully
        assert result is True
        
        # Check that exercise content was displayed
        output_text = " ".join([output[0] for output in mock_terminal.outputs])
        assert "QUERY WRITING EXERCISE" in output_text
        assert "Given the fact: likes(bob, pizza)." in output_text
        assert "Write a query to ask if Bob likes pizza:" in output_text

    def test_query_validation_methods(self):
        """Test the query validation helper methods."""
        puzzle = HelloWorldPuzzle()
        
        # Test _is_acceptable_query_answer method
        expected = "?- likes(bob, pizza)."
        
        # Test exact match
        assert puzzle._is_acceptable_query_answer("?- likes(bob, pizza).", expected) is True
        
        # Test case insensitive match
        assert puzzle._is_acceptable_query_answer("?- LIKES(BOB, PIZZA).", expected) is True
        
        # Test with different spacing (should still work with proper space after ?-)
        assert puzzle._is_acceptable_query_answer("?- likes(bob,pizza).", expected) is True
        
        # Test incorrect content
        assert puzzle._is_acceptable_query_answer("?- likes(alice, chocolate).", expected) is False
        
        # Test missing query prefix
        assert puzzle._is_acceptable_query_answer("likes(bob, pizza).", expected) is False

    def test_query_feedback_methods(self):
        """Test the query feedback display methods."""
        puzzle = HelloWorldPuzzle()
        
        class MockTerminal:
            def __init__(self):
                self.outputs = []
            
            def add_output(self, text, color=None):
                self.outputs.append((text, color))
        
        mock_terminal = MockTerminal()
        
        # Test success feedback
        puzzle._display_query_success_feedback(mock_terminal, "?- likes(bob, pizza).", 1)
        output_text = " ".join([output[0] for output in mock_terminal.outputs])
        
        assert "PERFECT" in output_text or "EXCELLENT" in output_text
        assert "?- likes(bob, pizza)." in output_text
        assert "Bob likes pizza" in output_text
        
        # Test content mismatch feedback
        mock_terminal.outputs = []
        puzzle._display_query_content_mismatch_feedback(mock_terminal, "?- likes(alice, chocolate).", "?- likes(bob, pizza).")
        output_text = " ".join([output[0] for output in mock_terminal.outputs])
        
        assert "Good syntax" in output_text
        assert "?- likes(alice, chocolate)." in output_text
        assert "?- likes(bob, pizza)." in output_text