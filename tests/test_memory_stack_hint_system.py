"""
Tests for MemoryStackHintSystem

Validates Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackHintSystem,
    FailureScenario,
)
from prologresurrected.game.complexity import ComplexityLevel


class TestMemoryStackHintSystemInitialization:
    """Test hint system initialization."""
    
    def test_initialization_with_scenario(self):
        """Test hint system initializes with scenario type."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        
        assert hint_system.scenario_type == FailureScenario.MEMORY_LEAK
        assert hint_system.queries_made == 0
        assert hint_system.discoveries == set()
        assert hint_system.hint_count == 0
    
    def test_initialization_defaults_to_beginner(self):
        """Test hint system defaults to BEGINNER complexity level."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        
        assert hint_system.current_complexity_level == ComplexityLevel.BEGINNER


class TestProgressTracking:
    """Test progress tracking functionality (Requirement 4.1)."""
    
    def test_update_progress_queries(self):
        """Test updating queries made count."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        
        hint_system.update_progress(5, set())
        
        assert hint_system.queries_made == 5
    
    def test_update_progress_discoveries(self):
        """Test updating discoveries set."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        
        discoveries = {"error", "memory_anomaly"}
        hint_system.update_progress(3, discoveries)
        
        assert hint_system.discoveries == discoveries
    
    def test_update_progress_both(self):
        """Test updating both queries and discoveries."""
        hint_system = MemoryStackHintSystem(FailureScenario.NULL_POINTER)
        
        discoveries = {"null_parameter"}
        hint_system.update_progress(7, discoveries)
        
        assert hint_system.queries_made == 7
        assert hint_system.discoveries == discoveries
    
    def test_reset_progress(self):
        """Test resetting progress tracking."""
        hint_system = MemoryStackHintSystem(FailureScenario.DEADLOCK)
        
        # Set some progress
        hint_system.update_progress(10, {"deadlock", "pattern"})
        hint_system.hint_count = 3
        
        # Reset
        hint_system.reset_progress()
        
        assert hint_system.queries_made == 0
        assert hint_system.discoveries == set()
        assert hint_system.hint_count == 0


class TestHintProgression:
    """Test hint progression logic (Requirements 4.1, 4.2, 4.3)."""
    
    def test_exploration_phase_0_queries(self):
        """Test hints in exploration phase with 0 queries."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should be exploration hint
        assert "explore" in hint.lower() or "start" in hint.lower() or "frame" in hint.lower()
    
    def test_exploration_phase_2_queries(self):
        """Test hints in exploration phase with 2 queries."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.update_progress(2, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should still be exploration hint
        assert len(hint) > 0
    
    def test_investigation_phase_3_queries(self):
        """Test hints in investigation phase with 3 queries."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.update_progress(3, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should be investigation hint
        assert len(hint) > 0
    
    def test_investigation_phase_5_queries(self):
        """Test hints in investigation phase with 5 queries."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        hint_system.update_progress(5, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should be investigation hint
        assert len(hint) > 0
    
    def test_diagnosis_phase_6_queries(self):
        """Test hints in diagnosis phase with 6 queries."""
        hint_system = MemoryStackHintSystem(FailureScenario.NULL_POINTER)
        hint_system.update_progress(6, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should be diagnosis hint (but if no discoveries, guides to find anomalies)
        assert len(hint) > 0
        # With no discoveries, should guide to find anomalies
        assert "anomal" in hint.lower() or "diagnos" in hint.lower()
    
    def test_diagnosis_phase_10_queries(self):
        """Test hints in diagnosis phase with many queries."""
        hint_system = MemoryStackHintSystem(FailureScenario.DEADLOCK)
        hint_system.update_progress(10, {"deadlock"})
        
        hint = hint_system.get_adaptive_hint()
        
        # Should be diagnosis hint
        assert len(hint) > 0


class TestComplexityAdaptation:
    """Test complexity-adapted hint generation (Requirements 4.4, 4.5)."""
    
    def test_beginner_includes_examples(self):
        """Test BEGINNER hints include examples and templates."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # BEGINNER should include query examples
        assert "?-" in hint  # Should contain query syntax
    
    def test_intermediate_moderate_guidance(self):
        """Test INTERMEDIATE provides moderate guidance without templates."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should provide guidance
        assert len(hint) > 0
        # But less detailed than BEGINNER
        assert len(hint) < 500  # Reasonable upper bound
    
    def test_advanced_minimal_guidance(self):
        """Test ADVANCED provides minimal guidance."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        hint_system.set_complexity_level(ComplexityLevel.ADVANCED)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should be brief
        assert len(hint) > 0
        assert len(hint) < 300  # Should be concise
    
    def test_expert_no_hints(self):
        """Test EXPERT level provides no hints."""
        hint_system = MemoryStackHintSystem(FailureScenario.NULL_POINTER)
        hint_system.set_complexity_level(ComplexityLevel.EXPERT)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        # Should indicate hints not available
        assert "not available" in hint.lower() or "expert" in hint.lower()
    
    def test_complexity_change_resets_hint_count(self):
        """Test changing complexity resets hint count (Requirement 6.5)."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        
        # Use some hints
        hint_system.update_progress(1, set())
        hint_system.get_adaptive_hint()
        hint_system.get_adaptive_hint()
        
        assert hint_system.hint_count == 2
        
        # Change complexity
        hint_system.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Hint count should be reset
        assert hint_system.hint_count == 0


class TestContextSpecificHints:
    """Test context-specific hints based on discoveries."""
    
    def test_error_discovery_hint(self):
        """Test hint when error status is discovered."""
        hint_system = MemoryStackHintSystem(FailureScenario.NULL_POINTER)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(4, {"error"})
        
        hint = hint_system.get_adaptive_hint()
        
        # Should mention error or parameters
        assert "error" in hint.lower() or "param" in hint.lower()
    
    def test_memory_anomaly_hint(self):
        """Test hint when memory anomaly is discovered."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(4, {"memory_anomaly"})
        
        hint = hint_system.get_adaptive_hint()
        
        # Should mention memory or allocation
        assert "memory" in hint.lower() or "allocat" in hint.lower()
    
    def test_recursion_discovery_hint(self):
        """Test hint when recursion pattern is discovered."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(4, {"recursion"})
        
        hint = hint_system.get_adaptive_hint()
        
        # Should mention recursion or depth
        assert "recurs" in hint.lower() or "depth" in hint.lower()
    
    def test_null_parameter_hint(self):
        """Test hint when null parameter is discovered."""
        hint_system = MemoryStackHintSystem(FailureScenario.NULL_POINTER)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(4, {"null_parameter"})
        
        hint = hint_system.get_adaptive_hint()
        
        # Should mention null or parameters
        assert "null" in hint.lower() or "parameter" in hint.lower()
    
    def test_deadlock_discovery_hint(self):
        """Test hint when deadlock pattern is discovered."""
        hint_system = MemoryStackHintSystem(FailureScenario.DEADLOCK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(4, {"deadlock"})
        
        hint = hint_system.get_adaptive_hint()
        
        # Should mention lock or waiting
        assert "lock" in hint.lower() or "wait" in hint.lower()


class TestQuerySuggestions:
    """Test query suggestion generation (Requirements 4.4, 4.5)."""
    
    def test_beginner_exploration_suggestions(self):
        """Test query suggestions in exploration phase at BEGINNER level."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        
        suggestion = hint_system.generate_query_suggestion("exploration")
        
        # Should provide a query suggestion
        assert suggestion is not None
        assert "?-" in suggestion
        assert suggestion.endswith(".")
    
    def test_beginner_investigation_suggestions(self):
        """Test query suggestions in investigation phase at BEGINNER level."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(4, {"memory_anomaly"})
        
        suggestion = hint_system.generate_query_suggestion("investigation")
        
        # Should provide a query suggestion
        assert suggestion is not None
        assert "?-" in suggestion
    
    def test_intermediate_no_suggestions(self):
        """Test no query suggestions at INTERMEDIATE level."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        suggestion = hint_system.generate_query_suggestion("exploration")
        
        # Should not provide suggestions
        assert suggestion is None
    
    def test_advanced_no_suggestions(self):
        """Test no query suggestions at ADVANCED level."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        hint_system.set_complexity_level(ComplexityLevel.ADVANCED)
        
        suggestion = hint_system.generate_query_suggestion("exploration")
        
        # Should not provide suggestions
        assert suggestion is None
    
    def test_diagnosis_phase_no_suggestions(self):
        """Test no query suggestions in diagnosis phase."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        
        suggestion = hint_system.generate_query_suggestion("diagnosis")
        
        # Should not provide suggestions in diagnosis phase
        assert suggestion is None


