"""
Tutorial Flow E2E Tests

Tests for the Hello World Prolog tutorial functionality and user interactions.
"""

from playwright.sync_api import Page, expect


class TestTutorialFlow:
    """Test cases for tutorial flow and interactions."""
    
    def test_tutorial_initialization(self, logic_quest_page: Page):
        """Test that tutorial initializes correctly."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check terminal interface is loaded
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        
        # Check tutorial welcome message
        expect(page.locator("text=Starting Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        
        # Check that terminal input is available
        terminal_input = page.locator("input[placeholder='Enter command...']")
        expect(terminal_input).to_be_visible()
        expect(terminal_input).to_be_enabled()
        
        # Check prompt is visible
        expect(page.locator("text=LOGIC-1 >")).to_be_visible()
    
    def test_tutorial_navigation_commands(self, logic_quest_page: Page):
        """Test tutorial navigation using commands."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Get terminal input
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Test 'next' command
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should advance to next step
        expect(page.locator("text=> next")).to_be_visible()
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
        
        # Test 'continue' command
        terminal_input.fill("continue")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should advance further
        expect(page.locator("text=> continue")).to_be_visible()
    
    def test_tutorial_menu_return(self, logic_quest_page: Page):
        """Test returning to menu from tutorial."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Use menu command
        terminal_input = page.locator("input[placeholder='Enter command...']")
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should return to welcome screen
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
    
    def test_tutorial_content_progression(self, logic_quest_page: Page):
        """Test that tutorial content progresses through all steps."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Progress through tutorial steps
        tutorial_steps = [
            "Welcome to Prolog Programming",
            "Your First Prolog Fact", 
            "Create Your First Fact",
            "Asking Questions with Queries",
            "Variables: The Power of 'What If?'",
            "Congratulations, Logic Programmer!"
        ]
        
        # Check first step is visible
        expect(page.locator(f"text={tutorial_steps[0]}")).to_be_visible()
        
        # Progress through remaining steps
        for i in range(1, len(tutorial_steps)):
            terminal_input.fill("next")
            terminal_input.press("Enter")
            page.wait_for_timeout(500)
            
            # Check that we've progressed to the next step
            expect(page.locator(f"text={tutorial_steps[i]}")).to_be_visible()
        
        # At the end, should show completion message
        expect(page.locator("text=Tutorial complete! 🎉")).to_be_visible()
    
    def test_tutorial_invalid_commands(self, logic_quest_page: Page):
        """Test handling of invalid commands in tutorial."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Try invalid command
        terminal_input.fill("invalid_command")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show helpful message
        expect(page.locator("text=> invalid_command")).to_be_visible()
        expect(page.locator("text=Type 'next' to continue or 'menu' to return.")).to_be_visible()


class TestTutorialTerminalInterface:
    """Test the terminal interface during tutorial."""
    
    def test_terminal_input_functionality(self, logic_quest_page: Page):
        """Test that terminal input works correctly."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Test typing in input
        terminal_input.fill("test input")
        expect(terminal_input).to_have_value("test input")
        
        # Test Enter key
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Input should be echoed in terminal
        expect(page.locator("text=> test input")).to_be_visible()
        
        # Input field should be cleared
        expect(terminal_input).to_have_value("")
    
    def test_terminal_output_display(self, logic_quest_page: Page):
        """Test that terminal output is displayed correctly."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check that output area exists and has content
        terminal_output = page.locator("[data-testid='terminal-output'], .terminal-output, div:has-text('Starting Hello World Prolog Tutorial')")
        expect(terminal_output.first).to_be_visible()
        
        # Check that tutorial content is displayed
        expect(page.locator("text=Starting Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
    
    def test_terminal_scrolling(self, logic_quest_page: Page):
        """Test that terminal scrolls with content."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Add multiple lines to test scrolling
        for i in range(10):
            terminal_input.fill(f"test line {i}")
            terminal_input.press("Enter")
            page.wait_for_timeout(100)
        
        # Check that recent content is visible
        expect(page.locator("text=> test line 9")).to_be_visible()
        
        # Earlier content might be scrolled out of view, but terminal should handle it
        # The terminal area should have scroll capability
        terminal_area = page.locator("div").filter(has_text="Starting Hello World Prolog Tutorial").first
        expect(terminal_area).to_be_visible()
    
    def test_terminal_styling(self, logic_quest_page: Page):
        """Test that terminal has correct cyberpunk styling."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check terminal window styling
        terminal_window = page.locator("text=CYBERDYNE SYSTEMS TERMINAL").locator("..")
        expect(terminal_window).to_be_visible()
        
        # Check that monospace font is used
        terminal_input = page.locator("input[placeholder='Enter command...']")
        font_family = terminal_input.evaluate("el => getComputedStyle(el).fontFamily")
        assert "monospace" in font_family.lower()
        
        # Check that terminal has dark background
        terminal_bg = terminal_input.evaluate("el => getComputedStyle(el).backgroundColor")
        # Should be dark (black or very dark)
        assert "rgb(0, 0, 0)" in terminal_bg or "rgba(0, 0, 0" in terminal_bg


class TestTutorialEducationalContent:
    """Test the educational content delivery in tutorial."""
    
    def test_prolog_concepts_introduction(self, logic_quest_page: Page):
        """Test that Prolog concepts are properly introduced."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Check that key Prolog concepts are mentioned
        expect(page.locator("text=FACTS")).to_be_visible()
        expect(page.locator("text=RULES")).to_be_visible()
        expect(page.locator("text=QUERIES")).to_be_visible()
        
        # Check educational explanations
        expect(page.locator("text=Things that are unconditionally true")).to_be_visible()
        expect(page.locator("text=Logical relationships and conditions")).to_be_visible()
        expect(page.locator("text=Questions you ask the system")).to_be_visible()
    
    def test_tutorial_examples_display(self, logic_quest_page: Page):
        """Test that tutorial examples are displayed correctly."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Progress to facts explanation
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Check that Prolog syntax examples are shown
        expect(page.locator("text=likes(alice, chocolate).")).to_be_visible()
        expect(page.locator("text=parent(tom, bob).")).to_be_visible()
        
        # Check syntax explanation
        expect(page.locator("text='likes' is the PREDICATE")).to_be_visible()
        expect(page.locator("text='alice' and 'chocolate' are ARGUMENTS")).to_be_visible()
    
    def test_tutorial_progression_logic(self, logic_quest_page: Page):
        """Test that tutorial follows logical learning progression."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Should start with introduction
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        
        # Progress to facts
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
        
        # Progress to fact creation
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Create Your First Fact")).to_be_visible()
        
        # Progress to queries
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Asking Questions with Queries")).to_be_visible()
        
        # Each step should build on the previous
        # Facts -> Fact Creation -> Queries -> Variables -> Completion
        # This follows a logical learning progression


class TestTutorialUserExperience:
    """Test user experience aspects of the tutorial."""
    
    def test_tutorial_feedback_messages(self, logic_quest_page: Page):
        """Test that tutorial provides appropriate feedback."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Test invalid command feedback
        terminal_input.fill("invalid")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Type 'next' to continue or 'menu' to return.")).to_be_visible()
        
        # Test valid command feedback
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should progress without error messages
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
    
    def test_tutorial_completion_experience(self, logic_quest_page: Page):
        """Test the tutorial completion experience."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Progress through all steps quickly
        for _ in range(6):  # Number of tutorial steps
            terminal_input.fill("next")
            terminal_input.press("Enter")
            page.wait_for_timeout(300)
        
        # Should show completion message
        expect(page.locator("text=Tutorial complete! 🎉")).to_be_visible()
        expect(page.locator("text=Type 'menu' to return to main menu.")).to_be_visible()
        
        # Test return to menu after completion
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()