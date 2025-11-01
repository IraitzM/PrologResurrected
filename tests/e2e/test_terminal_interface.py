"""
Terminal Interface E2E Tests

Tests for the terminal interface functionality, styling, and user interactions.
"""

from playwright.sync_api import Page, expect


class TestTerminalInterface:
    """Test cases for terminal interface functionality."""
    
    def test_terminal_window_structure(self, logic_quest_page: Page):
        """Test that terminal window has correct structure."""
        page = logic_quest_page
        
        # Start tutorial to access terminal
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check terminal window components
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=LOGIC-1 >")).to_be_visible()
        
        # Check input field
        terminal_input = page.locator("input[placeholder='Enter command...']")
        expect(terminal_input).to_be_visible()
        expect(terminal_input).to_be_enabled()
        
        # Check that output area exists
        output_area = page.locator("div").filter(has_text="Starting Hello World Prolog Tutorial")
        expect(output_area).to_be_visible()
    
    def test_terminal_header(self, logic_quest_page: Page):
        """Test terminal header functionality."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check header elements
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Main Menu")).to_be_visible()
        
        # Test Main Menu button functionality
        page.locator("text=Main Menu").click()
        page.wait_for_timeout(1000)
        
        # Should return to welcome screen
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
    
    def test_terminal_prompt_display(self, logic_quest_page: Page):
        """Test that terminal prompt is displayed correctly."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check prompt styling and text
        prompt = page.locator("text=LOGIC-1 >")
        expect(prompt).to_be_visible()
        
        # Prompt should be styled with yellow color
        prompt_color = prompt.evaluate("el => getComputedStyle(el).color")
        # Should be yellow or bright color
        assert any(color in prompt_color.lower() for color in ["rgb(255, 255, 0)", "yellow", "rgb(255"])


class TestTerminalInput:
    """Test terminal input functionality."""
    
    def test_input_field_properties(self, logic_quest_page: Page):
        """Test input field properties and styling."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Check input properties
        expect(terminal_input).to_be_visible()
        expect(terminal_input).to_be_enabled()
        expect(terminal_input).to_have_attribute("placeholder", "Enter command...")
        
        # Check styling
        bg_color = terminal_input.evaluate("el => getComputedStyle(el).backgroundColor")
        font_family = terminal_input.evaluate("el => getComputedStyle(el).fontFamily")
        
        # Should have transparent/dark background
        assert "rgba(0, 0, 0, 0)" in bg_color or "transparent" in bg_color
        
        # Should use monospace font
        assert "monospace" in font_family.lower()
    
    def test_input_typing_and_clearing(self, logic_quest_page: Page):
        """Test typing in input and clearing behavior."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Test typing
        test_text = "test input text"
        terminal_input.fill(test_text)
        expect(terminal_input).to_have_value(test_text)
        
        # Test clearing on Enter
        terminal_input.press("Enter")
        page.wait_for_timeout(300)
        expect(terminal_input).to_have_value("")
        
        # Test that input was echoed
        expect(page.locator(f"text=> {test_text}")).to_be_visible()
    
    def test_enter_key_handling(self, logic_quest_page: Page):
        """Test Enter key handling in terminal input."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Test Enter with empty input
        terminal_input.press("Enter")
        page.wait_for_timeout(300)
        
        # Should not add empty line to output
        expect(page.locator("text=> ")).not_to_be_visible()
        
        # Test Enter with content
        terminal_input.fill("help")
        terminal_input.press("Enter")
        page.wait_for_timeout(300)
        
        # Should process command
        expect(page.locator("text=> help")).to_be_visible()
    
    def test_input_focus_behavior(self, logic_quest_page: Page):
        """Test input field focus behavior."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Click on input to focus
        terminal_input.click()
        
        # Should be focused and ready for typing
        expect(terminal_input).to_be_focused()
        
        # Test typing after focus
        page.keyboard.type("focused input")
        expect(terminal_input).to_have_value("focused input")


