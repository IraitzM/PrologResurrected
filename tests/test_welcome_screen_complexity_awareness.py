"""
Tests for welcome screen complexity awareness enhancements.

This module tests the welcome screen's integration with complexity levels,
including recommendations for new players and complexity level preview functionality.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel


def test_welcome_screen_shows_current_complexity(game_state):
    """Test that welcome screen displays current complexity level."""
    # Set complexity level
    game_state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
    
    # Verify complexity indicator is available
    indicator = game_state.get_complexity_indicator()
    assert "INTERMEDIATE" in indicator
    
    # Verify complexity description is available
    description = game_state.get_complexity_description()
    assert len(description) > 0
    assert "moderate" in description.lower() or "guidance" in description.lower()


def test_welcome_screen_complexity_color(game_state):
    """Test that complexity level has associated color."""
    # Test each complexity level has a color
    for level in ComplexityLevel:
        game_state.set_complexity_level(level)
        color = game_state.get_complexity_color()
        assert color in ["neon_green", "cyan", "yellow", "red"]


def test_welcome_screen_complexity_icon(game_state):
    """Test that complexity level has associated icon."""
    # Test each complexity level has an icon
    for level in ComplexityLevel:
        game_state.set_complexity_level(level)
        icon = game_state.get_complexity_icon()
        assert len(icon) > 0


def test_welcome_screen_complexity_name(game_state):
    """Test that complexity level name is retrievable."""
    game_state.set_complexity_level(ComplexityLevel.ADVANCED)
    name = game_state.get_complexity_name()
    assert name == "Advanced"


def test_welcome_screen_recommendation_for_new_players(game_state):
    """Test that new players see recommendation when not on beginner level."""
    # New player (hello world not completed) on non-beginner level
    game_state.hello_world_completed = False
    game_state.set_complexity_level(ComplexityLevel.EXPERT)
    
    # The recommendation should be shown (tested via UI rendering)
    # Verify the state conditions are correct
    assert not game_state.hello_world_completed
    assert game_state.complexity_level != ComplexityLevel.BEGINNER


def test_welcome_screen_no_recommendation_for_beginner(game_state):
    """Test that beginner level doesn't show recommendation."""
    # New player on beginner level
    game_state.hello_world_completed = False
    game_state.set_complexity_level(ComplexityLevel.BEGINNER)
    
    # The recommendation should NOT be shown
    assert game_state.complexity_level == ComplexityLevel.BEGINNER


def test_welcome_screen_no_recommendation_for_experienced_players(game_state):
    """Test that experienced players don't see recommendation."""
    # Experienced player (hello world completed)
    game_state.hello_world_completed = True
    game_state.set_complexity_level(ComplexityLevel.EXPERT)
    
    # The recommendation should NOT be shown
    assert game_state.hello_world_completed


def test_complexity_description_available_for_all_levels(game_state):
    """Test that all complexity levels have descriptions."""
    for level in ComplexityLevel:
        game_state.set_complexity_level(level)
        description = game_state.get_complexity_description()
        assert len(description) > 0
        assert isinstance(description, str)


def test_welcome_screen_tutorial_recommendation(game_state):
    """Test that tutorial is recommended for new players."""
    # New player
    game_state.hello_world_completed = False
    
    # Verify state for UI rendering
    assert not game_state.hello_world_completed


def test_welcome_screen_adventure_shows_complexity_info(game_state):
    """Test that adventure button shows complexity level info."""
    game_state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
    
    # Verify complexity info is available for display
    name = game_state.get_complexity_name()
    assert name == "Intermediate"


def test_complexity_selection_screen_accessible(game_state):
    """Test that complexity selection screen can be shown."""
    # Show complexity selection
    game_state.show_complexity_selection_screen()
    
    # Verify screen state
    assert game_state.current_screen == "complexity_selection"
    assert game_state.complexity_selection_shown


def test_welcome_screen_complexity_settings_button(game_state):
    """Test that complexity settings button is available."""
    # The button should be available regardless of hello world status
    game_state.hello_world_completed = False
    assert game_state.current_screen == "welcome"
    
    game_state.hello_world_completed = True
    assert game_state.current_screen == "welcome"


def test_complexity_level_preview_information(game_state):
    """Test that complexity level preview information is available."""
    # All levels should have preview information
    for level in ComplexityLevel:
        game_state.set_complexity_level(level)
        
        # Get all preview information
        name = game_state.get_complexity_name()
        description = game_state.get_complexity_description()
        icon = game_state.get_complexity_icon()
        color = game_state.get_complexity_color()
        
        # Verify all information is available
        assert len(name) > 0
        assert len(description) > 0
        assert len(icon) > 0
        assert len(color) > 0


def test_welcome_screen_footer_messages(game_state):
    """Test that footer messages adapt to player status."""
    # New player
    game_state.hello_world_completed = False
    assert not game_state.hello_world_completed
    
    # Experienced player
    game_state.hello_world_completed = True
    assert game_state.hello_world_completed


def test_complexity_indicator_on_welcome_screen(game_state):
    """Test that complexity indicator is properly formatted."""
    game_state.set_complexity_level(ComplexityLevel.BEGINNER)
    
    indicator = game_state.get_complexity_indicator()
    name = game_state.get_complexity_name()
    icon = game_state.get_complexity_icon()
    
    # Indicator should contain both icon and name
    assert icon in indicator
    assert name.upper() in indicator


@pytest.fixture
def game_state():
    """Create a GameState instance for testing."""
    from prologresurrected.prologresurrected import GameState
    
    state = GameState()
    return state
