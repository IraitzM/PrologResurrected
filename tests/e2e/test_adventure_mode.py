"""
Adventure Mode E2E Tests

Tests for the main Logic Quest adventure mode functionality and interactions.
"""

from playwright.sync_api import Page, expect


class TestAdventureMode:
    """Test cases for adventure mode functionality."""
    
    def test_adventure_initialization(self, logic_quest_page: Page):
        """Test that adventure mode initializes correctly."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check terminal interface is loaded
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        
        # Check adventure intro message
        expect(page.locator("text=INITIALIZING LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL")).to_be_visible()
        
        # Check that terminal input is available
        terminal_input = page.locator("input[placeholder='Enter command...']")
        expect(terminal_input).to_be_visible()
        expect(terminal_input).to_be_enabled()
        
        # Check prompt is visible
        expect(page.locator("text=LOGIC-1 >")).to_be_visible()
    
    def test_adventure_story_content(self, logic_quest_page: Page):
        """Test that adventure story content is displayed."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check story elements are present
        expect(page.locator("text=The year is 1985")).to_be_visible()
        expect(page.locator("text=junior programmer")).to_be_visible()
        expect(page.locator("text=LOGIC-1 AI SYSTEM MALFUNCTION")).to_be_visible()
        expect(page.locator("text=Prolog")).to_be_visible()
        
        # Check cyberpunk atmosphere
        expect(page.locator("text=Neon lights flicker")).to_be_visible()
        expect(page.locator("text=Cyberdyne Systems")).to_be_visible()
    
    def test_adventure_ascii_art_display(self, logic_quest_page: Page):
        """Test that ASCII art is displayed in adventure mode."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check that Cyberdyne logo ASCII art is displayed
        # The exact ASCII art might be complex, so check for key parts
        expect(page.locator("text=SYSTEMS LOGIC-1 TERMINAL")).to_be_visible()
        
        # ASCII art should be visible in the terminal output
        terminal_content = page.locator("div").filter(has_text="INITIALIZING LOGIC QUEST")
        expect(terminal_content).to_be_visible()


class TestAdventureCommands:
    """Test command handling in adventure mode."""
    
    def test_help_command(self, logic_quest_page: Page):
        """Test the help command functionality."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Use help command
        terminal_input.fill("help")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Check help output
        expect(page.locator("text=> help")).to_be_visible()
        expect(page.locator("text=Available commands:")).to_be_visible()
        expect(page.locator("text=help - Show this help")).to_be_visible()
        expect(page.locator("text=status - Show game status")).to_be_visible()
        expect(page.locator("text=menu - Return to main menu")).to_be_visible()
    
    def test_status_command(self, logic_quest_page: Page):
        """Test the status command functionality."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Use status command
        terminal_input.fill("status")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Check status output
        expect(page.locator("text=> status")).to_be_visible()
        expect(page.locator("text=Current Level: 0")).to_be_visible()
        expect(page.locator("text=Score: 0")).to_be_visible()
        expect(page.locator("text=Concepts Learned: 0")).to_be_visible()
    
    def test_menu_command(self, logic_quest_page: Page):
        """Test returning to menu via command."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Use menu command
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should return to welcome screen
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
        expect(page.locator("text=Begin Main Adventure")).to_be_visible()
    
    def test_unknown_command_handling(self, logic_quest_page: Page):
        """Test handling of unknown commands."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Use unknown command
        terminal_input.fill("unknown_command")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Check error handling
        expect(page.locator("text=> unknown_command")).to_be_visible()
        expect(page.locator("text=Unknown command. Type 'help' for available commands.")).to_be_visible()


class TestAdventureTerminalInterface:
    """Test terminal interface in adventure mode."""
    
    def test_terminal_input_echo(self, logic_quest_page: Page):
        """Test that terminal input is echoed correctly."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Test various inputs
        test_commands = ["help", "status", "test input", "123"]
        
        for command in test_commands:
            terminal_input.fill(command)
            terminal_input.press("Enter")
            page.wait_for_timeout(300)
            
            # Input should be echoed with prompt
            expect(page.locator(f"text=> {command}")).to_be_visible()
            
            # Input field should be cleared
            expect(terminal_input).to_have_value("")
    
    def test_terminal_output_formatting(self, logic_quest_page: Page):
        """Test that terminal output is properly formatted."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check that different colored text is present
        # (Colors are applied via HTML spans with inline styles)
        page_content = page.content()
        
        # Should contain colored spans
        assert "color: #00ffff" in page_content  # cyan
        assert "color: #ffff00" in page_content  # yellow
        assert "color: #00ff00" in page_content  # green
    
    def test_terminal_scrolling_behavior(self, logic_quest_page: Page):
        """Test terminal scrolling with multiple commands."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Add many commands to test scrolling
        for i in range(15):
            terminal_input.fill(f"test command {i}")
            terminal_input.press("Enter")
            page.wait_for_timeout(100)
        
        # Recent commands should be visible
        expect(page.locator("text=> test command 14")).to_be_visible()
        
        # Terminal should handle overflow gracefully
        terminal_area = page.locator("div").filter(has_text="INITIALIZING LOGIC QUEST").first
        expect(terminal_area).to_be_visible()