class TestHintAvailability:
    """Test hint availability based on complexity level."""
    
    def test_beginner_hints_always_available(self):
        """Test hints are always available at BEGINNER level."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.BEGINNER)
        hint_system.update_progress(0, set())
        
        # Should be able to get multiple hints
        for i in range(5):
            hint = hint_system.get_adaptive_hint()
            assert len(hint) > 0
            assert "not available" not in hint.lower()
    
    def test_intermediate_hint_limit(self):
        """Test hint limit at INTERMEDIATE level."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        hint_system.update_progress(0, set())
        
        # Get hints up to limit (3 for INTERMEDIATE)
        hints = []
        for i in range(4):
            hint = hint_system.get_adaptive_hint()
            hints.append(hint)
        
        # Last hint should indicate limit reached
        assert "used all" in hints[-1].lower() or "remaining" in hints[-1].lower()
    
    def test_advanced_hint_limit(self):
        """Test hint limit at ADVANCED level."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        hint_system.set_complexity_level(ComplexityLevel.ADVANCED)
        hint_system.update_progress(3, set())  # Need attempts for ADVANCED
        
        # Get hints up to limit (2 for ADVANCED)
        hints = []
        for i in range(3):
            hint = hint_system.get_adaptive_hint()
            hints.append(hint)
        
        # Last hint should indicate limit reached
        assert "used all" in hints[-1].lower() or "remaining" in hints[-1].lower()


class TestDifferentScenarios:
    """Test hint system works with different failure scenarios."""
    
    def test_memory_leak_scenario(self):
        """Test hint system with memory leak scenario."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        assert len(hint) > 0
    
    def test_stack_overflow_scenario(self):
        """Test hint system with stack overflow scenario."""
        hint_system = MemoryStackHintSystem(FailureScenario.STACK_OVERFLOW)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        assert len(hint) > 0
    
    def test_null_pointer_scenario(self):
        """Test hint system with null pointer scenario."""
        hint_system = MemoryStackHintSystem(FailureScenario.NULL_POINTER)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        assert len(hint) > 0
    
    def test_deadlock_scenario(self):
        """Test hint system with deadlock scenario."""
        hint_system = MemoryStackHintSystem(FailureScenario.DEADLOCK)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        assert len(hint) > 0
    
    def test_resource_exhaustion_scenario(self):
        """Test hint system with resource exhaustion scenario."""
        hint_system = MemoryStackHintSystem(FailureScenario.RESOURCE_EXHAUSTION)
        hint_system.update_progress(0, set())
        
        hint = hint_system.get_adaptive_hint()
        
        assert len(hint) > 0


class TestHintIncrement:
    """Test hint count increments correctly."""
    
    def test_hint_count_increments(self):
        """Test hint count increments with each hint request."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.update_progress(0, set())
        
        assert hint_system.hint_count == 0
        
        hint_system.get_adaptive_hint()
        assert hint_system.hint_count == 1
        
        hint_system.get_adaptive_hint()
        assert hint_system.hint_count == 2
    
    def test_hint_count_persists_across_progress_updates(self):
        """Test hint count persists when progress is updated."""
        hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
        hint_system.update_progress(0, set())
        
        hint_system.get_adaptive_hint()
        hint_system.get_adaptive_hint()
        
        assert hint_system.hint_count == 2
        
        # Update progress
        hint_system.update_progress(5, {"memory_anomaly"})
        
        # Hint count should still be 2
        assert hint_system.hint_count == 2
