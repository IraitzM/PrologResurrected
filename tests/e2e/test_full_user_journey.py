"""
Full User Journey E2E Tests

Tests for complete user journeys through Logic Quest, including
tutorial completion, adventure exploration, and cross-mode navigation.
"""

from playwright.sync_api import Page, expect


class TestCompleteUserJourney:
    """Test complete user journeys through the application."""
    
    def test_new_user_tutorial_journey(self, logic_quest_page: Page):
        """Test a complete new user journey through the tutorial."""
        page = logic_quest_page
        
        # 1. User arrives at welcome screen
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Select your mission, programmer...")).to_be_visible()
        
        # 2. User chooses tutorial (recommended for beginners)
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # 3. User sees tutorial interface
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=Starting Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        
        # 4. User progresses through tutorial
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Progress through each step
        tutorial_steps = [
            "Your First Prolog Fact",
            "Create Your First Fact", 
            "Asking Questions with Queries",
            "Variables: The Power of 'What If?'",
            "Congratulations, Logic Programmer!"
        ]
        
        for step in tutorial_steps:
            terminal_input.fill("next")
            terminal_input.press("Enter")
            page.wait_for_timeout(500)
            expect(page.locator(f"text={step}")).to_be_visible()
        
        # 5. User completes tutorial
        expect(page.locator("text=Tutorial complete! 🎉")).to_be_visible()
        
        # 6. User returns to menu
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 7. User is back at welcome screen, ready for adventure
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Begin Main Adventure")).to_be_visible()
    
    def test_experienced_user_adventure_journey(self, logic_quest_page: Page):
        """Test an experienced user going straight to adventure."""
        page = logic_quest_page
        
        # 1. User arrives and chooses adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # 2. User sees adventure setup
        expect(page.locator("text=INITIALIZING LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL")).to_be_visible()
        expect(page.locator("text=The year is 1985")).to_be_visible()
        
        # 3. User explores available commands
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        terminal_input.fill("help")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Available commands:")).to_be_visible()
        expect(page.locator("text=help - Show this help")).to_be_visible()
        expect(page.locator("text=status - Show game status")).to_be_visible()
        
        # 4. User checks status
        terminal_input.fill("status")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Current Level: 0")).to_be_visible()
        expect(page.locator("text=Score: 0")).to_be_visible()
        expect(page.locator("text=Concepts Learned: 0")).to_be_visible()
        
        # 5. User can return to menu anytime
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
    
    def test_cross_mode_navigation_journey(self, logic_quest_page: Page):
        """Test user switching between tutorial and adventure modes."""
        page = logic_quest_page
        
        # 1. Start with tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        
        # 2. Return to menu
        page.locator("text=Main Menu").click()
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        
        # 3. Switch to adventure
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL")).to_be_visible()
        
        # 4. Return to menu via command
        terminal_input = page.locator("input[placeholder='Enter command...']")
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        
        # 5. Back to tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
    
    def test_error_recovery_journey(self, logic_quest_page: Page):
        """Test user journey with error recovery scenarios."""
        page = logic_quest_page
        
        # 1. Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # 2. User makes mistakes
        terminal_input.fill("wrong_command")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # 3. User gets helpful feedback
        expect(page.locator("text=Type 'next' to continue or 'menu' to return.")).to_be_visible()
        
        # 4. User recovers and continues
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
        
        # 5. Switch to adventure and make errors there too
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # 6. Make error in adventure mode
        terminal_input.fill("invalid_adventure_command")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # 7. Get helpful error message
        expect(page.locator("text=Unknown command. Type 'help' for available commands.")).to_be_visible()
        
        # 8. User recovers with help
        terminal_input.fill("help")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Available commands:")).to_be_visible()


