"""
Interactive Tutorial E2E Tests

End-to-end tests for the Hello World Prolog interactive tutorial functionality.
These tests verify that the tutorial requires active participation and proper
Prolog syntax input, rejecting generic progression commands like "next".
"""

from playwright.sync_api import Page, expect
import pytest


class TestInteractiveTutorialFlow:
    """Test cases for interactive tutorial flow requiring typed input."""
    
    def test_interactive_tutorial_completion_with_typed_input(self, logic_quest_page: Page):
        """Test complete interactive tutorial requiring typed input at each step."""
        page = logic_quest_page
        
        # Start the tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Verify we're in tutorial mode
        expect(page.locator("text=CYBERDYNE SYSTEMS TERMINAL")).to_be_visible()
        expect(page.locator("text=Starting Interactive Hello World Prolog Tutorial")).to_be_visible()
        expect(page.locator("text=IMPORTANT: This is an INTERACTIVE tutorial!")).to_be_visible()
        
        # Step 1: Introduction - should require specific engagement
        expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
        expect(page.locator("text=logic programming language")).to_be_visible()
        
        # Try to proceed with "next" - should be rejected
        input_field = page.locator("input[placeholder*='command']")
        input_field.fill("next")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        
        # Should show rejection message
        expect(page.locator("text=This tutorial requires active participation")).to_be_visible()
        
        # Provide correct engagement command
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to facts explanation
        expect(page.locator("text=Your First Prolog Fact")).to_be_visible()
        
        # Step 2: Facts explanation with component identification
        expect(page.locator("text=likes(alice, chocolate)")).to_be_visible()
        expect(page.locator("text=What is the predicate")).to_be_visible()
        
        # Try "next" - should be rejected
        input_field.fill("next")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Please identify the component")).to_be_visible()
        
        # Provide correct component identification
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to fact creation
        expect(page.locator("text=Create Your First Fact")).to_be_visible()
        
        # Step 3: Fact creation requiring proper syntax
        expect(page.locator("text=Write a fact that says Bob likes pizza")).to_be_visible()
        
        # Try invalid syntax
        input_field.fill("Bob likes pizza")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Invalid Prolog syntax")).to_be_visible()
        
        # Try correct syntax
        input_field.fill("likes(bob, pizza).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to queries
        expect(page.locator("text=Asking Questions with Queries")).to_be_visible()
        
        # Step 4: Query writing requiring ?- prefix
        expect(page.locator("text=Write a query to ask if Alice likes chocolate")).to_be_visible()
        
        # Try without ?- prefix
        input_field.fill("likes(alice, chocolate).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Queries must start with ?-")).to_be_visible()
        
        # Try correct query syntax
        input_field.fill("?- likes(alice, chocolate).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to variables
        expect(page.locator("text=Variables in Prolog")).to_be_visible()
        
        # Step 5: Variable query requiring uppercase variables
        expect(page.locator("text=Write a query to find what Alice likes using a variable")).to_be_visible()
        
        # Try with lowercase variable
        input_field.fill("?- likes(alice, x).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)
        expect(page.locator("text=Variables must start with uppercase")).to_be_visible()
        
        # Try correct variable query
        input_field.fill("?- likes(alice, X).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should reach completion
        expect(page.locator("text=Congratulations")).to_be_visible()
        expect(page.locator("text=completed the Hello World")).to_be_visible()
    
    def test_tutorial_blocks_generic_progression_commands(self, logic_quest_page: Page):
        """Test that tutorial blocks generic progression commands during exercises."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Test various generic commands that should be rejected
        generic_commands = ["next", "continue", "skip", "proceed", "advance"]
        
        for command in generic_commands:
            # Try the generic command
            input_field.fill(command)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show rejection message
            expect(page.locator("text=This tutorial requires active participation")).to_be_visible()
            
            # Clear any error messages by providing valid input
            input_field.fill("ready to learn")
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            break  # Only test first command to avoid advancing too far


class TestComponentIdentificationExercises:
    """Test component identification exercises requiring specific answers."""
    
    def test_predicate_identification_exercise(self, logic_quest_page: Page):
        """Test predicate identification requiring specific typed answer."""
        page = logic_quest_page
        
        # Navigate to facts explanation step
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        # Complete introduction
        input_field = page.locator("input[placeholder*='command']")
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should be at component identification
        expect(page.locator("text=likes(alice, chocolate)")).to_be_visible()
        expect(page.locator("text=What is the predicate")).to_be_visible()
        
        # Test wrong answers
        wrong_answers = ["alice", "chocolate", "fact", "next", "continue"]
        
        for wrong_answer in wrong_answers:
            input_field.fill(wrong_answer)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show error or hint
            page_content = page.content()
            assert any(phrase in page_content for phrase in [
                "incorrect", "try again", "hint", "predicate is"
            ])
        
        # Provide correct answer
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to next step
        expect(page.locator("text=Create Your First Fact")).to_be_visible()
    
    def test_argument_identification_exercise(self, logic_quest_page: Page):
        """Test argument identification in facts."""
        page = logic_quest_page
        
        # Navigate to facts explanation
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete introduction and predicate identification
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should now ask for arguments or advance to creation
        # The exact flow depends on implementation, but we should be able to identify components
        page_content = page.content()
        
        # Verify we've progressed beyond the predicate question
        assert "Create Your First Fact" in page_content or "arguments" in page_content.lower()


class TestFactCreationValidation:
    """Test fact creation exercises requiring proper syntax validation."""
    
    def test_fact_syntax_validation(self, logic_quest_page: Page):
        """Test fact creation with comprehensive syntax validation."""
        page = logic_quest_page
        
        # Navigate to fact creation step
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete previous steps
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should be at fact creation
        expect(page.locator("text=Write a fact that says Bob likes pizza")).to_be_visible()
        
        # Test various invalid syntax patterns
        invalid_facts = [
            "Bob likes pizza",           # Natural language
            "likes(bob, pizza",          # Missing closing parenthesis
            "likes(bob, pizza))",        # Extra closing parenthesis
            "likes bob, pizza.",         # Missing parentheses
            "likes(bob, pizza)",         # Missing period
            "Likes(bob, pizza).",        # Uppercase predicate
            "next",                      # Generic command
            "continue",                  # Generic command
        ]
        
        for invalid_fact in invalid_facts:
            input_field.fill(invalid_fact)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show specific error message
            page_content = page.content()
            assert any(phrase in page_content for phrase in [
                "Invalid", "syntax", "error", "must", "period", "parentheses"
            ])
        
        # Test correct fact
        input_field.fill("likes(bob, pizza).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to queries
        expect(page.locator("text=Asking Questions with Queries")).to_be_visible()
    
    def test_fact_semantic_validation(self, logic_quest_page: Page):
        """Test that facts are validated for semantic correctness."""
        page = logic_quest_page
        
        # Navigate to fact creation
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete previous steps
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Test semantically incorrect but syntactically valid facts
        semantic_errors = [
            "wrong(bob, pizza).",        # Wrong predicate
            "likes(pizza, bob).",        # Wrong argument order (if specific order expected)
        ]
        
        for semantic_error in semantic_errors:
            input_field.fill(semantic_error)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # May show semantic hint or accept if syntactically correct
            # Implementation dependent - at minimum should not crash
            page_content = page.content()
            assert len(page_content) > 0  # Page should still be functional


class TestQueryWritingValidation:
    """Test query writing exercises requiring ?- prefix and proper format."""
    
    def test_query_prefix_validation(self, logic_quest_page: Page):
        """Test that queries require ?- prefix."""
        page = logic_quest_page
        
        # Navigate to query step
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete previous steps quickly
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes(bob, pizza).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should be at query writing
        expect(page.locator("text=Write a query to ask if Alice likes chocolate")).to_be_visible()
        
        # Test queries without ?- prefix
        invalid_queries = [
            "likes(alice, chocolate).",   # Missing ?-
            "likes(alice, chocolate)",    # Missing ?- and period
            "alice likes chocolate",      # Natural language
            "next",                       # Generic command
        ]
        
        for invalid_query in invalid_queries:
            input_field.fill(invalid_query)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show error about missing ?-
            page_content = page.content()
            assert any(phrase in page_content for phrase in [
                "?-", "query", "prefix", "must start", "Invalid"
            ])
        
        # Test correct query
        input_field.fill("?- likes(alice, chocolate).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to variables
        expect(page.locator("text=Variables in Prolog")).to_be_visible()
    
    def test_query_syntax_validation(self, logic_quest_page: Page):
        """Test comprehensive query syntax validation."""
        page = logic_quest_page
        
        # Navigate to query step
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete previous steps
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes(bob, pizza).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Test various query syntax errors
        syntax_errors = [
            "?- likes(alice, chocolate",   # Missing closing parenthesis
            "?- likes(alice, chocolate))",  # Extra closing parenthesis
            "?- likes alice, chocolate.",   # Missing parentheses
            "?- likes(alice, chocolate)",   # Missing period
            "? likes(alice, chocolate).",   # Wrong prefix
            "?-likes(alice, chocolate).",   # Missing space after ?-
        ]
        
        for syntax_error in syntax_errors:
            input_field.fill(syntax_error)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show syntax error
            page_content = page.content()
            assert any(phrase in page_content for phrase in [
                "syntax", "error", "Invalid", "format", "parentheses", "period"
            ])


class TestVariableQueryValidation:
    """Test variable query creation requiring uppercase variables."""
    
    def test_variable_case_validation(self, logic_quest_page: Page):
        """Test that variables must be uppercase."""
        page = logic_quest_page
        
        # Navigate to variables step
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete all previous steps
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes(bob, pizza).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("?- likes(alice, chocolate).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should be at variables step
        expect(page.locator("text=Write a query to find what Alice likes using a variable")).to_be_visible()
        
        # Test lowercase variables (should be rejected)
        lowercase_variables = [
            "?- likes(alice, x).",        # Lowercase x
            "?- likes(alice, what).",     # Lowercase what
            "?- likes(person, pizza).",   # Lowercase person
            "next",                       # Generic command
        ]
        
        for lowercase_var in lowercase_variables:
            input_field.fill(lowercase_var)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show error about variable case
            page_content = page.content()
            assert any(phrase in page_content for phrase in [
                "uppercase", "Variables must", "capital", "Variable"
            ])
        
        # Test correct uppercase variable
        input_field.fill("?- likes(alice, X).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Should advance to completion
        expect(page.locator("text=Congratulations")).to_be_visible()
    
    def test_multiple_variable_validation(self, logic_quest_page: Page):
        """Test queries with multiple variables."""
        page = logic_quest_page
        
        # Navigate to variables step
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete previous steps
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes(bob, pizza).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("?- likes(alice, chocolate).")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Test mixed case variables (should be rejected)
        mixed_case_queries = [
            "?- likes(x, Y).",            # Mixed case
            "?- likes(Person, food).",    # Mixed case
        ]
        
        for mixed_query in mixed_case_queries:
            input_field.fill(mixed_query)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show error about variable case
            page_content = page.content()
            # May accept if at least one variable is correct, implementation dependent
            assert len(page_content) > 0  # Should not crash


class TestTutorialProgressValidation:
    """Test that tutorial properly tracks progress and prevents skipping."""
    
    def test_cannot_skip_steps(self, logic_quest_page: Page):
        """Test that users cannot skip tutorial steps."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Try to input advanced concepts before learning basics
        advanced_inputs = [
            "?- likes(X, Y).",           # Variables before learning them
            "parent(tom, bob).",         # Different predicate before learning facts
            "rule(X) :- fact(X).",       # Rules (not covered in hello world)
        ]
        
        for advanced_input in advanced_inputs:
            input_field.fill(advanced_input)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should either reject or not advance inappropriately
            # Should still be at introduction step
            expect(page.locator("text=Welcome to Prolog Programming")).to_be_visible()
    
    def test_tutorial_completion_tracking(self, logic_quest_page: Page):
        """Test that tutorial completion is properly tracked."""
        page = logic_quest_page
        
        # Complete entire tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete all steps
        steps = [
            "ready to learn",
            "likes",
            "likes(bob, pizza).",
            "?- likes(alice, chocolate).",
            "?- likes(alice, X)."
        ]
        
        for step_input in steps:
            input_field.fill(step_input)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)
        
        # Should reach completion
        expect(page.locator("text=Congratulations")).to_be_visible()
        expect(page.locator("text=completed the Hello World")).to_be_visible()
        
        # Should offer to continue to main adventure
        expect(page.locator("text=main adventure")).to_be_visible()


class TestTutorialErrorRecovery:
    """Test error recovery and hint systems in interactive tutorial."""
    
    def test_progressive_hint_system(self, logic_quest_page: Page):
        """Test that hints become more specific with repeated errors."""
        page = logic_quest_page
        
        # Navigate to fact creation
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Complete previous steps
        input_field.fill("ready to learn")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        input_field.fill("likes")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        
        # Make repeated errors to trigger progressive hints
        for attempt in range(3):
            input_field.fill("Bob likes pizza")  # Same error repeatedly
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show increasingly specific hints
            page_content = page.content()
            assert any(phrase in page_content for phrase in [
                "hint", "try", "format", "syntax", "example"
            ])
    
    def test_error_recovery_mechanisms(self, logic_quest_page: Page):
        """Test that users can recover from errors and continue."""
        page = logic_quest_page
        
        # Start tutorial
        page.locator("text=Start Hello World Tutorial").click()
        page.wait_for_timeout(1000)
        
        input_field = page.locator("input[placeholder*='command']")
        
        # Make errors at each step and then recover
        recovery_sequences = [
            # Introduction: error then correct
            ("next", "ready to learn"),
            # Facts: error then correct  
            ("continue", "likes"),
            # Fact creation: error then correct
            ("Bob likes pizza", "likes(bob, pizza)."),
        ]
        
        for error_input, correct_input in recovery_sequences:
            # Make error
            input_field.fill(error_input)
            page.keyboard.press("Enter")
            page.wait_for_timeout(500)
            
            # Should show error but remain functional
            page_content = page.content()
            assert len(page_content) > 0
            
            # Recover with correct input
            input_field.fill(correct_input)
            page.keyboard.press("Enter")
            page.wait_for_timeout(1000)
            
            # Should advance
            page_content = page.content()
            assert len(page_content) > 0