class TestTerminalOutput:
    """Test terminal output functionality."""
    
    def test_output_display(self, logic_quest_page: Page):
        """Test that output is displayed correctly."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check initial output
        expect(page.locator("text=Starting Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        
        # Add more output by entering commands
        terminal_input = page.locator("input[placeholder='Enter command...']")
        terminal_input.fill("test output")
        terminal_input.press("Enter")
        page.wait_for_timeout(300)
        
        # New output should be visible
        expect(page.locator("text=> test output")).to_be_visible()
    
    def test_output_color_formatting(self, logic_quest_page: Page):
        """Test that output uses correct color formatting."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check that colored output is present
        page_content = page.content()
        
        # Should contain HTML spans with color styles
        assert "color: #00ffff" in page_content  # cyan
        assert "color: #ffff00" in page_content  # yellow
        assert "color: #00ff00" in page_content  # green
        
        # Add command to test input echo color
        terminal_input = page.locator("input[placeholder='Enter command...']")
        terminal_input.fill("test")
        terminal_input.press("Enter")
        page.wait_for_timeout(300)
        
        # Input echo should be cyan colored
        updated_content = page.content()
        assert "color: #00ffff" in updated_content
    
    def test_output_scrolling(self, logic_quest_page: Page):
        """Test output area scrolling behavior."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Add many lines to test scrolling
        for i in range(20):
            terminal_input.fill(f"line {i}")
            terminal_input.press("Enter")
            page.wait_for_timeout(50)
        
        # Recent lines should be visible
        expect(page.locator("text=> line 19")).to_be_visible()
        
        # Output area should handle overflow
        output_area = page.locator("div").filter(has_text="Starting Hello World Prolog Tutorial").first
        
        # Check that output area has scroll capability
        scroll_height = output_area.evaluate("el => el.scrollHeight")
        client_height = output_area.evaluate("el => el.clientHeight")
        
        # If there's overflow, scrollHeight should be greater than clientHeight
        if scroll_height > client_height:
            # Test scrolling to bottom
            output_area.evaluate("el => el.scrollTop = el.scrollHeight")
            page.wait_for_timeout(100)
            
            # Most recent content should still be visible
            expect(page.locator("text=> line 19")).to_be_visible()
    
    def test_output_text_formatting(self, logic_quest_page: Page):
        """Test output text formatting and styling."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check text formatting properties
        output_text = page.locator("text=Starting Hello World Prolog Tutorial").first
        
        # Should use monospace font
        font_family = output_text.evaluate("el => getComputedStyle(el).fontFamily")
        assert "monospace" in font_family.lower()
        
        # Should have appropriate line height for readability
        line_height = output_text.evaluate("el => getComputedStyle(el).lineHeight")
        # Line height should be reasonable (not too tight)
        assert line_height != "normal"  # Should have explicit line height


class TestTerminalStyling:
    """Test terminal cyberpunk styling."""
    
    def test_cyberpunk_color_scheme(self, logic_quest_page: Page):
        """Test that cyberpunk color scheme is applied."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check background is dark
        body_bg = page.locator("body").evaluate("el => getComputedStyle(el).backgroundColor")
        assert "rgb(0, 0, 0)" in body_bg
        
        # Check that neon colors are used
        page_content = page.content()
        
        # Should contain neon color codes
        neon_colors = ["#00ff00", "#00ffff", "#ffff00"]  # green, cyan, yellow
        for color in neon_colors:
            assert color in page_content
    
    def test_terminal_window_styling(self, logic_quest_page: Page):
        """Test terminal window styling."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check terminal header styling
        header = page.locator("text=CYBERDYNE SYSTEMS TERMINAL")
        expect(header).to_be_visible()
        
        # Terminal should have retro appearance
        # Check for monospace font usage
        terminal_area = page.locator("input[placeholder='Enter command...']")
        font_family = terminal_area.evaluate("el => getComputedStyle(el).fontFamily")
        assert "monospace" in font_family.lower()
    
    def test_retro_terminal_effects(self, logic_quest_page: Page):
        """Test retro terminal visual effects."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check that terminal has appropriate styling
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Should have green border (cyberpunk style)
        border_color = terminal_input.evaluate("el => getComputedStyle(el).borderColor")
        # Should be green or bright color
        assert any(color in border_color.lower() for color in ["rgb(0, 255, 0)", "green"])
        
        # Text should be green
        text_color = terminal_input.evaluate("el => getComputedStyle(el).color")
        assert any(color in text_color.lower() for color in ["rgb(0, 255, 0)", "green"])


class TestTerminalAccessibility:
    """Test terminal accessibility features."""
    
    def test_keyboard_navigation(self, logic_quest_page: Page):
        """Test keyboard navigation in terminal."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Test Tab navigation
        page.keyboard.press("Tab")
        
        # Should be able to reach input field
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Click to focus and test keyboard input
        terminal_input.click()
        page.keyboard.type("keyboard test")
        expect(terminal_input).to_have_value("keyboard test")
        
        # Test Enter key
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        expect(page.locator("text=> keyboard test")).to_be_visible()
    
    def test_screen_reader_compatibility(self, logic_quest_page: Page):
        """Test screen reader compatibility."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check that important elements have accessible text
        terminal_input = page.locator("input[placeholder='Enter command...']")
        expect(terminal_input).to_have_attribute("placeholder", "Enter command...")
        
        # Check that output text is in accessible format
        page_content = page.content()
        
        # Important text should be in the DOM as text content
        assert "Starting Hello World Prolog Tutorial" in page_content
        assert "Welcome to Prolog Programming" in page_content
        
        # Should not rely solely on color for information
        expect(page.locator("text=LOGIC-1 >")).to_be_visible()
    
    def test_high_contrast_mode(self, logic_quest_page: Page):
        """Test terminal in high contrast scenarios."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check that text has sufficient contrast
        # Neon green on black should have high contrast
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        bg_color = terminal_input.evaluate("el => getComputedStyle(el).backgroundColor")
        text_color = terminal_input.evaluate("el => getComputedStyle(el).color")
        
        # Background should be dark/transparent
        assert "rgba(0, 0, 0" in bg_color or "transparent" in bg_color
        
        # Text should be bright
        assert "rgb(0, 255, 0)" in text_color or "green" in text_color.lower()
        
        # This provides high contrast for accessibility