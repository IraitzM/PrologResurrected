"""
Integration tests for HelloWorldPuzzle with mock terminal.

Tests the complete tutorial flow and terminal interaction.
"""

import pytest
from unittest.mock import Mock, MagicMock
from game.hello_world_puzzle import HelloWorldPuzzle
from game.tutorial_content import TutorialStep


class MockTerminal:
    """Mock terminal for testing tutorial interaction."""
    
    def __init__(self):
        self.output_lines = []
        self.all_output_history = []  # Keep full history even after clears
        self.add_output = Mock(side_effect=self._add_output)
        self.clear_terminal = Mock(side_effect=self._clear_terminal)
    
    def _add_output(self, text, color="green"):
        """Mock implementation of add_output."""
        formatted_output = f"[{color}] {text}"
        self.output_lines.append(formatted_output)
        self.all_output_history.append(formatted_output)
    
    def _clear_terminal(self):
        """Mock implementation of clear_terminal."""
        self.output_lines.clear()


class TestHelloWorldIntegration:
    """Integration tests for HelloWorldPuzzle."""

    def test_run_method_basic_flow(self):
        """Test that the run method executes without errors."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Run the tutorial
        result = puzzle.run(terminal)
        
        # Should complete successfully
        assert result is True
        assert puzzle.completed is True
        
        # Should have produced output for each step
        assert len(terminal.all_output_history) >= 6  # At least one output per step
        
        # Check that all step methods were called (they output completion messages)
        output_text = " ".join(terminal.all_output_history)
        assert "Introduction step completed successfully" in output_text
        assert "Facts explanation step completed successfully" in output_text
        assert "Fact creation step completed successfully" in output_text
        assert "Queries explanation step completed successfully" in output_text
        assert "Variables introduction step completed successfully" in output_text
        assert "Completion step completed successfully" in output_text

    def test_run_method_with_exception_handling(self):
        """Test that the run method handles exceptions gracefully."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Mock a step method in the step_methods dictionary to raise an exception
        from game.tutorial_content import TutorialStep
        original_method = puzzle.step_methods[TutorialStep.INTRODUCTION]
        puzzle.step_methods[TutorialStep.INTRODUCTION] = Mock(side_effect=Exception("Test exception"))
        
        # Run the tutorial
        result = puzzle.run(terminal)
        
        # Should handle the exception and return False
        assert result is False
        assert not puzzle.completed
        
        # Should have error output
        error_outputs = [line for line in terminal.output_lines if "error" in line.lower() or "Error" in line]
        assert len(error_outputs) > 0
        
        # Restore original method
        puzzle.step_methods[TutorialStep.INTRODUCTION] = original_method

    def test_step_progression(self):
        """Test that steps progress correctly."""
        puzzle = HelloWorldPuzzle()
        
        # Start at introduction
        assert puzzle.current_step() == TutorialStep.INTRODUCTION
        
        # Progress through steps
        steps = [
            TutorialStep.INTRODUCTION,
            TutorialStep.FACTS_EXPLANATION,
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION,
            TutorialStep.COMPLETION
        ]
        
        for i, expected_step in enumerate(steps):
            assert puzzle.current_step() == expected_step
            if i < len(steps) - 1:  # Don't advance past the last step
                puzzle.next_step()

    def test_tutorial_session_lifecycle(self):
        """Test tutorial session start and end lifecycle."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Session should be active initially
        assert puzzle.tutorial_session.session_active
        
        # Run tutorial
        puzzle.run(terminal)
        
        # Session should be ended after run completes
        assert not puzzle.tutorial_session.session_active

    def test_progress_tracking_during_run(self):
        """Test that progress is tracked during tutorial execution."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Get initial progress
        initial_progress = puzzle.get_tutorial_progress()
        assert initial_progress["completion_percentage"] == 0
        assert initial_progress["steps_completed"] == 0
        
        # Run tutorial
        puzzle.run(terminal)
        
        # Check final progress
        final_progress = puzzle.get_tutorial_progress()
        assert final_progress["completion_percentage"] > initial_progress["completion_percentage"]
        assert final_progress["steps_completed"] > initial_progress["steps_completed"]

    def test_validation_integration(self):
        """Test that validation works correctly with different step contexts."""
        puzzle = HelloWorldPuzzle()
        
        # Test fact creation validation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        result = puzzle.validate_solution("likes(alice, chocolate).")
        assert hasattr(result, 'is_valid')
        
        # Test query validation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        result = puzzle.validate_solution("?- likes(alice, chocolate).")
        assert hasattr(result, 'is_valid')
        
        # Test variable query validation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.VARIABLES_INTRODUCTION)
        result = puzzle.validate_solution("?- likes(X, chocolate).")
        assert hasattr(result, 'is_valid')

    def test_hint_system_integration(self):
        """Test that hint system works across different steps."""
        puzzle = HelloWorldPuzzle()
        
        # Test hints for different steps
        steps_to_test = [
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION
        ]
        
        for step in steps_to_test:
            puzzle.tutorial_session.navigator.jump_to_step(step)
            
            # Get multiple hint levels
            hint1 = puzzle.get_hint(1)
            hint2 = puzzle.get_hint(2)
            
            assert isinstance(hint1, str)
            assert isinstance(hint2, str)
            assert len(hint1) > 0
            assert len(hint2) > 0
            
            # Hints should be different for different levels
            assert hint1 != hint2

    def test_reset_integration(self):
        """Test that reset works correctly after running tutorial."""
        puzzle = HelloWorldPuzzle()
        terminal = MockTerminal()
        
        # Run tutorial and make some progress
        puzzle.run(terminal)
        assert puzzle.completed
        
        # Reset
        puzzle.reset()
        
        # Should be back to initial state
        assert not puzzle.completed
        assert puzzle.current_step() == TutorialStep.INTRODUCTION
        assert puzzle.attempts == 0
        assert puzzle.hints_used == 0
        
        # Should be able to run again
        result = puzzle.run(terminal)
        assert result is True