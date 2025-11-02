"""
Integration tests for HelloWorldPuzzle with the main game system.

Tests the integration of HelloWorldPuzzle with PuzzleManager and StoryEngine
to ensure proper tutorial completion tracking and transitions.
"""

import pytest
from game.puzzles import PuzzleManager
from game.story import StoryEngine


class TestHelloWorldGameIntegration:
    """Test HelloWorldPuzzle integration with the main game system."""

    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle_manager = PuzzleManager()
        self.story_engine = StoryEngine()

    def test_hello_world_puzzle_auto_registration(self):
        """Test that HelloWorldPuzzle is automatically registered."""
        # HelloWorldPuzzle should be automatically registered
        assert "hello_world_prolog" in self.puzzle_manager.available_puzzles
        
        hello_world = self.puzzle_manager.get_hello_world_puzzle()
        assert hello_world is not None
        assert hello_world.puzzle_id == "hello_world_prolog"
        assert hello_world.title == "Hello World Prolog Challenge"

    def test_hello_world_completion_tracking(self):
        """Test that hello world completion is properly tracked."""
        # Initially not completed
        assert not self.puzzle_manager.is_hello_world_completed()
        assert not self.story_engine.is_hello_world_completed()
        
        # Should recommend hello world for new users
        assert self.puzzle_manager.should_recommend_hello_world()

    def test_hello_world_completion_flow(self):
        """Test the complete hello world completion flow."""
        # Start and complete the hello world puzzle
        success = self.puzzle_manager.start_puzzle("hello_world_prolog")
        assert success
        
        # Simulate completion by directly marking it complete
        # (In real usage, this would happen through the puzzle's run method)
        hello_world = self.puzzle_manager.get_hello_world_puzzle()
        hello_world.completed = True
        
        # Submit a successful result to trigger completion tracking
        from game.puzzles import PuzzleResult
        result = PuzzleResult(
            success=True,
            score=100,
            feedback="Tutorial completed!",
            hints_used=0,
            attempts=1
        )
        
        # Manually trigger completion (simulating what would happen in the real flow)
        self.puzzle_manager._complete_puzzle(hello_world, result)
        
        # Check that completion is tracked
        assert self.puzzle_manager.is_hello_world_completed()
        
        # Check that concepts are learned
        stats = self.puzzle_manager.get_player_stats()
        assert stats["hello_world_completed"]
        assert "prolog_basics" in stats["concepts_mastered"]
        assert "facts" in stats["concepts_mastered"]
        assert "queries" in stats["concepts_mastered"]
        assert "variables" in stats["concepts_mastered"]

    def test_story_engine_hello_world_integration(self):
        """Test StoryEngine integration with hello world completion."""
        # Initially not completed
        assert not self.story_engine.is_hello_world_completed()
        
        # Mark as completed
        self.story_engine.mark_hello_world_completed()
        
        # Check completion status
        assert self.story_engine.is_hello_world_completed()
        
        # Check that concepts are learned
        progress = self.story_engine.get_player_progress()
        assert progress["hello_world_completed"]
        assert "prolog_basics" in progress["concepts_learned"]
        assert "facts" in progress["concepts_learned"]
        assert "queries" in progress["concepts_learned"]
        assert "variables" in progress["concepts_learned"]

    def test_hello_world_transition_story(self):
        """Test that transition story is available."""
        transition_story = self.story_engine.get_hello_world_transition_story()
        
        assert transition_story is not None
        assert transition_story.title == "TUTORIAL COMPLETE - READY FOR THE REAL CHALLENGE"
        assert len(transition_story.content) > 0
        assert "tutorial" in transition_story.title.lower() or "complete" in transition_story.title.lower()

    def test_puzzle_manager_progress_summary_includes_hello_world(self):
        """Test that progress summary includes hello world completion status."""
        summary = self.puzzle_manager.get_progress_summary()
        
        assert "hello_world_completed" in summary
        assert summary["hello_world_completed"] == False  # Initially not completed
        
        # Complete hello world
        self.puzzle_manager.player_stats["hello_world_completed"] = True
        
        summary = self.puzzle_manager.get_progress_summary()
        assert summary["hello_world_completed"] == True

    def test_hello_world_recommendation_logic(self):
        """Test the logic for recommending hello world tutorial."""
        # Should recommend for new users
        assert self.puzzle_manager.should_recommend_hello_world()
        
        # Complete hello world
        self.puzzle_manager.player_stats["hello_world_completed"] = True
        
        # Should not recommend after completion
        assert not self.puzzle_manager.should_recommend_hello_world()
        
        # Reset and complete another puzzle
        self.puzzle_manager.player_stats["hello_world_completed"] = False
        self.puzzle_manager.completed_puzzles.append("some_other_puzzle")
        
        # Should not recommend if other puzzles are completed
        assert not self.puzzle_manager.should_recommend_hello_world()

    def test_hello_world_as_level_zero(self):
        """Test that hello world functions as level 0 / entry point."""
        # Get next puzzle for a new player
        next_puzzle = self.puzzle_manager.get_next_puzzle(current_level=0)
        
        # Should return hello world as the first puzzle
        assert next_puzzle is not None
        assert next_puzzle.puzzle_id == "hello_world_prolog"

    def test_integration_with_existing_puzzle_system(self):
        """Test that hello world integrates properly with existing puzzle system."""
        # Register additional puzzles
        from game.puzzles import SimpleFactPuzzle
        additional_puzzle = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(additional_puzzle)
        
        # Should have both puzzles
        assert len(self.puzzle_manager.available_puzzles) == 2
        assert "hello_world_prolog" in self.puzzle_manager.available_puzzles
        assert "simple_fact_1" in self.puzzle_manager.available_puzzles
        
        # Hello world should still be recommended first
        next_puzzle = self.puzzle_manager.get_next_puzzle(current_level=1)
        assert next_puzzle.puzzle_id == "hello_world_prolog"