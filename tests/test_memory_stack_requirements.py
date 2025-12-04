"""
Requirements validation tests for Memory Stack Puzzle data models.

Validates that the implementation meets Requirements 7.1, 7.2, and 7.3
from the requirements document.
"""

from prologresurrected.game.memory_stack_puzzle import (
    StackFrame,
    StackFrameGenerator,
    FailureScenario
)


class TestRequirement71:
    """
    Requirement 7.1: WHEN the puzzle presents stack frames THEN the system 
    SHALL include realistic properties such as function names, parameters, 
    and timestamps.
    """
    
    def test_stack_frame_has_all_required_properties(self):
        """Verify stack frames include all required realistic properties."""
        frame = StackFrame(
            frame_id=1,
            function_name="init_system",
            caller_id=None,
            timestamp=1000,
            memory_allocated=4096,
            status="active",
            parameters={"config": "default"}
        )
        
        # Requirement 7.1: Must have function name
        assert hasattr(frame, 'function_name')
        assert isinstance(frame.function_name, str)
        assert len(frame.function_name) > 0
        
        # Requirement 7.1: Must have parameters
        assert hasattr(frame, 'parameters')
        assert isinstance(frame.parameters, dict)
        
        # Requirement 7.1: Must have timestamp
        assert hasattr(frame, 'timestamp')
        assert isinstance(frame.timestamp, int)
        assert frame.timestamp > 0
        
        # Additional realistic properties
        assert hasattr(frame, 'frame_id')
        assert hasattr(frame, 'memory_allocated')
        assert hasattr(frame, 'status')
    
    def test_generated_frames_have_realistic_properties(self):
        """Verify generated frames have realistic properties."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        for frame in frames:
            # Requirement 7.1: Realistic function names
            assert frame.function_name in StackFrameGenerator.SYSTEM_FUNCTIONS
            
            # Requirement 7.1: Realistic timestamps (increasing)
            assert frame.timestamp >= 1000
            
            # Requirement 7.1: Realistic memory allocation
            assert frame.memory_allocated > 0
            
            # Requirement 7.1: Valid status
            assert frame.status in ["active", "completed", "error"]


class TestRequirement72:
    """
    Requirement 7.2: WHEN the puzzle presents stack frames THEN the system 
    SHALL include at least one anomaly that indicates the failure cause.
    """
    
    def test_memory_leak_has_anomaly(self):
        """Verify memory leak scenario includes detectable anomaly."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Requirement 7.2: Must have anomaly (multiple large allocations)
        large_allocations = [
            f for f in frames 
            if f.memory_allocated >= 1048576  # 1MB or more
        ]
        assert len(large_allocations) >= 3, "Memory leak should have multiple large allocations"
        
        # Anomaly: allocate_buffer frames without cleanup
        allocate_frames = [f for f in frames if f.function_name == "allocate_buffer"]
        assert len(allocate_frames) >= 3, "Memory leak should have multiple allocations"
    
    def test_stack_overflow_has_anomaly(self):
        """Verify stack overflow scenario includes detectable anomaly."""
        generator = StackFrameGenerator(FailureScenario.STACK_OVERFLOW, seed=42)
        frames = generator.generate_stack_trace(num_frames=20)
        
        # Requirement 7.2: Must have anomaly (excessive recursion)
        recursive_frames = [f for f in frames if f.function_name == "recursive_process"]
        assert len(recursive_frames) >= 15, "Stack overflow should have excessive recursion"
        
        # Anomaly: depth exceeds max_depth
        depths = [f.parameters.get("depth", 0) for f in recursive_frames]
        max_depths = [f.parameters.get("max_depth", 0) for f in recursive_frames]
        
        # At least one frame should exceed max depth
        exceeds_max = any(d > m for d, m in zip(depths, max_depths) if m > 0)
        assert exceeds_max, "Stack overflow should have frames exceeding max depth"
    
    def test_null_pointer_has_anomaly(self):
        """Verify null pointer scenario includes detectable anomaly."""
        generator = StackFrameGenerator(FailureScenario.NULL_POINTER, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Requirement 7.2: Must have anomaly (null parameters)
        null_param_frames = [
            f for f in frames 
            if any(v is None for v in f.parameters.values())
        ]
        assert len(null_param_frames) >= 1, "Null pointer should have frames with null parameters"
        
        # Anomaly: error status
        error_frames = [f for f in frames if f.status == "error"]
        assert len(error_frames) >= 1, "Null pointer should have error status frames"
    
    def test_deadlock_has_anomaly(self):
        """Verify deadlock scenario includes detectable anomaly."""
        generator = StackFrameGenerator(FailureScenario.DEADLOCK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Requirement 7.2: Must have anomaly (circular lock waiting)
        lock_frames = [f for f in frames if f.function_name == "acquire_lock"]
        assert len(lock_frames) >= 2, "Deadlock should have multiple lock frames"
        
        # Anomaly: frames waiting for each other's locks
        waiting_locks = [
            (f.parameters.get("lock_id"), f.parameters.get("waiting_for"))
            for f in lock_frames
            if "waiting_for" in f.parameters
        ]
        assert len(waiting_locks) >= 2, "Deadlock should have circular waiting pattern"
    
    def test_resource_exhaustion_has_anomaly(self):
        """Verify resource exhaustion scenario includes detectable anomaly."""
        generator = StackFrameGenerator(FailureScenario.RESOURCE_EXHAUSTION, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Requirement 7.2: Must have anomaly (excessive resource usage)
        dataset_frames = [f for f in frames if f.function_name == "load_dataset"]
        assert len(dataset_frames) >= 5, "Resource exhaustion should have multiple dataset loads"
        
        # Anomaly: total memory usage is excessive
        total_memory = sum(f.memory_allocated for f in dataset_frames)
        assert total_memory >= 50 * 1024 * 1024, "Resource exhaustion should use excessive memory"


class TestRequirement73:
    """
    Requirement 7.3: WHEN the player examines the data THEN the system 
    SHALL ensure the anomaly is discoverable through logical queries.
    """
    
    def test_anomaly_discoverable_via_prolog_facts(self):
        """Verify anomalies are discoverable through Prolog fact queries."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Convert to Prolog facts
        all_facts = []
        for frame in frames:
            facts = frame.to_prolog_facts()
            all_facts.extend(facts)
        
        # Requirement 7.3: Anomaly should be discoverable via queries
        # For memory leak: can query for multiple allocate_buffer frames
        allocate_facts = [
            f for f in all_facts 
            if "allocate_buffer" in f and f.startswith("frame(")
        ]
        assert len(allocate_facts) >= 3, "Memory leak anomaly should be discoverable via frame queries"
        
        # Can query for high memory allocations
        high_memory_facts = [
            f for f in all_facts 
            if f.startswith("allocated(") and "1048576" in f
        ]
        assert len(high_memory_facts) >= 3, "High memory allocations should be discoverable"
    
    def test_relationships_discoverable_via_calls_facts(self):
        """Verify frame relationships are discoverable through calls facts."""
        generator = StackFrameGenerator(FailureScenario.STACK_OVERFLOW, seed=42)
        frames = generator.generate_stack_trace(num_frames=20)
        
        # Convert to Prolog facts
        all_facts = []
        for frame in frames:
            facts = frame.to_prolog_facts()
            all_facts.extend(facts)
        
        # Requirement 7.3: Relationships should be discoverable
        calls_facts = [f for f in all_facts if f.startswith("calls(")]
        assert len(calls_facts) > 0, "Frame relationships should be discoverable via calls facts"
        
        # Can trace call chains
        recursive_frames = [f for f in frames if f.function_name == "recursive_process"]
        if len(recursive_frames) >= 2:
            # Should have calls relationships between recursive frames
            recursive_ids = [f.frame_id for f in recursive_frames]
            recursive_calls = [
                f for f in calls_facts 
                if any(str(rid) in f for rid in recursive_ids)
            ]
            assert len(recursive_calls) > 0, "Recursive call chain should be discoverable"
    
    def test_parameters_discoverable_via_param_facts(self):
        """Verify parameters are discoverable through param facts."""
        generator = StackFrameGenerator(FailureScenario.NULL_POINTER, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Convert to Prolog facts
        all_facts = []
        for frame in frames:
            facts = frame.to_prolog_facts()
            all_facts.extend(facts)
        
        # Requirement 7.3: Parameters should be discoverable
        param_facts = [f for f in all_facts if f.startswith("param(")]
        assert len(param_facts) > 0, "Parameters should be discoverable via param facts"
        
        # Null parameters should be discoverable
        null_param_facts = [f for f in param_facts if "null" in f]
        assert len(null_param_facts) >= 1, "Null parameters should be discoverable"
    
    def test_status_discoverable_via_status_facts(self):
        """Verify frame status is discoverable through status facts."""
        generator = StackFrameGenerator(FailureScenario.NULL_POINTER, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Convert to Prolog facts
        all_facts = []
        for frame in frames:
            facts = frame.to_prolog_facts()
            all_facts.extend(facts)
        
        # Requirement 7.3: Status should be discoverable
        status_facts = [f for f in all_facts if f.startswith("status(")]
        assert len(status_facts) > 0, "Status should be discoverable via status facts"
        
        # Error status should be discoverable
        error_status_facts = [f for f in status_facts if "error" in f]
        assert len(error_status_facts) >= 1, "Error status should be discoverable"
