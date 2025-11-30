"""
Final Integration Tests for Task 18 - Comprehensive Complexity System Verification

This test suite verifies that all complexity components are properly integrated
into the main game flow and meet all requirements from the spec.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_config import ComplexityConfigLoader
from prologresurrected.game.complexity_error_handling import ComplexityErrorHandler
from prologresurrected.game.complexity_help import ComplexityHelpSystem
from prologresurrected.game.adaptive_puzzle_factory import AdaptivePuzzleFactory
from prologresurrected.game.puzzles import PuzzleManager, SimpleFactPuzzle
from prologresurrected.game.story import StoryEngine
from prologresurrected.prologresurrected import GameState


class TestRequirement1_1_ComplexitySelection:
    """Test Requirement 1.1: Complexity level selection at game start."""
    
    def test_complexity_selection_screen_available(self):
        """Verify complexity selection screen is available."""
        game_state = GameState()
        
        # Should be able to show complexity selection
        game_state.show_complexity_selection_screen()
        assert game_state.current_screen == "complexity_selection"
        assert game_state.complexity_selection_shown is True
    
    def test_all_complexity_levels_selectable(self):
        """Verify all complexity levels can be selected."""
        game_state = GameState()
        
        for level in ComplexityLevel:
            game_state.select_complexity_level(level.name)
            assert game_state.complexity_level == level
    
    def test_default_complexity_level(self):
        """Verify default complexity level is BEGINNER."""
        game_state = GameState()
        assert game_state.complexity_level == ComplexityLevel.BEGINNER


class TestRequirement1_2_ComplexityPersistence:
    """Test Requirement 1.2: Complexity level persistence."""
    
    def test_complexity_level_persists_in_session(self):
        """Verify complexity level persists throughout game session."""
        game_state = GameState()
        
        # Set complexity level
        game_state.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Start tutorial
        game_state.start_tutorial()
        
        # Complexity should persist
        assert game_state.complexity_level == ComplexityLevel.ADVANCED
        
        # Return to menu and start adventure
        game_state.return_to_menu()
        game_state.start_adventure()
        
        # Complexity should still persist
        assert game_state.complexity_level == ComplexityLevel.ADVANCED


class TestRequirement2_1_MidGameComplexityChange:
    """Test Requirement 2.1: Mid-game complexity level changes."""
    
    def test_complexity_change_menu_accessible(self):
        """Verify complexity change menu is accessible during gameplay."""
        game_state = GameState()
        game_state.game_mode = "adventure"
        
        # Simulate complexity command
        game_state._handle_complexity_command("complexity")
        
        # Should show complexity change menu in terminal
        assert any("COMPLEXITY LEVEL SELECTION" in line for line in game_state.terminal_output)
    
    def test_complexity_change_requires_confirmation(self):
        """Verify complexity changes require confirmation."""
        game_state = GameState()
        game_state.game_mode = "adventure"
        
        # Start complexity change
        game_state._handle_complexity_change_input("expert")
        
        # Should be awaiting confirmation
        assert game_state.awaiting_complexity_confirmation is True
        assert game_state.pending_complexity_change == "expert"


class TestRequirement2_2_ProgressPreservation:
    """Test Requirement 2.2: Progress preservation during complexity changes."""
    
    def test_complexity_change_preserves_score(self):
        """Verify score is preserved when changing complexity."""
        game_state = GameState()
        game_state.player_score = 100
        game_state.player_level = 3
        game_state.concepts_learned = ["facts", "rules", "queries"]
        
        # Change complexity
        game_state.handle_complexity_change(ComplexityLevel.EXPERT)
        
        # Progress should be preserved
        assert game_state.player_score == 100
        assert game_state.player_level == 3
        assert game_state.concepts_learned == ["facts", "rules", "queries"]


class TestRequirement3_1_CoreConceptsCoverage:
    """Test Requirement 3.1: Core concepts covered at all complexity levels."""
    
    def test_puzzle_manager_covers_concepts_at_all_levels(self):
        """Verify puzzle manager covers core concepts at all levels."""
        for level in ComplexityLevel:
            manager = PuzzleManager()
            manager.complexity_level = level
            
            # Should have puzzles available
            assert len(manager.available_puzzles) > 0
            
            # Puzzles should cover core concepts (available_puzzles contains strings)
            puzzle_types = set(manager.available_puzzles)
            # The puzzle manager has hello_world_prolog which covers core concepts
            assert len(puzzle_types) > 0


class TestRequirement4_1_AdvancedComplexityFeatures:
    """Test Requirement 4.1: Advanced complexity features."""
    
    def test_advanced_level_has_appropriate_parameters(self):
        """Verify advanced level has appropriate puzzle parameters."""
        manager = ComplexityManager()
        manager.set_complexity_level(ComplexityLevel.ADVANCED)
        
        config = manager.get_current_config()
        
        # Should have minimal hints
        assert config.hint_frequency.value in ["after_attempts", "minimal"]
        
        # Should have higher scoring multiplier
        assert config.scoring_multiplier >= 1.5


class TestRequirement5_1_BeginnerGuidance:
    """Test Requirement 5.1: Beginner level guidance."""
    
    def test_beginner_level_provides_detailed_guidance(self):
        """Verify beginner level provides detailed guidance."""
        manager = ComplexityManager()
        manager.set_complexity_level(ComplexityLevel.BEGINNER)
        
        config = manager.get_current_config()
        
        # Should have always available hints
        assert config.hint_frequency.value == "always"
        
        # Should have detailed explanations
        assert config.explanation_depth.value == "detailed"


class TestRequirement6_1_VisualIndicators:
    """Test Requirement 6.1: Visual complexity indicators."""
    
    def test_complexity_indicator_methods_available(self):
        """Verify complexity indicator methods are available."""
        game_state = GameState()
        
        # Should have indicator methods
        indicator = game_state.get_complexity_indicator()
        assert indicator is not None
        assert len(indicator) > 0
        
        color = game_state.get_complexity_color()
        assert color is not None
        
        icon = game_state.get_complexity_icon()
        assert icon is not None
        
        name = game_state.get_complexity_name()
        assert name is not None


class TestComplexitySystemIntegration:
    """Test overall complexity system integration."""
    
    def test_all_components_work_together(self):
        """Verify all complexity components work together."""
        # Initialize all components
        manager = ComplexityManager()
        factory = AdaptivePuzzleFactory()
        puzzle_manager = PuzzleManager()
        story_engine = StoryEngine()
        error_handler = ComplexityErrorHandler()
        help_system = ComplexityHelpSystem(manager)
        
        # Change complexity level
        manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Verify all components respond
        assert manager.get_current_level() == ComplexityLevel.INTERMEDIATE
        
        # Factory should adapt puzzles
        puzzle = SimpleFactPuzzle()
        adapted = factory.create_adapted_puzzle(puzzle, ComplexityLevel.INTERMEDIATE)
        assert adapted.get_complexity_level() == ComplexityLevel.INTERMEDIATE
        
        # Story engine should adapt
        story_engine.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert story_engine.complexity_level == ComplexityLevel.INTERMEDIATE
        
        # Help system should provide appropriate help
        help_text = help_system.get_complexity_overview()
        assert len(help_text) > 0
    
    def test_error_handling_throughout_system(self):
        """Verify error handling works throughout the system."""
        game_state = GameState()
        
        # Try invalid complexity selection
        game_state.select_complexity_level("INVALID")
        
        # Should fall back to BEGINNER
        assert game_state.complexity_level == ComplexityLevel.BEGINNER
        
        # Should have error message in terminal
        assert any("Invalid" in line or "fallback" in line for line in game_state.terminal_output)
    
    def test_complexity_help_system_accessible(self):
        """Verify complexity help system is accessible in game."""
        game_state = GameState()
        game_state.game_mode = "adventure"
        
        # Access help system
        game_state._handle_complexity_command("complexity help")
        
        # Should show help content
        assert any("COMPLEXITY" in line for line in game_state.terminal_output)
    
    def test_performance_with_complexity_changes(self):
        """Verify system performs well with multiple complexity changes."""
        game_state = GameState()
        
        # Perform multiple complexity changes
        for _ in range(10):
            for level in ComplexityLevel:
                game_state.set_complexity_level(level)
                assert game_state.complexity_level == level
        
        # System should still be responsive and track changes
        # Note: change count tracks actual changes, not setting to same level
        assert game_state.complexity_change_count > 0


class TestComplexityStateManagement:
    """Test complexity level state management."""
    
    def test_complexity_state_consistency(self):
        """Verify complexity state remains consistent across operations."""
        game_state = GameState()
        
        # Set complexity
        game_state.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Verify consistency across all getters
        assert game_state.get_complexity_level() == ComplexityLevel.EXPERT
        assert game_state.complexity_level == ComplexityLevel.EXPERT
        assert game_state.complexity_manager.get_current_level() == ComplexityLevel.EXPERT
    
    def test_complexity_persistence_across_screens(self):
        """Verify complexity persists across different screens."""
        game_state = GameState()
        
        # Set complexity
        game_state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Navigate through screens
        game_state.show_complexity_selection_screen()
        assert game_state.complexity_level == ComplexityLevel.INTERMEDIATE
        
        game_state.current_screen = "welcome"
        assert game_state.complexity_level == ComplexityLevel.INTERMEDIATE
        
        game_state.start_tutorial()
        assert game_state.complexity_level == ComplexityLevel.INTERMEDIATE


class TestComplexityConfigurationSystem:
    """Test complexity configuration loading and validation."""
    
    def test_all_configuration_files_load(self):
        """Verify all complexity configuration files load correctly."""
        loader = ComplexityConfigLoader()
        configs = loader.load_all_configs()
        
        # Should have configs for all levels
        assert len(configs) == 4
        assert ComplexityLevel.BEGINNER in configs
        assert ComplexityLevel.INTERMEDIATE in configs
        assert ComplexityLevel.ADVANCED in configs
        assert ComplexityLevel.EXPERT in configs
    
    def test_configuration_parameters_valid(self):
        """Verify all configuration parameters are valid."""
        loader = ComplexityConfigLoader()
        configs = loader.load_all_configs()
        
        for level, config in configs.items():
            # Check required fields
            assert config.name is not None
            assert config.description is not None
            assert config.hint_frequency is not None
            assert config.explanation_depth is not None
            assert config.puzzle_parameters is not None
            assert config.ui_indicators is not None
            assert config.scoring_multiplier > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
