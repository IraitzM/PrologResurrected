"""
Unit tests for visual complexity indicators.

Tests the visual complexity indicator components and their integration
with the game state and UI.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.prologresurrected import GameState


class TestVisualComplexityIndicators:
    """Test suite for visual complexity indicators (Task 8)."""
    
    def test_complexity_icon_helper_method(self):
        """Test get_complexity_icon helper method returns correct icons."""
        state = GameState()
        
        # Test all complexity levels
        icons = {
            ComplexityLevel.BEGINNER: "🌱",
            ComplexityLevel.INTERMEDIATE: "⚡",
            ComplexityLevel.ADVANCED: "🔥",
            ComplexityLevel.EXPERT: "💀",
        }
        
        for level, expected_icon in icons.items():
            state.set_complexity_level(level)
            assert state.get_complexity_icon() == expected_icon
    
    def test_complexity_name_helper_method(self):
        """Test get_complexity_name helper method returns correct names."""
        state = GameState()
        
        # Test all complexity levels
        names = {
            ComplexityLevel.BEGINNER: "Beginner",
            ComplexityLevel.INTERMEDIATE: "Intermediate",
            ComplexityLevel.ADVANCED: "Advanced",
            ComplexityLevel.EXPERT: "Expert",
        }
        
        for level, expected_name in names.items():
            state.set_complexity_level(level)
            assert state.get_complexity_name() == expected_name
    
    def test_complexity_color_helper_method(self):
        """Test get_complexity_color helper method returns correct colors."""
        state = GameState()
        
        # Test all complexity levels
        colors = {
            ComplexityLevel.BEGINNER: "neon_green",
            ComplexityLevel.INTERMEDIATE: "cyan",
            ComplexityLevel.ADVANCED: "yellow",
            ComplexityLevel.EXPERT: "red",
        }
        
        for level, expected_color in colors.items():
            state.set_complexity_level(level)
            assert state.get_complexity_color() == expected_color
    
    def test_complexity_indicator_components_consistency(self):
        """Test that all indicator components are consistent with each other."""
        state = GameState()
        
        for level in ComplexityLevel:
            state.set_complexity_level(level)
            
            # Get all components
            icon = state.get_complexity_icon()
            name = state.get_complexity_name()
            color = state.get_complexity_color()
            indicator = state.get_complexity_indicator()
            
            # Verify they are all non-empty
            assert icon, f"Icon should not be empty for {level}"
            assert name, f"Name should not be empty for {level}"
            assert color, f"Color should not be empty for {level}"
            assert indicator, f"Indicator should not be empty for {level}"
            
            # Verify indicator contains icon and name
            assert icon in indicator, f"Indicator should contain icon for {level}"
            assert name.upper() in indicator, f"Indicator should contain name for {level}"
    
    def test_complexity_indicator_updates_immediately(self):
        """Test that complexity indicators update immediately when level changes (Requirement 6.2)."""
        state = GameState()
        
        # Start with beginner
        state.set_complexity_level(ComplexityLevel.BEGINNER)
        beginner_icon = state.get_complexity_icon()
        beginner_name = state.get_complexity_name()
        beginner_color = state.get_complexity_color()
        
        # Change to expert
        state.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Verify immediate update
        assert state.get_complexity_icon() != beginner_icon
        assert state.get_complexity_name() != beginner_name
        assert state.get_complexity_color() != beginner_color
        
        # Verify new values are correct
        assert state.get_complexity_icon() == "💀"
        assert state.get_complexity_name() == "Expert"
        assert state.get_complexity_color() == "red"
    
    def test_complexity_indicator_color_coding_consistency(self):
        """Test that color coding is consistent across all levels (Requirement 6.3)."""
        state = GameState()
        
        # Define expected color scheme
        expected_colors = {
            ComplexityLevel.BEGINNER: "neon_green",
            ComplexityLevel.INTERMEDIATE: "cyan",
            ComplexityLevel.ADVANCED: "yellow",
            ComplexityLevel.EXPERT: "red",
        }
        
        for level, expected_color in expected_colors.items():
            state.set_complexity_level(level)
            actual_color = state.get_complexity_color()
            
            assert actual_color == expected_color, \
                f"Color for {level.name} should be {expected_color}, got {actual_color}"
    
    def test_complexity_indicator_in_terminal_context(self):
        """Test that complexity indicator works in terminal/game context."""
        state = GameState()
        
        # Set up game mode
        state.game_mode = "adventure"
        state.current_screen = "adventure"
        
        # Test different levels
        for level in ComplexityLevel:
            state.set_complexity_level(level)
            
            # Verify indicator components are available
            icon = state.get_complexity_icon()
            name = state.get_complexity_name()
            color = state.get_complexity_color()
            
            assert icon
            assert name
            assert color
    
    def test_complexity_indicator_badge_components(self):
        """Test that badge components have all required information."""
        state = GameState()
        
        for level in ComplexityLevel:
            state.set_complexity_level(level)
            
            # Get badge components
            icon = state.get_complexity_icon()
            name = state.get_complexity_name()
            color = state.get_complexity_color()
            
            # Verify icon is an emoji
            assert len(icon) > 0
            
            # Verify name is capitalized properly
            assert name[0].isupper()
            
            # Verify color is a valid color name
            assert color in ["neon_green", "cyan", "yellow", "red", "neon_cyan", "neon_yellow", "neon_red"]
    
    def test_complexity_indicator_persistence_across_changes(self):
        """Test that indicator updates persist across multiple changes."""
        state = GameState()
        
        # Make multiple changes
        changes = [
            ComplexityLevel.BEGINNER,
            ComplexityLevel.EXPERT,
            ComplexityLevel.INTERMEDIATE,
            ComplexityLevel.ADVANCED,
        ]
        
        for level in changes:
            state.set_complexity_level(level)
            
            # Verify indicator reflects current level
            config = state.complexity_manager.get_current_config()
            assert state.get_complexity_icon() == config.ui_indicators["icon"]
            assert state.get_complexity_name() == config.name
            assert state.get_complexity_color() == config.ui_indicators["color"]
    
    def test_complexity_indicator_available_from_start(self):
        """Test that complexity indicators are available from game start."""
        state = GameState()
        
        # Even with default state, indicators should be available
        assert state.get_complexity_icon() == "🌱"  # Default is BEGINNER
        assert state.get_complexity_name() == "Beginner"
        assert state.get_complexity_color() == "neon_green"
    
    def test_complexity_indicator_in_welcome_screen_context(self):
        """Test that complexity indicator works in welcome screen context."""
        state = GameState()
        
        # Welcome screen should show current complexity
        state.current_screen = "welcome"
        
        # Test indicator is available
        indicator = state.get_complexity_indicator()
        icon = state.get_complexity_icon()
        name = state.get_complexity_name()
        color = state.get_complexity_color()
        
        assert indicator
        assert icon in indicator
        assert name.upper() in indicator
        assert color
