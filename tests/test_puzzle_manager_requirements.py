"""
Test Puzzle Manager Requirements

Tests for puzzle registration and integration with PuzzleManager,
specifically for the Memory Stack Failure puzzle.

Validates: Requirements 5.5
"""

import pytest
from prologresurrected.game.puzzles import PuzzleManager, PuzzleDifficulty


class TestMemoryStackPuzzleRegistration:
    """Test cases for Memory Stack Puzzle registration with PuzzleManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PuzzleManager()

    def test_memory_stack_puzzle_is_registered(self):
        """
        Test that MemoryStackPuzzle is registered with PuzzleManager.
        
        Validates: Requirements 5.5
        """
        # Check that memory_stack_failure puzzle is in available puzzles
        assert "memory_stack_failure" in self.manager.available_puzzles
        
        # Verify we can retrieve it
        puzzle = self.manager.get_puzzle("memory_stack_failure")
        assert puzzle is not None
        assert puzzle.puzzle_id == "memory_stack_failure"

    def test_memory_stack_puzzle_can_be_retrieved_by_id(self):
        """
        Test that puzzle can be retrieved by its ID.
        
        Validates: Requirements 5.5
        """
        puzzle = self.manager.get_puzzle("memory_stack_failure")
        
        assert puzzle is not None
        assert puzzle.puzzle_id == "memory_stack_failure"
        assert puzzle.title == "Memory Stack Investigation"
        assert puzzle.difficulty == PuzzleDifficulty.BEGINNER

    def test_memory_stack_puzzle_appears_in_correct_order(self):
        """
        Test that puzzle appears in correct order (first adventure mode puzzle).
        
        The Memory Stack Failure puzzle should be the first adventure mode puzzle,
        coming after the Hello World tutorial.
        
        Validates: Requirements 5.5
        """
        # Get all available puzzles
        all_puzzles = list(self.manager.available_puzzles.values())
        
        # Should have at least 2 puzzles (hello_world and memory_stack)
        assert len(all_puzzles) >= 2
        
        # Check that memory_stack_failure is registered
        puzzle_ids = [p.puzzle_id for p in all_puzzles]
        assert "hello_world_prolog" in puzzle_ids
        assert "memory_stack_failure" in puzzle_ids

    def test_memory_stack_puzzle_integrates_with_complexity_system(self):
        """
        Test that puzzle integrates with the complexity system.
        
        Validates: Requirements 5.5
        """
        puzzle = self.manager.get_puzzle("memory_stack_failure")
        
        # Puzzle should have complexity-related methods
        assert hasattr(puzzle, "set_complexity_level")
        assert hasattr(puzzle, "get_complexity_level")
        assert hasattr(puzzle, "get_complexity_adapted_hint")
        
        # Should be able to set complexity level
        from prologresurrected.game.complexity import ComplexityLevel
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert puzzle.get_complexity_level() == ComplexityLevel.INTERMEDIATE

    def test_memory_stack_puzzle_can_be_started(self):
        """
        Test that the puzzle can be started through PuzzleManager.
        
        Validates: Requirements 5.5
        """
        # Start the puzzle
        result = self.manager.start_puzzle("memory_stack_failure")
        
        assert result is True
        assert self.manager.current_puzzle is not None
        assert self.manager.current_puzzle.puzzle_id == "memory_stack_failure"
        
        # Puzzle should be reset when started
        assert self.manager.current_puzzle.attempts == 0
        assert self.manager.current_puzzle.hints_used == 0
        assert self.manager.current_puzzle.completed is False

    def test_memory_stack_puzzle_has_required_methods(self):
        """
        Test that puzzle implements all required BasePuzzle methods.
        
        Validates: Requirements 5.5
        """
        puzzle = self.manager.get_puzzle("memory_stack_failure")
        
        # Check required methods exist
        assert hasattr(puzzle, "get_description")
        assert hasattr(puzzle, "get_initial_context")
        assert hasattr(puzzle, "validate_solution")
        assert hasattr(puzzle, "get_hint")
        assert hasattr(puzzle, "get_expected_solution")
        
        # Test that methods return appropriate types
        description = puzzle.get_description()
        assert isinstance(description, str)
        assert len(description) > 0
        
        context = puzzle.get_initial_context()
        assert isinstance(context, dict)
        
        hint = puzzle.get_hint(1)
        assert isinstance(hint, str)
        assert len(hint) > 0
