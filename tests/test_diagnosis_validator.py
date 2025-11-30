"""
Unit tests for DiagnosisValidator class.

Tests diagnosis validation for each failure scenario including:
- Correct diagnosis recognition with multiple phrasings
- Partial diagnosis detection
- Incorrect diagnosis feedback
- Empty diagnosis handling
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import (
    DiagnosisValidator,
    DiagnosisResult,
    FailureScenario,
)


class TestDiagnosisValidatorMemoryLeak:
    """Test diagnosis validation for memory leak scenario."""
    
    def test_correct_diagnosis_exact_phrasing(self):
        """Test that exact phrasing is recognized as correct."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("The system has a memory leak")
        
        assert result.is_correct
        assert not result.is_partial
        assert "correct" in result.feedback.lower()
        assert result.explanation is not None
        assert "memory leak" in result.explanation.lower()
    
    def test_correct_diagnosis_alternative_phrasing_1(self):
        """Test alternative phrasing: allocated not freed."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis(
            "Memory is being allocated but not freed"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_alternative_phrasing_2(self):
        """Test alternative phrasing: allocated no release."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis(
            "The buffers are allocated with no release"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_alternative_phrasing_3(self):
        """Test alternative phrasing: memory not released."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis(
            "Memory is not being released after allocation"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_partial_diagnosis_memory_problem(self):
        """Test partial diagnosis: identifies memory problem but not specific."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("There's a memory problem")
        
        assert not result.is_correct
        assert result.is_partial
        assert "right track" in result.feedback.lower()
    
    def test_partial_diagnosis_allocation_only(self):
        """Test partial diagnosis: mentions allocation but not the leak."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("Memory allocation is happening")
        
        assert not result.is_correct
        assert result.is_partial
    
    def test_incorrect_diagnosis(self):
        """Test incorrect diagnosis."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("The system has a deadlock")
        
        assert not result.is_correct
        assert not result.is_partial
        assert "not quite" in result.feedback.lower()
    
    def test_empty_diagnosis(self):
        """Test empty diagnosis."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("")
        
        assert not result.is_correct
        assert not result.is_partial
        assert "provide a diagnosis" in result.feedback.lower()


class TestDiagnosisValidatorStackOverflow:
    """Test diagnosis validation for stack overflow scenario."""
    
    def test_correct_diagnosis_stack_overflow(self):
        """Test correct diagnosis: stack overflow."""
        validator = DiagnosisValidator(FailureScenario.STACK_OVERFLOW)
        result = validator.validate_diagnosis("Stack overflow occurred")
        
        assert result.is_correct
        assert not result.is_partial
        assert result.explanation is not None
    
    def test_correct_diagnosis_recursive_too_deep(self):
        """Test correct diagnosis: recursion too deep."""
        validator = DiagnosisValidator(FailureScenario.STACK_OVERFLOW)
        result = validator.validate_diagnosis(
            "The recursive function went too deep"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_excessive_recursion(self):
        """Test correct diagnosis: excessive recursion."""
        validator = DiagnosisValidator(FailureScenario.STACK_OVERFLOW)
        result = validator.validate_diagnosis("Excessive recursion caused the failure")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_partial_diagnosis_recursion_only(self):
        """Test partial diagnosis: mentions recursion but not the problem."""
        validator = DiagnosisValidator(FailureScenario.STACK_OVERFLOW)
        result = validator.validate_diagnosis("There is recursion happening")
        
        assert not result.is_correct
        assert result.is_partial


class TestDiagnosisValidatorNullPointer:
    """Test diagnosis validation for null pointer scenario."""
    
    def test_correct_diagnosis_null_pointer(self):
        """Test correct diagnosis: null pointer."""
        validator = DiagnosisValidator(FailureScenario.NULL_POINTER)
        result = validator.validate_diagnosis("Null pointer error")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_null_parameter(self):
        """Test correct diagnosis: null parameter."""
        validator = DiagnosisValidator(FailureScenario.NULL_POINTER)
        result = validator.validate_diagnosis(
            "The function received a null parameter"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_invalid_parameter(self):
        """Test correct diagnosis: invalid parameter."""
        validator = DiagnosisValidator(FailureScenario.NULL_POINTER)
        result = validator.validate_diagnosis("Invalid parameter passed to function")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_partial_diagnosis_null_only(self):
        """Test partial diagnosis: mentions null but not specific."""
        validator = DiagnosisValidator(FailureScenario.NULL_POINTER)
        result = validator.validate_diagnosis("There are null values")
        
        assert not result.is_correct
        assert result.is_partial


class TestDiagnosisValidatorDeadlock:
    """Test diagnosis validation for deadlock scenario."""
    
    def test_correct_diagnosis_deadlock(self):
        """Test correct diagnosis: deadlock."""
        validator = DiagnosisValidator(FailureScenario.DEADLOCK)
        result = validator.validate_diagnosis("Deadlock occurred")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_circular_wait(self):
        """Test correct diagnosis: circular wait."""
        validator = DiagnosisValidator(FailureScenario.DEADLOCK)
        result = validator.validate_diagnosis(
            "There is a circular wait on locks"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_locks_waiting(self):
        """Test correct diagnosis: locks waiting on each other."""
        validator = DiagnosisValidator(FailureScenario.DEADLOCK)
        result = validator.validate_diagnosis(
            "The locks are waiting for each other"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_partial_diagnosis_lock_problem(self):
        """Test partial diagnosis: mentions lock problem."""
        validator = DiagnosisValidator(FailureScenario.DEADLOCK)
        result = validator.validate_diagnosis("There's a lock problem")
        
        assert not result.is_correct
        assert result.is_partial


class TestDiagnosisValidatorResourceExhaustion:
    """Test diagnosis validation for resource exhaustion scenario."""
    
    def test_correct_diagnosis_resource_exhaustion(self):
        """Test correct diagnosis: resource exhaustion."""
        validator = DiagnosisValidator(FailureScenario.RESOURCE_EXHAUSTION)
        result = validator.validate_diagnosis("Resource exhaustion")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_too_much_memory(self):
        """Test correct diagnosis: too much memory."""
        validator = DiagnosisValidator(FailureScenario.RESOURCE_EXHAUSTION)
        result = validator.validate_diagnosis(
            "The system used too much memory"
        )
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_excessive_memory(self):
        """Test correct diagnosis: excessive memory."""
        validator = DiagnosisValidator(FailureScenario.RESOURCE_EXHAUSTION)
        result = validator.validate_diagnosis("Excessive memory usage")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_correct_diagnosis_out_of_memory(self):
        """Test correct diagnosis: out of memory."""
        validator = DiagnosisValidator(FailureScenario.RESOURCE_EXHAUSTION)
        result = validator.validate_diagnosis("System ran out of memory")
        
        assert result.is_correct
        assert not result.is_partial
    
    def test_partial_diagnosis_high_memory(self):
        """Test partial diagnosis: mentions high memory."""
        validator = DiagnosisValidator(FailureScenario.RESOURCE_EXHAUSTION)
        result = validator.validate_diagnosis("Memory usage is high")
        
        assert not result.is_correct
        assert result.is_partial


class TestDiagnosisValidatorHints:
    """Test hint generation for diagnosis."""
    
    def test_hint_few_queries(self):
        """Test hint when player has made few queries."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        hint = validator.get_hint_for_diagnosis(queries_made=2, discoveries=set())
        
        assert "investigate" in hint.lower() or "query" in hint.lower()
    
    def test_hint_with_discoveries(self):
        """Test hint when player has made discoveries."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        hint = validator.get_hint_for_diagnosis(
            queries_made=5,
            discoveries={"memory_anomaly", "pattern"}
        )
        
        assert "pattern" in hint.lower() or "together" in hint.lower()
    
    def test_hint_many_queries_no_discoveries(self):
        """Test hint when player has made many queries but no discoveries."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        hint = validator.get_hint_for_diagnosis(queries_made=10, discoveries=set())
        
        assert len(hint) > 0
        assert "pattern" in hint.lower() or "anomal" in hint.lower()


class TestDiagnosisValidatorCaseInsensitive:
    """Test that diagnosis validation is case-insensitive."""
    
    def test_uppercase_diagnosis(self):
        """Test diagnosis in uppercase."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("THE SYSTEM HAS A MEMORY LEAK")
        
        assert result.is_correct
    
    def test_mixed_case_diagnosis(self):
        """Test diagnosis in mixed case."""
        validator = DiagnosisValidator(FailureScenario.STACK_OVERFLOW)
        result = validator.validate_diagnosis("Stack OverFlow Occurred")
        
        assert result.is_correct
    
    def test_lowercase_diagnosis(self):
        """Test diagnosis in lowercase."""
        validator = DiagnosisValidator(FailureScenario.DEADLOCK)
        result = validator.validate_diagnosis("deadlock")
        
        assert result.is_correct


class TestDiagnosisValidatorWhitespace:
    """Test that diagnosis validation handles whitespace correctly."""
    
    def test_extra_whitespace(self):
        """Test diagnosis with extra whitespace."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("  memory   leak  ")
        
        assert result.is_correct
    
    def test_whitespace_only(self):
        """Test diagnosis with only whitespace."""
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("   ")
        
        assert not result.is_correct
        assert not result.is_partial
