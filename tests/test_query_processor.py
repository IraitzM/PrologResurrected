"""
Tests for QueryProcessor - query execution engine.

Tests Requirements 2.2, 3.1, 3.3, 8.1, 8.3, 8.4
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import (
    QueryProcessor,
    StackFrame,
    QueryResult,
)


@pytest.fixture
def sample_stack_frames():
    """Create sample stack frames for testing."""
    return [
        StackFrame(
            frame_id=1,
            function_name="init_system",
            caller_id=None,
            timestamp=1000,
            memory_allocated=2048,
            status="completed",
            parameters={"mode": "startup"},
        ),
        StackFrame(
            frame_id=2,
            function_name="load_config",
            caller_id=1,
            timestamp=1050,
            memory_allocated=4096,
            status="completed",
            parameters={"config_file": "system.cfg"},
        ),
        StackFrame(
            frame_id=3,
            function_name="start_ai_core",
            caller_id=2,
            timestamp=1100,
            memory_allocated=8192,
            status="active",
            parameters={"core_id": 1},
        ),
        StackFrame(
            frame_id=4,
            function_name="process_request",
            caller_id=3,
            timestamp=1150,
            memory_allocated=2048,
            status="error",
            parameters={"request_id": 42, "data": "null"},
        ),
    ]


@pytest.fixture
def query_processor(sample_stack_frames):
    """Create a QueryProcessor with sample data."""
    return QueryProcessor(sample_stack_frames)


class TestRequirement22_31_QueryExecution:
    """Test Requirement 2.2 and 3.1: Query execution returns matching facts."""
    
    def test_execute_simple_query_with_exact_match(self, query_processor):
        """Test executing a query with exact values."""
        result = query_processor.execute_query("?- frame(1, init_system, 1000, completed).")
        
        assert result.success
        assert len(result.results) == 1
        assert "1 result" in result.formatted_output or "matching fact" in result.formatted_output
    
    def test_execute_query_with_no_matches(self, query_processor):
        """Test executing a query that matches no facts."""
        result = query_processor.execute_query("?- frame(999, nonexistent, 0, active).")
        
        assert result.success
        assert len(result.results) == 0
        assert "No" in result.formatted_output or "not found" in result.formatted_output.lower()
    
    def test_execute_query_with_single_variable(self, query_processor):
        """Test executing a query with one variable."""
        result = query_processor.execute_query("?- frame(1, X, 1000, completed).")
        
        assert result.success
        assert len(result.results) == 1
        assert result.results[0]["X"] == "init_system"
    
    def test_execute_query_with_multiple_variables(self, query_processor):
        """Test executing a query with multiple variables."""
        result = query_processor.execute_query("?- frame(1, X, Y, Z).")
        
        assert result.success
        assert len(result.results) == 1
        assert result.results[0]["X"] == "init_system"
        assert result.results[0]["Y"] == 1000
        assert result.results[0]["Z"] == "completed"
    
    def test_execute_query_returns_all_matches(self, query_processor):
        """Test that query returns all matching facts."""
        result = query_processor.execute_query("?- status(X, completed).")
        
        assert result.success
        # Should match frames 1 and 2 which have completed status
        assert len(result.results) == 2
        frame_ids = [r["X"] for r in result.results]
        assert 1 in frame_ids
        assert 2 in frame_ids


class TestRequirement33_VariableBinding:
    """Test Requirement 3.3: Variable binding in queries."""
    
    def test_variable_binding_with_all_variables(self, query_processor):
        """Test query with all variables returns all facts."""
        result = query_processor.execute_query("?- frame(A, B, C, D).")
        
        assert result.success
        assert len(result.results) == 4  # All 4 frames
        
        # Check that each result has all variables bound
        for binding in result.results:
            assert "A" in binding
            assert "B" in binding
            assert "C" in binding
            assert "D" in binding
    
    def test_variable_binding_consistency(self, query_processor):
        """Test that same variable binds consistently."""
        # Query where same variable appears twice - should only match if values are same
        result = query_processor.execute_query("?- status(X, completed).")
        
        assert result.success
        # All bindings should have consistent X values
        for binding in result.results:
            assert isinstance(binding["X"], int)
    
    def test_variable_binding_with_mixed_constants(self, query_processor):
        """Test variable binding mixed with constants."""
        result = query_processor.execute_query("?- frame(X, load_config, Y, completed).")
        
        assert result.success
        assert len(result.results) == 1
        assert result.results[0]["X"] == 2
        assert result.results[0]["Y"] == 1050
    
    def test_underscore_as_anonymous_variable(self, query_processor):
        """Test underscore as anonymous variable (matches anything)."""
        result = query_processor.execute_query("?- frame(1, _, _, _).")
        
        assert result.success
        assert len(result.results) == 1


class TestRequirement81_ExactMatching:
    """Test Requirement 8.1: Exact matching queries."""
    
    def test_exact_match_all_constants(self, query_processor):
        """Test query with all constant values."""
        result = query_processor.execute_query("?- allocated(1, 2048).")
        
        assert result.success
        assert len(result.results) == 1
    
    def test_exact_match_no_match(self, query_processor):
        """Test exact match that doesn't exist."""
        result = query_processor.execute_query("?- allocated(1, 9999).")
        
        assert result.success
        assert len(result.results) == 0
    
    def test_exact_match_with_string_parameter(self, query_processor):
        """Test exact match with string parameter."""
        result = query_processor.execute_query("?- param(1, mode, startup).")
        
        assert result.success
        assert len(result.results) == 1
    
    def test_exact_match_relationship(self, query_processor):
        """Test exact match for relationship facts."""
        result = query_processor.execute_query("?- calls(1, 2).")
        
        assert result.success
        assert len(result.results) == 1


