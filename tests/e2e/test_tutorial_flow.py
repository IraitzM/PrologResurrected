"""
Tutorial Flow E2E Tests

Tests for the Hello World Prolog tutorial functionality and user interactions.
These tests focus on the core tutorial logic without requiring a full server.
"""

import pytest
from unittest.mock import Mock, MagicMock
from game.hello_world_puzzle import HelloWorldPuzzle
from game.tutorial_content import TutorialStep


class MockPage:
    """Mock Playwright page for testing without browser."""
    
    def __init__(self):
        self.elements = {}
        self.clicks = []
        self.inputs = []
        
    def locator(self, selector):
        mock_locator = Mock()
        mock_locator.click = Mock(side_effect=lambda: self.clicks.append(selector))
        mock_locator.fill = Mock(side_effect=lambda text: self.inputs.append((selector, text)))
        mock_locator.press = Mock()
        return mock_locator
        
    def wait_for_timeout(self, ms):
        pass


class TestTutorialFlowLogic:
    """Test cases for tutorial flow logic without browser dependency."""
    
    def test_tutorial_initialization_logic(self):
        """Test that tutorial initializes correctly."""
        puzzle = HelloWorldPuzzle()
        
        # Check initial state
        assert puzzle.current_step() == TutorialStep.INTRODUCTION
        assert not puzzle.completed
        assert puzzle.tutorial_session.session_active
        
        # Check tutorial content is available
        content = puzzle.tutorial_session.get_current_content()
        assert "title" in content
        assert "explanation" in content
        assert content["title"] == "🚀 Welcome to Prolog Programming"
    
    def test_tutorial_navigation_logic(self):
        """Test tutorial navigation logic."""
        puzzle = HelloWorldPuzzle()
        
        # Test step progression
        initial_step = puzzle.current_step()
        assert initial_step == TutorialStep.INTRODUCTION
        
        # Advance to next step
        success = puzzle.next_step()
        assert success
        assert puzzle.current_step() == TutorialStep.FACTS_EXPLANATION
        
        # Continue advancing
        success = puzzle.next_step()
        assert success
        assert puzzle.current_step() == TutorialStep.FACT_CREATION
        
        # Test backward navigation
        success = puzzle.previous_step()
        assert success
        assert puzzle.current_step() == TutorialStep.FACTS_EXPLANATION
    
    def test_tutorial_reset_logic(self):
        """Test tutorial reset functionality."""
        puzzle = HelloWorldPuzzle()
        
        # Advance through several steps
        puzzle.next_step()
        puzzle.next_step()
        assert puzzle.current_step() == TutorialStep.FACT_CREATION
        
        # Reset tutorial
        puzzle.reset()
        
        # Should be back at the beginning
        assert puzzle.current_step() == TutorialStep.INTRODUCTION
        assert not puzzle.completed
        assert puzzle.attempts == 0
        assert puzzle.hints_used == 0
    
    def test_tutorial_content_progression_logic(self):
        """Test that tutorial content progresses through all steps correctly."""
        puzzle = HelloWorldPuzzle()
        
        # Expected step progression
        expected_steps = [
            TutorialStep.INTRODUCTION,
            TutorialStep.FACTS_EXPLANATION,
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION,
            TutorialStep.COMPLETION
        ]
        
        # Test progression through all steps
        for i, expected_step in enumerate(expected_steps):
            current_step = puzzle.current_step()
            assert current_step == expected_step
            
            # Get content for current step
            content = puzzle.tutorial_session.get_current_content()
            assert "title" in content
            assert len(content["title"]) > 0
            
            # Advance to next step (except for last step)
            if i < len(expected_steps) - 1:
                success = puzzle.next_step()
                assert success
        
        # Should be at completion
        assert puzzle.current_step() == TutorialStep.COMPLETION
    
    def test_tutorial_validation_logic(self):
        """Test validation logic for different tutorial steps."""
        puzzle = HelloWorldPuzzle()
        
        # Test fact validation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Valid fact
        result = puzzle.validate_solution("likes(bob, pizza).")
        assert result.is_valid
        
        # Invalid fact (missing period)
        result = puzzle.validate_solution("likes(bob, pizza)")
        assert not result.is_valid
        assert "period" in result.error_message.lower()
        
        # Test query validation
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        
        # Valid query
        result = puzzle.validate_solution("?- likes(bob, pizza).")
        assert result.is_valid
        
        # Invalid query (missing ?-)
        result = puzzle.validate_solution("likes(bob, pizza).")
        assert not result.is_valid
        assert "?-" in result.error_message


