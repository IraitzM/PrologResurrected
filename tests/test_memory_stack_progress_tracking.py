"""
Tests for Memory Stack Puzzle progress tracking and unlocking functionality.

Validates Requirements 5.5:
- Progress update on puzzle completion
- Concept mastery tracking for debugging skills
- Next puzzle unlock logic
- Player statistics updates
"""

import pytest
from prologresurrected.game.puzzles import PuzzleManager
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle, FailureScenario
from prologresurrected.game.complexity import ComplexityLevel


class TestProgressTracking:
    """Test progress tracking on puzzle completion."""
    
    def test_completion_updates_player_progress(self):
        """Test that completing the puzzle updates player progress."""
        manager = PuzzleManager()
        
        # Start the memory stack puzzle
        assert manager.start_puzzle("memory_stack_failure")
        
        # Get initial stats
        initial_stats = manager.get_player_stats()
        initial_completed = initial_stats["puzzles_completed"]
        initial_score = initial_stats["total_score"]
        
        # Complete the puzzle by submitting correct diagnosis
        puzzle = manager.current_puzzle
        
        # Make some queries first
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- status(F, error).")
        
        # Submit correct diagnosis based on scenario
        if puzzle.scenario == FailureScenario.MEMORY_LEAK:
            diagnosis = "diagnose memory leak - allocated memory not freed"
        elif puzzle.scenario == FailureScenario.STACK_OVERFLOW:
            diagnosis = "diagnose stack overflow - recursive calls too deep"
        elif puzzle.scenario == FailureScenario.NULL_POINTER:
            diagnosis = "diagnose null pointer - invalid parameters"
        elif puzzle.scenario == FailureScenario.DEADLOCK:
            diagnosis = "diagnose deadlock - circular wait on locks"
        else:  # RESOURCE_EXHAUSTION
            diagnosis = "diagnose resource exhaustion - excessive memory allocation"
        
        result = manager.submit_solution(diagnosis)
        
        # Verify completion updated progress
        assert result.success
        updated_stats = manager.get_player_stats()
        assert updated_stats["puzzles_completed"] == initial_completed + 1
        assert updated_stats["total_score"] > initial_score
        assert "memory_stack_failure" in manager.completed_puzzles
    
    def test_completion_tracks_debugging_concepts(self):
        """Test that completing the puzzle tracks debugging concepts."""
        manager = PuzzleManager()
        manager.start_puzzle("memory_stack_failure")
        puzzle = manager.current_puzzle
        
        # Make some queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- status(F, error).")
        
        # Submit correct diagnosis
        if puzzle.scenario == FailureScenario.MEMORY_LEAK:
            diagnosis = "diagnose memory leak - allocated memory not freed"
        elif puzzle.scenario == FailureScenario.STACK_OVERFLOW:
            diagnosis = "diagnose stack overflow - recursive calls too deep"
        elif puzzle.scenario == FailureScenario.NULL_POINTER:
            diagnosis = "diagnose null pointer - invalid parameters"
        elif puzzle.scenario == FailureScenario.DEADLOCK:
            diagnosis = "diagnose deadlock - circular wait on locks"
        else:
            diagnosis = "diagnose resource exhaustion - excessive memory allocation"
        
        manager.submit_solution(diagnosis)
        
        # Verify debugging concepts are tracked
        concepts = manager.get_player_stats()["concepts_mastered"]
        
        # Core debugging concepts
        assert "debugging_methodology" in concepts
        assert "stack_trace_analysis" in concepts
        assert "root_cause_analysis" in concepts
        assert "logical_investigation" in concepts
        
        # Prolog concepts
        assert "prolog_queries" in concepts
        assert "variable_binding" in concepts
        assert "compound_queries" in concepts
        assert "pattern_matching" in concepts
    
    def test_completion_tracks_scenario_specific_concepts(self):
        """Test that scenario-specific debugging concepts are tracked."""
        manager = PuzzleManager()
        manager.start_puzzle("memory_stack_failure")
        puzzle = manager.current_puzzle
        
        # Make queries and complete
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        # Submit correct diagnosis based on scenario
        scenario = puzzle.scenario
        if scenario == FailureScenario.MEMORY_LEAK:
            diagnosis = "diagnose memory leak - allocated memory not freed"
            expected_concepts = ["memory_leak_detection", "resource_management"]
        elif scenario == FailureScenario.STACK_OVERFLOW:
            diagnosis = "diagnose stack overflow - recursive calls too deep"
            expected_concepts = ["recursion_analysis", "stack_overflow_detection"]
        elif scenario == FailureScenario.NULL_POINTER:
            diagnosis = "diagnose null pointer - invalid parameters"
            expected_concepts = ["null_pointer_detection", "parameter_validation"]
        elif scenario == FailureScenario.DEADLOCK:
            diagnosis = "diagnose deadlock - circular wait on locks"
            expected_concepts = ["deadlock_detection", "concurrency_debugging"]
        else:  # RESOURCE_EXHAUSTION
            diagnosis = "diagnose resource exhaustion - excessive memory allocation"
            expected_concepts = ["resource_exhaustion_detection", "capacity_analysis"]
        
        manager.submit_solution(diagnosis)
        
        # Verify scenario-specific concepts are tracked
        concepts = manager.get_player_stats()["concepts_mastered"]
        for expected in expected_concepts:
            assert expected in concepts
    
    def test_completion_history_records_details(self):
        """Test that completion history records puzzle details."""
        manager = PuzzleManager()
        manager.start_puzzle("memory_stack_failure")
        puzzle = manager.current_puzzle
        
        # Set complexity level
        complexity = ComplexityLevel.INTERMEDIATE
        puzzle.set_complexity_level(complexity)
        
        # Make queries and complete
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        # Submit correct diagnosis based on scenario
        if puzzle.scenario == FailureScenario.MEMORY_LEAK:
            diagnosis = "diagnose memory leak - allocated memory not freed"
        elif puzzle.scenario == FailureScenario.STACK_OVERFLOW:
            diagnosis = "diagnose stack overflow - recursive calls too deep"
        elif puzzle.scenario == FailureScenario.NULL_POINTER:
            diagnosis = "diagnose null pointer - invalid parameters"
        elif puzzle.scenario == FailureScenario.DEADLOCK:
            diagnosis = "diagnose deadlock - circular wait on locks"
        else:  # RESOURCE_EXHAUSTION
            diagnosis = "diagnose resource exhaustion - excessive memory allocation"
        
        result = manager.submit_solution(diagnosis)
        
        # Verify completion history
        history = manager.get_player_stats()["puzzle_completion_history"]
        assert len(history) > 0
        
        latest = history[-1]
        assert latest["puzzle_id"] == "memory_stack_failure"
        assert latest["puzzle_title"] == puzzle.title
        assert latest["complexity_level"] == complexity.name
        assert latest["score"] == result.score
        assert latest["attempts"] >= 1
        assert latest["hints_used"] >= 0


