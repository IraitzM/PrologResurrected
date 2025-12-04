"""
Unit tests for GameState complexity level integration.

Tests the integration of complexity level management within the GameState class,
including state persistence, level changes, and UI indicator updates.
"""

import pytest
from prologresurrected.prologresurrected import GameState
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager


class TestGameStateComplexityIntegration:
    """Test complexity level integration in GameState."""

    def setup_method(self):
        """Set up test fixtures."""
        self.game_state = GameState()

    def test_default_complexity_level(self):
        """Test that GameState initializes with BEGINNER complexity level."""
        assert self.game_state.complexity_level == ComplexityLevel.BEGINNER
        assert self.game_state.get_complexity_level() == ComplexityLevel.BEGINNER

    def test_complexity_selection_shown_default(self):
        """Test that complexity selection shown flag defaults to False."""
        assert self.game_state.complexity_selection_shown is False

    def test_complexity_change_count_default(self):
        """Test that complexity change count defaults to 0."""
        assert self.game_state.complexity_change_count == 0

    def test_set_complexity_level_valid(self):
        """Test setting a valid complexity level."""
        self.game_state.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.game_state.complexity_level == ComplexityLevel.ADVANCED
        assert self.game_state.get_complexity_level() == ComplexityLevel.ADVANCED

    def test_set_complexity_level_invalid(self):
        """Test setting an invalid complexity level falls back to BEGINNER."""
        # Invalid input should fall back to BEGINNER level
        self.game_state.set_complexity_level("invalid")
        # Should fall back to BEGINNER
        assert self.game_state.complexity_level == ComplexityLevel.BEGINNER

    def test_set_complexity_level_updates_manager(self):
        """Test that setting complexity level updates the complexity manager."""
        self.game_state.set_complexity_level(ComplexityLevel.EXPERT)
        assert self.game_state.complexity_manager.get_current_level() == ComplexityLevel.EXPERT

    def test_complexity_change_count_tracking(self):
        """Test that complexity changes are tracked correctly."""
        # Initial state
        assert self.game_state.complexity_change_count == 0
        
        # First change
        self.game_state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert self.game_state.complexity_change_count == 1
        
        # Second change
        self.game_state.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.game_state.complexity_change_count == 2
        
        # Setting same level doesn't increment
        self.game_state.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.game_state.complexity_change_count == 2

    def test_show_complexity_selection(self):
        """Test marking complexity selection as shown."""
        assert self.game_state.complexity_selection_shown is False
        self.game_state.show_complexity_selection()
        assert self.game_state.complexity_selection_shown is True

    def test_handle_complexity_change_tracking(self):
        """Test that handle_complexity_change properly tracks changes."""
        initial_count = self.game_state.complexity_change_count
        self.game_state.handle_complexity_change(ComplexityLevel.INTERMEDIATE)
        
        assert self.game_state.complexity_level == ComplexityLevel.INTERMEDIATE
        assert self.game_state.complexity_change_count == initial_count + 1

    def test_handle_complexity_change_in_tutorial_mode(self):
        """Test complexity change handling during tutorial mode."""
        self.game_state.game_mode = "tutorial"
        self.game_state.terminal_output = []
        
        self.game_state.handle_complexity_change(ComplexityLevel.ADVANCED)
        
        # Check that confirmation messages were added
        assert len(self.game_state.terminal_output) >= 2
        assert "Complexity level changed to Advanced" in self.game_state.terminal_output[0]

    def test_handle_complexity_change_in_adventure_mode(self):
        """Test complexity change handling during adventure mode."""
        self.game_state.game_mode = "adventure"
        self.game_state.terminal_output = []
        
        self.game_state.handle_complexity_change(ComplexityLevel.EXPERT)
        
        # Check that confirmation messages were added
        assert len(self.game_state.terminal_output) >= 2
        assert "Complexity level changed to Expert" in self.game_state.terminal_output[0]

    def test_handle_complexity_change_in_menu_mode(self):
        """Test complexity change handling during menu mode (no terminal output)."""
        self.game_state.game_mode = "menu"
        self.game_state.terminal_output = []
        
        self.game_state.handle_complexity_change(ComplexityLevel.INTERMEDIATE)
        
        # Should not add terminal output in menu mode
        assert len(self.game_state.terminal_output) == 0
        # But should still change the level
        assert self.game_state.complexity_level == ComplexityLevel.INTERMEDIATE

    def test_get_complexity_indicator(self):
        """Test getting complexity indicator string."""
        # Test default (BEGINNER)
        indicator = self.game_state.get_complexity_indicator()
        assert "BEGINNER" in indicator
        assert "🌱" in indicator
        
        # Test ADVANCED
        self.game_state.set_complexity_level(ComplexityLevel.ADVANCED)
        indicator = self.game_state.get_complexity_indicator()
        assert "ADVANCED" in indicator
        assert "🔥" in indicator

    def test_get_complexity_color(self):
        """Test getting complexity level color."""
        # Test default (BEGINNER)
        color = self.game_state.get_complexity_color()
        assert color == "neon_green"
        
        # Test EXPERT
        self.game_state.set_complexity_level(ComplexityLevel.EXPERT)
        color = self.game_state.get_complexity_color()
        assert color == "red"

    def test_complexity_manager_property_lazy_initialization(self):
        """Test that complexity manager is lazily initialized."""
        # Access the property
        manager = self.game_state.complexity_manager
        assert isinstance(manager, ComplexityManager)
        
        # Should return the same instance on subsequent calls
        assert self.game_state.complexity_manager is manager

    def test_complexity_manager_syncs_with_state(self):
        """Test that complexity manager syncs with GameState level."""
        # Change state level first
        self.game_state.complexity_level = ComplexityLevel.INTERMEDIATE
        
        # Access manager (should sync with state)
        manager = self.game_state.complexity_manager
        assert manager.get_current_level() == ComplexityLevel.INTERMEDIATE

    def test_complexity_persistence_across_mode_changes(self):
        """Test that complexity level persists across game mode changes."""
        # Set complexity level
        self.game_state.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Change game modes
        self.game_state.game_mode = "tutorial"
        assert self.game_state.get_complexity_level() == ComplexityLevel.ADVANCED
        
        self.game_state.game_mode = "adventure"
        assert self.game_state.get_complexity_level() == ComplexityLevel.ADVANCED
        
        self.game_state.game_mode = "menu"
        assert self.game_state.get_complexity_level() == ComplexityLevel.ADVANCED

    def test_all_complexity_levels_supported(self):
        """Test that all complexity levels can be set and retrieved."""
        for level in ComplexityLevel:
            self.game_state.set_complexity_level(level)
            assert self.game_state.get_complexity_level() == level
            assert self.game_state.complexity_manager.get_current_level() == level

    def test_complexity_indicator_updates_right_panel(self):
        """Test that complexity changes update the right panel."""
        self.game_state.game_mode = "tutorial"
        
        # Change complexity level
        self.game_state.handle_complexity_change(ComplexityLevel.EXPERT)
        
        # Check that right panel was updated with complexity info
        assert "COMPLEXITY" in self.game_state.right_panel_title
        assert "EXPERT" in self.game_state.right_panel_content
        assert "💀" in self.game_state.right_panel_content  # Expert icon
        assert self.game_state.right_panel_color == "red"  # Expert color

    def test_complexity_change_count_in_right_panel(self):
        """Test that complexity change count is displayed in right panel."""
        self.game_state.game_mode = "adventure"
        
        # Make several changes
        self.game_state.handle_complexity_change(ComplexityLevel.INTERMEDIATE)
        self.game_state.handle_complexity_change(ComplexityLevel.ADVANCED)
        
        # Check that change count is displayed
        assert "Changes Made: 2" in self.game_state.right_panel_content

    def test_complexity_state_isolation(self):
        """Test that complexity state changes don't affect other game state."""
        # Store initial values
        initial_score = self.game_state.player_score
        initial_level = self.game_state.player_level
        initial_concepts = self.game_state.concepts_learned.copy()
        
        # Change complexity
        self.game_state.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Verify other state unchanged
        assert self.game_state.player_score == initial_score
        assert self.game_state.player_level == initial_level
        assert self.game_state.concepts_learned == initial_concepts

    def test_complexity_manager_configuration_access(self):
        """Test accessing complexity configuration through GameState."""
        self.game_state.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Access configuration through the manager
        config = self.game_state.complexity_manager.get_current_config()
        assert config.name == "Intermediate"
        assert config.scoring_multiplier == 1.2
        
        # Test puzzle parameters access
        params = self.game_state.complexity_manager.get_puzzle_parameters()
        assert params["max_variables"] == 4
        assert params["max_predicates"] == 5