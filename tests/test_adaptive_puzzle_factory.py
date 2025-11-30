"""
Unit tests for the AdaptivePuzzleFactory module.

Tests puzzle adaptation functionality across different complexity levels
and puzzle types, ensuring proper parameter application and validation.
"""

import pytest
from unittest.mock import Mock, patch
from prologresurrected.game.adaptive_puzzle_factory import AdaptivePuzzleFactory
from prologresurrected.game.puzzles import BasePuzzle, PuzzleDifficulty, PuzzleType
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.validation import ValidationResult


class MockPuzzle(BasePuzzle):
    """Mock puzzle for testing purposes."""
    
    def __init__(self, puzzle_id="test_puzzle", title="Test Puzzle"):
        super().__init__(puzzle_id, title, PuzzleDifficulty.BEGINNER)
        self.description_calls = 0
        self.hint_calls = 0
    
    def get_description(self) -> str:
        self.description_calls += 1
        return "Test puzzle description"
    
    def get_initial_context(self) -> dict:
        return {"facts": [], "rules": []}
    
    def validate_solution(self, user_input: str) -> ValidationResult:
        return ValidationResult(is_valid=True)
    
    def get_hint(self, hint_level: int) -> str:
        self.hint_calls += 1
        return f"Test hint level {hint_level}"
    
    def get_expected_solution(self) -> str:
        return "test_solution."