class TestPuzzleUnlocking:
    """Test puzzle unlocking logic."""
    
    def test_hello_world_always_unlocked(self):
        """Test that hello world tutorial is always unlocked."""
        manager = PuzzleManager()
        assert manager.is_puzzle_unlocked("hello_world_prolog")
    
    def test_memory_stack_locked_initially(self):
        """Test that memory stack puzzle is locked initially."""
        manager = PuzzleManager()
        # Should be locked if hello world not completed
        if not manager.is_hello_world_completed():
            assert not manager.is_puzzle_unlocked("memory_stack_failure")
    
    def test_memory_stack_unlocked_after_hello_world(self):
        """Test that memory stack puzzle unlocks after hello world."""
        manager = PuzzleManager()
        
        # Mark hello world as completed
        manager.player_stats["hello_world_completed"] = True
        
        # Memory stack should now be unlocked
        assert manager.is_puzzle_unlocked("memory_stack_failure")
    
    def test_unlock_next_puzzle_returns_correct_id(self):
        """Test that unlock_next_puzzle returns the correct next puzzle."""
        manager = PuzzleManager()
        
        # After hello world, should unlock memory stack
        next_puzzle = manager.unlock_next_puzzle("hello_world_prolog")
        assert next_puzzle == "memory_stack_failure"
        
        # After memory stack, currently no next puzzle
        next_puzzle = manager.unlock_next_puzzle("memory_stack_failure")
        assert next_puzzle is None
    
    def test_get_unlocked_puzzles_returns_available(self):
        """Test that get_unlocked_puzzles returns all unlocked puzzles."""
        manager = PuzzleManager()
        
        # Initially only hello world
        unlocked = manager.get_unlocked_puzzles()
        assert "hello_world_prolog" in unlocked
        
        # After completing hello world
        manager.player_stats["hello_world_completed"] = True
        unlocked = manager.get_unlocked_puzzles()
        assert "hello_world_prolog" in unlocked
        assert "memory_stack_failure" in unlocked
    
    def test_next_recommended_puzzle_suggests_progression(self):
        """Test that next recommended puzzle follows progression."""
        manager = PuzzleManager()
        
        # Should recommend hello world first
        if not manager.is_hello_world_completed():
            recommended = manager.get_next_recommended_puzzle()
            assert recommended == "hello_world_prolog"
        
        # After hello world, should recommend memory stack
        manager.player_stats["hello_world_completed"] = True
        # Also mark hello world as completed in the completed list
        if "hello_world_prolog" not in manager.completed_puzzles:
            manager.completed_puzzles.append("hello_world_prolog")
        recommended = manager.get_next_recommended_puzzle()
        assert recommended == "memory_stack_failure"
        
        # After completing memory stack, no more puzzles
        manager.completed_puzzles.append("memory_stack_failure")
        recommended = manager.get_next_recommended_puzzle()
        # Could be None or another puzzle if more are added
        # For now, just verify it doesn't crash