class TestAdventureStoryProgression:
    """Test story progression in adventure mode."""
    
    def test_initial_story_setup(self, logic_quest_page: Page):
        """Test that initial story setup is complete."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check all story elements are present
        story_elements = [
            "The year is 1985",
            "junior programmer",
            "LOGIC-1 AI SYSTEM MALFUNCTION",
            "logic circuits are scrambled",
            "Prolog - the language of logic programming"
        ]
        
        for element in story_elements:
            expect(page.locator(f"text={element}")).to_be_visible()
    
    def test_cyberpunk_atmosphere(self, logic_quest_page: Page):
        """Test that cyberpunk atmosphere is established."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check cyberpunk elements
        cyberpunk_elements = [
            "Neon lights flicker",
            "rain streaks down the glass",
            "Cyberdyne Systems building",
            "night shift",
            "alarms begin blaring"
        ]
        
        for element in cyberpunk_elements:
            expect(page.locator(f"text={element}")).to_be_visible()
    
    def test_educational_context_setup(self, logic_quest_page: Page):
        """Test that educational context is properly established."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check educational setup
        educational_elements = [
            "Prolog",
            "logic programming",
            "logical reasoning",
            "reasoning circuits",
            "logical pathways"
        ]
        
        for element in educational_elements:
            expect(page.locator(f"text={element}")).to_be_visible()


class TestAdventureUserExperience:
    """Test user experience in adventure mode."""
    
    def test_immersive_experience(self, logic_quest_page: Page):
        """Test that adventure mode provides immersive experience."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # Check immersive elements
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=LOGIC-1 >")).to_be_visible()
        
        # Check that story creates urgency
        expect(page.locator("text=CRITICAL ERROR")).to_be_visible()
        expect(page.locator("text=4 hours")).to_be_visible()
        expect(page.locator("text=You're our only hope")).to_be_visible()
    
    def test_command_discoverability(self, logic_quest_page: Page):
        """Test that users can discover available commands."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Help command should be discoverable
        terminal_input.fill("help")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should list all available commands
        expect(page.locator("text=Available commands:")).to_be_visible()
        
        # Commands should be clearly listed
        commands = ["help", "status", "menu"]
        for command in commands:
            expect(page.locator(f"text={command} -")).to_be_visible()
    
    def test_error_recovery(self, logic_quest_page: Page):
        """Test that users can recover from errors gracefully."""
        page = logic_quest_page
        
        # Start adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Make an error
        terminal_input.fill("invalid")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should get helpful error message
        expect(page.locator("text=Unknown command")).to_be_visible()
        expect(page.locator("text=Type 'help' for available commands")).to_be_visible()
        
        # Should be able to recover with help
        terminal_input.fill("help")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Available commands:")).to_be_visible()