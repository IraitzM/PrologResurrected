"""
Tests for Memory Stack Puzzle completion and scoring functionality.

Validates Requirements 5.2, 5.4, 5.5, 7.5:
- Completion flag setting on correct diagnosis
- Score calculation based on queries and hints used
- Complexity multiplier in scoring
- Completion explanation with educational content
- Real-world debugging connections
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackPuzzle,
    FailureScenario,
)
from prologresurrected.game.complexity import ComplexityLevel


class TestPuzzleCompletion:
    """Test puzzle completion flag and state management."""
    
    def test_puzzle_starts_incomplete(self):
        """Test that puzzle starts in incomplete state."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        assert puzzle.completed is False
        assert puzzle.diagnosis_submitted is False
    
    def test_correct_diagnosis_marks_complete(self):
        """Test that correct diagnosis marks puzzle as complete."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Submit correct diagnosis
        result = puzzle.validate_solution("diagnose memory leak - allocated memory not freed")
        
        assert result.is_valid is True
        assert puzzle.completed is True
        assert puzzle.diagnosis_submitted is True
    
    def test_incorrect_diagnosis_keeps_incomplete(self):
        """Test that incorrect diagnosis keeps puzzle incomplete."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Submit incorrect diagnosis
        result = puzzle.validate_solution("diagnose stack overflow")
        
        assert result.is_valid is False
        assert puzzle.completed is False
        assert puzzle.diagnosis_submitted is True
    
    def test_partial_diagnosis_keeps_incomplete(self):
        """Test that partial diagnosis keeps puzzle incomplete."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Submit partial diagnosis
        result = puzzle.validate_solution("diagnose memory problem")
        
        assert result.is_valid is False
        assert puzzle.completed is False


class TestScoreCalculation:
    """Test score calculation with various factors."""
    
    def test_perfect_score_no_queries_no_hints(self):
        """Test perfect score with minimal queries and no hints."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Make a few efficient queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- allocated(Id, Bytes).")
        puzzle.validate_solution("?- frame(Id, allocate_buffer, Time, Status).")
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        # Calculate score
        score = puzzle._calculate_score()
        
        # Should have high score (base 100, no penalties, BEGINNER multiplier 1.0)
        assert score >= 90
        assert score <= 100
    
    def test_score_with_query_penalty(self):
        """Test that excessive queries reduce score."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Make many queries (more than optimal)
        for i in range(15):
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        # Calculate score
        score = puzzle._calculate_score()
        
        # Should have reduced score due to query penalty
        assert score < 90
    
    def test_score_with_hint_penalty(self):
        """Test that hints reduce score."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Make a few queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        # Use hints
        puzzle.request_hint()
        puzzle.request_hint()
        puzzle.request_hint()
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        # Calculate score
        score = puzzle._calculate_score()
        
        # Should have reduced score due to hint penalty
        assert score < 90
    
    def test_complexity_multiplier_beginner(self):
        """Test complexity multiplier for BEGINNER level."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Make efficient queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- allocated(Id, Bytes).")
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        score = puzzle._calculate_score()
        
        # BEGINNER multiplier is 1.0
        assert score >= 90
        assert score <= 100
    
    def test_complexity_multiplier_expert(self):
        """Test complexity multiplier for EXPERT level."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Make efficient queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- allocated(Id, Bytes).")
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        score = puzzle._calculate_score()
        
        # EXPERT multiplier is 2.0, so score should be higher
        assert score >= 180  # Base ~90-100 * 2.0
    
    def test_minimum_score_floor(self):
        """Test that score has a minimum floor even with many penalties."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Make excessive queries
        for i in range(50):
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        # Use many hints
        for i in range(10):
            puzzle.request_hint()
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        score = puzzle._calculate_score()
        
        # Should still have minimum score
        assert score >= 10


class TestCompletionStatistics:
    """Test completion statistics and reporting."""
    
    def test_statistics_before_completion(self):
        """Test statistics before puzzle is completed."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        stats = puzzle.get_completion_statistics()
        
        assert stats["completed"] is False
        assert "message" in stats
    
    def test_statistics_after_completion(self):
        """Test comprehensive statistics after completion."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Make some queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- allocated(Id, Bytes).")
        puzzle.validate_solution("?- status(Id, error).")
        
        # Use a hint
        puzzle.request_hint()
        
        # Submit correct diagnosis
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        
        # Verify all required fields
        assert stats["completed"] is True
        assert stats["scenario_type"] == "memory_leak"
        assert stats["complexity_level"] == "intermediate"
        assert stats["queries_made"] == 3
        assert stats["hints_used"] == 1
        assert "discoveries_found" in stats
        assert "score_breakdown" in stats
        assert "efficiency_rating" in stats
        assert "educational_summary" in stats
    
    def test_score_breakdown_components(self):
        """Test that score breakdown includes all components."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Make queries and complete
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        breakdown = stats["score_breakdown"]
        
        # Verify all score components
        assert "base_score" in breakdown
        assert "query_penalty" in breakdown
        assert "hint_penalty" in breakdown
        assert "score_before_multiplier" in breakdown
        assert "complexity_multiplier" in breakdown
        assert "final_score" in breakdown
        
        # Verify calculations are consistent
        expected_before_multiplier = (
            breakdown["base_score"] 
            - breakdown["query_penalty"] 
            - breakdown["hint_penalty"]
        )
        assert breakdown["score_before_multiplier"] == max(10, expected_before_multiplier)
    
    def test_efficiency_ratings(self):
        """Test efficiency rating calculations."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Efficient completion
        for i in range(5):
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        efficiency = stats["efficiency_rating"]
        
        assert "query_efficiency" in efficiency
        assert "hint_efficiency" in efficiency
        assert efficiency["query_efficiency"] == "Excellent"
        assert efficiency["hint_efficiency"] == "Perfect"


class TestEducationalContent:
    """Test educational content and real-world connections."""
    
    def test_educational_summary_present(self):
        """Test that educational summary is included in completion."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        edu_summary = stats["educational_summary"]
        
        # Verify educational content structure
        assert "concept" in edu_summary
        assert "real_world_application" in edu_summary
        assert "debugging_techniques" in edu_summary
        assert "prolog_connection" in edu_summary
        assert "skills_practiced" in edu_summary
    
    def test_memory_leak_educational_content(self):
        """Test educational content for memory leak scenario."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        puzzle.validate_solution("diagnose memory leak")
        stats = puzzle.get_completion_statistics()
        edu_summary = stats["educational_summary"]
        
        assert "Memory Leak" in edu_summary["concept"]
        assert len(edu_summary["debugging_techniques"]) > 0
        assert "memory" in edu_summary["real_world_application"].lower()
    
    def test_stack_overflow_educational_content(self):
        """Test educational content for stack overflow scenario."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.STACK_OVERFLOW, seed=42)
        
        puzzle.validate_solution("diagnose stack overflow")
        stats = puzzle.get_completion_statistics()
        edu_summary = stats["educational_summary"]
        
        assert "Stack Overflow" in edu_summary["concept"]
        assert len(edu_summary["debugging_techniques"]) > 0
        assert "recursive" in edu_summary["real_world_application"].lower()
    
    def test_null_pointer_educational_content(self):
        """Test educational content for null pointer scenario."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.NULL_POINTER, seed=42)
        
        puzzle.validate_solution("diagnose null pointer")
        stats = puzzle.get_completion_statistics()
        edu_summary = stats["educational_summary"]
        
        assert "Null Pointer" in edu_summary["concept"]
        assert len(edu_summary["debugging_techniques"]) > 0
        assert "null" in edu_summary["real_world_application"].lower()
    
    def test_deadlock_educational_content(self):
        """Test educational content for deadlock scenario."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.DEADLOCK, seed=42)
        
        puzzle.validate_solution("diagnose deadlock")
        stats = puzzle.get_completion_statistics()
        edu_summary = stats["educational_summary"]
        
        assert "Deadlock" in edu_summary["concept"]
        assert len(edu_summary["debugging_techniques"]) > 0
        assert "lock" in edu_summary["real_world_application"].lower()
    
    def test_resource_exhaustion_educational_content(self):
        """Test educational content for resource exhaustion scenario."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.RESOURCE_EXHAUSTION, seed=42)
        
        puzzle.validate_solution("diagnose resource exhaustion")
        stats = puzzle.get_completion_statistics()
        edu_summary = stats["educational_summary"]
        
        assert "Resource Exhaustion" in edu_summary["concept"]
        assert len(edu_summary["debugging_techniques"]) > 0
        assert "resource" in edu_summary["real_world_application"].lower()
    
    def test_skills_practiced_list(self):
        """Test that skills practiced list is comprehensive."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        puzzle.validate_solution("diagnose memory leak")
        stats = puzzle.get_completion_statistics()
        skills = stats["educational_summary"]["skills_practiced"]
        
        # Should have multiple skills listed
        assert len(skills) >= 4
        
        # Check for key skills
        skills_text = " ".join(skills).lower()
        assert "logical reasoning" in skills_text or "pattern" in skills_text
        assert "investigation" in skills_text or "analysis" in skills_text


