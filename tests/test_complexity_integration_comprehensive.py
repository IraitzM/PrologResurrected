"""
Comprehensive integration tests for adaptive complexity levels feature.

Tests complete complexity level flows including:
- End-to-end complexity level selection and gameplay (Requirement 1.1)
- Complexity level changes during active gameplay (Requirement 2.1)
- Educational objectives met at all complexity levels (Requirement 3.1)
- UI complexity indicators throughout the system (Requirement 6.1)
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.puzzles import PuzzleManager, SimpleFactPuzzle
from prologresurrected.game.story import StoryEngine
from prologresurrected.game.adaptive_puzzle_factory import AdaptivePuzzleFactory
from prologresurrected.game.hello_world_puzzle import HelloWorldPuzzle


class TestCompleteComplexityFlows:
    """Test complete end-to-end complexity level flows (Requirement 1.1)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.complexity_manager = ComplexityManager()
        self.puzzle_manager = PuzzleManager()
        self.story_engine = StoryEngine()
        self.factory = AdaptivePuzzleFactory()
    
    def test_complete_beginner_flow(self):
        """Test complete game flow at beginner complexity level."""
        # Set beginner level
        self.complexity_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        self.story_engine.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Verify configuration
        config = self.complexity_manager.get_current_config()
        assert config.name == "Beginner"
        assert config.scoring_multiplier == 1.0
        assert config.hint_frequency.value == "always"
        
        # Register and start a puzzle
        puzzle = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(puzzle)
        self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
        
        # Verify puzzle is adapted for beginner
        current_puzzle = self.puzzle_manager.current_puzzle
        assert current_puzzle.get_complexity_level() == ComplexityLevel.BEGINNER
        assert hasattr(current_puzzle, '_adaptation_params')
        assert current_puzzle._adaptation_params['provide_templates'] is True
        assert current_puzzle._adaptation_params['show_examples'] is True
        
        # Verify hints are available
        hint = self.puzzle_manager.get_hint()
        assert hint is not None
        assert len(hint) > 0
        assert "Hints are not available" not in hint
        
        # Complete puzzle and verify scoring
        result = self.puzzle_manager.submit_solution("likes(alice, chocolate).")
        assert result.success is True
        assert result.score > 0
        
        # Verify story content is appropriate for beginners
        intro = self.story_engine.get_intro_story()
        assert intro is not None
        assert len(intro.content) > 0
    
    def test_complete_expert_flow(self):
        """Test complete game flow at expert complexity level."""
        # Set expert level
        self.complexity_manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.puzzle_manager.set_complexity_level(ComplexityLevel.EXPERT)
        self.story_engine.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Verify configuration
        config = self.complexity_manager.get_current_config()
        assert config.name == "Expert"
        assert config.scoring_multiplier == 2.0
        assert config.hint_frequency.value == "none"
        
        # Register and start a puzzle
        puzzle = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(puzzle)
        self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
        
        # Verify puzzle is adapted for expert
        current_puzzle = self.puzzle_manager.current_puzzle
        assert current_puzzle.get_complexity_level() == ComplexityLevel.EXPERT
        assert hasattr(current_puzzle, '_adaptation_params')
        assert current_puzzle._adaptation_params['require_optimization'] is True
        
        # Verify hints are not available
        hint = self.puzzle_manager.get_hint()
        assert "Hints are not available at Expert level" in hint
        
        # Complete puzzle and verify scoring multiplier
        result = self.puzzle_manager.submit_solution("likes(alice, chocolate).")
        assert result.success is True
        # Expert should have higher score due to 2.0x multiplier
        assert result.score > 0
    
    def test_all_complexity_levels_flow(self):
        """Test that all complexity levels work end-to-end."""
        puzzle = SimpleFactPuzzle()
        
        for level in ComplexityLevel:
            # Set complexity level
            self.complexity_manager.set_complexity_level(level)
            self.puzzle_manager.set_complexity_level(level)
            self.story_engine.set_complexity_level(level)
            
            # Register and start puzzle
            self.puzzle_manager.register_puzzle(puzzle)
            self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
            
            # Verify puzzle is adapted correctly
            current_puzzle = self.puzzle_manager.current_puzzle
            assert current_puzzle.get_complexity_level() == level
            
            # Verify configuration is loaded
            config = self.complexity_manager.get_current_config()
            assert config.name in ["Beginner", "Intermediate", "Advanced", "Expert"]
            
            # Verify story engine works
            intro = self.story_engine.get_intro_story()
            assert intro is not None
            
            # Complete puzzle
            result = self.puzzle_manager.submit_solution("likes(alice, chocolate).")
            assert result.success is True
            
            # Reset for next level
            self.puzzle_manager = PuzzleManager()


