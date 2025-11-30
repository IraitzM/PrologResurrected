"""
Unit tests for mid-game complexity level change functionality.

Tests the ability to change complexity levels during gameplay with
confirmation dialogs and progress preservation.
"""

import pytest
from prologresurrected.prologresurrected import GameState
from prologresurrected.game.complexity import ComplexityLevel


class TestComplexityChangeFunctionality:
    """Test suite for complexity level change during gameplay."""

    def setup_method(self):
        """Set up test fixtures."""
        self.state = GameState()

    def test_complexity_command_shows_menu(self):
        """Test that 'complexity' command shows the complexity change menu."""
        # Start adventure mode
        self.state.game_mode = "adventure"
        self.state.current_screen = "adventure"
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Type 'complexity' command
        self.state._handle_adventure_input("complexity")
        
        # Verify menu is shown
        output_text = " ".join(self.state.terminal_output)
        assert "COMPLEXITY LEVEL SELECTION" in output_text
        assert "Available Complexity Levels:" in output_text
        assert "BEGINNER" in output_text
        assert "INTERMEDIATE" in output_text
        assert "ADVANCED" in output_text
        assert "EXPERT" in output_text

    def test_complexity_change_requires_confirmation(self):
        """Test that changing complexity level requires confirmation."""
        self.state.game_mode = "adventure"
        self.state.current_screen = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Show complexity menu
        self.state._show_complexity_change_menu()
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Select a different level
        self.state._handle_complexity_change_input("advanced")
        
        # Verify confirmation is requested
        output_text = " ".join(self.state.terminal_output)
        assert "CONFIRM COMPLEXITY CHANGE" in output_text
        assert "Type 'yes' to confirm or 'no' to cancel" in output_text
        assert self.state.awaiting_complexity_confirmation is True
        assert self.state.pending_complexity_change == "advanced"

    def test_complexity_change_confirmation_yes(self):
        """Test confirming complexity level change."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        self.state.player_score = 100
        self.state.player_level = 2
        self.state.concepts_learned = ["facts", "queries"]
        
        # Set up pending change
        self.state.pending_complexity_change = "expert"
        self.state.awaiting_complexity_confirmation = True
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Confirm the change
        self.state._handle_complexity_confirmation("yes")
        
        # Verify change was applied
        assert self.state.complexity_level == ComplexityLevel.EXPERT
        assert self.state.awaiting_complexity_confirmation is False
        assert self.state.pending_complexity_change == ""
        
        # Verify progress was preserved
        assert self.state.player_score == 100
        assert self.state.player_level == 2
        assert self.state.concepts_learned == ["facts", "queries"]
        
        # Verify confirmation message
        output_text = " ".join(self.state.terminal_output)
        assert "Complexity level changed successfully" in output_text
        assert "progress has been preserved" in output_text

    def test_complexity_change_confirmation_no(self):
        """Test cancelling complexity level change."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Set up pending change
        self.state.pending_complexity_change = "expert"
        self.state.awaiting_complexity_confirmation = True
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Cancel the change
        self.state._handle_complexity_confirmation("no")
        
        # Verify change was not applied
        assert self.state.complexity_level == ComplexityLevel.BEGINNER
        assert self.state.awaiting_complexity_confirmation is False
        assert self.state.pending_complexity_change == ""
        
        # Verify cancellation message
        output_text = " ".join(self.state.terminal_output)
        assert "Complexity change cancelled" in output_text

    def test_complexity_change_preserves_progress(self):
        """Test that complexity change preserves player progress and score."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Set up game state with progress
        self.state.player_score = 500
        self.state.player_level = 3
        self.state.concepts_learned = ["facts", "queries", "rules"]
        
        # Perform complexity change
        self.state.pending_complexity_change = "intermediate"
        self.state.awaiting_complexity_confirmation = True
        self.state._handle_complexity_confirmation("yes")
        
        # Verify all progress is preserved
        assert self.state.player_score == 500
        assert self.state.player_level == 3
        assert self.state.concepts_learned == ["facts", "queries", "rules"]
        assert self.state.complexity_level == ComplexityLevel.INTERMEDIATE

    def test_complexity_change_displays_confirmation_message(self):
        """Test that complexity change displays a confirmation message."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Perform complexity change
        self.state.handle_complexity_change(ComplexityLevel.ADVANCED)
        
        # Verify confirmation message is displayed
        output_text = " ".join(self.state.terminal_output)
        assert "Complexity level changed to" in output_text
        assert "ADVANCED" in output_text or "Advanced" in output_text

    def test_complexity_change_same_level_rejected(self):
        """Test that changing to the same level is rejected."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.INTERMEDIATE
        
        # Show complexity menu
        self.state._show_complexity_change_menu()
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Try to select the same level
        self.state._handle_complexity_change_input("intermediate")
        
        # Verify rejection message
        output_text = " ".join(self.state.terminal_output)
        assert "already at" in output_text.lower()
        assert self.state.awaiting_complexity_confirmation is False

    def test_complexity_change_invalid_level(self):
        """Test handling of invalid complexity level input."""
        self.state.game_mode = "adventure"
        
        # Show complexity menu
        self.state._show_complexity_change_menu()
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Try invalid input
        self.state._handle_complexity_change_input("invalid")
        
        # Verify error message
        output_text = " ".join(self.state.terminal_output)
        assert "Invalid complexity level" in output_text

    def test_complexity_change_cancel(self):
        """Test cancelling complexity change from menu."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Show complexity menu
        self.state._show_complexity_change_menu()
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Cancel
        self.state._handle_complexity_change_input("cancel")
        
        # Verify cancellation
        assert self.state.awaiting_complexity_confirmation is False
        assert self.state.pending_complexity_change == ""
        output_text = " ".join(self.state.terminal_output)
        assert "cancelled" in output_text.lower()

    def test_complexity_change_in_tutorial_mode(self):
        """Test that complexity change works in tutorial mode."""
        self.state.game_mode = "tutorial"
        self.state.tutorial_active = True
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Type 'complexity' command
        self.state._handle_tutorial_input("complexity")
        
        # Verify menu is shown
        output_text = " ".join(self.state.terminal_output)
        assert "COMPLEXITY LEVEL SELECTION" in output_text

    def test_complexity_change_updates_indicator(self):
        """Test that complexity change updates the UI indicator."""
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Get initial indicator
        initial_indicator = self.state.get_complexity_indicator()
        assert "BEGINNER" in initial_indicator
        
        # Change complexity
        self.state.handle_complexity_change(ComplexityLevel.EXPERT)
        
        # Get new indicator
        new_indicator = self.state.get_complexity_indicator()
        assert "EXPERT" in new_indicator
        assert new_indicator != initial_indicator

    def test_complexity_change_count_tracking(self):
        """Test that complexity changes are tracked."""
        self.state.complexity_level = ComplexityLevel.BEGINNER
        initial_count = self.state.complexity_change_count
        
        # Change complexity multiple times
        self.state.handle_complexity_change(ComplexityLevel.INTERMEDIATE)
        assert self.state.complexity_change_count == initial_count + 1
        
        self.state.handle_complexity_change(ComplexityLevel.ADVANCED)
        assert self.state.complexity_change_count == initial_count + 2
        
        # Changing to same level should not increment
        self.state.handle_complexity_change(ComplexityLevel.ADVANCED)
        assert self.state.complexity_change_count == initial_count + 2

    def test_help_command_shows_complexity_option(self):
        """Test that help command includes complexity change option."""
        self.state.game_mode = "adventure"
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Type 'help' command
        self.state._handle_adventure_input("help")
        
        # Verify complexity option is shown
        output_text = " ".join(self.state.terminal_output)
        assert "complexity" in output_text.lower()

    def test_status_command_shows_complexity_level(self):
        """Test that status command shows current complexity level."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.ADVANCED
        
        # Clear terminal
        self.state.terminal_output = []
        
        # Type 'status' command
        self.state._handle_adventure_input("status")
        
        # Verify complexity level is shown
        output_text = " ".join(self.state.terminal_output)
        assert "CURRENT COMPLEXITY LEVEL" in output_text
        assert "ADVANCED" in output_text

    def test_complexity_change_flow_integration(self):
        """Test complete complexity change flow from start to finish."""
        self.state.game_mode = "adventure"
        self.state.complexity_level = ComplexityLevel.BEGINNER
        self.state.player_score = 250
        
        # Step 1: Show menu
        self.state._handle_adventure_input("complexity")
        assert "COMPLEXITY LEVEL SELECTION" in " ".join(self.state.terminal_output)
        
        # Step 2: Select level
        self.state.terminal_output = []
        self.state._handle_adventure_input("expert")
        assert "CONFIRM COMPLEXITY CHANGE" in " ".join(self.state.terminal_output)
        assert self.state.awaiting_complexity_confirmation is True
        
        # Step 3: Confirm
        self.state.terminal_output = []
        self.state._handle_adventure_input("yes")
        assert self.state.complexity_level == ComplexityLevel.EXPERT
        assert self.state.player_score == 250  # Progress preserved
        assert "successfully" in " ".join(self.state.terminal_output).lower()
        assert self.state.awaiting_complexity_confirmation is False


class TestComplexityChangeRequirements:
    """Test suite verifying requirements 2.1, 2.2, 2.3, 2.4."""

    def setup_method(self):
        """Set up test fixtures."""
        self.state = GameState()

    def test_requirement_2_1_menu_option_available(self):
        """
        Requirement 2.1: WHEN the player accesses the game menu 
        THEN the system SHALL provide an option to change complexity level.
        """
        self.state.game_mode = "adventure"
        self.state.terminal_output = []
        
        # Access help (game menu)
        self.state._handle_adventure_input("help")
        
        # Verify complexity option is available
        output_text = " ".join(self.state.terminal_output)
        assert "complexity" in output_text.lower()

    def test_requirement_2_2_new_level_applies_to_subsequent_puzzles(self):
        """
        Requirement 2.2: WHEN the player changes complexity level 
        THEN the system SHALL apply the new level to all subsequent puzzles.
        """
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Change complexity level
        self.state.handle_complexity_change(ComplexityLevel.EXPERT)
        
        # Verify new level is active
        assert self.state.get_complexity_level() == ComplexityLevel.EXPERT
        assert self.state.complexity_manager.get_current_level() == ComplexityLevel.EXPERT

    def test_requirement_2_3_confirmation_message_displayed(self):
        """
        Requirement 2.3: WHEN the complexity level is changed 
        THEN the system SHALL display a confirmation message indicating the change.
        """
        self.state.game_mode = "adventure"
        self.state.terminal_output = []
        
        # Change complexity level
        self.state.handle_complexity_change(ComplexityLevel.INTERMEDIATE)
        
        # Verify confirmation message
        output_text = " ".join(self.state.terminal_output)
        assert "Complexity level changed" in output_text
        assert "INTERMEDIATE" in output_text or "Intermediate" in output_text

    def test_requirement_2_4_progress_preserved(self):
        """
        Requirement 2.4: WHEN the complexity level is changed 
        THEN the system SHALL preserve the player's current progress and score.
        """
        # Set up game state with progress
        self.state.player_score = 750
        self.state.player_level = 4
        self.state.concepts_learned = ["facts", "queries", "rules", "unification"]
        self.state.complexity_level = ComplexityLevel.BEGINNER
        
        # Store original values
        original_score = self.state.player_score
        original_level = self.state.player_level
        original_concepts = self.state.concepts_learned.copy()
        
        # Change complexity level
        self.state.handle_complexity_change(ComplexityLevel.EXPERT)
        
        # Verify all progress is preserved
        assert self.state.player_score == original_score
        assert self.state.player_level == original_level
        assert self.state.concepts_learned == original_concepts