class TestRequirement83_CompoundQueries:
    """Test Requirement 8.3: Compound queries with multiple conditions."""
    
    def test_compound_query_two_conditions(self, query_processor):
        """Test compound query with two conditions."""
        result = query_processor.execute_query(
            "?- frame(X, load_config, Y, Z), status(X, completed)."
        )
        
        assert result.success
        assert len(result.results) == 1
        assert result.results[0]["X"] == 2
    
    def test_compound_query_three_conditions(self, query_processor):
        """Test compound query with three conditions."""
        result = query_processor.execute_query(
            "?- frame(X, Y, Z, completed), calls(1, X), allocated(X, A)."
        )
        
        assert result.success
        assert len(result.results) == 1
        assert result.results[0]["X"] == 2
        assert result.results[0]["A"] == 4096
    
    def test_compound_query_no_matches(self, query_processor):
        """Test compound query where conditions don't all match."""
        result = query_processor.execute_query(
            "?- frame(X, init_system, Y, Z), status(X, error)."
        )
        
        assert result.success
        assert len(result.results) == 0
    
    def test_compound_query_variable_sharing(self, query_processor):
        """Test compound query with shared variables between conditions."""
        result = query_processor.execute_query(
            "?- calls(X, Y), frame(Y, load_config, Z, W)."
        )
        
        assert result.success
        assert len(result.results) == 1
        assert result.results[0]["X"] == 1
        assert result.results[0]["Y"] == 2
    
    def test_compound_query_filters_results(self, query_processor):
        """Test that compound queries filter to only matching results."""
        # First condition matches multiple frames, second narrows it down
        result = query_processor.execute_query(
            "?- frame(X, Y, Z, W), allocated(X, 2048)."
        )
        
        assert result.success
        # Should match frames 1 and 4 which have 2048 bytes allocated
        assert len(result.results) == 2
        frame_ids = [r["X"] for r in result.results]
        assert 1 in frame_ids
        assert 4 in frame_ids


class TestRequirement84_NegationQueries:
    """Test Requirement 8.4: Negation queries (checking for missing facts)."""
    
    def test_negation_query_fact_exists(self, query_processor):
        """Test negation when fact exists (negation fails)."""
        result = query_processor.execute_query("?- \\+ frame(1, init_system, 1000, completed).")
        
        assert result.success
        assert len(result.results) == 0
        assert "No" in result.formatted_output or "exists" in result.formatted_output
    
    def test_negation_query_fact_missing(self, query_processor):
        """Test negation when fact doesn't exist (negation succeeds)."""
        result = query_processor.execute_query("?- \\+ frame(999, nonexistent, 0, error).")
        
        assert result.success
        assert len(result.results) == 1
        assert "Yes" in result.formatted_output or "does not exist" in result.formatted_output
    
    def test_negation_query_with_variables(self, query_processor):
        """Test negation with variables."""
        # Check if there's no frame with status "crashed"
        result = query_processor.execute_query("?- \\+ status(X, crashed).")
        
        assert result.success
        assert len(result.results) == 1  # Negation succeeds
    
    def test_negation_in_compound_query(self, query_processor):
        """Test negation as part of compound query."""
        result = query_processor.execute_query(
            "?- frame(X, Y, Z, completed), \\+ allocated(X, 8192)."
        )
        
        assert result.success
        # Should match completed frames that don't have 8192 bytes allocated
        # Frames 1 and 2 are completed, frame 1 has 2048, frame 2 has 4096
        assert len(result.results) == 2


