"""
Tests for ResultFormatter - result formatting and display.

Tests Requirements 2.3, 2.4, 9.3, 9.5
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import (
    ResultFormatter,
    FailureScenario,
)


@pytest.fixture
def sample_facts_db():
    """Create a sample fact database for testing."""
    return {
        "frame": [
            (1, "init_system", 1000, "completed"),
            (2, "load_config", 1050, "completed"),
            (3, "start_ai_core", 1100, "active"),
            (4, "process_request", 1150, "error"),
        ],
        "calls": [
            (1, 2),
            (2, 3),
            (3, 4),
        ],
        "allocated": [
            (1, 2048),
            (2, 4096),
            (3, 8192),
            (4, 2048),
        ],
        "param": [
            (1, "mode", "startup"),
            (2, "config_file", "system.cfg"),
            (3, "core_id", 1),
            (4, "request_id", 42),
            (4, "data", "null"),
        ],
        "status": [
            (1, "completed"),
            (2, "completed"),
            (3, "active"),
            (4, "error"),
        ],
    }


@pytest.fixture
def formatter(sample_facts_db):
    """Create a ResultFormatter with sample data."""
    return ResultFormatter(sample_facts_db)


class TestRequirement23_ResultFormatting:
    """Test Requirement 2.3: Clear result display with formatting."""
    
    def test_format_single_result_with_variables(self, formatter):
        """Test formatting a single result with variable bindings."""
        results = [{"X": "init_system", "Y": 1000, "Z": "completed"}]
        arguments = ["1", "X", "Y", "Z"]
        
        output = formatter.format_results(results, arguments, "frame")
        
        assert "Found 1 result" in output
        assert "X = init_system" in output
        assert "Y = 1000" in output
        assert "Z = completed" in output
    
    def test_format_multiple_results(self, formatter):
        """Test formatting multiple results."""
        results = [
            {"X": 1, "Y": "completed"},
            {"X": 2, "Y": "completed"},
        ]
        arguments = ["X", "Y"]
        
        output = formatter.format_results(results, arguments, "status")
        
        assert "Found 2 result" in output
        assert "1." in output
        assert "2." in output
        assert "X = 1" in output
        assert "X = 2" in output
    
    def test_format_result_without_variables(self, formatter):
        """Test formatting when query has no variables (exact match)."""
        results = [{}]  # Empty binding means exact match
        arguments = ["1", "init_system", "1000", "completed"]
        
        output = formatter.format_results(results, arguments, "frame")
        
        assert "Yes" in output
        assert "matching fact" in output
    
    def test_format_result_consistency(self, formatter):
        """Test that formatting is consistent across multiple calls."""
        results = [{"X": "test", "Y": 123}]
        arguments = ["X", "Y"]
        
        output1 = formatter.format_results(results, arguments, "test")
        output2 = formatter.format_results(results, arguments, "test")
        
        assert output1 == output2


class TestRequirement24_95_EmptyResultHandling:
    """Test Requirements 2.4 and 9.5: Empty result handling with explanations."""
    
    def test_empty_result_with_unknown_predicate(self, formatter):
        """Test empty result when predicate doesn't exist."""
        output = formatter.format_empty_result("unknown_pred", ["X", "Y"])
        
        assert "No facts found for predicate 'unknown_pred'" in output
        assert "Available predicates" in output
        assert "frame" in output
        assert "status" in output
    
    def test_empty_result_with_variables(self, formatter):
        """Test empty result explanation when query has variables."""
        output = formatter.format_empty_result("frame", ["999", "X", "Y", "Z"])
        
        assert "No results found matching the pattern" in output
        assert "Suggestions" in output
        assert "different constant values" in output or "more general variables" in output
    
    def test_empty_result_with_constants(self, formatter):
        """Test empty result explanation when query has all constants."""
        output = formatter.format_empty_result("frame", ["999", "nonexistent", "0", "error"])
        
        assert "No exact match found" in output
        assert "Suggestions" in output
        assert "variables" in output
        assert "Example" in output
    
    def test_empty_result_provides_helpful_suggestions(self, formatter):
        """Test that empty results include actionable suggestions."""
        output = formatter.format_empty_result("status", ["999", "crashed"])
        
        # Should provide suggestions
        assert "Suggestions" in output or "Try" in output
        # Should mention using variables
        assert "variable" in output.lower() or "uppercase" in output.lower()


class TestRequirement93_SignificanceDetection:
    """Test Requirement 9.3: Significance detection for important discoveries."""
    
    def test_detect_error_status_significance(self, formatter):
        """Test that error status queries are marked significant."""
        matches = [{"X": 4}]
        is_sig, disc_type = formatter.detect_significance(
            "status", ["X", "error"], matches
        )
        
        assert is_sig is True
        assert disc_type == "error"
    
    def test_detect_pattern_significance(self, formatter):
        """Test that queries with many results are marked significant."""
        # Create many matches
        matches = [{"X": i} for i in range(10)]
        is_sig, disc_type = formatter.detect_significance(
            "frame", ["X", "Y", "Z", "W"], matches
        )
        
        assert is_sig is True
        assert disc_type == "pattern"
    
    def test_detect_memory_anomaly(self, formatter):
        """Test detection of high memory allocation."""
        matches = [{"X": 1, "Y": 10485760}]  # 10MB
        is_sig, disc_type = formatter.detect_significance(
            "allocated", ["X", "Y"], matches
        )
        
        assert is_sig is True
        assert disc_type == "memory_anomaly"
    
    def test_detect_null_parameter(self, formatter):
        """Test detection of null parameters."""
        matches = [{"X": 4, "Y": "data", "Z": "null"}]
        is_sig, disc_type = formatter.detect_significance(
            "param", ["X", "Y", "Z"], matches
        )
        
        assert is_sig is True
        assert disc_type == "null_parameter"
    
    def test_detect_recursion_pattern(self, formatter):
        """Test detection of recursive call patterns."""
        # Many caller-callee relationships
        matches = [{"X": i, "Y": i+1} for i in range(15)]
        is_sig, disc_type = formatter.detect_significance(
            "calls", ["X", "Y"], matches
        )
        
        assert is_sig is True
        assert disc_type == "recursion"
    
    def test_no_significance_for_normal_queries(self, formatter):
        """Test that normal queries are not marked significant."""
        matches = [{"X": 1, "Y": "completed"}]
        is_sig, disc_type = formatter.detect_significance(
            "status", ["X", "Y"], matches
        )
        
        assert is_sig is False
        assert disc_type is None