class TestComplexityChangeDuringGameplay:
    """Test complexity level changes during active gameplay (Requirement 2.1)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle_manager = PuzzleManager()
        self.complexity_manager = ComplexityManager()
    
    def test_complexity_change_preserves_progress(self):
        """Test that changing complexity preserves player progress."""
        # Start at beginner level
        self.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Register and start a puzzle
        puzzle = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(puzzle)
        self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
        
        # Make some progress
        self.puzzle_manager.submit_solution("wrong_answer")
        self.puzzle_manager.get_hint()
        
        # Record current state
        attempts_before = self.puzzle_manager.current_puzzle.attempts
        hints_before = self.puzzle_manager.current_puzzle.hints_used
        score_before = self.puzzle_manager.player_stats["total_score"]
        
        # Change complexity level
        self.puzzle_manager.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Verify progress is preserved
        assert self.puzzle_manager.current_puzzle.attempts == attempts_before
        assert self.puzzle_manager.current_puzzle.hints_used == hints_before
        assert self.puzzle_manager.player_stats["total_score"] == score_before
        
        # Verify new complexity is applied
        assert self.puzzle_manager.current_puzzle.get_complexity_level() == ComplexityLevel.ADVANCED
    
    def test_complexity_change_applies_to_future_puzzles(self):
        """Test that complexity changes apply to future puzzles."""
        # Start at beginner
        self.puzzle_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Complete a puzzle at beginner
        puzzle1 = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(puzzle1)
        self.puzzle_manager.start_puzzle(puzzle1.puzzle_id)
        result1 = self.puzzle_manager.submit_solution("likes(alice, chocolate).")
        assert result1.success is True
        
        # Change to expert
        self.puzzle_manager.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Start a new puzzle (reuse SimpleFactPuzzle with different ID)
        puzzle2 = SimpleFactPuzzle()
        # Manually change the puzzle ID to make it a "new" puzzle
        puzzle2.puzzle_id = "simple_fact_2"
        self.puzzle_manager.register_puzzle(puzzle2)
        self.puzzle_manager.start_puzzle(puzzle2.puzzle_id)
        
        # Verify new puzzle uses expert level
        assert self.puzzle_manager.current_puzzle.get_complexity_level() == ComplexityLevel.EXPERT
    
    def test_multiple_complexity_changes(self):
        """Test multiple complexity changes during gameplay."""
        puzzle = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(puzzle)
        
        # Change through all levels
        levels = [
            ComplexityLevel.BEGINNER,
            ComplexityLevel.INTERMEDIATE,
            ComplexityLevel.ADVANCED,
            ComplexityLevel.EXPERT,
            ComplexityLevel.BEGINNER  # Back to beginner
        ]
        
        for level in levels:
            self.puzzle_manager.set_complexity_level(level)
            self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
            
            # Verify level is applied
            assert self.puzzle_manager.current_puzzle.get_complexity_level() == level
            
            # Verify configuration matches
            config = self.puzzle_manager.complexity_manager.get_current_config()
            assert config.name == level.name.capitalize()
    
    def test_complexity_change_confirmation_message(self):
        """Test that complexity changes provide confirmation."""
        # Change complexity level
        old_level = self.complexity_manager.get_current_level()
        new_level = ComplexityLevel.ADVANCED
        
        self.complexity_manager.set_complexity_level(new_level)
        
        # Verify change was applied
        assert self.complexity_manager.get_current_level() == new_level
        assert self.complexity_manager.get_current_level() != old_level
        
        # Verify configuration is accessible
        config = self.complexity_manager.get_current_config()
        assert config.name == "Advanced"


class TestEducationalObjectivesAllLevels:
    """Test that educational objectives are met at all complexity levels (Requirement 3.1)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle_manager = PuzzleManager()
        self.story_engine = StoryEngine()
        self.hello_world = HelloWorldPuzzle()
    
    def test_core_concepts_covered_at_all_levels(self):
        """Test that core Prolog concepts are covered at all complexity levels."""
        core_concepts = ["facts", "queries", "variables", "prolog_basics"]
        
        for level in ComplexityLevel:
            # Set complexity level
            self.story_engine.set_complexity_level(level)
            
            # Complete hello world tutorial
            self.story_engine.mark_hello_world_completed()
            
            # Verify core concepts are learned
            progress = self.story_engine.get_player_progress()
            for concept in core_concepts:
                assert concept in progress["concepts_learned"], \
                    f"Concept '{concept}' not learned at {level.name} level"
            
            # Reset for next level
            self.story_engine = StoryEngine()
    
    def test_learning_objectives_maintained_across_levels(self):
        """Test that learning objectives are maintained regardless of complexity."""
        puzzle = SimpleFactPuzzle()
        
        for level in ComplexityLevel:
            # Set complexity level
            self.puzzle_manager.set_complexity_level(level)
            
            # Register and complete puzzle
            self.puzzle_manager.register_puzzle(puzzle)
            self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
            result = self.puzzle_manager.submit_solution("likes(alice, chocolate).")
            
            # Verify puzzle can be completed at all levels
            assert result.success is True, f"Puzzle failed at {level.name} level"
            
            # Verify concepts are tracked (SimpleFactPuzzle tracks "basic_prolog")
            stats = self.puzzle_manager.get_player_stats()
            assert "basic_prolog" in stats["concepts_mastered"]
            
            # Reset for next level
            self.puzzle_manager = PuzzleManager()
    
    def test_explanation_depth_adapts_to_level(self):
        """Test that explanation depth adapts while maintaining educational value."""
        for level in ComplexityLevel:
            self.story_engine.set_complexity_level(level)
            
            # Get story content
            intro = self.story_engine.get_intro_story()
            assert intro is not None
            assert len(intro.content) > 0
            
            # Verify content exists at all levels
            assert intro.title is not None
            assert len(intro.title) > 0
            
            # Content should be adapted but still present
            content_text = "\n".join(intro.content)
            assert len(content_text) > 0
    
    def test_hello_world_tutorial_works_at_all_levels(self):
        """Test that Hello World tutorial works at all complexity levels."""
        for level in ComplexityLevel:
            hello_world = HelloWorldPuzzle()
            hello_world.set_complexity_level(level)
            
            # Verify puzzle is initialized
            assert hello_world.puzzle_id == "hello_world_prolog"
            assert hello_world.get_complexity_level() == level
            
            # Verify core tutorial concepts are present
            assert hasattr(hello_world, 'title')
            # HelloWorldPuzzle has get_description method
            description = hello_world.get_description()
            assert description is not None and len(description) > 0
            
            # Tutorial should be completable at all levels
            assert hello_world.max_score > 0


