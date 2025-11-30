"""
Test suite for QueryValidator class.

Tests validation of Prolog queries for the Memory Stack Puzzle,
including simple queries, compound queries, and negation queries.

Validates Requirements 2.1 and 2.5:
- 2.1: Query syntax validation
- 2.5: Specific syntax error feedback
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import QueryValidator
from prologresurrected.game.validation import ValidationResult


class TestSimpleQueryValidation:
    """Test validation of simple (single predicate) queries."""
    
    def test_valid_simple_queries(self):
        """Test that valid simple queries pass validation."""
        valid_queries = [
            "?- frame(1, init_system, 1000, active).",
            "?- calls(1, 2).",
            "?- allocated(3, 1048576).",
            "?- param(4, buffer_size, 1024).",
            "?- status(5, error).",
            "?- frame(X, Y, Z, W).",  # All variables
            "?- frame(1, X, Y, Z).",  # Mixed
            "?- calls(X, Y).",  # Variables in relationships
        ]
        
        for query in valid_queries:
            result = QueryValidator.validate_query(query)
            assert result.is_valid, f"Query '{query}' should be valid but got: {result.error_message}"
            assert result.parsed_components is not None
            assert result.parsed_components["type"] == "simple"
    
    def test_missing_query_prefix(self):
        """Test detection of missing ?- prefix."""
        result = QueryValidator.validate_query("frame(1, X, Y, Z).")
        assert not result.is_valid
        assert "prefix" in result.error_message.lower()
        assert "?-" in result.hint
    
    def test_missing_period(self):
        """Test detection of missing period at end."""
        result = QueryValidator.validate_query("?- frame(1, X, Y, Z)")
        assert not result.is_valid
        assert "period" in result.error_message.lower()
    
    def test_empty_query(self):
        """Test detection of empty query."""
        result = QueryValidator.validate_query("")
        assert not result.is_valid
        assert "empty" in result.error_message.lower()
        
        result = QueryValidator.validate_query("   ")
        assert not result.is_valid
        assert "empty" in result.error_message.lower()
    
    def test_empty_query_body(self):
        """Test detection of empty query body."""
        result = QueryValidator.validate_query("?- .")
        assert not result.is_valid
        assert "empty" in result.error_message.lower()
    
    def test_missing_parentheses(self):
        """Test detection of missing parentheses."""
        result = QueryValidator.validate_query("?- frame 1 X Y Z.")
        assert not result.is_valid
        assert "parenthes" in result.error_message.lower()
    
    def test_uppercase_predicate(self):
        """Test detection of uppercase predicate name."""
        result = QueryValidator.validate_query("?- Frame(1, X, Y, Z).")
        assert not result.is_valid
        assert "lowercase" in result.error_message.lower()
    
    def test_invalid_predicate_name(self):
        """Test detection of invalid predicate names."""
        result = QueryValidator.validate_query("?- 123invalid(X, Y).")
        assert not result.is_valid
        
        result = QueryValidator.validate_query("?- pred-name(X, Y).")
        assert not result.is_valid
    
    def test_unknown_predicate(self):
        """Test detection of unknown predicates."""
        result = QueryValidator.validate_query("?- unknown_pred(X, Y).")
        assert not result.is_valid
        assert "unknown" in result.error_message.lower()
        assert "frame" in result.hint or "calls" in result.hint
    
    def test_mismatched_parentheses(self):
        """Test detection of mismatched parentheses."""
        result = QueryValidator.validate_query("?- frame(1, X, Y, Z.")
        assert not result.is_valid
        assert "parenthes" in result.error_message.lower()
        
        result = QueryValidator.validate_query("?- frame1, X, Y, Z).")
        assert not result.is_valid
    
    def test_empty_arguments(self):
        """Test detection of empty argument list."""
        result = QueryValidator.validate_query("?- frame().")
        assert not result.is_valid
        assert "empty" in result.error_message.lower()
    
    def test_invalid_arguments(self):
        """Test detection of invalid argument formats."""
        result = QueryValidator.validate_query("?- frame(1, X, @invalid, Z).")
        assert not result.is_valid
        assert "invalid" in result.error_message.lower()
        
        result = QueryValidator.validate_query("?- frame(1, X, , Z).")
        assert not result.is_valid
    
    def test_parsed_components_structure(self):
        """Test that parsed components have correct structure."""
        result = QueryValidator.validate_query("?- frame(1, init_system, 1000, active).")
        assert result.is_valid
        assert result.parsed_components["type"] == "simple"
        assert result.parsed_components["predicate"] == "frame"
        assert result.parsed_components["arguments"] == ["1", "init_system", "1000", "active"]
        assert "full_query" in result.parsed_components


class TestCompoundQueryValidation:
    """Test validation of compound queries with multiple conditions."""
    
    def test_valid_compound_queries(self):
        """Test that valid compound queries pass validation."""
        valid_queries = [
            "?- frame(X, Y, Z, active), allocated(X, M).",
            "?- calls(1, 2), calls(2, 3).",
            "?- frame(X, allocate_buffer, T, S), allocated(X, 1048576).",
            "?- status(X, error), param(X, Y, null).",
            "?- frame(X, Y, Z, W), calls(A, X), allocated(X, M).",
        ]
        
        for query in valid_queries:
            result = QueryValidator.validate_query(query)
            assert result.is_valid, f"Query '{query}' should be valid but got: {result.error_message}"
            assert result.parsed_components is not None
            assert result.parsed_components["type"] == "compound"
            assert result.parsed_components["condition_count"] >= 2
    
    def test_compound_query_with_two_conditions(self):
        """Test compound query with exactly two conditions."""
        result = QueryValidator.validate_query("?- frame(X, Y, Z, W), allocated(X, M).")
        assert result.is_valid
        assert result.parsed_components["condition_count"] == 2
        
        conditions = result.parsed_components["conditions"]
        assert len(conditions) == 2
        assert conditions[0]["predicate"] == "frame"
        assert conditions[1]["predicate"] == "allocated"
    
    def test_compound_query_with_three_conditions(self):
        """Test compound query with three conditions."""
        result = QueryValidator.validate_query("?- frame(X, Y, Z, W), calls(A, X), allocated(X, M).")
        assert result.is_valid
        assert result.parsed_components["condition_count"] == 3
    
    def test_compound_query_error_in_first_condition(self):
        """Test error detection in first condition of compound query."""
        result = QueryValidator.validate_query("?- Frame(X, Y, Z, W), allocated(X, M).")
        assert not result.is_valid
        assert "condition 1" in result.error_message.lower()
        assert "lowercase" in result.error_message.lower()
    
    def test_compound_query_error_in_second_condition(self):
        """Test error detection in second condition of compound query."""
        result = QueryValidator.validate_query("?- frame(X, Y, Z, W), Allocated(X, M).")
        assert not result.is_valid
        assert "condition 2" in result.error_message.lower()
    
    def test_compound_query_with_unknown_predicate(self):
        """Test compound query with unknown predicate in one condition."""
        result = QueryValidator.validate_query("?- frame(X, Y, Z, W), unknown(X, M).")
        assert not result.is_valid
        assert "unknown" in result.error_message.lower()
    
    def test_compound_query_preserves_commas_in_arguments(self):
        """Test that commas inside parentheses are not treated as separators."""
        result = QueryValidator.validate_query("?- frame(1, 2, 3, 4), calls(5, 6).")
        assert result.is_valid
        
        conditions = result.parsed_components["conditions"]
        assert len(conditions) == 2
        assert len(conditions[0]["arguments"]) == 4
        assert len(conditions[1]["arguments"]) == 2


class TestNegationQueryValidation:
    """Test validation of negation queries."""
    
    def test_valid_negation_queries(self):
        """Test that valid negation queries pass validation."""
        valid_queries = [
            "?- \\+ status(1, error).",
            "?- \\+ param(X, Y, null).",
            "?- \\+ frame(X, Y, Z, error).",
            "?- \\+ allocated(X, 0).",
        ]
        
        for query in valid_queries:
            result = QueryValidator.validate_query(query)
            assert result.is_valid, f"Query '{query}' should be valid but got: {result.error_message}"
            assert result.parsed_components is not None
            assert result.parsed_components["type"] == "negation"
    
    def test_negation_query_structure(self):
        """Test that negation query has correct parsed structure."""
        result = QueryValidator.validate_query("?- \\+ status(1, error).")
        assert result.is_valid
        assert result.parsed_components["type"] == "negation"
        assert result.parsed_components["negated_predicate"] == "status"
        assert result.parsed_components["negated_arguments"] == ["1", "error"]
    
    def test_negation_with_variables(self):
        """Test negation queries with variables."""
        result = QueryValidator.validate_query("?- \\+ param(X, Y, null).")
        assert result.is_valid
        assert result.parsed_components["negated_arguments"] == ["X", "Y", "null"]
    
    def test_empty_negation(self):
        """Test detection of empty negation."""
        result = QueryValidator.validate_query("?- \\+ .")
        assert not result.is_valid
        assert "empty" in result.error_message.lower()
    
    def test_negation_with_invalid_predicate(self):
        """Test negation with invalid predicate."""
        result = QueryValidator.validate_query("?- \\+ Frame(X, Y, Z, W).")
        assert not result.is_valid
        assert "lowercase" in result.error_message.lower()
    
    def test_negation_with_unknown_predicate(self):
        """Test negation with unknown predicate."""
        result = QueryValidator.validate_query("?- \\+ unknown(X, Y).")
        assert not result.is_valid
        assert "unknown" in result.error_message.lower()
    
    def test_compound_query_with_negation(self):
        """Test compound query containing negation."""
        result = QueryValidator.validate_query("?- frame(X, Y, Z, W), \\+ status(X, error).")
        assert result.is_valid
        assert result.parsed_components["type"] == "compound"
        
        conditions = result.parsed_components["conditions"]
        assert len(conditions) == 2
        assert conditions[0]["is_negation"] is False
        assert conditions[1]["is_negation"] is True


class TestQueryValidatorErrorMessages:
    """Test that error messages are helpful and specific."""
    
    def test_error_messages_are_not_none(self):
        """Test that invalid queries always have error messages."""
        invalid_queries = [
            "frame(1, X, Y, Z).",  # Missing ?-
            "?- frame(1, X, Y, Z)",  # Missing period
            "?- Frame(1, X, Y, Z).",  # Uppercase predicate
            "?- unknown(X, Y).",  # Unknown predicate
            "?- frame().",  # Empty arguments
        ]
        
        for query in invalid_queries:
            result = QueryValidator.validate_query(query)
            assert not result.is_valid
            assert result.error_message is not None
            assert len(result.error_message) > 0
    
    def test_hints_are_provided(self):
        """Test that invalid queries always have hints."""
        invalid_queries = [
            "frame(1, X, Y, Z).",
            "?- frame(1, X, Y, Z)",
            "?- Frame(1, X, Y, Z).",
            "?- unknown(X, Y).",
        ]
        
        for query in invalid_queries:
            result = QueryValidator.validate_query(query)
            assert not result.is_valid
            assert result.hint is not None
            assert len(result.hint) > 0
    
    def test_hints_contain_examples(self):
        """Test that hints contain helpful examples."""
        result = QueryValidator.validate_query("frame(1, X, Y, Z).")
        assert "?-" in result.hint
        
        result = QueryValidator.validate_query("?- unknown(X, Y).")
        assert any(pred in result.hint for pred in ["frame", "calls", "allocated", "param", "status"])
    
    def test_error_messages_are_specific(self):
        """Test that error messages identify specific problems."""
        result = QueryValidator.validate_query("frame(1, X, Y, Z).")
        assert "prefix" in result.error_message.lower()
        
        result = QueryValidator.validate_query("?- Frame(1, X, Y, Z).")
        assert "lowercase" in result.error_message.lower()
        
        result = QueryValidator.validate_query("?- unknown(X, Y).")
        assert "unknown" in result.error_message.lower()


class TestQueryValidatorEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_whitespace_handling(self):
        """Test that queries with extra whitespace are handled correctly."""
        queries_with_whitespace = [
            "?-   frame(1, X, Y, Z).",
            "?- frame( 1 , X , Y , Z ).",
            "?-frame(1,X,Y,Z).",
            "  ?- frame(1, X, Y, Z).  ",
        ]
        
        for query in queries_with_whitespace:
            result = QueryValidator.validate_query(query)
            assert result.is_valid, f"Query with whitespace should be valid: '{query}'"
    
    def test_variable_naming_conventions(self):
        """Test various valid variable naming conventions."""
        valid_variables = [
            "?- frame(X, Y, Z, W).",
            "?- frame(X1, Y2, Z3, W4).",
            "?- frame(Var1, Var2, Var3, Var4).",
            "?- frame(_, _A, _B, _C).",
            "?- frame(VAR, VAR2, VAR_NAME, V).",
        ]
        
        for query in valid_variables:
            result = QueryValidator.validate_query(query)
            assert result.is_valid, f"Query with valid variables should pass: '{query}'"
    
    def test_atom_naming_conventions(self):
        """Test various valid atom naming conventions."""
        valid_atoms = [
            "?- frame(1, init_system, 1000, active).",
            "?- frame(1, init_system_v2, 1000, active).",
            "?- frame(1, a, 1000, active).",
            "?- frame(1, abc123, 1000, active).",
        ]
        
        for query in valid_atoms:
            result = QueryValidator.validate_query(query)
            assert result.is_valid, f"Query with valid atoms should pass: '{query}'"
    
    def test_number_arguments(self):
        """Test queries with numeric arguments."""
        result = QueryValidator.validate_query("?- frame(1, init_system, 1000, active).")
        assert result.is_valid
        
        result = QueryValidator.validate_query("?- allocated(5, 1048576).")
        assert result.is_valid
    
    def test_very_long_query(self):
        """Test handling of very long compound queries."""
        # Build a long compound query
        conditions = [f"frame(X{i}, Y{i}, Z{i}, W{i})" for i in range(10)]
        query = "?- " + ", ".join(conditions) + "."
        
        result = QueryValidator.validate_query(query)
        assert result.is_valid
        assert result.parsed_components["condition_count"] == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
