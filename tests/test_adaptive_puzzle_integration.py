"""
Integration tests for the AdaptivePuzzleFactory with PuzzleManager.

Tests the complete integration of puzzle adaptation functionality
within the game's puzzle management system.
"""

import pytest
from prologresurrected.game.puzzles import PuzzleManager, SimpleFactPuzzle
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.adaptive_puzzle_factory import AdaptivePuzzleFactory


class TestAdaptivePuzzleIntegration:
    """Integration tests for adaptive puzzle functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PuzzleManager()
        self.factory = AdaptivePuzzleFactory()
        self.simple_puzzle = SimpleFactPuzzle()
    
    def test_puzzle_manager_uses_adaptive_factory(self):
        """Test that PuzzleManager uses AdaptivePuzzleFactory for puzzle adaptation."""
        # Register a puzzle
        self.manager.register_puzzle(self.simple_puzzle)
        
        # Set complexity level to expert
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Start the puzzle
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        # Current puzzle should be adapted for expert level
        current_puzzle = self.manager.current_puzzle
        assert current_puzzle is not None
        assert current_puzzle.get_complexity_level() == ComplexityLevel.EXPERT
        assert hasattr(current_puzzle, '_adaptation_params')
        
        # Check that expert-level adaptations are applied
        params = current_puzzle._adaptation_params
        assert params['hint_frequency'] == "none"
        assert params['explanation_detail'] == "minimal"
        assert params['require_optimization'] is True
    
    def test_complexity_change_re_adapts_puzzle(self):
        """Test that changing complexity level re-adapts the current puzzle."""
        # Register and start a puzzle at beginner level
        self.manager.register_puzzle(self.simple_puzzle)
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        # Verify beginner adaptations
        current_puzzle = self.manager.current_puzzle
        assert current_puzzle.get_complexity_level() == ComplexityLevel.BEGINNER
        beginner_params = current_puzzle._adaptation_params
        assert beginner_params['provide_templates'] is True
        assert beginner_params['show_examples'] is True
        
        # Change to intermediate level
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Current puzzle should be re-adapted
        current_puzzle = self.manager.current_puzzle
        assert current_puzzle.get_complexity_level() == ComplexityLevel.INTERMEDIATE
        intermediate_params = current_puzzle._adaptation_params
        assert intermediate_params['provide_templates'] is False
        assert intermediate_params['show_examples'] is True
    
    def test_adapted_puzzle_maintains_state_during_complexity_change(self):
        """Test that puzzle state is preserved when complexity changes."""
        # Register and start a puzzle
        self.manager.register_puzzle(self.simple_puzzle)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        # Make some attempts and use hints
        self.manager.submit_solution("wrong_answer")
        self.manager.get_hint()
        
        # Record current state
        current_puzzle = self.manager.current_puzzle
        attempts_before = current_puzzle.attempts
        hints_before = current_puzzle.hints_used
        
        # Change complexity level
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # State should be preserved
        current_puzzle = self.manager.current_puzzle
        assert current_puzzle.attempts == attempts_before
        assert current_puzzle.hints_used == hints_before
        assert current_puzzle.get_complexity_level() == ComplexityLevel.ADVANCED
    
    def test_different_puzzle_types_get_appropriate_adaptations(self):
        """Test that different puzzle types receive appropriate adaptations."""
        # Test with SimpleFactPuzzle (fact creation type)
        self.manager.register_puzzle(self.simple_puzzle)
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        current_puzzle = self.manager.current_puzzle
        
        # Should have fact-specific adaptations for beginners
        assert hasattr(current_puzzle, '_beginner_template')
        assert current_puzzle._show_syntax_help is True
        assert current_puzzle._provide_examples is True
    
    def test_adapted_puzzle_scoring_uses_complexity_multiplier(self):
        """Test that adapted puzzles use complexity-based scoring."""
        self.manager.register_puzzle(self.simple_puzzle)
        
        # Test beginner scoring (1.0x multiplier)
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        result_beginner = self.manager.submit_solution("likes(alice, chocolate).")
        beginner_score = result_beginner.score
        
        # Reset and test expert scoring (2.0x multiplier)
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        result_expert = self.manager.submit_solution("likes(alice, chocolate).")
        expert_score = result_expert.score
        
        # Expert should have higher score due to multiplier
        assert expert_score > beginner_score
        # Should be approximately 2x (allowing for rounding)
        assert abs(expert_score - beginner_score * 2) <= 1
    
    def test_adapted_puzzle_hint_system_respects_complexity(self):
        """Test that adapted puzzles provide hints according to complexity level."""
        self.manager.register_puzzle(self.simple_puzzle)
        
        # Test beginner level (hints always available)
        self.manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        hint_beginner = self.manager.get_hint()
        assert hint_beginner is not None
        assert len(hint_beginner) > 0
        assert "Think about the problem structure." not in hint_beginner  # Should be detailed
        
        # Test expert level (no hints)
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        hint_expert = self.manager.get_hint()
        assert hint_expert is not None
        assert "Hints are not available at Expert level" in hint_expert
    
    def test_get_adapted_puzzle_method(self):
        """Test the get_adapted_puzzle method in PuzzleManager."""
        self.manager.register_puzzle(self.simple_puzzle)
        
        # Get adapted puzzle for different levels
        beginner_puzzle = self.manager.get_adapted_puzzle(
            self.simple_puzzle.puzzle_id, 
            ComplexityLevel.BEGINNER
        )
        expert_puzzle = self.manager.get_adapted_puzzle(
            self.simple_puzzle.puzzle_id, 
            ComplexityLevel.EXPERT
        )
        
        assert beginner_puzzle is not None
        assert expert_puzzle is not None
        assert beginner_puzzle.get_complexity_level() == ComplexityLevel.BEGINNER
        assert expert_puzzle.get_complexity_level() == ComplexityLevel.EXPERT
        
        # Should have different adaptation parameters
        assert beginner_puzzle._adaptation_params != expert_puzzle._adaptation_params
    
    def test_adaptation_summary_provides_useful_info(self):
        """Test that adaptation summary provides useful information."""
        self.manager.register_puzzle(self.simple_puzzle)
        self.manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        self.manager.start_puzzle(self.simple_puzzle.puzzle_id)
        
        summary = self.manager.get_adaptation_summary(self.simple_puzzle.puzzle_id)
        
        assert summary is not None
        assert summary['complexity_level'] == 'INTERMEDIATE'
        assert summary['puzzle_id'] == self.simple_puzzle.puzzle_id
        assert summary['puzzle_type'] == 'fact_creation'
        assert 'adaptations' in summary
        assert summary['is_valid'] is True
    
    def test_can_adapt_puzzle_check(self):
        """Test the can_adapt_puzzle method."""
        self.manager.register_puzzle(self.simple_puzzle)
        
        can_adapt = self.manager.can_adapt_puzzle(self.simple_puzzle.puzzle_id)
        assert can_adapt is True
        
        # Non-existent puzzle should return False
        can_adapt_nonexistent = self.manager.can_adapt_puzzle("nonexistent_puzzle")
        assert can_adapt_nonexistent is False
    
    def test_factory_integration_with_puzzle_manager(self):
        """Test that the factory is properly integrated with PuzzleManager."""
        # PuzzleManager should have an adaptive factory
        assert hasattr(self.manager, 'adaptive_factory')
        assert isinstance(self.manager.adaptive_factory, AdaptivePuzzleFactory)
        
        # Factory should be able to adapt puzzles
        assert self.manager.adaptive_factory.can_adapt_puzzle(self.simple_puzzle)
        
        # Factory should have all required methods
        assert hasattr(self.manager.adaptive_factory, 'create_adapted_puzzle')
        assert hasattr(self.manager.adaptive_factory, 'validate_adaptation')
        assert hasattr(self.manager.adaptive_factory, 'get_adaptation_summary')


class TestAdaptivePuzzleFactoryStandalone:
    """Test AdaptivePuzzleFactory as a standalone component."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.factory = AdaptivePuzzleFactory()
        self.simple_puzzle = SimpleFactPuzzle()
    
    def test_factory_can_adapt_all_complexity_levels(self):
        """Test that factory can adapt puzzles for all complexity levels."""
        for level in ComplexityLevel:
            adapted = self.factory.create_adapted_puzzle(self.simple_puzzle, level)
            
            assert adapted is not None
            assert adapted.get_complexity_level() == level
            assert self.factory.validate_adaptation(adapted, level) is True
    
    def test_factory_adaptation_is_consistent(self):
        """Test that factory produces consistent adaptations."""
        # Create multiple adaptations of the same puzzle at the same level
        adapted1 = self.factory.create_adapted_puzzle(self.simple_puzzle, ComplexityLevel.INTERMEDIATE)
        adapted2 = self.factory.create_adapted_puzzle(self.simple_puzzle, ComplexityLevel.INTERMEDIATE)
        
        # Should have the same adaptation parameters
        assert adapted1._adaptation_params == adapted2._adaptation_params
        assert adapted1.get_complexity_level() == adapted2.get_complexity_level()
    
    def test_factory_handles_edge_cases(self):
        """Test that factory handles edge cases gracefully."""
        # Test with None puzzle (should raise ValueError)
        with pytest.raises(ValueError, match="base_puzzle must be a BasePuzzle instance"):
            self.factory.create_adapted_puzzle(None, ComplexityLevel.BEGINNER)
        
        # Test validation with mismatched level
        adapted = self.factory.create_adapted_puzzle(self.simple_puzzle, ComplexityLevel.BEGINNER)
        is_valid = self.factory.validate_adaptation(adapted, ComplexityLevel.EXPERT)
        assert is_valid is False