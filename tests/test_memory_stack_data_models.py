"""
Unit tests for Memory Stack Puzzle data models and stack frame generation.

Tests the StackFrame dataclass and StackFrameGenerator to ensure they
produce valid, realistic stack traces with embedded anomalies.
"""

from prologresurrected.game.memory_stack_puzzle import (
    StackFrame,
    StackFrameGenerator,
    FailureScenario
)


class TestStackFrame:
    """Test the StackFrame dataclass."""
    
    def test_stack_frame_creation(self):
        """Test creating a basic stack frame."""
        frame = StackFrame(
            frame_id=1,
            function_name="test_function",
            caller_id=None,
            timestamp=1000,
            memory_allocated=4096,
            status="active",
            parameters={"arg1": "value1"}
        )
        
        assert frame.frame_id == 1
        assert frame.function_name == "test_function"
        assert frame.caller_id is None
        assert frame.timestamp == 1000
        assert frame.memory_allocated == 4096
        assert frame.status == "active"
        assert frame.parameters == {"arg1": "value1"}
    
    def test_stack_frame_to_prolog_facts(self):
        """Test converting a stack frame to Prolog facts."""
        frame = StackFrame(
            frame_id=1,
            function_name="init_system",
            caller_id=None,
            timestamp=1000,
            memory_allocated=2048,
            status="completed",
            parameters={"config": "default"}
        )
        
        facts = frame.to_prolog_facts()
        
        # Check that all required facts are present
        assert any("frame(1, init_system, 1000, completed)" in fact for fact in facts)
        assert any("allocated(1, 2048)" in fact for fact in facts)
        assert any("param(1, config, default)" in fact for fact in facts)
        assert any("status(1, completed)" in fact for fact in facts)
        
        # Should not have calls fact since caller_id is None
        assert not any("calls(" in fact for fact in facts)
    
    def test_stack_frame_with_caller(self):
        """Test stack frame with caller relationship."""
        frame = StackFrame(
            frame_id=2,
            function_name="load_config",
            caller_id=1,
            timestamp=1050,
            memory_allocated=1024,
            status="active",
            parameters={}
        )
        
        facts = frame.to_prolog_facts()
        
        # Should have calls fact
        assert any("calls(1, 2)" in fact for fact in facts)
    
    def test_stack_frame_with_multiple_parameters(self):
        """Test stack frame with multiple parameters."""
        frame = StackFrame(
            frame_id=3,
            function_name="process_data",
            caller_id=2,
            timestamp=1100,
            memory_allocated=8192,
            status="active",
            parameters={
                "input": "data.txt",
                "size": 1024,
                "mode": "read"
            }
        )
        
        facts = frame.to_prolog_facts()
        
        # Check all parameters are present
        assert any("param(3, input, data.txt)" in fact for fact in facts)
        assert any("param(3, size, 1024)" in fact for fact in facts)
        assert any("param(3, mode, read)" in fact for fact in facts)
    
    def test_stack_frame_with_null_parameter(self):
        """Test stack frame with null parameter value."""
        frame = StackFrame(
            frame_id=4,
            function_name="validate",
            caller_id=3,
            timestamp=1200,
            memory_allocated=512,
            status="error",
            parameters={"data": None}
        )
        
        facts = frame.to_prolog_facts()
        
        # Null should be represented as "null"
        assert any("param(4, data, null)" in fact for fact in facts)


