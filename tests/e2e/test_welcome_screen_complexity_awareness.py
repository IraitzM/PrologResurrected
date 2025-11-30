"""
End-to-end tests for welcome screen complexity awareness.

This module tests the welcome screen's UI integration with complexity levels,
including visual indicators, recommendations, and navigation.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_welcome_screen_displays_complexity_indicator(page: Page, base_url: str):
    """Test that welcome screen displays current complexity level indicator."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Check that complexity indicator is visible
    expect(page.locator("text=Current Complexity:")).to_be_visible()
    
    # Check that a complexity level is displayed (default is BEGINNER)
    expect(page.locator("text=BEGINNER")).to_be_visible()


@pytest.mark.e2e
def test_welcome_screen_shows_complexity_description(page: Page, base_url: str):
    """Test that welcome screen shows complexity level description."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Check that a description is visible (BEGINNER default)
    # The description should contain guidance-related text
    page.wait_for_selector("text=/guidance|hints|explanations/i", timeout=5000)


@pytest.mark.e2e
def test_welcome_screen_shows_recommendation_for_non_beginner(page: Page, base_url: str):
    """Test that welcome screen shows recommendation when not on beginner level."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Navigate to complexity settings
    page.click("text=Complexity Settings")
    
    # Wait for complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)
    
    # Select EXPERT level
    page.click("text=EXPERT")
    
    # Continue with selected level
    page.click("text=Continue with Selected Level")
    
    # Wait to return to welcome screen
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Check that recommendation is visible for new players
    expect(page.locator("text=/Recommendation for New Players/i")).to_be_visible()


@pytest.mark.e2e
def test_welcome_screen_complexity_settings_button(page: Page, base_url: str):
    """Test that complexity settings button is accessible from welcome screen."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Check that Complexity Settings button is visible
    expect(page.locator("text=Complexity Settings")).to_be_visible()
    
    # Click the button
    page.click("text=Complexity Settings")
    
    # Verify we're on the complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)


@pytest.mark.e2e
def test_complexity_selection_shows_recommendations(page: Page, base_url: str):
    """Test that complexity selection screen shows recommendations."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Navigate to complexity settings
    page.click("text=Complexity Settings")
    
    # Wait for complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)
    
    # Check that recommendation box is visible
    expect(page.locator("text=/Recommendation for New Players/i")).to_be_visible()
    
    # Check that recommendation mentions BEGINNER
    expect(page.locator("text=/BEGINNER level/i")).to_be_visible()


@pytest.mark.e2e
def test_complexity_selection_shows_preview_information(page: Page, base_url: str):
    """Test that complexity selection screen shows preview information."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Navigate to complexity settings
    page.click("text=Complexity Settings")
    
    # Wait for complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)
    
    # Check that preview information box is visible
    expect(page.locator("text=/What Each Level Means/i")).to_be_visible()
    
    # Check that all levels are mentioned in preview
    expect(page.locator("text=/BEGINNER.*Detailed explanations/i")).to_be_visible()
    expect(page.locator("text=/INTERMEDIATE.*Moderate explanations/i")).to_be_visible()
    expect(page.locator("text=/ADVANCED.*Brief explanations/i")).to_be_visible()
    expect(page.locator("text=/EXPERT.*Minimal explanations/i")).to_be_visible()


@pytest.mark.e2e
def test_complexity_selection_shows_all_levels(page: Page, base_url: str):
    """Test that complexity selection screen shows all complexity levels."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Navigate to complexity settings
    page.click("text=Complexity Settings")
    
    # Wait for complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)
    
    # Check that all complexity levels are visible
    expect(page.locator("text=BEGINNER").first).to_be_visible()
    expect(page.locator("text=INTERMEDIATE").first).to_be_visible()
    expect(page.locator("text=ADVANCED").first).to_be_visible()
    expect(page.locator("text=EXPERT").first).to_be_visible()


@pytest.mark.e2e
def test_welcome_screen_tutorial_recommendation(page: Page, base_url: str):
    """Test that tutorial is recommended for new players."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Check that tutorial button has recommendation marker
    expect(page.locator("text=/Recommended for first-time players/i")).to_be_visible()


@pytest.mark.e2e
def test_welcome_screen_shows_complexity_on_game_modes(page: Page, base_url: str):
    """Test that game mode buttons show complexity level information."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Check that adventure button shows complexity info
    expect(page.locator("text=/Start at.*level/i")).to_be_visible()


@pytest.mark.e2e
def test_welcome_screen_footer_adapts_to_player_status(page: Page, base_url: str):
    """Test that footer message adapts based on player status."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # For new players, should see tutorial recommendation
    expect(page.locator("text=/New to Prolog/i")).to_be_visible()
    
    # Should also see complexity tip
    expect(page.locator("text=/tutorial adapts to your selected complexity level/i")).to_be_visible()


@pytest.mark.e2e
def test_complexity_level_change_updates_welcome_screen(page: Page, base_url: str):
    """Test that changing complexity level updates welcome screen display."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Verify initial level (BEGINNER)
    expect(page.locator("text=BEGINNER").first).to_be_visible()
    
    # Navigate to complexity settings
    page.click("text=Complexity Settings")
    
    # Wait for complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)
    
    # Select INTERMEDIATE level
    page.click("text=INTERMEDIATE")
    
    # Continue with selected level
    page.click("text=Continue with Selected Level")
    
    # Wait to return to welcome screen
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Verify level changed to INTERMEDIATE
    expect(page.locator("text=INTERMEDIATE").first).to_be_visible()


@pytest.mark.e2e
def test_complexity_selection_can_change_anytime_message(page: Page, base_url: str):
    """Test that complexity selection screen shows 'change anytime' message."""
    page.goto(base_url)
    
    # Wait for page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=5000)
    
    # Navigate to complexity settings
    page.click("text=Complexity Settings")
    
    # Wait for complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL", timeout=5000)
    
    # Check that message about changing anytime is visible
    expect(page.locator("text=/change the complexity level at any time/i")).to_be_visible()