class TestAdaptivePuzzleFactory:
    """Test cases for the AdaptivePuzzleFactory class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.factory = AdaptivePuzzleFactory()
        self.mock_puzzle = MockPuzzle()
    
    def test_factory_initialization(self):
        """Test that the factory initializes correctly."""
        assert self.factory is not None
        assert self.factory.complexity_manager is not None
        assert len(self.factory.adaptation_strategies) == 4  # Four complexity levels
        assert len(self.factory.puzzle_type_mappings) > 0
    
    def test_adaptation_strategies_structure(self):
        """Test that adaptation strategies are properly structured."""
        for level in ComplexityLevel:
            assert level in self.factory.adaptation_strategies
            strategy = self.factory.adaptation_strategies[level]
            
            # Check required keys are present
            required_keys = [
                "max_variables", "max_predicates", "allow_complex_syntax",
                "provide_templates", "show_examples", "hint_frequency",
                "explanation_detail", "error_recovery"
            ]
            for key in required_keys:
                assert key in strategy, f"Missing key {key} in {level.name} strategy"
    
    def test_create_adapted_puzzle_basic(self):
        """Test basic puzzle adaptation functionality."""
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.BEGINNER
        )
        
        assert adapted is not None
        assert adapted.get_complexity_level() == ComplexityLevel.BEGINNER
        assert hasattr(adapted, '_adaptation_params')
        assert adapted._adaptation_params['provide_templates'] is True
        assert adapted._adaptation_params['show_examples'] is True
    
    def test_adaptation_preserves_original(self):
        """Test that adaptation doesn't modify the original puzzle."""
        original_level = self.mock_puzzle.get_complexity_level()
        original_max_score = self.mock_puzzle.max_score
        
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.EXPERT
        )
        
        # Original should be unchanged
        assert self.mock_puzzle.get_complexity_level() == original_level
        assert self.mock_puzzle.max_score == original_max_score
        assert not hasattr(self.mock_puzzle, '_adaptation_params')
        
        # Adapted should be different
        assert adapted.get_complexity_level() == ComplexityLevel.EXPERT
        # Max score should be the same (not modified by adaptation)
        assert adapted.max_score == original_max_score
        assert hasattr(adapted, '_adaptation_params')
    
    def test_beginner_level_adaptations(self):
        """Test adaptations specific to beginner level."""
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.BEGINNER
        )
        
        params = adapted._adaptation_params
        assert params['max_variables'] == 2
        assert params['max_predicates'] == 3
        assert params['allow_complex_syntax'] is False
        assert params['provide_templates'] is True
        assert params['show_examples'] is True
        assert params['hint_frequency'] == "always"
        assert params['explanation_detail'] == "detailed"
        # Max score should not be changed by adaptation
        assert adapted.max_score == 100  # Default max score
    
    def test_intermediate_level_adaptations(self):
        """Test adaptations specific to intermediate level."""
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.INTERMEDIATE
        )
        
        params = adapted._adaptation_params
        assert params['max_variables'] == 4
        assert params['max_predicates'] == 5
        assert params['allow_complex_syntax'] is True
        assert params['provide_templates'] is False
        assert params['show_examples'] is True
        assert params['hint_frequency'] == "on_request"
        assert params['explanation_detail'] == "moderate"
        # Max score should not be changed by adaptation
        assert adapted.max_score == 100  # Default max score
    
    def test_advanced_level_adaptations(self):
        """Test adaptations specific to advanced level."""
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.ADVANCED
        )
        
        params = adapted._adaptation_params
        assert params['max_variables'] == 6
        assert params['max_predicates'] == 8
        assert params['allow_complex_syntax'] is True
        assert params['provide_templates'] is False
        assert params['show_examples'] is False
        assert params['hint_frequency'] == "after_attempts"
        assert params['explanation_detail'] == "brief"
        assert params['require_optimization'] is True
        # Max score should not be changed by adaptation
        assert adapted.max_score == 100  # Default max score
    
    def test_expert_level_adaptations(self):
        """Test adaptations specific to expert level."""
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.EXPERT
        )
        
        params = adapted._adaptation_params
        assert params['max_variables'] == 8
        assert params['max_predicates'] == 12
        assert params['allow_complex_syntax'] is True
        assert params['provide_templates'] is False
        assert params['show_examples'] is False
        assert params['hint_frequency'] == "none"
        assert params['explanation_detail'] == "minimal"
        assert params['require_optimization'] is True
        assert params['include_edge_cases'] is True
        # Max score should not be changed by adaptation
        assert adapted.max_score == 100  # Default max score
    
    def test_fact_puzzle_specific_adaptations(self):
        """Test adaptations specific to fact creation puzzles."""
        # Mock the puzzle type detection
        with patch.object(self.factory, '_get_puzzle_type', return_value=PuzzleType.FACT_CREATION):
            # Test beginner fact puzzle
            adapted_beginner = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.BEGINNER
            )
            assert hasattr(adapted_beginner, '_beginner_template')
            assert adapted_beginner._show_syntax_help is True
            assert adapted_beginner._provide_examples is True
            
            # Test expert fact puzzle
            adapted_expert = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.EXPERT
            )
            assert adapted_expert._require_optimization is True
            assert adapted_expert._include_edge_cases is True
            assert adapted_expert._multiple_valid_solutions is True
    
    def test_query_puzzle_specific_adaptations(self):
        """Test adaptations specific to query writing puzzles."""
        with patch.object(self.factory, '_get_puzzle_type', return_value=PuzzleType.QUERY_WRITING):
            # Test beginner query puzzle
            adapted_beginner = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.BEGINNER
            )
            assert adapted_beginner._show_query_syntax is True
            assert adapted_beginner._provide_query_templates is True
            assert adapted_beginner._explain_variable_usage is True
            
            # Test expert query puzzle
            adapted_expert = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.EXPERT
            )
            assert adapted_expert._require_optimization is True
            assert adapted_expert._multiple_solution_paths is True
            assert adapted_expert._performance_constraints is True
    
    def test_rule_puzzle_specific_adaptations(self):
        """Test adaptations specific to rule definition puzzles."""
        with patch.object(self.factory, '_get_puzzle_type', return_value=PuzzleType.RULE_DEFINITION):
            # Test beginner rule puzzle
            adapted_beginner = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.BEGINNER
            )
            assert adapted_beginner._show_rule_syntax is True
            assert adapted_beginner._provide_rule_templates is True
            assert adapted_beginner._explain_implication is True
            assert adapted_beginner._max_conditions == 2
            
            # Test advanced rule puzzle
            adapted_advanced = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.ADVANCED
            )
            assert adapted_advanced._max_conditions == 5
            assert adapted_advanced._allow_disjunctions is True
            assert adapted_advanced._require_multiple_rules is True
    
    def test_pattern_puzzle_specific_adaptations(self):
        """Test adaptations specific to pattern matching puzzles."""
        with patch.object(self.factory, '_get_puzzle_type', return_value=PuzzleType.PATTERN_MATCHING):
            # Test beginner pattern puzzle
            adapted_beginner = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.BEGINNER
            )
            assert adapted_beginner._show_pattern_examples is True
            assert adapted_beginner._explain_unification is True
            assert adapted_beginner._max_pattern_complexity == 2
            
            # Test advanced pattern puzzle
            adapted_advanced = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.ADVANCED
            )
            assert adapted_advanced._max_pattern_complexity == 5
            assert adapted_advanced._require_complex_unification is True
    
    def test_deduction_puzzle_specific_adaptations(self):
        """Test adaptations specific to logical deduction puzzles."""
        with patch.object(self.factory, '_get_puzzle_type', return_value=PuzzleType.LOGICAL_DEDUCTION):
            # Test beginner deduction puzzle
            adapted_beginner = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.BEGINNER
            )
            assert adapted_beginner._show_reasoning_steps is True
            assert adapted_beginner._explain_backtracking is True
            assert adapted_beginner._max_inference_depth == 2
            
            # Test expert deduction puzzle
            adapted_expert = self.factory.create_adapted_puzzle(
                self.mock_puzzle, 
                ComplexityLevel.EXPERT
            )
            assert adapted_expert._require_optimization is True
            assert adapted_expert._include_edge_cases is True
            assert adapted_expert._performance_constraints is True
    
    def test_get_puzzle_type(self):
        """Test puzzle type detection."""
        # Test known puzzle ID
        hello_world_puzzle = MockPuzzle("hello_world_prolog", "Hello World")
        puzzle_type = self.factory._get_puzzle_type(hello_world_puzzle)
        assert puzzle_type == PuzzleType.FACT_CREATION
        
        # Test unknown puzzle ID (should default to FACT_CREATION)
        unknown_puzzle = MockPuzzle("unknown_puzzle", "Unknown")
        puzzle_type = self.factory._get_puzzle_type(unknown_puzzle)
        assert puzzle_type == PuzzleType.FACT_CREATION
    
    def test_get_complexity_parameters(self):
        """Test getting complexity parameters."""
        params = self.factory.get_complexity_parameters(ComplexityLevel.BEGINNER)
        assert params['max_variables'] == 2
        assert params['provide_templates'] is True
        
        params = self.factory.get_complexity_parameters(ComplexityLevel.EXPERT)
        assert params['max_variables'] == 8
        assert params['include_edge_cases'] is True
    
    def test_get_supported_puzzle_types(self):
        """Test getting supported puzzle types."""
        types = self.factory.get_supported_puzzle_types()
        assert len(types) == 5  # All PuzzleType enum values
        assert PuzzleType.FACT_CREATION in types
        assert PuzzleType.QUERY_WRITING in types
        assert PuzzleType.RULE_DEFINITION in types
        assert PuzzleType.PATTERN_MATCHING in types
        assert PuzzleType.LOGICAL_DEDUCTION in types
    
    def test_can_adapt_puzzle(self):
        """Test puzzle adaptation capability check."""
        # All puzzles should be adaptable since we have a default mapping
        assert self.factory.can_adapt_puzzle(self.mock_puzzle) is True
        
        # Test with specific puzzle types
        with patch.object(self.factory, '_get_puzzle_type', return_value=PuzzleType.FACT_CREATION):
            assert self.factory.can_adapt_puzzle(self.mock_puzzle) is True
    
    def test_validate_adaptation(self):
        """Test adaptation validation."""
        # Test valid adaptation
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.BEGINNER
        )
        assert self.factory.validate_adaptation(adapted, ComplexityLevel.BEGINNER) is True
        
        # Test invalid adaptation (wrong level)
        assert self.factory.validate_adaptation(adapted, ComplexityLevel.EXPERT) is False
        
        # Test puzzle without adaptations
        unadapted = MockPuzzle()
        assert self.factory.validate_adaptation(unadapted, ComplexityLevel.BEGINNER) is False
    
    def test_get_adaptation_summary(self):
        """Test getting adaptation summary."""
        adapted = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.INTERMEDIATE
        )
        
        summary = self.factory.get_adaptation_summary(adapted)
        assert summary['complexity_level'] == 'INTERMEDIATE'
        assert summary['puzzle_id'] == 'test_puzzle'
        assert summary['puzzle_type'] == 'fact_creation'
        assert 'adaptations' in summary
        # Max score should not be changed by adaptation
        assert summary['max_score'] == 100  # Default max score
        assert summary['is_valid'] is True
        
        # Test puzzle without adaptations
        unadapted = MockPuzzle()
        summary = self.factory.get_adaptation_summary(unadapted)
        assert 'error' in summary
    
    def test_create_complexity_specific_puzzle(self):
        """Test creating complexity-specific puzzles."""
        # This method returns None for now (not implemented)
        result = self.factory.create_complexity_specific_puzzle(
            PuzzleType.FACT_CREATION,
            ComplexityLevel.BEGINNER
        )
        assert result is None
    
    def test_adaptation_parameters_consistency(self):
        """Test that adaptation parameters are consistent across levels."""
        for level in ComplexityLevel:
            adapted = self.factory.create_adapted_puzzle(self.mock_puzzle, level)
            params = adapted._adaptation_params
            
            # Check that all parameters are present
            assert 'max_variables' in params
            assert 'max_predicates' in params
            assert 'allow_complex_syntax' in params
            assert 'provide_templates' in params
            assert 'show_examples' in params
            
            # Check logical consistency
            if level == ComplexityLevel.BEGINNER:
                assert params['max_variables'] <= params['max_predicates']
                assert params['provide_templates'] is True
            elif level == ComplexityLevel.EXPERT:
                assert params['max_variables'] >= 6
                assert params['provide_templates'] is False
    
    def test_multiple_adaptations_independence(self):
        """Test that multiple adaptations are independent."""
        adapted1 = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.BEGINNER
        )
        adapted2 = self.factory.create_adapted_puzzle(
            self.mock_puzzle, 
            ComplexityLevel.EXPERT
        )
        
        # Should have different parameters
        assert adapted1._adaptation_params != adapted2._adaptation_params
        assert adapted1.get_complexity_level() != adapted2.get_complexity_level()
        # Max scores should be the same (not modified by adaptation)
        assert adapted1.max_score == adapted2.max_score
        
        # Should not affect each other
        adapted1._adaptation_params['test_param'] = 'test_value'
        assert 'test_param' not in adapted2._adaptation_params