class TestStackFrameGenerator:
    """Test the StackFrameGenerator class."""
    
    def test_generator_initialization(self):
        """Test creating a stack frame generator."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
        
        assert generator.scenario == FailureScenario.MEMORY_LEAK
        assert generator.frames == []
        assert generator.next_frame_id == 1
        assert generator.current_timestamp == 1000
    
    def test_generate_stack_trace_basic(self):
        """Test generating a basic stack trace."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Should generate requested number of frames
        assert len(frames) >= 10
        
        # All frames should have valid IDs
        frame_ids = [f.frame_id for f in frames]
        assert len(frame_ids) == len(set(frame_ids))  # All unique
        
        # Timestamps should be increasing
        timestamps = [f.frame_id for f in frames]
        assert timestamps == sorted(timestamps)
    
    def test_memory_leak_scenario(self):
        """Test memory leak scenario generation."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Should have multiple allocate_buffer frames
        allocate_frames = [f for f in frames if f.function_name == "allocate_buffer"]
        assert len(allocate_frames) >= 3
        
        # All allocate frames should have large memory allocation
        for frame in allocate_frames:
            assert frame.memory_allocated == 1048576  # 1MB
            assert frame.status == "active"
    
    def test_stack_overflow_scenario(self):
        """Test stack overflow scenario generation."""
        generator = StackFrameGenerator(FailureScenario.STACK_OVERFLOW, seed=42)
        frames = generator.generate_stack_trace(num_frames=20)
        
        # Should have many recursive_process frames
        recursive_frames = [f for f in frames if f.function_name == "recursive_process"]
        assert len(recursive_frames) >= 15
        
        # Check depth parameter increases
        depths = [f.parameters.get("depth", 0) for f in recursive_frames]
        assert max(depths) >= 10  # Exceeds reasonable depth
    
    def test_null_pointer_scenario(self):
        """Test null pointer scenario generation."""
        generator = StackFrameGenerator(FailureScenario.NULL_POINTER, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Should have at least one frame with null parameters
        null_frames = [
            f for f in frames 
            if any(v is None for v in f.parameters.values())
        ]
        assert len(null_frames) >= 1
        
        # At least one should have error status
        error_frames = [f for f in frames if f.status == "error"]
        assert len(error_frames) >= 1
    
    def test_deadlock_scenario(self):
        """Test deadlock scenario generation."""
        generator = StackFrameGenerator(FailureScenario.DEADLOCK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Should have acquire_lock frames
        lock_frames = [f for f in frames if f.function_name == "acquire_lock"]
        assert len(lock_frames) >= 2
        
        # Check for circular waiting pattern
        waiting_locks = [
            f.parameters.get("waiting_for") 
            for f in lock_frames 
            if "waiting_for" in f.parameters
        ]
        assert len(waiting_locks) >= 2
    
    def test_resource_exhaustion_scenario(self):
        """Test resource exhaustion scenario generation."""
        generator = StackFrameGenerator(FailureScenario.RESOURCE_EXHAUSTION, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        
        # Should have multiple load_dataset frames with high memory
        dataset_frames = [f for f in frames if f.function_name == "load_dataset"]
        assert len(dataset_frames) >= 5
        
        # Total memory should be very high
        total_memory = sum(f.memory_allocated for f in dataset_frames)
        assert total_memory >= 50 * 1024 * 1024  # At least 50MB
    
    def test_prolog_facts_generation(self):
        """Test that generated frames can be converted to Prolog facts."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=5)
        
        # Convert all frames to Prolog facts
        all_facts = []
        for frame in frames:
            facts = frame.to_prolog_facts()
            all_facts.extend(facts)
        
        # Should have facts for all frames
        assert len(all_facts) > 0
        
        # All facts should end with period
        for fact in all_facts:
            assert fact.endswith(".")
        
        # Should have frame facts
        frame_facts = [f for f in all_facts if f.startswith("frame(")]
        assert len(frame_facts) == len(frames)
    
    def test_reproducible_generation(self):
        """Test that generation is reproducible with same seed."""
        gen1 = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=123)
        frames1 = gen1.generate_stack_trace(num_frames=10)
        
        gen2 = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=123)
        frames2 = gen2.generate_stack_trace(num_frames=10)
        
        # Should generate identical traces
        assert len(frames1) == len(frames2)
        for f1, f2 in zip(frames1, frames2):
            assert f1.frame_id == f2.frame_id
            assert f1.function_name == f2.function_name
            assert f1.memory_allocated == f2.memory_allocated