class TestUIComplexityIndicators:
    """Test UI complexity indicators throughout the system (Requirement 6.1)."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.complexity_manager = ComplexityManager()
    
    def test_complexity_indicator_available_for_all_levels(self):
        """Test that UI indicators are available for all complexity levels."""
        for level in ComplexityLevel:
            config = self.complexity_manager.get_config(level)
            
            # Verify UI indicators exist
            assert "icon" in config.ui_indicators
            assert "color" in config.ui_indicators
            assert "badge" in config.ui_indicators
            
            # Verify indicators are not empty
            assert len(config.ui_indicators["icon"]) > 0
            assert len(config.ui_indicators["color"]) > 0
            assert len(config.ui_indicators["badge"]) > 0
    
    def test_complexity_indicator_consistency(self):
        """Test that complexity indicators are consistent."""
        expected_indicators = {
            ComplexityLevel.BEGINNER: {"icon": "🌱", "color": "neon_green", "badge": "BEGINNER"},
            ComplexityLevel.INTERMEDIATE: {"icon": "⚡", "color": "cyan", "badge": "INTERMEDIATE"},
            ComplexityLevel.ADVANCED: {"icon": "🔥", "color": "yellow", "badge": "ADVANCED"},
            ComplexityLevel.EXPERT: {"icon": "💀", "color": "red", "badge": "EXPERT"},
        }
        
        for level, expected in expected_indicators.items():
            config = self.complexity_manager.get_config(level)
            
            assert config.ui_indicators["icon"] == expected["icon"]
            assert config.ui_indicators["color"] == expected["color"]
            assert config.ui_indicators["badge"] == expected["badge"]
    
    def test_complexity_indicator_updates_on_change(self):
        """Test that indicators update when complexity changes."""
        # Start at beginner
        self.complexity_manager.set_complexity_level(ComplexityLevel.BEGINNER)
        beginner_config = self.complexity_manager.get_current_config()
        beginner_icon = beginner_config.ui_indicators["icon"]
        
        # Change to expert
        self.complexity_manager.set_complexity_level(ComplexityLevel.EXPERT)
        expert_config = self.complexity_manager.get_current_config()
        expert_icon = expert_config.ui_indicators["icon"]
        
        # Verify indicators changed
        assert beginner_icon != expert_icon
        assert beginner_icon == "🌱"
        assert expert_icon == "💀"
    
    def test_complexity_display_methods(self):
        """Test methods for displaying complexity information."""
        for level in ComplexityLevel:
            self.complexity_manager.set_complexity_level(level)
            
            # Test display methods
            name = self.complexity_manager.get_level_name(level)
            description = self.complexity_manager.get_level_description(level)
            indicators = self.complexity_manager.get_ui_indicators()
            
            # Verify all display information is available
            assert name is not None and len(name) > 0
            assert description is not None and len(description) > 0
            assert indicators is not None
            assert "icon" in indicators
            assert "color" in indicators


class TestComplexityIntegrationWithAllComponents:
    """Test complexity integration with all game components."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.complexity_manager = ComplexityManager()
        self.puzzle_manager = PuzzleManager()
        self.story_engine = StoryEngine()
        self.factory = AdaptivePuzzleFactory()
    
    def test_complexity_manager_puzzle_manager_integration(self):
        """Test integration between ComplexityManager and PuzzleManager."""
        # Set complexity in manager
        self.complexity_manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Set same level in puzzle manager
        self.puzzle_manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Verify both are synchronized
        assert self.complexity_manager.get_current_level() == ComplexityLevel.INTERMEDIATE
        assert self.puzzle_manager.complexity_manager.get_current_level() == ComplexityLevel.INTERMEDIATE
    
    def test_complexity_manager_story_engine_integration(self):
        """Test integration between ComplexityManager and StoryEngine."""
        for level in ComplexityLevel:
            self.complexity_manager.set_complexity_level(level)
            self.story_engine.set_complexity_level(level)
            
            # Verify story engine uses correct level
            intro = self.story_engine.get_intro_story()
            assert intro is not None
            
            # Story content should be available at all levels
            assert len(intro.content) > 0
    
    def test_complexity_factory_integration(self):
        """Test integration between complexity system and adaptive factory."""
        puzzle = SimpleFactPuzzle()
        
        for level in ComplexityLevel:
            # Create adapted puzzle
            adapted = self.factory.create_adapted_puzzle(puzzle, level)
            
            # Verify adaptation
            assert adapted.get_complexity_level() == level
            assert self.factory.validate_adaptation(adapted, level) is True
            
            # Verify adaptation summary
            summary = self.factory.get_adaptation_summary(adapted)
            assert summary["complexity_level"] == level.name
            assert summary["is_valid"] is True
    
    def test_end_to_end_complexity_flow_with_all_components(self):
        """Test complete end-to-end flow with all components integrated."""
        # Initialize all components at beginner level
        level = ComplexityLevel.BEGINNER
        self.complexity_manager.set_complexity_level(level)
        self.puzzle_manager.set_complexity_level(level)
        self.story_engine.set_complexity_level(level)
        
        # Get story intro
        intro = self.story_engine.get_intro_story()
        assert intro is not None
        
        # Create and start puzzle
        puzzle = SimpleFactPuzzle()
        self.puzzle_manager.register_puzzle(puzzle)
        self.puzzle_manager.start_puzzle(puzzle.puzzle_id)
        
        # Verify puzzle is adapted
        current_puzzle = self.puzzle_manager.current_puzzle
        assert current_puzzle.get_complexity_level() == level
        
        # Get hint (should be available at beginner)
        hint = self.puzzle_manager.get_hint()
        assert hint is not None
        assert "Hints are not available" not in hint
        
        # Complete puzzle
        result = self.puzzle_manager.submit_solution("likes(alice, chocolate).")
        assert result.success is True
        
        # Change complexity mid-game
        new_level = ComplexityLevel.EXPERT
        self.complexity_manager.set_complexity_level(new_level)
        self.puzzle_manager.set_complexity_level(new_level)
        self.story_engine.set_complexity_level(new_level)
        
        # Verify all components updated
        assert self.complexity_manager.get_current_level() == new_level
        assert self.puzzle_manager.complexity_manager.get_current_level() == new_level
        
        # Start new puzzle at expert level (reuse SimpleFactPuzzle)
        expert_puzzle = SimpleFactPuzzle()
        expert_puzzle.puzzle_id = "expert_fact_puzzle"
        self.puzzle_manager.register_puzzle(expert_puzzle)
        self.puzzle_manager.start_puzzle(expert_puzzle.puzzle_id)
        
        # Verify expert adaptations
        assert self.puzzle_manager.current_puzzle.get_complexity_level() == new_level
        
        # Hints should not be available at expert
        expert_hint = self.puzzle_manager.get_hint()
        assert "Hints are not available at Expert level" in expert_hint


