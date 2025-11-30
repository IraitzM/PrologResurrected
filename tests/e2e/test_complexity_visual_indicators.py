"""
End-to-end tests for visual complexity indicators in the UI.

Tests Requirements 6.1, 6.2, 6.3:
- 6.1: Complexity level displayed in terminal header
- 6.2: Visual indicator updates immediately on change
- 6.3: Consistent color coding and styling
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def page_with_game(page: Page):
    """Navigate to the game and start a mode."""
    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")
    return page


def test_complexity_indicator_in_header(page_with_game: Page):
    """Test that complexity level is displayed in the main header (Requirement 6.1)."""
    page = page_with_game
    
    # Start tutorial to get to game screen
    page.get_by_text("Start Hello World Tutorial").click()
    
    # Select a complexity level
    page.get_by_text("BEGINNER").click()
    page.get_by_text("Continue with Selected Level").click()
    
    # Wait for game screen to load
    page.wait_for_selector("text=LOGIC QUEST")
    
    # Check that complexity indicator is visible in header
    # The header should contain the complexity level badge
    header = page.locator("text=LOGIC QUEST").locator("..")
    expect(header).to_contain_text("Beginner")
    expect(header).to_contain_text("🌱")


def test_complexity_indicator_in_terminal_header(page_with_game: Page):
    """Test that complexity level is displayed in terminal header (Requirement 6.1)."""
    page = page_with_game
    
    # Start tutorial
    page.get_by_text("Start Hello World Tutorial").click()
    
    # Select intermediate level
    page.get_by_text("INTERMEDIATE").click()
    page.get_by_text("Continue with Selected Level").click()
    
    # Wait for game screen
    page.wait_for_selector("text=CYBERDYNE SYSTEMS TERMINAL")
    
    # Check terminal header contains complexity indicator
    terminal_header = page.locator("text=CYBERDYNE SYSTEMS TERMINAL").locator("..")
    expect(terminal_header).to_contain_text("Intermediate")
    expect(terminal_header).to_contain_text("⚡")


def test_complexity_indicator_color_coding(page_with_game: Page):
    """Test that complexity levels use consistent color coding (Requirement 6.3)."""
    page = page_with_game
    
    # Test different complexity levels and their colors
    complexity_levels = [
        ("BEGINNER", "🌱", "Beginner"),
        ("INTERMEDIATE", "⚡", "Intermediate"),
        ("ADVANCED", "🔥", "Advanced"),
        ("EXPERT", "💀", "Expert"),
    ]
    
    for level_name, icon, display_name in complexity_levels:
        # Go to welcome screen
        page.goto("http://localhost:3000")
        page.wait_for_load_state("networkidle")
        
        # Start tutorial
        page.get_by_text("Start Hello World Tutorial").click()
        
        # Select complexity level
        page.get_by_text(level_name).click()
        page.get_by_text("Continue with Selected Level").click()
        
        # Wait for game screen
        page.wait_for_selector("text=LOGIC QUEST")
        
        # Verify the indicator shows correct icon and name
        page.wait_for_selector(f"text={icon}")
        page.wait_for_selector(f"text={display_name}")


def test_complexity_indicator_updates_on_change(page_with_game: Page):
    """Test that visual indicator updates immediately when complexity changes (Requirement 6.2)."""
    page = page_with_game
    
    # Start adventure mode
    page.get_by_text("Begin Main Adventure").click()
    
    # Select beginner level
    page.get_by_text("BEGINNER").click()
    page.get_by_text("Continue with Selected Level").click()
    
    # Wait for game screen
    page.wait_for_selector("text=LOGIC QUEST")
    
    # Verify initial complexity indicator
    expect(page.locator("text=🌱")).to_be_visible()
    expect(page.locator("text=Beginner")).to_be_visible()
    
    # Change complexity level via command
    input_field = page.locator("input[placeholder='Enter command...']")
    input_field.fill("complexity")
    input_field.press("Enter")
    
    # Wait for complexity menu
    page.wait_for_selector("text=COMPLEXITY LEVEL SELECTION")
    
    # Select advanced level
    input_field.fill("advanced")
    input_field.press("Enter")
    
    # Confirm the change
    page.wait_for_selector("text=CONFIRM COMPLEXITY CHANGE")
    input_field.fill("yes")
    input_field.press("Enter")
    
    # Wait for confirmation message
    page.wait_for_selector("text=Complexity level changed successfully")
    
    # Verify the indicator updated immediately
    expect(page.locator("text=🔥")).to_be_visible()
    expect(page.locator("text=Advanced")).to_be_visible()
    
    # Verify old indicator is no longer visible
    expect(page.locator("text=🌱")).not_to_be_visible()


def test_complexity_indicator_consistency_across_ui(page_with_game: Page):
    """Test that complexity indicator is shown consistently across all UI components (Requirement 6.3)."""
    page = page_with_game
    
    # Start tutorial
    page.get_by_text("Start Hello World Tutorial").click()
    
    # Select expert level
    page.get_by_text("EXPERT").click()
    page.get_by_text("Continue with Selected Level").click()
    
    # Wait for game screen
    page.wait_for_selector("text=LOGIC QUEST")
    
    # Count how many times the complexity indicator appears
    # Should appear in: main header, terminal header
    expert_icons = page.locator("text=💀")
    expert_text = page.locator("text=Expert")
    
    # Verify multiple instances (at least 2: header and terminal)
    expect(expert_icons).to_have_count(2)
    expect(expert_text).to_have_count(2)


def test_welcome_screen_shows_current_complexity(page_with_game: Page):
    """Test that welcome screen displays current complexity level."""
    page = page_with_game
    
    # Welcome screen should show current complexity
    expect(page.locator("text=Current Complexity:")).to_be_visible()
    expect(page.locator("text=Beginner")).to_be_visible()
    expect(page.locator("text=🌱")).to_be_visible()


def test_complexity_settings_button_accessible(page_with_game: Page):
    """Test that complexity settings are easily accessible from welcome screen."""
    page = page_with_game
    
    # Complexity settings button should be visible
    complexity_button = page.get_by_text("Complexity Settings")
    expect(complexity_button).to_be_visible()
    
    # Click it to open complexity selection
    complexity_button.click()
    
    # Should show complexity selection screen
    page.wait_for_selector("text=SELECT COMPLEXITY LEVEL")
    expect(page.locator("text=BEGINNER")).to_be_visible()
    expect(page.locator("text=INTERMEDIATE")).to_be_visible()
    expect(page.locator("text=ADVANCED")).to_be_visible()
    expect(page.locator("text=EXPERT")).to_be_visible()
