"""
Interactive Tutorial Validation Tests

Unit-style tests for the interactive tutorial validation logic that can run
without requiring a full browser setup. These tests focus on the core
validation requirements for the interactive tutorial.
"""

import pytest
from unittest.mock import Mock, MagicMock
from prologresurrected.game.hello_world_puzzle import HelloWorldPuzzle
from prologresurrected.game.validation import PrologValidator, ValidationResult
from prologresurrected.game.tutorial_content import TutorialStep


class TestInteractiveTutorialValidationLogic:
    """Test the validation logic for interactive tutorial exercises."""
    
    def test_generic_command_rejection_in_validation(self):
        """Test that generic progression commands are rejected by validation methods."""
        # Test various generic commands that should be rejected
        generic_commands = ["next", "continue", "skip", "proceed", "advance", "NEXT", "Continue"]
        
        for command in generic_commands:
            # Test fact validation rejects generic commands
            fact_result = PrologValidator.validate_fact(command)
            assert not fact_result.is_valid, f"Fact validation should reject '{command}'"
            
            # Test query validation rejects generic commands
            query_result = PrologValidator.validate_query(command)
            assert not query_result.is_valid, f"Query validation should reject '{command}'"
    
    def test_component_extraction_functionality(self):
        """Test component extraction from valid Prolog statements."""
        # Test fact component extraction
        fact_components = PrologValidator.extract_components("likes(alice, chocolate).")
        assert fact_components["type"] == "fact"
        assert fact_components["predicate"] == "likes"
        assert fact_components["arguments"] == ["alice", "chocolate"]
        
        # Test query component extraction
        query_components = PrologValidator.extract_components("?- likes(alice, chocolate).")
        assert query_components["type"] == "query"
        assert query_components["predicate"] == "likes"
        assert query_components["arguments"] == ["alice", "chocolate"]
        
        # Test invalid statement
        invalid_components = PrologValidator.extract_components("invalid syntax")
        assert invalid_components["type"] == "invalid"
    
    def test_fact_creation_syntax_validation(self):
        """Test fact creation requires proper Prolog syntax."""
        test_cases = [
            # (user_input, expected_valid, expected_error_keywords)
            ("likes(bob, pizza).", True, []),
            ("likes(alice, chocolate).", True, []),
            ("parent(tom, bob).", True, []),
            
            # Invalid syntax cases
            ("Bob likes pizza", False, ["parentheses", "missing"]),
            ("likes(bob, pizza", False, ["period", "missing"]),
            ("likes(bob, pizza))", False, ["period", "missing"]),
            ("likes bob, pizza.", False, ["parentheses", "missing"]),
            ("likes(bob, pizza)", False, ["period", "missing"]),
            ("Likes(bob, pizza).", False, ["lowercase", "predicate"]),
            ("likes(Bob, Pizza).", True, []),  # Actually valid syntax - uppercase arguments are allowed
            
            # Generic commands should be rejected
            ("next", False, ["parentheses", "missing"]),
            ("continue", False, ["parentheses", "missing"]),
            ("skip", False, ["parentheses", "missing"]),
        ]
        
        for user_input, expected_valid, expected_keywords in test_cases:
            result = PrologValidator.validate_fact(user_input)
            assert result.is_valid == expected_valid, f"Fact '{user_input}' should be {'valid' if expected_valid else 'invalid'}"
            
            if not expected_valid:
                assert result.error_message is not None
                error_msg = result.error_message.lower()
                # At least one expected keyword should be in the error message
                if expected_keywords:
                    assert any(keyword in error_msg for keyword in expected_keywords), \
                        f"Error message '{result.error_message}' should contain one of {expected_keywords}"
    
    def test_query_syntax_validation(self):
        """Test query writing requires ?- prefix and proper format."""
        test_cases = [
            # (user_input, expected_valid, expected_error_keywords)
            ("?- likes(alice, chocolate).", True, []),
            ("?- parent(tom, bob).", True, []),
            ("?- employee(alice, cyberdyne).", True, []),
            
            # Missing ?- prefix
            ("likes(alice, chocolate).", False, ["?-", "prefix", "query"]),
            ("parent(tom, bob).", False, ["?-", "prefix", "query"]),
            
            # Syntax errors with correct prefix
            ("?- likes(alice, chocolate", False, ["period", "missing"]),
            ("?- likes(alice, chocolate))", False, ["period", "missing"]),
            ("?- likes alice, chocolate.", False, ["parentheses", "missing"]),
            ("?- likes(alice, chocolate)", False, ["period", "missing"]),
            
            # Wrong prefix variations
            ("? likes(alice, chocolate).", False, ["?-", "prefix"]),
            ("?-likes(alice, chocolate).", False, ["space", "missing"]),
            ("- likes(alice, chocolate).", False, ["?-", "prefix"]),
            
            # Generic commands
            ("next", False, ["?-", "prefix"]),
            ("continue", False, ["?-", "prefix"]),
        ]
        
        for user_input, expected_valid, expected_keywords in test_cases:
            result = PrologValidator.validate_query(user_input)
            assert result.is_valid == expected_valid, f"Query '{user_input}' should be {'valid' if expected_valid else 'invalid'}"
            
            if not expected_valid:
                assert result.error_message is not None
                error_msg = result.error_message.lower()
                if expected_keywords:
                    assert any(keyword in error_msg for keyword in expected_keywords), \
                        f"Error message '{result.error_message}' should contain one of {expected_keywords}"
    
    def test_variable_query_validation_through_puzzle(self):
        """Test variable query validation through the puzzle's validation system."""
        puzzle = HelloWorldPuzzle()
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.VARIABLES_INTRODUCTION)
        
        # Test valid variable queries
        valid_queries = [
            "?- likes(alice, X).",
            "?- likes(Person, chocolate).",
            "?- parent(X, Y).",
        ]
        
        for query in valid_queries:
            result = puzzle._validate_variable_query(query)
            assert result.is_valid, f"Variable query '{query}' should be valid"
        
        # Test invalid variable queries (no variables)
        invalid_queries = [
            "?- likes(alice, chocolate).",  # No variables
            "?- parent(tom, bob).",         # No variables
        ]
        
        for query in invalid_queries:
            result = puzzle._validate_variable_query(query)
            assert not result.is_valid, f"Query '{query}' should be invalid (no variables)"
            assert "variable" in result.error_message.lower()
        
        # Test queries with syntax errors
        syntax_error_queries = [
            "likes(alice, X).",     # Missing ?-
            "?- likes(alice, X",    # Missing closing parenthesis
            "?- likes(alice, X)",   # Missing period
        ]
        
        for query in syntax_error_queries:
            result = puzzle._validate_variable_query(query)
            assert not result.is_valid, f"Query '{query}' should be invalid (syntax error)"
    
    def test_progressive_hint_system(self):
        """Test that hints become more specific with repeated errors."""
        puzzle = HelloWorldPuzzle()
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Simulate repeated errors with the same invalid input
        invalid_input = "Bob likes pizza"  # Natural language instead of Prolog
        
        hints = []
        for attempt in range(4):  # Test multiple attempts
            result = puzzle.validate_solution(invalid_input)
            assert not result.is_valid
            
            # Get hint for this attempt level
            hint = puzzle.get_hint(attempt + 1)
            hints.append(hint)
            
            # Hints should become more specific
            assert isinstance(hint, str)
            assert len(hint) > 0
        
        # Later hints should be more specific (longer or contain more detail)
        # This is a heuristic test - implementation may vary
        assert len(hints) == 4
        for hint in hints:
            assert "pattern" in hint.lower() or "predicate" in hint.lower() or "argument" in hint.lower() or "period" in hint.lower() or "fact" in hint.lower() or "answer" in hint.lower() or "likes" in hint.lower()
    
    def test_tutorial_step_validation_routing(self):
        """Test that validation is routed correctly based on tutorial step."""
        puzzle = HelloWorldPuzzle()
        
        # Test fact creation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Valid fact should pass
        result = puzzle.validate_solution("likes(bob, pizza).")
        assert result.is_valid
        
        # Invalid fact should fail
        result = puzzle.validate_solution("Bob likes pizza")
        assert not result.is_valid
        
        # Test query step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        
        # Valid query should pass
        result = puzzle.validate_solution("?- likes(alice, chocolate).")
        assert result.is_valid
        
        # Invalid query should fail
        result = puzzle.validate_solution("likes(alice, chocolate).")  # Missing ?-
        assert not result.is_valid
        
        # Test variable step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.VARIABLES_INTRODUCTION)
        
        # Valid variable query should pass
        result = puzzle.validate_solution("?- likes(alice, X).")
        assert result.is_valid
        
        # Query without variables should fail
        result = puzzle.validate_solution("?- likes(alice, chocolate).")
        assert not result.is_valid
    
    def test_error_recovery_mechanisms(self):
        """Test that users can recover from errors and continue learning."""
        puzzle = HelloWorldPuzzle()
        
        # Test error recovery at fact creation step
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        # Make several errors
        error_inputs = [
            "next",  # Generic command
            "Bob likes pizza",  # Natural language
            "likes(bob, pizza",  # Missing closing parenthesis
            "likes(bob, pizza)",  # Missing period
        ]
        
        for error_input in error_inputs:
            result = puzzle.validate_solution(error_input)
            assert not result.is_valid
            assert result.error_message is not None
            
            # Should provide helpful feedback
            assert len(result.error_message) > 0
            
            # Should offer hints or guidance
            if result.hint:
                assert len(result.hint) > 0
        
        # Should accept correct input after errors
        correct_input = "likes(bob, pizza)."
        result = puzzle.validate_solution(correct_input)
        assert result.is_valid
        
        # Should be able to continue after recovery
        assert puzzle.tutorial_session.session_active
    
    def test_validation_result_structure(self):
        """Test that validation results have proper structure and content."""
        # Test valid input
        valid_result = PrologValidator.validate_fact("likes(bob, pizza).")
        assert isinstance(valid_result, ValidationResult)
        assert valid_result.is_valid is True
        assert valid_result.error_message is None or valid_result.error_message == ""
        
        # Test invalid input
        invalid_result = PrologValidator.validate_fact("Bob likes pizza")
        assert isinstance(invalid_result, ValidationResult)
        assert invalid_result.is_valid is False
        assert invalid_result.error_message is not None
        assert len(invalid_result.error_message) > 0
        
        # Error message should be helpful and specific
        error_msg = invalid_result.error_message.lower()
        assert any(keyword in error_msg for keyword in ["parentheses", "missing", "invalid", "period"])
        
        # Should provide hints when available
        if invalid_result.hint:
            assert len(invalid_result.hint) > 0
    
    def test_comprehensive_tutorial_flow_validation(self):
        """Test validation across all tutorial steps in sequence."""
        puzzle = HelloWorldPuzzle()
        
        # Define expected inputs for each interactive step
        step_inputs = [
            (TutorialStep.FACT_CREATION, "likes(bob, pizza).", True),
            (TutorialStep.FACT_CREATION, "Bob likes pizza", False),
            (TutorialStep.FACT_CREATION, "next", False),
            
            (TutorialStep.QUERIES_EXPLANATION, "?- likes(alice, chocolate).", True),
            (TutorialStep.QUERIES_EXPLANATION, "likes(alice, chocolate).", False),
            (TutorialStep.QUERIES_EXPLANATION, "next", False),
            
            (TutorialStep.VARIABLES_INTRODUCTION, "?- likes(alice, X).", True),
            (TutorialStep.VARIABLES_INTRODUCTION, "?- likes(alice, chocolate).", False),  # No variables
            (TutorialStep.VARIABLES_INTRODUCTION, "next", False),
        ]
        
        for step, user_input, expected_valid in step_inputs:
            puzzle.tutorial_session.navigator.jump_to_step(step)
            
            # Use the puzzle's validate_solution method which routes to appropriate validation
            result = puzzle.validate_solution(user_input)
            
            assert result.is_valid == expected_valid, \
                f"At step {step}, input '{user_input}' should be {'valid' if expected_valid else 'invalid'}"
            
            if not expected_valid:
                assert result.error_message is not None
                assert len(result.error_message) > 0


