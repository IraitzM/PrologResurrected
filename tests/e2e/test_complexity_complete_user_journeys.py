"""
End-to-end tests for complete complexity level user journeys.

Tests complete user flows including:
- Complexity selection at game start
- Complexity changes during gameplay
- Visual indicators throughout the journey
- Educational progression at different levels
"""

import pytest
from playwright.sync_api import Page, expect


class TestComplexitySelectionUserJourney:
    """Test complete user journey with complexity selection (Requirement 1.1)."""
    
    def test_new_user_selects_complexity_before_tutorial(self, logic_quest_page: Page):
        """Test that new users select complexity before starting tutorial."""
        page = logic_quest_page
        
        # User arrives at welcome screen
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        
        # User clicks to start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Should show complexity selection screen
        expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
        
        # User sees all complexity options
        expect(page.locator("text=BEGINNER")).to_be_visible()
        expect(page.locator("text=INTERMEDIATE")).to_be_visible()
        expect(page.locator("text=ADVANCED")).to_be_visible()
        expect(page.locator("text=EXPERT")).to_be_visible()
        
        # User selects intermediate
        page.locator("text=INTERMEDIATE").first.click()
        page.wait_for_timeout(500)
        
        # User continues to tutorial
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Should now be in tutorial with intermediate complexity
        expect(page.locator("text=Starting Interactive Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=⚡")).to_be_visible()  # Intermediate icon
        expect(page.locator("text=Intermediate")).to_be_visible()
    
    def test_new_user_selects_complexity_before_adventure(self, logic_quest_page: Page):
        """Test that new users select complexity before starting adventure."""
        page = logic_quest_page
        
        # User clicks to start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Should show complexity selection screen
        expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
        
        # User selects advanced
        page.locator("text=ADVANCED").first.click()
        page.wait_for_timeout(500)
        
        # User continues to adventure
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Should now be in adventure with advanced complexity
        expect(page.locator("text=INITIALIZING LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=🔥")).to_be_visible()  # Advanced icon
        expect(page.locator("text=Advanced")).to_be_visible()
    
    def test_user_can_change_complexity_from_settings(self, logic_quest_page: Page):
        """Test that users can change complexity from settings."""
        page = logic_quest_page
        
        # User clicks complexity settings
        page.locator("text=Complexity Settings").click()
        page.wait_for_timeout(1000)
        
        # Should show complexity selection
        expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
        
        # User selects expert
        page.locator("text=EXPERT").first.click()
        page.wait_for_timeout(500)
        
        # User continues
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Should return to welcome screen with expert selected
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=💀")).to_be_visible()  # Expert icon
        expect(page.locator("text=Expert")).to_be_visible()