class TestTutorialEducationalContent:
    """Test the educational content delivery in tutorial."""
    
    def test_prolog_concepts_coverage(self):
        """Test that all key Prolog concepts are covered."""
        puzzle = HelloWorldPuzzle()
        
        # Check that all tutorial steps have educational content
        all_steps = [
            TutorialStep.INTRODUCTION,
            TutorialStep.FACTS_EXPLANATION,
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION,
            TutorialStep.COMPLETION
        ]
        
        for step in all_steps:
            puzzle.tutorial_session.navigator.jump_to_step(step)
            content = puzzle.tutorial_session.get_current_content()
            
            # Each step should have a title and explanation
            assert "title" in content
            assert len(content["title"]) > 0
            
            # Most steps should have explanation content
            if step != TutorialStep.COMPLETION:
                assert "explanation" in content
                assert len(content["explanation"]) > 0
    
    def test_tutorial_examples_content(self):
        """Test that tutorial examples are comprehensive and correct."""
        puzzle = HelloWorldPuzzle()
        
        # Check facts explanation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACTS_EXPLANATION)
        content = puzzle.tutorial_session.get_current_content()
        
        # Should have examples
        assert "examples" in content
        examples = content["examples"]
        assert len(examples) > 0
        
        # Examples should be valid Prolog facts
        from game.validation import PrologValidator
        for example in examples:
            result = PrologValidator.validate_fact(example)
            assert result.is_valid, f"Example '{example}' should be valid"
    
    def test_tutorial_learning_progression(self):
        """Test that tutorial follows logical learning progression."""
        puzzle = HelloWorldPuzzle()
        
        # Test that each step builds on the previous
        progression_concepts = []
        
        # Introduction - basic concepts
        content = puzzle.tutorial_session.get_current_content()
        assert "prolog" in content["title"].lower()
        progression_concepts.append("introduction")
        
        # Facts explanation
        puzzle.next_step()
        content = puzzle.tutorial_session.get_current_content()
        assert "fact" in content["title"].lower()
        progression_concepts.append("facts")
        
        # Fact creation (hands-on)
        puzzle.next_step()
        content = puzzle.tutorial_session.get_current_content()
        assert "create" in content["title"].lower() or "first" in content["title"].lower()
        progression_concepts.append("fact_creation")
        
        # Queries (building on facts)
        puzzle.next_step()
        content = puzzle.tutorial_session.get_current_content()
        assert "quer" in content["title"].lower() or "question" in content["title"].lower()
        progression_concepts.append("queries")
        
        # Variables (advanced queries)
        puzzle.next_step()
        content = puzzle.tutorial_session.get_current_content()
        assert "variable" in content["title"].lower()
        progression_concepts.append("variables")
        
        # Completion
        puzzle.next_step()
        content = puzzle.tutorial_session.get_current_content()
        assert "congratulation" in content["title"].lower() or "complete" in content["title"].lower()
        progression_concepts.append("completion")
        
        # Verify logical progression
        expected_progression = ["introduction", "facts", "fact_creation", "queries", "variables", "completion"]
        assert progression_concepts == expected_progression


class TestTutorialUserExperience:
    """Test user experience aspects of the tutorial."""
    
    def test_tutorial_hint_system(self):
        """Test that tutorial provides appropriate hints."""
        puzzle = HelloWorldPuzzle()
        
        # Test hints for different steps
        steps_to_test = [
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION
        ]
        
        for step in steps_to_test:
            puzzle.tutorial_session.navigator.jump_to_step(step)
            
            # Get hints at different levels
            hint1 = puzzle.get_hint(1)
            hint2 = puzzle.get_hint(2)
            
            assert isinstance(hint1, str)
            assert isinstance(hint2, str)
            assert len(hint1) > 0
            assert len(hint2) > 0
    
    def test_tutorial_completion_tracking(self):
        """Test the tutorial completion tracking and statistics."""
        puzzle = HelloWorldPuzzle()
        
        # Initial progress
        progress = puzzle.get_tutorial_progress()
        assert progress["completion_percentage"] == 0
        assert progress["steps_completed"] == 0
        
        # Complete some steps
        puzzle.tutorial_session.advance_step()  # Introduction -> Facts
        puzzle.tutorial_session.advance_step()  # Facts -> Fact Creation
        
        # Check progress
        progress = puzzle.get_tutorial_progress()
        assert progress["completion_percentage"] > 0
        assert progress["steps_completed"] > 0
        
        # Complete all steps
        while puzzle.tutorial_session.advance_step():
            pass
        
        # Should be fully complete
        progress = puzzle.get_tutorial_progress()
        assert progress["completion_percentage"] == 100
        
    def test_tutorial_error_handling_and_recovery(self):
        """Test error handling and recovery mechanisms."""
        puzzle = HelloWorldPuzzle()
        
        # Test validation with errors
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Test various error scenarios
        error_cases = [
            ("likes(bob, pizza", "Missing closing parenthesis"),
            ("likes(bob, pizza))", "Missing period"),
            ("Likes(bob, pizza).", "Uppercase predicate"),
            ("likes bob, pizza.", "Missing parentheses"),
        ]
        
        for invalid_input, expected_error_type in error_cases:
            result = puzzle.validate_solution(invalid_input)
            assert not result.is_valid
            assert result.error_message is not None
            assert len(result.error_message) > 0
            
            # Should provide helpful hints
            assert result.hint is not None
            assert len(result.hint) > 0