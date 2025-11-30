"""
End-to-end tests for complexity level selection interface.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def app_url():
    """Base URL for the application."""
    return "http://localhost:3000"


def test_complexity_selection_screen_display(page: Page, app_url: str):
    """Test that complexity selection screen displays correctly."""
    page.goto(app_url)
    
    # Wait for welcome screen to load
    expect(page.locator("text=LOGIC QUEST")).to_be_visible()
    
    # Click on complexity settings button
    complexity_button = page.locator("text=Complexity Settings")
    expect(complexity_button).to_be_visible()
    complexity_button.click()
    
    # Verify complexity selection screen is displayed
    expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
    
    # Verify all complexity level cards are present
    expect(page.locator("text=BEGINNER")).to_be_visible()
    expect(page.locator("text=INTERMEDIATE")).to_be_visible()
    expect(page.locator("text=ADVANCED")).to_be_visible()
    expect(page.locator("text=EXPERT")).to_be_visible()


def test_complexity_level_selection_and_indicators(page: Page, app_url: str):
    """Test selecting complexity levels and visual indicators."""
    page.goto(app_url)
    
    # Navigate to complexity selection
    page.locator("text=Complexity Settings").click()
    expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
    
    # Test selecting different levels
    test_levels = ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]
    
    for level in test_levels:
        # Click on the level card
        level_card = page.locator(f"text={level}").first
        level_card.click()
        
        # Verify the selection is reflected in the current selection display
        expect(page.locator(f"text=Current Selection: {level}")).to_be_visible()


def test_complexity_selection_flow_to_tutorial(page: Page, app_url: str):
    """Test the flow from complexity selection to tutorial."""
    page.goto(app_url)
    
    # Try to start tutorial (should show complexity selection first)
    tutorial_button = page.locator("text=Start Hello World Tutorial")
    tutorial_button.click()
    
    # Should show complexity selection screen
    expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
    
    # Select a complexity level
    page.locator("text=INTERMEDIATE").first.click()
    
    # Continue to tutorial
    continue_button = page.locator("text=Continue with Selected Level")
    expect(continue_button).to_be_visible()
    continue_button.click()
    
    # Should now be in tutorial mode
    expect(page.locator("text=Starting Interactive Hello World Prolog Tutorial")).to_be_visible()


def test_complexity_selection_flow_to_adventure(page: Page, app_url: str):
    """Test the flow from complexity selection to adventure."""
    page.goto(app_url)
    
    # Try to start adventure (should show complexity selection first)
    adventure_button = page.locator("text=Begin Main Adventure")
    adventure_button.click()
    
    # Should show complexity selection screen
    expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
    
    # Select a complexity level
    page.locator("text=ADVANCED").first.click()
    
    # Continue to adventure
    continue_button = page.locator("text=Continue with Selected Level")
    expect(continue_button).to_be_visible()
    continue_button.click()
    
    # Should now be in adventure mode
    expect(page.locator("text=INITIALIZING LOGIC QUEST")).to_be_visible()


def test_complexity_level_cards_styling(page: Page, app_url: str):
    """Test that complexity level cards have proper cyberpunk styling."""
    page.goto(app_url)
    
    # Navigate to complexity selection
    page.locator("text=Complexity Settings").click()
    
    # Verify cards have proper styling elements
    beginner_card = page.locator("text=BEGINNER").first
    expect(beginner_card).to_be_visible()
    
    # Check for presence of icons and descriptions
    expect(page.locator("text=🌱")).to_be_visible()  # Beginner icon
    expect(page.locator("text=⚡")).to_be_visible()  # Intermediate icon
    expect(page.locator("text=🔥")).to_be_visible()  # Advanced icon
    expect(page.locator("text=💀")).to_be_visible()  # Expert icon
    
    # Check for scoring multipliers
    expect(page.locator("text=1.0x")).to_be_visible()  # Beginner multiplier
    expect(page.locator("text=1.2x")).to_be_visible()  # Intermediate multiplier
    expect(page.locator("text=1.5x")).to_be_visible()  # Advanced multiplier
    expect(page.locator("text=2.0x")).to_be_visible()  # Expert multiplier


def test_complexity_indicator_in_terminal_header(page: Page, app_url: str):
    """Test that complexity level is shown in terminal header."""
    page.goto(app_url)
    
    # Start tutorial to get to terminal view
    page.locator("text=Start Hello World Tutorial").click()
    
    # Select complexity level
    page.locator("text=EXPERT").first.click()
    page.locator("text=Continue with Selected Level").click()
    
    # Verify terminal header includes complexity indicator
    expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL - 💀 EXPERT")).to_be_visible()


def test_return_to_welcome_from_complexity_selection(page: Page, app_url: str):
    """Test returning to welcome screen from complexity selection."""
    page.goto(app_url)
    
    # Navigate to complexity selection
    page.locator("text=Complexity Settings").click()
    expect(page.locator("text=SELECT COMPLEXITY LEVEL")).to_be_visible()
    
    # Select a level and continue (should return to welcome)
    page.locator("text=BEGINNER").first.click()
    page.locator("text=Continue with Selected Level").click()
    
    # Should be back at welcome screen
    expect(page.locator("text=LOGIC QUEST")).to_be_visible()
    expect(page.locator("text=A Prolog Learning Adventure")).to_be_visible()


def test_complexity_selection_persistence(page: Page, app_url: str):
    """Test that complexity selection persists during session."""
    page.goto(app_url)
    
    # Set complexity level
    page.locator("text=Complexity Settings").click()
    page.locator("text=ADVANCED").first.click()
    page.locator("text=Continue with Selected Level").click()
    
    # Start tutorial (should not show complexity selection again)
    page.locator("text=Start Hello World Tutorial").click()
    
    # Should go directly to tutorial, not complexity selection
    expect(page.locator("text=Starting Interactive Hello World Prolog Tutorial")).to_be_visible()
    
    # Verify complexity indicator shows ADVANCED
    expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL - 🔥 ADVANCED")).to_be_visible()