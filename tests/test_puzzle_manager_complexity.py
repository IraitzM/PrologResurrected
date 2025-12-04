"""
Unit tests for PuzzleManager complexity integration.

Tests the complexity-aware functionality added to PuzzleManager including
complexity level management and puzzle integration.
"""

import pytest
from prologresurrected.game.puzzles import PuzzleManager, SimpleFactPuzzle, BasePuzzle, PuzzleDifficulty
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.validation import ValidationResult


class MockComplexityPuzzle(BasePuzzle):
    """Mock puzzle for testing complexity integration."""

    def __init__(self, puzzle_id="complexity_test"):
        super().__init__(puzzle_id, "Complexity Test Puzzle", PuzzleDifficulty.BEGINNER)
        self.validation_result = ValidationResult(is_valid=True)

    def get_description(self):
        return "Test puzzle for complexity"

    def get_initial_context(self):
        return {"test": True}

    def validate_solution(self, user_input):
        return self.validation_result

    def get_hint(self, hint_level):
        return f"Test hint {hint_level}"

    def get_expected_solution(self):
        return "test_solution"


class TestPuzzleManagerComplexity:
    """Test complexity-aware functionality in PuzzleManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PuzzleManager()
        self.puzzle = MockComplexityPuzzle()

    def test_default_complexity_level(self):
        """Test that PuzzleManager starts with BEGINNER complexity level."""
        assert self.manager.get_complexity_level() == ComplexityLevel.BEGINNER

    def test_set_complexity_level(self):
        """Test setting complexity level in PuzzleManager."""
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.manager.get_complexity_level() == ComplexityLevel.ADVANCED

    def test_complexity_level_propagates_to_puzzle(self):
        """Test that complexity level is set on puzzles when started."""
        self.manager.register_puzzle(self.puzzle)
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Start the puzzle
        self.manager.start_puzzle(self.puzzle.puzzle_id)
        
        # Puzzle should have the same complexity level
        assert self.puzzle.get_complexity_level() == ComplexityLevel.EXPERT

    def test_complexity_level_updates_current_puzzle(self):
        """Test that changing complexity level updates the current puzzle."""
        self.manager.register_puzzle(self.puzzle)
        self.manager.start_puzzle(self.puzzle.puzzle_id)
        
        # Initially beginner
        assert self.puzzle.get_complexity_level() == ComplexityLevel.BEGINNER
        
        # Change complexity level
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Current puzzle should be updated
        assert self.puzzle.get_complexity_level() == ComplexityLevel.INTERMEDIATE

    def test_get_complexity_config(self):
        """Test getting complexity configuration."""
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        config = self.manager.get_complexity_config()
        
        assert config["name"] == "Advanced"
        assert config["level"] == ComplexityLevel.ADVANCED
        assert "ui_indicators" in config
        assert "scoring_multiplier" in config
        assert config["scoring_multiplier"] == 1.5

    def test_complexity_config_changes_with_level(self):
        """Test that complexity config changes when level changes."""
        # Test beginner config
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        beginner_config = self.manager.get_complexity_config()
        assert beginner_config["name"] == "Beginner"
        assert beginner_config["scoring_multiplier"] == 1.0

        # Test expert config
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        expert_config = self.manager.get_complexity_config()
        assert expert_config["name"] == "Expert"
        assert expert_config["scoring_multiplier"] == 2.0

    def test_puzzle_manager_with_simple_fact_puzzle(self):
        """Test PuzzleManager complexity integration with SimpleFactPuzzle."""
        simple_puzzle = SimpleFactPuzzle()
        self.manager.register_puzzle(simple_puzzle)
        
        # Set to expert level
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Start the puzzle
        self.manager.start_puzzle(simple_puzzle.puzzle_id)
        
        # Puzzle should have expert complexity
        assert simple_puzzle.get_complexity_level() == ComplexityLevel.EXPERT
        
        # Test that expert-level parameters are applied
        assert simple_puzzle.should_provide_template() is False
        assert simple_puzzle.requires_optimization() is True

    def test_complexity_aware_hint_system(self):
        """Test that hint system works with complexity levels."""
        self.manager.register_puzzle(self.puzzle)
        
        # Test beginner level hints
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle.puzzle_id)
        
        hint = self.manager.get_hint()
        # Beginner hints should be available and encouraging
        assert hint is not None
        assert len(hint) > 0
        # The hint system provides complexity-adapted hints, not the base hint text

        # Test expert level hints
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.manager.start_puzzle(self.puzzle.puzzle_id)
        hint = self.manager.get_hint()
        assert "Hints are not available at Expert level" in hint

    def test_complexity_aware_scoring(self):
        """Test that scoring includes complexity multipliers."""
        self.manager.register_puzzle(self.puzzle)
        
        # Test beginner scoring
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.puzzle.puzzle_id)
        
        result = self.manager.submit_solution("test_solution")
        beginner_score = result.score
        
        # Reset and test expert scoring
        self.puzzle.reset()
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.manager.start_puzzle(self.puzzle.puzzle_id)
        
        result = self.manager.submit_solution("test_solution")
        expert_score = result.score
        
        # Expert should have higher score due to 2x multiplier
        assert expert_score == beginner_score * 2

    def test_complexity_level_persistence(self):
        """Test that complexity level persists across puzzle changes."""
        puzzle1 = MockComplexityPuzzle("puzzle1")
        puzzle2 = MockComplexityPuzzle("puzzle2")
        
        self.manager.register_puzzle(puzzle1)
        self.manager.register_puzzle(puzzle2)
        
        # Set complexity level
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Start first puzzle
        self.manager.start_puzzle("puzzle1")
        assert puzzle1.get_complexity_level() == ComplexityLevel.INTERMEDIATE
        
        # Start second puzzle
        self.manager.start_puzzle("puzzle2")
        assert puzzle2.get_complexity_level() == ComplexityLevel.INTERMEDIATE
        
        # Manager should still have the same level
        assert self.manager.get_complexity_level() == ComplexityLevel.INTERMEDIATE

    def test_no_current_puzzle_complexity_operations(self):
        """Test complexity operations when no puzzle is current."""
        # Should not crash when no current puzzle
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.manager.get_complexity_level() == ComplexityLevel.ADVANCED
        
        config = self.manager.get_complexity_config()
        assert config["name"] == "Advanced"

    def test_complexity_manager_synchronization(self):
        """Test that PuzzleManager's complexity manager stays synchronized."""
        # Change level through manager
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Both should be synchronized
        assert self.manager.get_complexity_level() == ComplexityLevel.EXPERT
        assert self.manager.complexity_manager.get_current_level() == ComplexityLevel.EXPERT
        
        # Config should match
        manager_config = self.manager.get_complexity_config()
        direct_config = self.manager.complexity_manager.get_current_config()
        
        assert manager_config["name"] == direct_config.name
        assert manager_config["scoring_multiplier"] == direct_config.scoring_multiplier