class TestQueryResultFormatting:
    """Test query result formatting."""
    
    def test_format_single_result(self, query_processor):
        """Test formatting of single result."""
        result = query_processor.execute_query("?- frame(1, X, Y, Z).")
        
        assert result.success
        assert "1 result" in result.formatted_output or "Found 1" in result.formatted_output
        assert "X = init_system" in result.formatted_output
    
    def test_format_multiple_results(self, query_processor):
        """Test formatting of multiple results."""
        result = query_processor.execute_query("?- status(X, completed).")
        
        assert result.success
        assert "2 result" in result.formatted_output or "Found 2" in result.formatted_output
    
    def test_format_no_results(self, query_processor):
        """Test formatting when no results found."""
        result = query_processor.execute_query("?- frame(999, X, Y, Z).")
        
        assert result.success
        assert len(result.results) == 0
        assert "No" in result.formatted_output or "not found" in result.formatted_output.lower()
    
    def test_format_exact_match_no_variables(self, query_processor):
        """Test formatting when query has no variables."""
        result = query_processor.execute_query("?- frame(1, init_system, 1000, completed).")
        
        assert result.success
        assert "Yes" in result.formatted_output or "matching" in result.formatted_output


class TestInvalidQueryHandling:
    """Test handling of invalid queries."""
    
    def test_invalid_query_syntax(self, query_processor):
        """Test that invalid syntax is caught."""
        result = query_processor.execute_query("frame(1, X, Y, Z)")  # Missing ?- and .
        
        assert not result.success
        assert "Error" in result.formatted_output
    
    def test_unknown_predicate(self, query_processor):
        """Test query with unknown predicate."""
        result = query_processor.execute_query("?- unknown_pred(X, Y).")
        
        assert not result.success
        assert "Unknown predicate" in result.formatted_output


class TestSignificanceDetection:
    """Test detection of significant query results."""
    
    def test_error_status_is_significant(self, query_processor):
        """Test that queries finding error status are marked significant."""
        result = query_processor.execute_query("?- status(X, error).")
        
        assert result.success
        assert result.is_significant
        assert result.discovery_type == "error"
    
    def test_many_results_is_significant(self, query_processor):
        """Test that queries with many results are marked significant."""
        # Create processor with many frames
        many_frames = [
            StackFrame(
                frame_id=i,
                function_name=f"func_{i}",
                caller_id=i-1 if i > 1 else None,
                timestamp=1000 + i * 10,
                memory_allocated=2048,
                status="active",
                parameters={},
            )
            for i in range(1, 10)
        ]
        processor = QueryProcessor(many_frames)
        
        result = processor.execute_query("?- status(X, active).")
        
        assert result.success
        assert result.is_significant
        assert result.discovery_type == "pattern"