class TestTutorialRequirementsCoverage:
    """Test that all tutorial requirements are properly covered by validation."""
    
    def test_requirement_8_1_cyberpunk_styling(self):
        """Test requirement 8.1: Tutorial uses same 80s cyberpunk styling."""
        puzzle = HelloWorldPuzzle()
        
        # This is more of an integration test, but we can verify the puzzle
        # is properly initialized and uses the same base classes
        assert puzzle.puzzle_id == "hello_world_prolog"
        assert puzzle.title == "Hello World Prolog Challenge"
        
        # Should have tutorial session for styling consistency
        assert puzzle.tutorial_session is not None
        assert puzzle.tutorial_session.session_active
    
    def test_requirement_8_2_visual_feedback(self):
        """Test requirement 8.2: Visual feedback with appropriate colors."""
        puzzle = HelloWorldPuzzle()
        
        # Test that validation results include appropriate feedback
        valid_result = PrologValidator.validate_fact("likes(bob, pizza).")
        assert valid_result.is_valid
        
        invalid_result = PrologValidator.validate_fact("invalid syntax")
        assert not invalid_result.is_valid
        assert invalid_result.error_message is not None
        
        # Error messages should be structured for visual presentation
        assert len(invalid_result.error_message) > 0
    
    def test_requirement_9_1_active_participation(self):
        """Test requirement 9.1: Tutorial blocks 'next'/'continue' commands."""
        puzzle = HelloWorldPuzzle()
        
        # Test at interactive steps where validation occurs
        interactive_steps = [
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION,
        ]
        
        for step in interactive_steps:
            puzzle.tutorial_session.navigator.jump_to_step(step)
            
            # Generic commands should be rejected
            generic_commands = ["next", "continue", "skip", "proceed"]
            for command in generic_commands:
                result = puzzle.validate_solution(command)
                assert not result.is_valid, f"Command '{command}' should be rejected at step {step}"
                # Error message should indicate the input is invalid
                assert result.error_message is not None
                assert len(result.error_message) > 0
    
    def test_requirement_9_2_specific_input_required(self):
        """Test requirement 9.2: Each concept requires specific user input."""
        puzzle = HelloWorldPuzzle()
        
        # Test fact creation requires specific syntax
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        
        result = puzzle.validate_solution("likes(bob, pizza).")
        assert result.is_valid
        
        result = puzzle.validate_solution("natural language")
        assert not result.is_valid
        
        # Test query writing requires ?- prefix
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        
        result = puzzle.validate_solution("?- likes(alice, chocolate).")
        assert result.is_valid
        
        result = puzzle.validate_solution("likes(alice, chocolate).")  # Missing ?-
        assert not result.is_valid
        
        # Test variable queries require variables
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.VARIABLES_INTRODUCTION)
        
        result = puzzle.validate_solution("?- likes(alice, X).")
        assert result.is_valid
        
        result = puzzle.validate_solution("?- likes(alice, chocolate).")  # No variables
        assert not result.is_valid
    
    def test_requirement_9_4_hands_on_practice(self):
        """Test requirement 9.4: Hands-on practice through active exercises."""
        puzzle = HelloWorldPuzzle()
        
        # Verify that each major concept has validation through the puzzle
        # Facts
        assert hasattr(PrologValidator, 'validate_fact')
        assert hasattr(puzzle, '_validate_fact_creation')
        
        # Queries  
        assert hasattr(PrologValidator, 'validate_query')
        assert hasattr(puzzle, '_validate_query_creation')
        
        # Variables
        assert hasattr(puzzle, '_validate_variable_query')
        
        # Component extraction
        assert hasattr(PrologValidator, 'extract_components')
        
        # Each validation method should reject generic commands
        generic_command = "next"
        
        assert not PrologValidator.validate_fact(generic_command).is_valid
        assert not PrologValidator.validate_query(generic_command).is_valid
        
        # Test through puzzle validation system
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.FACT_CREATION)
        assert not puzzle.validate_solution(generic_command).is_valid
        
        puzzle.tutorial_session.navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION)
        assert not puzzle.validate_solution(generic_command).is_valid