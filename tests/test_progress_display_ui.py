"""
Unit tests for progress display UI functionality.

Tests that the status and achievements commands properly display
complexity-aware progress information to the player.
"""

import pytest
from prologresurrected.prologresurrected import GameState
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.puzzles import BasePuzzle, PuzzleDifficulty
from prologresurrected.game.validation import ValidationResult


class MockUITestPuzzle(BasePuzzle):
    """Mock puzzle for testing UI display."""

    def __init__(self, puzzle_id="ui_test", title="UI Test Puzzle"):
        super().__init__(puzzle_id, title, PuzzleDifficulty.BEGINNER)
        self.validation_result = ValidationResult(is_valid=True)

    def get_description(self):
        return "Test puzzle for UI display"

    def get_initial_context(self):
        return {"test": True}

    def validate_solution(self, user_input):
        return self.validation_result

    def get_hint(self, hint_level):
        return f"Test hint {hint_level}"

    def get_expected_solution(self):
        return "test_solution"


class TestProgressDisplayUI:
    """Test progress display UI functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.state = GameState()
        self.state.game_mode = "adventure"
        
        # Register test puzzles
        self.puzzle1 = MockUITestPuzzle("puzzle1", "Test Puzzle 1")
        self.puzzle2 = MockUITestPuzzle("puzzle2", "Test Puzzle 2")
        self.puzzle3 = MockUITestPuzzle("puzzle3", "Test Puzzle 3")
        
        self.state.puzzle_manager.register_puzzle(self.puzzle1)
        self.state.puzzle_manager.register_puzzle(self.puzzle2)
        self.state.puzzle_manager.register_puzzle(self.puzzle3)

    def test_status_command_displays_basic_progress(self):
        """Test that status command displays basic progress information."""
        # Complete a puzzle
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call status
        self.state.terminal_output = []
        self.state._show_player_status()
        
        # Check that output contains expected information
        output_text = "\n".join(self.state.terminal_output)
        
        assert "PLAYER STATUS REPORT" in output_text
        assert "OVERALL PROGRESS" in output_text
        assert "Total Score:" in output_text
        assert "Puzzles Completed: 1" in output_text
        assert "CURRENT COMPLEXITY LEVEL" in output_text
        assert "BEGINNER" in output_text

    def test_status_command_shows_complexity_achievements_summary(self):
        """Test that status command shows complexity achievements summary."""
        # Complete puzzles at different levels
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.state.puzzle_manager.start_puzzle(self.puzzle2.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call status
        self.state.terminal_output = []
        self.state._show_player_status()
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "COMPLEXITY ACHIEVEMENTS" in output_text
        assert "BEGINNER" in output_text
        assert "EXPERT" in output_text
        assert "1 puzzles" in output_text  # Each level has 1 puzzle

    def test_status_command_shows_hello_world_status(self):
        """Test that status command shows Hello World tutorial status."""
        # Clear terminal and call status
        self.state.terminal_output = []
        self.state._show_player_status()
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "Hello World Tutorial" in output_text
        assert "Not completed" in output_text
        
        # Mark as completed
        self.state.puzzle_manager.player_stats["hello_world_completed"] = True
        self.state.story_engine.mark_hello_world_completed()
        
        # Check again
        self.state.terminal_output = []
        self.state._show_player_status()
        
        output_text = "\n".join(self.state.terminal_output)
        assert "Completed" in output_text

    def test_achievements_command_displays_detailed_breakdown(self):
        """Test that achievements command displays detailed breakdown."""
        # Complete puzzles at different levels
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        result1 = self.state.puzzle_manager.submit_solution("test_solution")
        
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.ADVANCED)
        self.state.puzzle_manager.start_puzzle(self.puzzle2.puzzle_id)
        result2 = self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "COMPLEXITY ACHIEVEMENTS" in output_text
        assert "INTERMEDIATE" in output_text
        assert "ADVANCED" in output_text
        assert "Puzzles Completed: 1" in output_text
        assert "Total Score:" in output_text
        assert "Average Score:" in output_text

    def test_achievements_command_shows_all_levels(self):
        """Test that achievements command shows all complexity levels."""
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        output_text = "\n".join(self.state.terminal_output)
        
        # Should show all 4 levels
        assert "BEGINNER" in output_text
        assert "INTERMEDIATE" in output_text
        assert "ADVANCED" in output_text
        assert "EXPERT" in output_text

    def test_achievements_command_highlights_current_level(self):
        """Test that achievements command highlights the current complexity level."""
        # Set to intermediate level
        self.state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        # Check that intermediate is highlighted (has arrow marker)
        # We need to check the actual output structure
        output_lines = self.state.terminal_output
        
        # Find the line with INTERMEDIATE
        intermediate_line_idx = None
        for i, line in enumerate(output_lines):
            if "INTERMEDIATE" in line and "→" in line:
                intermediate_line_idx = i
                break
        
        assert intermediate_line_idx is not None, "Current level should be marked with arrow"

    def test_achievements_command_shows_completion_history(self):
        """Test that achievements command shows recent completion history."""
        # Complete multiple puzzles
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.state.puzzle_manager.start_puzzle(self.puzzle2.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "RECENT COMPLETIONS" in output_text
        assert "Test Puzzle 1" in output_text
        assert "Test Puzzle 2" in output_text
        assert "Score:" in output_text
        assert "Attempts:" in output_text
        assert "Hints:" in output_text

    def test_achievements_command_limits_history_display(self):
        """Test that achievements command limits history to last 5 completions."""
        # Complete 7 puzzles
        for i in range(7):
            puzzle = MockUITestPuzzle(f"puzzle_{i}", f"Test Puzzle {i}")
            self.state.puzzle_manager.register_puzzle(puzzle)
            self.state.puzzle_manager.start_puzzle(puzzle.puzzle_id)
            self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        output_text = "\n".join(self.state.terminal_output)
        
        # Should show "and X more" message
        assert "and 2 more" in output_text

    def test_status_updates_right_panel(self):
        """Test that status command updates the right panel."""
        # Complete a puzzle
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        # Call status
        self.state._show_player_status()
        
        # Check right panel content
        assert "PLAYER STATUS" in self.state.right_panel_content
        assert "Overall Progress" in self.state.right_panel_content
        assert "Current Complexity" in self.state.right_panel_content
        assert self.state.right_panel_title == "STATUS"

    def test_achievements_updates_right_panel(self):
        """Test that achievements command updates the right panel."""
        # Call achievements
        self.state._show_complexity_achievements()
        
        # Check right panel content
        assert "ACHIEVEMENTS" in self.state.right_panel_content
        assert "Track your progress" in self.state.right_panel_content
        assert self.state.right_panel_title == "ACHIEVEMENTS"

    def test_status_shows_no_puzzles_message_when_none_completed(self):
        """Test that status shows appropriate message when no puzzles completed."""
        # Clear terminal and call status
        self.state.terminal_output = []
        self.state._show_player_status()
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "No puzzles completed yet" in output_text

    def test_achievements_shows_no_completions_per_level(self):
        """Test that achievements shows no completions for unused levels."""
        # Complete only at beginner level
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        output_text = "\n".join(self.state.terminal_output)
        
        # Should show "No puzzles completed" for other levels
        assert "No puzzles completed at this level" in output_text

    def test_status_command_available_in_adventure_mode(self):
        """Test that status command works in adventure mode."""
        self.state.game_mode = "adventure"
        
        # Simulate status command
        self.state.terminal_output = []
        self.state.handle_terminal_input("status")
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "PLAYER STATUS REPORT" in output_text

    def test_achievements_command_available_in_adventure_mode(self):
        """Test that achievements command works in adventure mode."""
        self.state.game_mode = "adventure"
        
        # Simulate achievements command
        self.state.terminal_output = []
        self.state.handle_terminal_input("achievements")
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "COMPLEXITY ACHIEVEMENTS" in output_text

    def test_status_command_available_in_tutorial_mode(self):
        """Test that status command works in tutorial mode."""
        self.state.game_mode = "tutorial"
        self.state.tutorial_active = True
        
        # Simulate status command
        self.state.terminal_output = []
        self.state.handle_terminal_input("status")
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "PLAYER STATUS REPORT" in output_text

    def test_achievements_command_available_in_tutorial_mode(self):
        """Test that achievements command works in tutorial mode."""
        self.state.game_mode = "tutorial"
        self.state.tutorial_active = True
        
        # Simulate achievements command
        self.state.terminal_output = []
        self.state.handle_terminal_input("achievements")
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "COMPLEXITY ACHIEVEMENTS" in output_text

    def test_help_command_includes_achievements(self):
        """Test that help command mentions the achievements command."""
        self.state.game_mode = "adventure"
        
        # Simulate help command
        self.state.terminal_output = []
        self.state.handle_terminal_input("help")
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "achievements" in output_text.lower()
        assert "complexity-based achievements" in output_text.lower()

    def test_status_shows_scoring_multiplier(self):
        """Test that status shows the current complexity level's scoring multiplier."""
        # Set to expert level (higher multiplier)
        self.state.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Clear terminal and call status
        self.state.terminal_output = []
        self.state._show_player_status()
        
        output_text = "\n".join(self.state.terminal_output)
        
        assert "Scoring Multiplier:" in output_text
        # Expert level should have a multiplier
        assert "x" in output_text

    def test_achievements_shows_average_scores(self):
        """Test that achievements display shows average scores per level."""
        # Complete multiple puzzles at same level
        self.state.puzzle_manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        self.state.puzzle_manager.start_puzzle(self.puzzle1.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        self.state.puzzle_manager.start_puzzle(self.puzzle2.puzzle_id)
        self.state.puzzle_manager.submit_solution("test_solution")
        
        # Clear terminal and call achievements
        self.state.terminal_output = []
        self.state._show_complexity_achievements()
        
        output_text = "\n".join(self.state.terminal_output)
        
        # Should show average score
        assert "Average Score:" in output_text
        # Should show 2 puzzles completed
        assert "Puzzles Completed: 2" in output_text