class TestCompletionFeedback:
    """Test completion feedback and narrative integration."""
    
    def test_completion_includes_score_info(self):
        """Test that completion feedback includes score information."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        result = puzzle.validate_solution("diagnose memory leak")
        
        # Check that score is in parsed components
        assert "score" in result.parsed_components
        assert result.parsed_components["score"] > 0
        assert "statistics" in result.parsed_components
    
    def test_completion_narrative_present(self):
        """Test that completion includes narrative conclusion."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        result = puzzle.validate_solution("diagnose memory leak")
        
        # Completion narrative should be in the error_message (which contains full feedback)
        # Since is_valid is True, error_message is None, but we can check parsed_components
        assert result.parsed_components["is_correct"] is True
        assert result.parsed_components["explanation"] is not None
    
    def test_score_formatting(self):
        """Test that score information is properly formatted."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        formatted = puzzle._format_score_information(stats)
        
        # Check formatting includes key elements
        assert "PERFORMANCE ANALYSIS" in formatted
        assert "SCORE BREAKDOWN" in formatted
        assert "FINAL SCORE" in formatted
        assert "Complexity Level" in formatted
        assert "Queries Made" in formatted


class TestQueryEfficiency:
    """Test query efficiency calculations and ratings."""
    
    def test_excellent_efficiency_rating(self):
        """Test excellent efficiency rating for optimal queries."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Make 5 queries (optimal range)
        for i in range(5):
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        puzzle.validate_solution("diagnose memory leak")
        stats = puzzle.get_completion_statistics()
        
        assert stats["efficiency_rating"]["query_efficiency"] == "Excellent"
        assert stats["score_breakdown"]["query_penalty"] == 0
    
    def test_good_efficiency_rating(self):
        """Test good efficiency rating for moderate queries."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Make 10 queries (moderate range)
        for i in range(10):
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        puzzle.validate_solution("diagnose memory leak")
        stats = puzzle.get_completion_statistics()
        
        assert stats["efficiency_rating"]["query_efficiency"] == "Good"
        assert stats["score_breakdown"]["query_penalty"] > 0
        assert stats["score_breakdown"]["query_penalty"] <= 12
    
    def test_needs_improvement_efficiency_rating(self):
        """Test efficiency rating for excessive queries."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Make 20 queries (excessive)
        for i in range(20):
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
        
        puzzle.validate_solution("diagnose memory leak")
        stats = puzzle.get_completion_statistics()
        
        assert stats["efficiency_rating"]["query_efficiency"] == "Could be improved"
        assert stats["score_breakdown"]["query_penalty"] > 12


