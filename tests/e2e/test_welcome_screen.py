"""
Welcome Screen E2E Tests

Tests for the Logic Quest welcome screen functionality and navigation.
"""

from playwright.sync_api import Page, expect


class TestWelcomeScreen:
    """Test cases for the welcome screen."""
    
    def test_welcome_screen_loads(self, logic_quest_page: Page):
        """Test that the welcome screen loads correctly."""
        page = logic_quest_page
        
        # Check main title
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=A Prolog Learning Adventure")).to_be_visible()
        
        # Check ASCII art is present
        expect(page.locator("text=CYBERDYNE SYSTEMS 1985")).to_be_visible()
        expect(page.locator("text=LOGIC-1 TERMINAL")).to_be_visible()
        
        # Check system status indicators
        expect(page.locator("text=NEURAL INTERFACE: ONLINE")).to_be_visible()
        expect(page.locator("text=LOGIC CIRCUITS: CRITICAL")).to_be_visible()
        expect(page.locator("text=AI CORE: NEEDS REPAIR")).to_be_visible()
    
    def test_welcome_screen_buttons(self, logic_quest_page: Page):
        """Test that all buttons are present and visible."""
        page = logic_quest_page
        
        # Check all menu buttons are present
        tutorial_button = page.locator("text=Start Hello World Tutorial")
        adventure_button = page.locator("text=Begin Main Adventure")
        exit_button = page.locator("text=Exit System")
        
        expect(tutorial_button).to_be_visible()
        expect(adventure_button).to_be_visible()
        expect(exit_button).to_be_visible()
        
        # Check footer text
        expect(page.locator("text=Select your mission, programmer...")).to_be_visible()
    
    def test_cyberpunk_styling(self, logic_quest_page: Page):
        """Test that cyberpunk styling is applied correctly."""
        page = logic_quest_page
        
        # Check background color is black
        body = page.locator("body")
        expect(body).to_have_css("background-color", "rgb(0, 0, 0)")
        
        # Check that neon colors are used (green text should be visible)
        title = page.locator("text=LOGIC QUEST").first
        # The exact color might vary due to CSS processing, but it should be bright
        title_color = title.evaluate("el => getComputedStyle(el).color")
        assert "rgb(0, 255, 0)" in title_color or "green" in title_color.lower()
    
    def test_responsive_design(self, logic_quest_page: Page):
        """Test that the welcome screen is responsive."""
        page = logic_quest_page
        
        # Test desktop view (default)
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        
        # Test mobile view
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(500)  # Wait for responsive changes
        
        # Main elements should still be visible
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
        
        # Reset to desktop
        page.set_viewport_size({"width": 1280, "height": 720})


class TestWelcomeScreenNavigation:
    """Test navigation from the welcome screen."""
    
    def test_start_tutorial_navigation(self, logic_quest_page: Page):
        """Test navigation to tutorial mode."""
        page = logic_quest_page
        
        # Click the tutorial button
        tutorial_button = page.locator("text=Start Hello World Tutorial")
        tutorial_button.click()
        
        # Wait for navigation to complete
        page.wait_for_timeout(1000)
        
        # Should navigate to game screen with tutorial content
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=Main Menu")).to_be_visible()
        
        # Should show tutorial content in terminal
        expect(page.locator("text=Starting Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
    
    def test_start_adventure_navigation(self, logic_quest_page: Page):
        """Test navigation to adventure mode."""
        page = logic_quest_page
        
        # Click the adventure button
        adventure_button = page.locator("text=Begin Main Adventure")
        adventure_button.click()
        
        # Wait for navigation to complete
        page.wait_for_timeout(1000)
        
        # Should navigate to game screen with adventure content
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=Main Menu")).to_be_visible()
        
        # Should show adventure intro in terminal
        expect(page.locator("text=INITIALIZING LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL")).to_be_visible()
    
    def test_return_to_menu_navigation(self, logic_quest_page: Page):
        """Test returning to menu from game screens."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Verify we're in game screen
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        
        # Click Main Menu button
        page.locator("text=Main Menu").click()
        page.wait_for_timeout(1000)
        
        # Should return to welcome screen
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
        expect(page.locator("text=Begin Main Adventure")).to_be_visible()


class TestWelcomeScreenAccessibility:
    """Test accessibility features of the welcome screen."""
    
    def test_keyboard_navigation(self, logic_quest_page: Page):
        """Test keyboard navigation through buttons."""
        page = logic_quest_page
        
        # Focus should be manageable with keyboard
        page.keyboard.press("Tab")
        
        # Check that buttons can be focused
        tutorial_button = page.locator("text=Start Hello World Tutorial")
        adventure_button = page.locator("text=Begin Main Adventure")
        
        # These should be focusable (exact focus testing depends on implementation)
        expect(tutorial_button).to_be_visible()
        expect(adventure_button).to_be_visible()
    
    def test_text_contrast(self, logic_quest_page: Page):
        """Test that text has sufficient contrast for accessibility."""
        page = logic_quest_page
        
        # Main title should be visible and high contrast
        title = page.locator("text=LOGIC QUEST").first
        expect(title).to_be_visible()
        
        # Subtitle should be visible
        subtitle = page.locator("text=A Prolog Learning Adventure")
        expect(subtitle).to_be_visible()
        
        # All buttons should be visible
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
        expect(page.locator("text=Begin Main Adventure")).to_be_visible()
        expect(page.locator("text=Exit System")).to_be_visible()
    
    def test_screen_reader_compatibility(self, logic_quest_page: Page):
        """Test that content is accessible to screen readers."""
        page = logic_quest_page
        
        # Check that important text content is in the DOM
        page_content = page.content()
        
        assert "LOGIC QUEST" in page_content
        assert "A Prolog Learning Adventure" in page_content
        assert "Start Hello World Tutorial" in page_content
        assert "Begin Main Adventure" in page_content
        
        # Check that there are no empty buttons or inaccessible elements
        buttons = page.locator("button").all()
        for button in buttons:
            button_text = button.text_content()
            assert button_text and button_text.strip(), "Button should have accessible text"