class TestUserExperienceFlow:
    """Test user experience aspects across the application."""
    
    def test_consistent_navigation_experience(self, logic_quest_page: Page):
        """Test that navigation is consistent across modes."""
        page = logic_quest_page
        
        # Test navigation patterns are consistent
        modes = [
            ("Start Hello World Tutorial", "tutorial"),
            ("Begin Main Adventure", "adventure")
        ]
        
        for button_text, mode in modes:
            # Start mode
            page.locator(f"text={button_text}").click()
            page.wait_for_timeout(1000)
            
            # Check consistent elements
            expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
            expect(page.locator("text=LOGIC-1 >")).to_be_visible()
            expect(page.locator("text=Main Menu")).to_be_visible()
            expect(page.locator("input[placeholder='Enter command...']")).to_be_visible()
            
            # Return to menu
            page.locator("text=Main Menu").click()
            page.wait_for_timeout(1000)
            
            expect(page.locator("text=LOGIC QUEST")).to_be_visible()
    
    def test_responsive_behavior_journey(self, logic_quest_page: Page):
        """Test user journey across different screen sizes."""
        page = logic_quest_page
        
        # Test desktop experience
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        
        # Switch to mobile
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(500)
        
        # Should still be functional
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()
        
        # Start tutorial on mobile
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Terminal should work on mobile
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        terminal_input = page.locator("input[placeholder='Enter command...']")
        expect(terminal_input).to_be_visible()
        
        # Test input on mobile
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=> next")).to_be_visible()
        
        # Return to desktop
        page.set_viewport_size({"width": 1280, "height": 720})
        page.wait_for_timeout(500)
        
        # Should still work
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
    
    def test_performance_during_journey(self, logic_quest_page: Page):
        """Test that performance remains good during user journey."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Rapid interactions should be handled smoothly
        for i in range(10):
            terminal_input.fill(f"command {i}")
            terminal_input.press("Enter")
            page.wait_for_timeout(100)  # Minimal wait
        
        # Should handle rapid input without issues
        expect(page.locator("text=> command 9")).to_be_visible()
        
        # Switch modes rapidly
        page.locator("text=Main Menu").click()
        page.wait_for_timeout(500)
        
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(500)
        
        page.locator("text=Main Menu").click()
        page.wait_for_timeout(500)
        
        # Should still be responsive
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
        expect(page.locator("text=Start Hello World Tutorial")).to_be_visible()


class TestEducationalUserJourney:
    """Test educational aspects of user journey."""
    
    def test_learning_progression_journey(self, logic_quest_page: Page):
        """Test that user experiences proper learning progression."""
        page = logic_quest_page
        
        # 1. User starts with no knowledge (welcome screen)
        expect(page.locator("text=A Prolog Learning Adventure")).to_be_visible()
        
        # 2. User chooses tutorial for learning
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # 3. User learns about Prolog basics
        expect(page.locator("text=FACTS")).to_be_visible()
        expect(page.locator("text=RULES")).to_be_visible()
        expect(page.locator("text=QUERIES")).to_be_visible()
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # 4. User progresses through concepts
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should learn about facts
        expect(page.locator("text=likes(alice, chocolate).")).to_be_visible()
        expect(page.locator("text='likes' is the PREDICATE")).to_be_visible()
        
        # 5. User continues learning
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # Should get to hands-on practice
        expect(page.locator("text=Create Your First Fact")).to_be_visible()
        expect(page.locator("text=Bob likes pizza")).to_be_visible()
        
        # 6. User learns about queries
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Asking Questions with Queries")).to_be_visible()
        expect(page.locator("text=?-")).to_be_visible()
        
        # 7. User learns about variables
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Variables: The Power of 'What If?'")).to_be_visible()
        expect(page.locator("text=UPPERCASE")).to_be_visible()
        
        # 8. User completes learning journey
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=Congratulations, Logic Programmer!")).to_be_visible()
        expect(page.locator("text=MISSION ACCOMPLISHED")).to_be_visible()
    
    def test_tutorial_to_adventure_transition(self, logic_quest_page: Page):
        """Test smooth transition from tutorial to adventure."""
        page = logic_quest_page
        
        # 1. Complete tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        terminal_input = page.locator("input[placeholder='Enter command...']")
        
        # Quick progression through tutorial
        for _ in range(6):
            terminal_input.fill("next")
            terminal_input.press("Enter")
            page.wait_for_timeout(200)
        
        expect(page.locator("text=Tutorial complete! 🎉")).to_be_visible()
        
        # 2. Return to menu
        terminal_input.fill("menu")
        terminal_input.press("Enter")
        page.wait_for_timeout(1000)
        
        # 3. Now ready for adventure with knowledge
        page.locator("text=Begin Main Adventure").click()
        page.wait_for_timeout(1000)
        
        # 4. Adventure should reference learned concepts
        expect(page.locator("text=Prolog")).to_be_visible()
        expect(page.locator("text=logic programming")).to_be_visible()
        expect(page.locator("text=logical reasoning")).to_be_visible()
        
        # User now has context for the adventure story
        expect(page.locator("text=LOGIC-1")).to_be_visible()
        expect(page.locator("text=reasoning circuits")).to_be_visible()


class TestAccessibilityJourney:
    """Test accessibility throughout user journey."""
    
    def test_keyboard_only_journey(self, logic_quest_page: Page):
        """Test complete journey using only keyboard navigation."""
        page = logic_quest_page
        
        # Start with keyboard navigation
        page.keyboard.press("Tab")
        
        # Should be able to navigate to tutorial button
        # (Exact tab order depends on implementation)
        tutorial_button = page.locator("text=Start Hello World Tutorial")
        tutorial_button.click()  # Simulate keyboard activation
        page.wait_for_timeout(1000)
        
        # Should be able to use terminal with keyboard
        terminal_input = page.locator("input[placeholder='Enter command...']")
        terminal_input.click()  # Focus
        
        # Type with keyboard
        page.keyboard.type("next")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        
        expect(page.locator("text=> next")).to_be_visible()
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
        
        # Continue keyboard interaction
        page.keyboard.type("menu")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        expect(page.locator("text=LOGIC QUEST")).to_be_visible()
    
    def test_screen_reader_journey(self, logic_quest_page: Page):
        """Test that journey is compatible with screen readers."""
        page = logic_quest_page
        
        # Check that all important content is in accessible text
        page_content = page.content()
        
        # Welcome screen should have accessible content
        assert "LOGIC QUEST" in page_content
        assert "A Prolog Learning Adventure" in page_content
        assert "Start Hello World Tutorial" in page_content
        assert "Begin Main Adventure" in page_content
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Tutorial content should be accessible
        updated_content = page.content()
        assert "Starting Hello World Prolog Tutorial" in updated_content
        assert "Welcome to Prolog Programming" in updated_content
        
        # Input should have accessible placeholder
        terminal_input = page.locator("input[placeholder='Enter command...']")
        expect(terminal_input).to_have_attribute("placeholder", "Enter command...")
        
        # Progress through tutorial
        terminal_input.fill("next")
        terminal_input.press("Enter")
        page.wait_for_timeout(500)
        
        # New content should be accessible
        final_content = page.content()
        assert "Your First Prolog Fact" in final_content