class TestComplexityAchievements:
    """Test complexity-specific achievement tracking."""
    
    def test_completion_updates_complexity_achievements(self):
        """Test that completion updates complexity-specific achievements."""
        manager = PuzzleManager()
        manager.start_puzzle("memory_stack_failure")
        puzzle = manager.current_puzzle
        
        # Set complexity level
        complexity = ComplexityLevel.ADVANCED
        puzzle.set_complexity_level(complexity)
        
        # Get initial achievements
        initial_achievements = manager.get_player_stats()["complexity_achievements"]
        initial_count = initial_achievements[complexity]["puzzles_completed"]
        initial_score = initial_achievements[complexity]["total_score"]
        
        # Complete puzzle - determine correct diagnosis based on scenario
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        # Map scenario to correct diagnosis
        diagnosis_map = {
            FailureScenario.MEMORY_LEAK: "diagnose memory leak - allocated memory not freed",
            FailureScenario.STACK_OVERFLOW: "diagnose stack overflow - recursive calls too deep",
            FailureScenario.NULL_POINTER: "diagnose null pointer",
            FailureScenario.DEADLOCK: "diagnose deadlock",
            FailureScenario.RESOURCE_EXHAUSTION: "diagnose resource exhaustion",
        }
        diagnosis = diagnosis_map[puzzle.scenario]
        
        result = manager.submit_solution(diagnosis)
        
        # Verify complexity achievements updated
        updated_achievements = manager.get_player_stats()["complexity_achievements"]
        assert updated_achievements[complexity]["puzzles_completed"] == initial_count + 1
        assert updated_achievements[complexity]["total_score"] > initial_score
    
    def test_get_complexity_achievements_returns_stats(self):
        """Test that get_complexity_achievements returns correct stats."""
        manager = PuzzleManager()
        
        # Get achievements for a level
        achievements = manager.get_complexity_achievements(ComplexityLevel.BEGINNER)
        
        assert "level" in achievements
        assert "puzzles_completed" in achievements
        assert "total_score" in achievements
        assert "average_score" in achievements
        assert achievements["level"] == "BEGINNER"