class TestRequirement32_RelationshipQueries:
    """Test Requirement 3.2: Relationship query evaluation and chain traversal."""
    
    def test_find_call_chain_callees(self, query_processor):
        """Test finding all callees in a chain."""
        # Frame 1 calls 2, 2 calls 3, 3 calls 4
        # So from frame 1, callees should be [2, 3, 4]
        chain = query_processor.find_call_chain(1, "callees")
        
        assert 2 in chain
        assert 3 in chain
        assert 4 in chain
        assert 1 not in chain  # Start frame not included
    
    def test_find_call_chain_callers(self, query_processor):
        """Test finding all callers in a chain."""
        # Frame 4 is called by 3, 3 by 2, 2 by 1
        # So from frame 4, callers should be [3, 2, 1]
        chain = query_processor.find_call_chain(4, "callers")
        
        assert 3 in chain
        assert 2 in chain
        assert 1 in chain
        assert 4 not in chain  # Start frame not included
    
    def test_find_call_chain_leaf_frame(self, query_processor):
        """Test call chain from a leaf frame (no callees)."""
        chain = query_processor.find_call_chain(4, "callees")
        
        assert len(chain) == 0  # Frame 4 calls nothing
    
    def test_find_call_chain_root_frame(self, query_processor):
        """Test call chain from a root frame (no callers)."""
        chain = query_processor.find_call_chain(1, "callers")
        
        assert len(chain) == 0  # Frame 1 has no caller
    
    def test_find_call_path_exists(self, query_processor):
        """Test finding a path between two frames."""
        path = query_processor.find_call_path(1, 4)
        
        assert path is not None
        assert path[0] == 1
        assert path[-1] == 4
        assert len(path) == 4  # [1, 2, 3, 4]
        assert path == [1, 2, 3, 4]
    
    def test_find_call_path_direct(self, query_processor):
        """Test finding a direct path (one hop)."""
        path = query_processor.find_call_path(1, 2)
        
        assert path is not None
        assert path == [1, 2]
    
    def test_find_call_path_same_frame(self, query_processor):
        """Test path from frame to itself."""
        path = query_processor.find_call_path(1, 1)
        
        assert path == [1]
    
    def test_find_call_path_no_path(self, query_processor):
        """Test when no path exists between frames."""
        # Can't go backwards in call chain
        path = query_processor.find_call_path(4, 1)
        
        assert path is None
    
    def test_get_relationship_info_middle_frame(self, query_processor):
        """Test getting relationship info for a middle frame."""
        info = query_processor.get_relationship_info(2)
        
        assert info["frame_id"] == 2
        assert info["direct_caller"] == 1
        assert 3 in info["direct_callees"]
        assert 1 in info["caller_chain"]
        assert 3 in info["callee_chain"]
        assert 4 in info["callee_chain"]
    
    def test_get_relationship_info_root_frame(self, query_processor):
        """Test getting relationship info for root frame."""
        info = query_processor.get_relationship_info(1)
        
        assert info["frame_id"] == 1
        assert info["direct_caller"] is None
        assert len(info["direct_callees"]) > 0
        assert len(info["caller_chain"]) == 0
        assert len(info["callee_chain"]) > 0
    
    def test_get_relationship_info_leaf_frame(self, query_processor):
        """Test getting relationship info for leaf frame."""
        info = query_processor.get_relationship_info(4)
        
        assert info["frame_id"] == 4
        assert info["direct_caller"] == 3
        assert len(info["direct_callees"]) == 0
        assert len(info["caller_chain"]) > 0
        assert len(info["callee_chain"]) == 0
    
    def test_format_relationship_info(self, query_processor):
        """Test formatting relationship information."""
        info = query_processor.get_relationship_info(2)
        formatted = query_processor.format_relationship_info(info)
        
        assert "frame 2" in formatted
        assert "Direct caller" in formatted
        assert "Direct callees" in formatted
        assert "caller chain" in formatted.lower()
        assert "callee chain" in formatted.lower()
    
    def test_relationship_cache(self, query_processor):
        """Test that relationship queries are cached."""
        # First call
        chain1 = query_processor.find_call_chain(1, "callees")
        
        # Second call should use cache
        chain2 = query_processor.find_call_chain(1, "callees")
        
        assert chain1 == chain2
        assert (1, "callees") in query_processor._relationship_cache
    
    def test_complex_call_chain(self):
        """Test call chain with branching structure."""
        # Create a more complex call structure:
        #     1
        #    / \
        #   2   3
        #  / \   \
        # 4   5   6
        frames = [
            StackFrame(1, "root", None, 1000, 2048, "active", {}),
            StackFrame(2, "branch_a", 1, 1010, 2048, "active", {}),
            StackFrame(3, "branch_b", 1, 1020, 2048, "active", {}),
            StackFrame(4, "leaf_a1", 2, 1030, 2048, "active", {}),
            StackFrame(5, "leaf_a2", 2, 1040, 2048, "active", {}),
            StackFrame(6, "leaf_b", 3, 1050, 2048, "active", {}),
        ]
        processor = QueryProcessor(frames)
        
        # From root, should find all descendants
        chain = processor.find_call_chain(1, "callees")
        assert len(chain) == 5  # All other frames
        assert all(i in chain for i in [2, 3, 4, 5, 6])
        
        # From branch_a, should find its descendants
        chain = processor.find_call_chain(2, "callees")
        assert len(chain) == 2
        assert 4 in chain
        assert 5 in chain
        
        # From leaf, should find path back to root
        chain = processor.find_call_chain(4, "callers")
        assert 2 in chain
        assert 1 in chain
