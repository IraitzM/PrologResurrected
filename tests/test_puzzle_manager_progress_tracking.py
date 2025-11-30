"""
Unit tests for PuzzleManager progress tracking with complexity integration.

Tests the complexity-aware progress tracking functionality including
achievements per complexity level and completion history.
"""

import pytest
from prologresurrected.game.puzzles import PuzzleManager, BasePuzzle, PuzzleDifficulty
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.validation import ValidationResult


class MockProgressPuzzle(BasePuzzle):
    """Mock puzzle for testing progress tracking."""

    def __init__(self, puzzle_id="progress_test", title="Progress Test"):
        super().__init__(puzzle_id, title, PuzzleDifficulty.BEGINNER)
        self.validation_result = ValidationResult(is_valid=True)

    def get_description(self):
        return "Test puzzle for progress tracking"

    def get_initial_context(self):
        return {"test": True}

    def validate_solution(self, user_input):
        return self.validation_result

    def get_hint(self, hint_level):
        return f"Test hint {hint_level}"

    def get_expected_solution(self):
        return "test_solution"


class TestPuzzleManagerProgressTracking:
    """Test complexity-aware progress tracking in PuzzleManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PuzzleManager()
        self.puzzle1 = MockProgressPuzzle("puzzle1", "Puzzle 1")
        self.puzzle2 = MockProgressPuzzle("puzzle2", "Puzzle 2")
        self.puzzle3 = MockProgressPuzzle("puzzle3", "Puzzle 3")

    def test_complexity_achievements_initialized(self):
        """Test that complexity achievements are initialized for all levels."""
        stats = self.manager.get_player_stats()
        
        assert "complexity_achievements" in stats
        assert ComplexityLevel.BEGINNER in stats["complexity_achievements"]
        assert ComplexityLevel.INTERMEDIATE in stats["complexity_achievements"]
        assert ComplexityLevel.ADVANCED in stats["complexity_achievements"]
        assert ComplexityLevel.EXPERT in stats["complexity_achievements"]
        
        # All should start at zero
        for level in ComplexityLevel:
            achievements = stats["complexity_achievements"][level]
            assert achievements["puzzles_completed"] == 0
            assert achievements["total_score"] == 0

    def test_completion_history_initialized(self):
        """Test that completion history is initialized."""
        stats = self.manager.get_player_stats()
        
        assert "puzzle_completion_history" in stats
        assert isinstance(stats["puzzle_completion_history"], list)
        assert len(stats["puzzle_completion_history"]) == 0

    def test_puzzle_completion_updates_complexity_achievements(self):
        """Test that completing a puzzle updates complexity-specific achievements."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        
        # Complete the puzzle
        result = self.manager.submit_solution("test_solution")
        
        # Check that intermediate achievements were updated
        achievements = self.manager.get_complexity_achievements(ComplexityLevel.INTERMEDIATE)
        assert achievements["puzzles_completed"] == 1
        assert achievements["total_score"] == result.score
        assert achievements["average_score"] == result.score
        
        # Other levels should still be at zero
        beginner_achievements = self.manager.get_complexity_achievements(ComplexityLevel.BEGINNER)
        assert beginner_achievements["puzzles_completed"] == 0

    def test_multiple_puzzles_at_different_complexity_levels(self):
        """Test completing multiple puzzles at different complexity levels."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.register_puzzle(self.puzzle2)
        self.manager.register_puzzle(self.puzzle3)
        
        # Complete puzzle 1 at beginner level
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        result1 = self.manager.submit_solution("test_solution")
        
        # Complete puzzle 2 at expert level
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.manager.start_puzzle(self.puzzle2.puzzle_id)
        result2 = self.manager.submit_solution("test_solution")
        
        # Complete puzzle 3 at beginner level
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle3.puzzle_id)
        result3 = self.manager.submit_solution("test_solution")
        
        # Check beginner achievements (2 puzzles)
        beginner = self.manager.get_complexity_achievements(ComplexityLevel.BEGINNER)
        assert beginner["puzzles_completed"] == 2
        assert beginner["total_score"] == result1.score + result3.score
        
        # Check expert achievements (1 puzzle)
        expert = self.manager.get_complexity_achievements(ComplexityLevel.EXPERT)
        assert expert["puzzles_completed"] == 1
        assert expert["total_score"] == result2.score

    def test_completion_history_records_all_completions(self):
        """Test that completion history records all puzzle completions."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.register_puzzle(self.puzzle2)
        
        # Complete puzzle 1 at intermediate level
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        result1 = self.manager.submit_solution("test_solution")
        
        # Complete puzzle 2 at advanced level
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        self.manager.start_puzzle(self.puzzle2.puzzle_id)
        result2 = self.manager.submit_solution("test_solution")
        
        # Check completion history
        stats = self.manager.get_player_stats()
        history = stats["puzzle_completion_history"]
        
        assert len(history) == 2
        
        # Check first completion
        assert history[0]["puzzle_id"] == self.puzzle1.puzzle_id
        assert history[0]["puzzle_title"] == self.puzzle1.title
        assert history[0]["complexity_level"] == "INTERMEDIATE"
        assert history[0]["score"] == result1.score
        assert history[0]["attempts"] == result1.attempts
        assert history[0]["hints_used"] == result1.hints_used
        
        # Check second completion
        assert history[1]["puzzle_id"] == self.puzzle2.puzzle_id
        assert history[1]["complexity_level"] == "ADVANCED"
        assert history[1]["score"] == result2.score

    def test_progress_summary_includes_complexity_achievements(self):
        """Test that progress summary includes complexity achievements."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        self.manager.submit_solution("test_solution")
        
        summary = self.manager.get_progress_summary()
        
        assert "complexity_achievements" in summary
        assert "EXPERT" in summary["complexity_achievements"]
        assert summary["complexity_achievements"]["EXPERT"]["puzzles_completed"] == 1
        assert summary["complexity_achievements"]["EXPERT"]["total_score"] > 0

    def test_progress_summary_includes_completion_history(self):
        """Test that progress summary includes completion history."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        self.manager.submit_solution("test_solution")
        
        summary = self.manager.get_progress_summary()
        
        assert "completion_history" in summary
        assert len(summary["completion_history"]) == 1
        assert summary["completion_history"][0]["puzzle_id"] == self.puzzle1.puzzle_id

    def test_get_all_complexity_achievements(self):
        """Test getting achievements for all complexity levels."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.register_puzzle(self.puzzle2)
        
        # Complete puzzles at different levels
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        self.manager.submit_solution("test_solution")
        
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        self.manager.start_puzzle(self.puzzle2.puzzle_id)
        self.manager.submit_solution("test_solution")
        
        # Get all achievements
        all_achievements = self.manager.get_all_complexity_achievements()
        
        assert len(all_achievements) == 4  # All 4 complexity levels
        assert "BEGINNER" in all_achievements
        assert "INTERMEDIATE" in all_achievements
        assert "ADVANCED" in all_achievements
        assert "EXPERT" in all_achievements
        
        # Check that beginner and advanced have completions
        assert all_achievements["BEGINNER"]["puzzles_completed"] == 1
        assert all_achievements["ADVANCED"]["puzzles_completed"] == 1
        assert all_achievements["INTERMEDIATE"]["puzzles_completed"] == 0
        assert all_achievements["EXPERT"]["puzzles_completed"] == 0

    def test_average_score_calculation_per_complexity_level(self):
        """Test that average scores are calculated correctly per complexity level."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.register_puzzle(self.puzzle2)
        
        # Complete two puzzles at beginner level
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        result1 = self.manager.submit_solution("test_solution")
        
        self.manager.start_puzzle(self.puzzle2.puzzle_id)
        result2 = self.manager.submit_solution("test_solution")
        
        # Check average score
        achievements = self.manager.get_complexity_achievements(ComplexityLevel.BEGINNER)
        expected_average = (result1.score + result2.score) / 2
        assert achievements["average_score"] == expected_average

    def test_complexity_achievements_in_progress_summary(self):
        """Test that complexity achievements are properly formatted in progress summary."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        result = self.manager.submit_solution("test_solution")
        
        summary = self.manager.get_progress_summary()
        
        # Check that intermediate achievements are in the summary
        intermediate_achievements = summary["complexity_achievements"]["INTERMEDIATE"]
        assert intermediate_achievements["puzzles_completed"] == 1
        assert intermediate_achievements["total_score"] == result.score
        assert intermediate_achievements["average_score"] == result.score

    def test_concept_coverage_tracking(self):
        """Test that core concept coverage is tracked."""
        coverage = self.manager.get_concept_coverage()
        
        # Should have all core concepts
        assert "prolog_basics" in coverage
        assert "facts" in coverage
        assert "queries" in coverage
        assert "variables" in coverage
        assert "rules" in coverage
        assert "unification" in coverage
        assert "backtracking" in coverage
        assert "recursion" in coverage
        
        # All should start as False
        for concept, covered in coverage.items():
            assert covered is False

    def test_concept_coverage_updates_on_completion(self):
        """Test that concept coverage updates when puzzles are completed."""
        # Get the hello world puzzle if available
        hello_world = self.manager.get_hello_world_puzzle()
        
        if hello_world:
            self.manager.start_puzzle(hello_world.puzzle_id)
            self.manager.submit_solution("hello_world.")
            
            # Check that concepts are now covered
            coverage = self.manager.get_concept_coverage()
            assert coverage["prolog_basics"] is True
            assert coverage["facts"] is True
            assert coverage["queries"] is True
            assert coverage["variables"] is True

    def test_ensures_concept_coverage_method(self):
        """Test that ensures_concept_coverage returns correct concepts."""
        # Test hello world puzzle
        concepts = self.manager.ensures_concept_coverage("hello_world_prolog")
        assert "prolog_basics" in concepts
        assert "facts" in concepts
        assert "queries" in concepts
        assert "variables" in concepts
        
        # Test simple fact puzzle
        concepts = self.manager.ensures_concept_coverage("simple_fact_1")
        assert "facts" in concepts
        assert "prolog_basics" in concepts

    def test_complexity_achievements_persist_across_level_changes(self):
        """Test that achievements persist when complexity level changes."""
        self.manager.register_puzzle(self.puzzle1)
        
        # Complete at beginner level
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle1.puzzle_id)
        result1 = self.manager.submit_solution("test_solution")
        
        # Change to expert level and check beginner achievements still exist
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        
        beginner_achievements = self.manager.get_complexity_achievements(ComplexityLevel.BEGINNER)
        assert beginner_achievements["puzzles_completed"] == 1
        assert beginner_achievements["total_score"] == result1.score

    def test_empty_achievements_have_zero_average(self):
        """Test that empty achievements have zero average score."""
        achievements = self.manager.get_complexity_achievements(ComplexityLevel.BEGINNER)
        
        assert achievements["puzzles_completed"] == 0
        assert achievements["total_score"] == 0
        assert achievements["average_score"] == 0