class TestAdaptivePuzzleFactoryIntegration:
    """Integration tests for the AdaptivePuzzleFactory."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.factory = AdaptivePuzzleFactory()
    
    def test_hello_world_puzzle_adaptation(self):
        """Test adaptation of the actual HelloWorldPuzzle."""
        try:
            from prologresurrected.game.hello_world_puzzle import HelloWorldPuzzle
            hello_world = HelloWorldPuzzle()
            
            # Test adaptation at different levels
            for level in ComplexityLevel:
                adapted = self.factory.create_adapted_puzzle(hello_world, level)
                assert adapted is not None
                assert adapted.get_complexity_level() == level
                assert self.factory.validate_adaptation(adapted, level) is True
                
        except ImportError:
            # HelloWorldPuzzle not available, skip test
            pytest.skip("HelloWorldPuzzle not available for integration test")
    
    def test_adaptation_with_complexity_manager(self):
        """Test that adaptations work correctly with ComplexityManager."""
        adapted = self.factory.create_adapted_puzzle(
            MockPuzzle(), 
            ComplexityLevel.ADVANCED
        )
        
        # Test that complexity-aware methods work
        hint = adapted.get_complexity_adapted_hint(1)
        assert hint is not None
        
        # Test complexity parameters
        params = adapted.get_complexity_parameters()
        assert params['max_variables'] == 6
        assert params['require_optimization'] is True