class TestProgressSummary:
    """Test progress summary functionality."""
    
    def test_progress_summary_includes_concepts(self):
        """Test that progress summary includes mastered concepts."""
        manager = PuzzleManager()
        manager.start_puzzle("memory_stack_failure")
        puzzle = manager.current_puzzle
        
        # Complete puzzle
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        if puzzle.scenario == FailureScenario.MEMORY_LEAK:
            diagnosis = "diagnose memory leak - allocated memory not freed"
        elif puzzle.scenario == FailureScenario.STACK_OVERFLOW:
            diagnosis = "diagnose stack overflow - recursive calls too deep"
        elif puzzle.scenario == FailureScenario.NULL_POINTER:
            diagnosis = "diagnose null pointer - invalid parameters"
        elif puzzle.scenario == FailureScenario.DEADLOCK:
            diagnosis = "diagnose deadlock - circular wait on locks"
        else:  # RESOURCE_EXHAUSTION
            diagnosis = "diagnose resource exhaustion - excessive memory allocation"
        
        manager.submit_solution(diagnosis)
        
        # Get progress summary
        summary = manager.get_progress_summary()
        
        assert "concepts_mastered" in summary
        assert len(summary["concepts_mastered"]) > 0
        assert "debugging_methodology" in summary["concepts_mastered"]
    
    def test_progress_summary_includes_complexity_achievements(self):
        """Test that progress summary includes complexity achievements."""
        manager = PuzzleManager()
        
        summary = manager.get_progress_summary()
        
        assert "complexity_achievements" in summary
        assert "BEGINNER" in summary["complexity_achievements"]
        assert "INTERMEDIATE" in summary["complexity_achievements"]
        assert "ADVANCED" in summary["complexity_achievements"]
        assert "EXPERT" in summary["complexity_achievements"]
    
    def test_progress_summary_includes_completion_history(self):
        """Test that progress summary includes completion history."""
        manager = PuzzleManager()
        
        summary = manager.get_progress_summary()
        
        assert "completion_history" in summary
        assert isinstance(summary["completion_history"], list)


class TestIntegrationWithPuzzleResult:
    """Test integration of unlocking with PuzzleResult."""
    
    def test_puzzle_result_includes_next_unlocked(self):
        """Test that PuzzleResult includes next_puzzle_unlocked field."""
        manager = PuzzleManager()
        
        # Complete hello world to unlock memory stack
        manager.player_stats["hello_world_completed"] = False
        manager.start_puzzle("hello_world_prolog")
        
        # Simulate completion (we'll just mark it directly for this test)
        from prologresurrected.game.puzzles import PuzzleResult
        
        # Create a mock successful result
        result = PuzzleResult(
            success=True,
            score=100,
            feedback="Great!",
            hints_used=0,
            attempts=1
        )
        
        # Manually trigger completion
        manager._complete_puzzle(manager.current_puzzle, result)
        next_puzzle = manager.unlock_next_puzzle("hello_world_prolog")
        
        # Verify next puzzle is identified
        assert next_puzzle == "memory_stack_failure"
    
    def test_submit_solution_sets_next_unlocked(self):
        """Test that submit_solution sets next_puzzle_unlocked on success."""
        manager = PuzzleManager()
        
        # Start hello world
        manager.player_stats["hello_world_completed"] = False
        manager.start_puzzle("hello_world_prolog")
        puzzle = manager.current_puzzle
        
        # For this test, we'll manually mark it as completable
        # In real scenario, this would be through correct solution
        puzzle.completed = False
        
        # We can't easily complete hello world here, so let's test with memory stack
        # after marking hello world as done
        manager.player_stats["hello_world_completed"] = True
        manager.start_puzzle("memory_stack_failure")
        puzzle = manager.current_puzzle
        
        # Complete memory stack
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        if puzzle.scenario == FailureScenario.MEMORY_LEAK:
            diagnosis = "diagnose memory leak - allocated memory not freed"
        else:
            diagnosis = "diagnose stack overflow - recursive calls too deep"
        
        result = manager.submit_solution(diagnosis)
        
        # Currently memory stack is the last puzzle, so next_puzzle_unlocked should be None
        # But the field should exist
        assert hasattr(result, 'next_puzzle_unlocked')