class TestHighlightFormatting:
    """Test highlight formatting for significant results."""
    
    def test_highlight_added_for_significant_results(self, formatter):
        """Test that significant results include highlighting."""
        results = [{"X": 4}]
        arguments = ["X", "error"]
        
        output = formatter.format_results(
            results, arguments, "status",
            is_significant=True, discovery_type="error"
        )
        
        assert "SIGNIFICANT" in output
        assert "Error status detected" in output
    
    def test_highlight_includes_discovery_type(self, formatter):
        """Test that highlight message reflects discovery type."""
        results = [{"X": i} for i in range(10)]
        arguments = ["X", "Y", "Z", "W"]
        
        output = formatter.format_results(
            results, arguments, "frame",
            is_significant=True, discovery_type="pattern"
        )
        
        assert "SIGNIFICANT" in output
        assert "Pattern detected" in output
    
    def test_no_highlight_for_non_significant_results(self, formatter):
        """Test that non-significant results don't include highlighting."""
        results = [{"X": 1, "Y": "completed"}]
        arguments = ["X", "Y"]
        
        output = formatter.format_results(
            results, arguments, "status",
            is_significant=False
        )
        
        assert "SIGNIFICANT" not in output
    
    def test_highlight_memory_anomaly(self, formatter):
        """Test highlighting for memory anomalies."""
        results = [{"X": 1, "Y": 10485760}]
        arguments = ["X", "Y"]
        
        output = formatter.format_results(
            results, arguments, "allocated",
            is_significant=True, discovery_type="memory_anomaly"
        )
        
        assert "SIGNIFICANT" in output
        assert "memory allocation" in output.lower()
    
    def test_highlight_includes_puzzle_hint(self, formatter):
        """Test that highlights include hint about puzzle solving."""
        results = [{"X": 4}]
        arguments = ["X", "error"]
        
        output = formatter.format_results(
            results, arguments, "status",
            is_significant=True, discovery_type="error"
        )
        
        assert "important for solving the puzzle" in output.lower() or "discovery" in output.lower()


class TestIntegrationWithScenarios:
    """Test ResultFormatter integration with different failure scenarios."""
    
    def test_format_with_memory_leak_scenario(self, formatter):
        """Test formatting with memory leak scenario context."""
        matches = [
            {"X": 1, "Y": 1048576},
            {"X": 2, "Y": 1048576},
            {"X": 3, "Y": 1048576},
        ]
        
        is_sig, disc_type = formatter.detect_significance(
            "allocated", ["X", "Y"], matches,
            scenario_type=FailureScenario.MEMORY_LEAK
        )
        
        # Should detect high memory allocation
        assert is_sig is True
        assert disc_type == "memory_anomaly"
    
    def test_format_with_null_pointer_scenario(self, formatter):
        """Test formatting with null pointer scenario context."""
        matches = [{"X": 4, "Y": "data", "Z": "null"}]
        
        is_sig, disc_type = formatter.detect_significance(
            "param", ["X", "Y", "Z"], matches,
            scenario_type=FailureScenario.NULL_POINTER
        )
        
        assert is_sig is True
        assert disc_type == "null_parameter"


class TestEdgeCases:
    """Test edge cases in result formatting."""
    
    def test_format_empty_results_list(self, formatter):
        """Test formatting with empty results list."""
        output = formatter.format_results([], ["X", "Y"], "frame")
        
        assert "No" in output or "not found" in output.lower()
    
    def test_format_with_special_characters(self, formatter):
        """Test formatting with special characters in values."""
        results = [{"X": "test_value", "Y": "data-123"}]
        arguments = ["X", "Y"]
        
        output = formatter.format_results(results, arguments, "test")
        
        assert "test_value" in output
        assert "data-123" in output
    
    def test_format_with_numeric_values(self, formatter):
        """Test formatting with various numeric values."""
        results = [{"X": 0, "Y": -1, "Z": 999999}]
        arguments = ["X", "Y", "Z"]
        
        output = formatter.format_results(results, arguments, "test")
        
        assert "X = 0" in output
        assert "Y = -1" in output
        assert "Z = 999999" in output
    
    def test_is_variable_helper(self, formatter):
        """Test the _is_variable helper method."""
        assert formatter._is_variable("X") is True
        assert formatter._is_variable("Variable") is True
        assert formatter._is_variable("_") is True
        assert formatter._is_variable("_anon") is True
        assert formatter._is_variable("atom") is False
        assert formatter._is_variable("123") is False