class TestIntegrationWithBasePuzzle:
    """Test integration with BasePuzzle scoring system."""
    
    def test_uses_base_puzzle_complexity_multiplier(self):
        """Test that complexity multiplier from BasePuzzle is used."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Test at different complexity levels
        for level in [ComplexityLevel.BEGINNER, ComplexityLevel.INTERMEDIATE, 
                      ComplexityLevel.ADVANCED, ComplexityLevel.EXPERT]:
            puzzle.reset()
            puzzle.set_complexity_level(level)
            
            puzzle.validate_solution("?- frame(X, Y, Z, W).")
            puzzle.validate_solution("diagnose memory leak")
            
            stats = puzzle.get_completion_statistics()
            multiplier = stats["score_breakdown"]["complexity_multiplier"]
            
            # Verify multiplier increases with complexity
            if level == ComplexityLevel.BEGINNER:
                assert multiplier == 1.0
            elif level == ComplexityLevel.EXPERT:
                assert multiplier == 2.0
    
    def test_hint_penalty_uses_hint_system(self):
        """Test that hint penalty uses the hint system calculation."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Use hints
        puzzle.request_hint()
        puzzle.request_hint()
        
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        hint_penalty = stats["score_breakdown"]["hint_penalty"]
        
        # Should have some penalty for hints
        assert hint_penalty > 0
