"""
Integration tests for Memory Stack Puzzle game state integration.

Tests the integration between GameState and MemoryStackPuzzle,
verifying that puzzle launch, query handling, diagnosis submission,
and hint requests work correctly.

Validates: Requirements 2.2, 2.3, 4.1, 5.1
"""

import pytest
from prologresurrected.prologresurrected import GameState
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle, FailureScenario
from prologresurrected.game.complexity import ComplexityLevel


class TestMemoryStackGameIntegration:
    """Test Memory Stack Puzzle integration with GameState."""
    
    def test_puzzle_can_be_launched_from_adventure_mode(self):
        """
        Test that the Memory Stack puzzle can be launched from adventure mode.
        
        Validates: Requirement 2.2 (puzzle launch)
        """
        # Create game state in adventure mode
        state = GameState()
        state.game_mode = "adventure"
        state.current_screen = "adventure"
        
        # Launch the puzzle
        state._launch_memory_stack_puzzle()
        
        # Verify puzzle is active
        assert hasattr(state, '_current_adventure_puzzle')
        assert state._current_adventure_puzzle is not None
        assert state._current_adventure_puzzle.puzzle_id == "memory_stack_failure"
        
        # Verify terminal output includes puzzle description
        terminal_text = "\n".join(state.terminal_output)
        assert "MEMORY STACK INVESTIGATION" in terminal_text
        assert "LOGIC-1" in terminal_text
    
    def test_query_input_is_handled_correctly(self):
        """
        Test that query input is routed to the puzzle and results are displayed.
        
        Validates: Requirement 2.2, 2.3 (query execution and display)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        state._current_adventure_puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Clear terminal for clean test
        state.terminal_output = []
        
        # Submit a query
        state._handle_puzzle_input("?- frame(X, Y, Z, W).")
        
        # Verify query was processed
        terminal_text = "\n".join(state.terminal_output)
        assert "Found" in terminal_text or "result" in terminal_text.lower()
        
        # Verify puzzle tracked the query
        assert len(state._current_adventure_puzzle.queries_made) > 0
    
    def test_diagnosis_submission_works(self):
        """
        Test that diagnosis submission is handled correctly.
        
        Validates: Requirement 5.1 (diagnosis submission)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        state._current_adventure_puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Clear terminal for clean test
        state.terminal_output = []
        
        # Submit a diagnosis
        state._handle_puzzle_input("diagnose memory leak")
        
        # Verify diagnosis was processed
        terminal_text = "\n".join(state.terminal_output)
        assert "diagnosis" in terminal_text.lower() or "correct" in terminal_text.lower()
        
        # Note: If diagnosis is correct, puzzle will be completed and cleared
        # So we just verify the terminal output shows it was processed
    
    def test_hint_request_uses_puzzle_hint_system(self):
        """
        Test that hint requests are routed to the puzzle's hint system.
        
        Validates: Requirement 4.1 (hint integration)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        state._current_adventure_puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Clear terminal for clean test
        state.terminal_output = []
        
        # Request a hint
        state._handle_puzzle_input("hint")
        
        # Verify hint was displayed
        terminal_text = "\n".join(state.terminal_output)
        assert len(terminal_text) > 0  # Some hint text should be displayed
        
        # Verify puzzle tracked the hint
        assert state._current_adventure_puzzle.hints_used > 0
    
    def test_exit_puzzle_returns_to_adventure_mode(self):
        """
        Test that exiting a puzzle returns to adventure mode.
        
        Validates: Requirement 2.2 (puzzle lifecycle)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        
        # Exit the puzzle
        state._handle_puzzle_input("exit puzzle")
        
        # Verify puzzle is no longer active
        assert state._current_adventure_puzzle is None
        
        # Verify terminal shows exit message
        terminal_text = "\n".join(state.terminal_output)
        assert "Exiting" in terminal_text or "Returning" in terminal_text
    
    def test_puzzle_completion_updates_player_stats(self):
        """
        Test that completing a puzzle updates player statistics.
        
        Validates: Requirement 5.2, 5.4 (completion and scoring)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        state._current_adventure_puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Record initial score
        initial_score = state.player_score
        initial_concepts = len(state.concepts_learned)
        
        # Mark puzzle as completed (simulate correct diagnosis)
        state._current_adventure_puzzle.completed = True
        
        # Handle completion
        state._handle_puzzle_completion()
        
        # Verify score increased
        assert state.player_score > initial_score
        
        # Verify concepts were added
        assert len(state.concepts_learned) > initial_concepts
        
        # Verify puzzle is no longer active
        assert state._current_adventure_puzzle is None
    
    def test_query_results_are_formatted_correctly(self):
        """
        Test that query results are formatted and displayed properly.
        
        Validates: Requirement 2.3 (result formatting)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        state._current_adventure_puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Clear terminal for clean test
        state.terminal_output = []
        
        # Submit a query that should return results
        state._handle_puzzle_input("?- frame(1, X, Y, Z).")
        
        # Verify results are formatted
        terminal_text = "\n".join(state.terminal_output)
        
        # Should contain result indicators
        assert any(keyword in terminal_text.lower() for keyword in [
            "found", "result", "yes", "match"
        ])
    
    def test_invalid_query_shows_error_message(self):
        """
        Test that invalid queries display appropriate error messages.
        
        Validates: Requirement 2.1, 2.5 (query validation)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        state._current_adventure_puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Clear terminal for clean test
        state.terminal_output = []
        
        # Submit an invalid query (missing period)
        state._handle_puzzle_input("?- frame(X, Y, Z, W)")
        
        # Verify error message is displayed
        terminal_text = "\n".join(state.terminal_output)
        assert any(keyword in terminal_text.lower() for keyword in [
            "error", "invalid", "missing", "period"
        ])
    
    def test_complexity_level_is_applied_to_puzzle(self):
        """
        Test that the game's complexity level is applied to the puzzle.
        
        Validates: Requirement 6.1, 6.2 (complexity adaptation)
        """
        # Create game state at EXPERT level
        state = GameState()
        state.game_mode = "adventure"
        state.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Launch the puzzle
        state._launch_memory_stack_puzzle()
        
        # Verify puzzle has the correct complexity level
        assert state._current_adventure_puzzle.current_complexity_level == ComplexityLevel.EXPERT
        
        # Verify puzzle description reflects complexity level
        # (EXPERT should not have beginner templates)
        description = state._current_adventure_puzzle.get_description()
        assert "MENTOR NOTE" not in description  # Beginner-specific guidance


class TestPuzzleInputRouting:
    """Test that input is correctly routed when in puzzle mode."""
    
    def test_adventure_input_routes_to_puzzle_when_active(self):
        """
        Test that adventure mode input is routed to puzzle handler when puzzle is active.
        
        Validates: Requirement 2.2 (input routing)
        """
        # Create game state with active puzzle
        state = GameState()
        state.game_mode = "adventure"
        state._current_adventure_puzzle = MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
        
        # Clear terminal
        state.terminal_output = []
        
        # Submit input through adventure handler
        state._handle_adventure_input("?- frame(X, Y, Z, W).")
        
        # Verify it was processed as a puzzle query
        assert len(state._current_adventure_puzzle.queries_made) > 0
    
    def test_adventure_commands_work_without_active_puzzle(self):
        """
        Test that adventure mode commands work when no puzzle is active.
        
        Validates: Requirement 2.2 (mode switching)
        """
        # Create game state without active puzzle
        state = GameState()
        state.game_mode = "adventure"
        
        # Clear terminal
        state.terminal_output = []
        
        # Submit a help command
        state._handle_adventure_input("help")
        
        # Verify help was displayed
        terminal_text = "\n".join(state.terminal_output)
        assert "commands" in terminal_text.lower() or "help" in terminal_text.lower()
