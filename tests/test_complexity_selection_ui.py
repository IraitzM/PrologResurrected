"""
Tests for complexity level selection UI functionality.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.prologresurrected import GameState


def test_complexity_selection_screen_display():
    """Test that complexity selection screen can be shown."""
    state = GameState()
    
    # Initially should not be shown
    assert not state.complexity_selection_shown
    assert state.current_screen == "welcome"
    
    # Show complexity selection
    state.show_complexity_selection_screen()
    
    assert state.complexity_selection_shown
    assert state.current_screen == "complexity_selection"


def test_complexity_level_selection():
    """Test selecting different complexity levels."""
    state = GameState()
    
    # Test selecting each level
    test_cases = [
        ("BEGINNER", ComplexityLevel.BEGINNER),
        ("INTERMEDIATE", ComplexityLevel.INTERMEDIATE),
        ("ADVANCED", ComplexityLevel.ADVANCED),
        ("EXPERT", ComplexityLevel.EXPERT),
    ]
    
    for level_name, expected_level in test_cases:
        state.select_complexity_level(level_name)
        assert state.complexity_level == expected_level
        assert state.get_complexity_level() == expected_level


def test_complexity_level_invalid_selection():
    """Test handling of invalid complexity level selection."""
    state = GameState()
    original_level = state.complexity_level
    
    # Try to select invalid level
    state.select_complexity_level("INVALID")
    
    # Should remain unchanged
    assert state.complexity_level == original_level


def test_complexity_indicator():
    """Test complexity level indicator generation."""
    state = GameState()
    
    # Test indicator for different levels
    state.set_complexity_level(ComplexityLevel.BEGINNER)
    indicator = state.get_complexity_indicator()
    assert "BEGINNER" in indicator
    assert "🌱" in indicator
    
    state.set_complexity_level(ComplexityLevel.EXPERT)
    indicator = state.get_complexity_indicator()
    assert "EXPERT" in indicator
    assert "💀" in indicator


def test_complexity_color():
    """Test complexity level color retrieval."""
    state = GameState()
    
    # Test colors for different levels
    state.set_complexity_level(ComplexityLevel.BEGINNER)
    color = state.get_complexity_color()
    assert color == "neon_green"
    
    state.set_complexity_level(ComplexityLevel.EXPERT)
    color = state.get_complexity_color()
    assert color == "red"


def test_pending_action_flow():
    """Test the pending action flow for complexity selection."""
    state = GameState()
    
    # Simulate starting tutorial without complexity selection shown
    state.complexity_selection_shown = False
    state.start_tutorial()
    
    # Should show complexity selection and set pending action
    assert state.current_screen == "complexity_selection"
    assert state.pending_action == "tutorial"
    
    # Continue from complexity selection
    state.continue_from_complexity_selection()
    
    # Should start tutorial and clear pending action
    assert state.game_mode == "tutorial"
    assert state.pending_action == ""


def test_adventure_pending_action_flow():
    """Test the pending action flow for adventure mode."""
    state = GameState()
    
    # Simulate starting adventure without complexity selection shown
    state.complexity_selection_shown = False
    state.start_adventure()
    
    # Should show complexity selection and set pending action
    assert state.current_screen == "complexity_selection"
    assert state.pending_action == "adventure"
    
    # Continue from complexity selection
    state.continue_from_complexity_selection()
    
    # Should start adventure and clear pending action
    assert state.game_mode == "adventure"
    assert state.pending_action == ""


def test_complexity_selection_already_shown():
    """Test behavior when complexity selection has already been shown."""
    state = GameState()
    
    # Mark complexity selection as already shown
    state.complexity_selection_shown = True
    
    # Starting tutorial should go directly to tutorial
    state.start_tutorial()
    assert state.game_mode == "tutorial"
    assert state.current_screen == "tutorial"
    
    # Reset for adventure test
    state.return_to_menu()
    
    # Starting adventure should go directly to adventure
    state.start_adventure()
    assert state.game_mode == "adventure"
    assert state.current_screen == "adventure"


def test_complexity_change_tracking():
    """Test that complexity level changes are tracked."""
    state = GameState()
    
    initial_count = state.complexity_change_count
    
    # Change complexity level
    state.set_complexity_level(ComplexityLevel.ADVANCED)
    assert state.complexity_change_count == initial_count + 1
    
    # Change again
    state.set_complexity_level(ComplexityLevel.EXPERT)
    assert state.complexity_change_count == initial_count + 2
    
    # Setting to same level should not increment (only actual changes are tracked)
    state.set_complexity_level(ComplexityLevel.EXPERT)
    assert state.complexity_change_count == initial_count + 2


def test_complexity_icon_retrieval():
    """Test that complexity level icons are retrieved correctly."""
    state = GameState()
    
    # Test icons for different levels
    state.set_complexity_level(ComplexityLevel.BEGINNER)
    icon = state.get_complexity_icon()
    assert icon == "🌱"
    
    state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
    icon = state.get_complexity_icon()
    assert icon == "⚡"
    
    state.set_complexity_level(ComplexityLevel.ADVANCED)
    icon = state.get_complexity_icon()
    assert icon == "🔥"
    
    state.set_complexity_level(ComplexityLevel.EXPERT)
    icon = state.get_complexity_icon()
    assert icon == "💀"


def test_complexity_name_retrieval():
    """Test that complexity level names are retrieved correctly."""
    state = GameState()
    
    # Test names for different levels
    state.set_complexity_level(ComplexityLevel.BEGINNER)
    name = state.get_complexity_name()
    assert name == "Beginner"
    
    state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
    name = state.get_complexity_name()
    assert name == "Intermediate"
    
    state.set_complexity_level(ComplexityLevel.ADVANCED)
    name = state.get_complexity_name()
    assert name == "Advanced"
    
    state.set_complexity_level(ComplexityLevel.EXPERT)
    name = state.get_complexity_name()
    assert name == "Expert"


def test_complexity_indicator_consistency():
    """Test that all complexity indicator components are consistent."""
    state = GameState()
    
    # Test consistency for each level
    for level in [ComplexityLevel.BEGINNER, ComplexityLevel.INTERMEDIATE, 
                  ComplexityLevel.ADVANCED, ComplexityLevel.EXPERT]:
        state.set_complexity_level(level)
        
        # Get all indicator components
        icon = state.get_complexity_icon()
        name = state.get_complexity_name()
        color = state.get_complexity_color()
        indicator = state.get_complexity_indicator()
        
        # Verify consistency
        assert icon in indicator
        assert name.upper() in indicator
        assert icon != ""
        assert name != ""
        assert color != ""


def test_complexity_indicator_updates_on_change():
    """Test that complexity indicators update when level changes."""
    state = GameState()
    
    # Start with beginner
    state.set_complexity_level(ComplexityLevel.BEGINNER)
    beginner_icon = state.get_complexity_icon()
    beginner_name = state.get_complexity_name()
    beginner_color = state.get_complexity_color()
    
    # Change to expert
    state.set_complexity_level(ComplexityLevel.EXPERT)
    expert_icon = state.get_complexity_icon()
    expert_name = state.get_complexity_name()
    expert_color = state.get_complexity_color()
    
    # Verify they are different
    assert beginner_icon != expert_icon
    assert beginner_name != expert_name
    assert beginner_color != expert_color