class TestComplexityConfigurationLoading:
    """Test complexity configuration loading and validation."""
    
    def test_configuration_loads_for_all_levels(self):
        """Test that configurations load correctly for all levels."""
        manager = ComplexityManager()
        
        for level in ComplexityLevel:
            config = manager.get_config(level)
            
            # Verify all required fields are present
            assert config.name is not None
            assert config.description is not None
            assert config.hint_frequency is not None
            assert config.explanation_depth is not None
            assert config.puzzle_parameters is not None
            assert config.ui_indicators is not None
            assert config.scoring_multiplier > 0
    
    def test_configuration_parameters_are_valid(self):
        """Test that configuration parameters are valid."""
        manager = ComplexityManager()
        
        for level in ComplexityLevel:
            params = manager.get_puzzle_parameters(level)
            
            # Verify parameters exist
            assert "max_variables" in params
            assert "max_predicates" in params
            assert "allow_complex_syntax" in params
            assert "provide_templates" in params
            assert "show_examples" in params
            
            # Verify parameter values are reasonable
            assert params["max_variables"] > 0
            assert params["max_predicates"] > 0
            assert isinstance(params["allow_complex_syntax"], bool)
            assert isinstance(params["provide_templates"], bool)
            assert isinstance(params["show_examples"], bool)
    
    def test_scoring_multipliers_increase_with_difficulty(self):
        """Test that scoring multipliers increase with complexity level."""
        manager = ComplexityManager()
        
        beginner_mult = manager.get_scoring_multiplier(ComplexityLevel.BEGINNER)
        intermediate_mult = manager.get_scoring_multiplier(ComplexityLevel.INTERMEDIATE)
        advanced_mult = manager.get_scoring_multiplier(ComplexityLevel.ADVANCED)
        expert_mult = manager.get_scoring_multiplier(ComplexityLevel.EXPERT)
        
        # Verify multipliers increase
        assert beginner_mult < intermediate_mult
        assert intermediate_mult < advanced_mult
        assert advanced_mult < expert_mult
        
        # Verify specific values
        assert beginner_mult == 1.0
        assert expert_mult == 2.0