class TestComplexityChangeDuringGameplay:
    """Test complexity changes during active gameplay (Requirement 2.1)."""
    
    def test_user_changes_complexity_during_tutorial(self, logic_quest_page: Page):
        """Test changing complexity level during tutorial."""
        page = logic_quest_page
        
        # Start tutorial at beginner
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=BEGINNER").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Verify beginner indicator
        expect(page.locator("text=🌱")).to_be_visible()
        expect(page.locator("text=Beginner")).to_be_visible()
        
        # User types complexity command
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("complexity")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show complexity menu
        expect(page.locator("text=COMPLEXITY LEVEL SELECTION")).to_be_visible()
        
        # User selects advanced
        input_field.fill("advanced")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show confirmation
        expect(page.locator("text=CONFIRM COMPLEXITY CHANGE")).to_be_visible()
        
        # User confirms
        input_field.fill("yes")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show success message
        expect(page.locator("text=Complexity level changed successfully")).to_be_visible()
        
        # Verify advanced indicator
        expect(page.locator("text=🔥")).to_be_visible()
        expect(page.locator("text=Advanced")).to_be_visible()
    
    def test_user_changes_complexity_during_adventure(self, logic_quest_page: Page):
        """Test changing complexity level during adventure."""
        page = logic_quest_page
        
        # Start adventure at intermediate
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        page.locator("text=INTERMEDIATE").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Verify intermediate indicator
        expect(page.locator("text=⚡")).to_be_visible()
        
        # Change to expert
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("complexity")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        input_field.fill("expert")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        input_field.fill("yes")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Verify expert indicator
        expect(page.locator("text=💀")).to_be_visible()
        expect(page.locator("text=Expert")).to_be_visible()
    
    def test_user_cancels_complexity_change(self, logic_quest_page: Page):
        """Test canceling a complexity change."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=BEGINNER").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Start complexity change
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("complexity")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        input_field.fill("expert")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Cancel the change
        input_field.fill("no")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show cancellation message
        expect(page.locator("text=Complexity change cancelled")).to_be_visible()
        
        # Should still be at beginner
        expect(page.locator("text=🌱")).to_be_visible()
        expect(page.locator("text=Beginner")).to_be_visible()


class TestVisualComplexityIndicators:
    """Test visual complexity indicators throughout user journey (Requirement 6.1)."""
    
    def test_complexity_indicator_in_welcome_screen(self, logic_quest_page: Page):
        """Test complexity indicator on welcome screen."""
        page = logic_quest_page
        
        # Should show current complexity
        expect(page.locator("text=Current Complexity:")).to_be_visible()
        expect(page.locator("text=🌱")).to_be_visible()  # Default beginner
        expect(page.locator("text=Beginner")).to_be_visible()
    
    def test_complexity_indicator_in_terminal_header(self, logic_quest_page: Page):
        """Test complexity indicator in terminal header."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=INTERMEDIATE").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Check terminal header
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=⚡")).to_be_visible()
        expect(page.locator("text=Intermediate")).to_be_visible()
    
    def test_complexity_indicator_persists_across_screens(self, logic_quest_page: Page):
        """Test that complexity indicator persists across different screens."""
        page = logic_quest_page
        
        # Set complexity to advanced
        page.locator("text=Complexity Settings").click()
        page.wait_for_timeout(1000)
        page.locator("text=ADVANCED").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Verify on welcome screen
        expect(page.locator("text=🔥")).to_be_visible()
        expect(page.locator("text=Advanced")).to_be_visible()
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Verify in tutorial
        expect(page.locator("text=🔥")).to_be_visible()
        expect(page.locator("text=Advanced")).to_be_visible()
        
        # Return to menu
        page.locator("text=Main Menu").click()
        page.wait_for_timeout(1000)
        
        # Verify still on welcome screen
        expect(page.locator("text=🔥")).to_be_visible()
        expect(page.locator("text=Advanced")).to_be_visible()
    
    def test_all_complexity_level_icons_display(self, logic_quest_page: Page):
        """Test that all complexity level icons display correctly."""
        page = logic_quest_page
        
        complexity_levels = [
            ("BEGINNER", "🌱"),
            ("INTERMEDIATE", "⚡"),
            ("ADVANCED", "🔥"),
            ("EXPERT", "💀"),
        ]
        
        for level_name, icon in complexity_levels:
            # Go to complexity settings
            page.goto("http://localhost:3001")
            page.wait_for_load_state("networkidle")
            page.locator("text=Complexity Settings").click()
            page.wait_for_timeout(1000)
            
            # Select level
            page.locator(f"text={level_name}").first.click()
            page.wait_for_timeout(500)
            page.locator("text=Continue with Selected Level").click()
            page.wait_for_timeout(1000)
            
            # Verify icon is displayed
            expect(page.locator(f"text={icon}")).to_be_visible()
            expect(page.locator(f"text={level_name.capitalize()}")).to_be_visible()


class TestEducationalProgressionAllLevels:
    """Test educational progression at all complexity levels (Requirement 3.1)."""
    
    def test_tutorial_completion_at_beginner_level(self, logic_quest_page: Page):
        """Test completing tutorial at beginner level."""
        page = logic_quest_page
        
        # Start tutorial at beginner
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=BEGINNER").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Verify tutorial starts
        expect(page.locator("text=Starting Interactive Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        
        # Verify beginner-specific content
        expect(page.locator("text=🌱")).to_be_visible()
        expect(page.locator("text=Beginner")).to_be_visible()
        
        # Tutorial should be interactive
        input_field = page.locator("input[placeholder='Enter command...']")
        expect(input_field).to_be_visible()
    
    def test_tutorial_completion_at_expert_level(self, logic_quest_page: Page):
        """Test completing tutorial at expert level."""
        page = logic_quest_page
        
        # Start tutorial at expert
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=EXPERT").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Verify tutorial starts
        expect(page.locator("text=Starting Interactive Hello World Prolog Tutorial")).to_be_visible()
        
        # Verify expert-specific indicators
        expect(page.locator("text=💀")).to_be_visible()
        expect(page.locator("text=Expert")).to_be_visible()
        
        # Tutorial should still be accessible at expert level
        input_field = page.locator("input[placeholder='Enter command...']")
        expect(input_field).to_be_visible()
    
    def test_core_concepts_accessible_at_all_levels(self, logic_quest_page: Page):
        """Test that core Prolog concepts are accessible at all levels."""
        page = logic_quest_page
        
        levels = ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]
        
        for level in levels:
            # Reset to welcome screen
            page.goto("http://localhost:3001")
            page.wait_for_load_state("networkidle")
            
            # Start tutorial at this level
            page.locator("text=Start Hello World Tutorial").click()
            page.wait_for_timeout(1000)
            page.locator(f"text={level}").first.click()
            page.locator("text=Continue with Selected Level").click()
            page.wait_for_timeout(1000)
            
            # Verify core concepts are mentioned
            expect(page.locator("text=FACTS")).to_be_visible()
            expect(page.locator("text=RULES")).to_be_visible()
            expect(page.locator("text=QUERIES")).to_be_visible()
            
            # Verify tutorial content is present
            expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()


class TestComplexityAchievementsTracking:
    """Test complexity-based achievements tracking."""
    
    def test_status_command_shows_complexity_info(self, logic_quest_page: Page):
        """Test that status command shows complexity information."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        page.locator("text=ADVANCED").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Type status command
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("status")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show complexity information
        expect(page.locator("text=CURRENT COMPLEXITY LEVEL")).to_be_visible()
        expect(page.locator("text=🔥")).to_be_visible()
        expect(page.locator("text=ADVANCED")).to_be_visible()
        expect(page.locator("text=Scoring Multiplier")).to_be_visible()
    
    def test_achievements_command_shows_complexity_achievements(self, logic_quest_page: Page):
        """Test that achievements command shows complexity-based achievements."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        page.locator("text=INTERMEDIATE").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Type achievements command
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("achievements")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show complexity achievements
        expect(page.locator("text=COMPLEXITY ACHIEVEMENTS")).to_be_visible()
        expect(page.locator("text=BEGINNER")).to_be_visible()
        expect(page.locator("text=INTERMEDIATE")).to_be_visible()
        expect(page.locator("text=ADVANCED")).to_be_visible()
        expect(page.locator("text=EXPERT")).to_be_visible()


class TestComplexitySelectionInterface:
    """Test complexity selection interface details."""
    
    def test_complexity_selection_shows_descriptions(self, logic_quest_page: Page):
        """Test that complexity selection shows level descriptions."""
        page = logic_quest_page
        
        # Go to complexity settings
        page.locator("text=Complexity Settings").click()
        page.wait_for_timeout(1000)
        
        # Should show descriptions for all levels
        expect(page.locator("text=Maximum guidance")).to_be_visible()  # Beginner
        expect(page.locator("text=Moderate guidance")).to_be_visible()  # Intermediate
        expect(page.locator("text=Minimal guidance")).to_be_visible()  # Advanced
        expect(page.locator("text=No guidance")).to_be_visible()  # Expert
    
    def test_complexity_selection_shows_scoring_multipliers(self, logic_quest_page: Page):
        """Test that complexity selection shows scoring multipliers."""
        page = logic_quest_page
        
        # Go to complexity settings
        page.locator("text=Complexity Settings").click()
        page.wait_for_timeout(1000)
        
        # Should show multipliers
        expect(page.locator("text=1.0x")).to_be_visible()  # Beginner
        expect(page.locator("text=1.2x")).to_be_visible()  # Intermediate
        expect(page.locator("text=1.5x")).to_be_visible()  # Advanced
        expect(page.locator("text=2.0x")).to_be_visible()  # Expert
    
    def test_complexity_selection_highlights_current_level(self, logic_quest_page: Page):
        """Test that complexity selection highlights the current level."""
        page = logic_quest_page
        
        # Set to advanced
        page.locator("text=Complexity Settings").click()
        page.wait_for_timeout(1000)
        page.locator("text=ADVANCED").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Go back to complexity settings
        page.locator("text=Complexity Settings").click()
        page.wait_for_timeout(1000)
        
        # Advanced should be highlighted or marked as current
        expect(page.locator("text=Current Selection: ADVANCED")).to_be_visible()


class TestComplexityErrorHandling:
    """Test error handling in complexity system."""
    
    def test_invalid_complexity_command_shows_error(self, logic_quest_page: Page):
        """Test that invalid complexity commands show helpful errors."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=BEGINNER").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Type complexity command
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("complexity")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Type invalid level
        input_field.fill("invalid_level")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show error message
        expect(page.locator("text=Invalid complexity level")).to_be_visible()
    
    def test_same_complexity_level_shows_message(self, logic_quest_page: Page):
        """Test that selecting the same complexity level shows appropriate message."""
        page = logic_quest_page
        
        # Start at beginner
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        page.locator("text=BEGINNER").first.click()
        page.locator("text=Continue with Selected Level").click()
        page.wait_for_timeout(1000)
        
        # Try to change to beginner again
        input_field = page.locator("input[placeholder='Enter command...']")
        input_field.fill("complexity")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        input_field.fill("beginner")
        input_field.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show message about already being at that level
        expect(page.locator("text=You are already at BEGINNER level")).to_be_visible()
