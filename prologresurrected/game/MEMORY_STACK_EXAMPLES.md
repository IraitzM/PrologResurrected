# Memory Stack Puzzle - Code Examples

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Query Examples](#query-examples)
3. [Custom Scenarios](#custom-scenarios)
4. [Integration Patterns](#integration-patterns)
5. [Testing Examples](#testing-examples)

---

## Basic Usage

### Example 1: Simple Puzzle Creation and Execution

```python
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackPuzzle,
    FailureScenario
)

# Create a puzzle with a specific scenario
puzzle = MemoryStackPuzzle(
    scenario=FailureScenario.MEMORY_LEAK,
    seed=42  # For reproducible testing
)

# Display the puzzle description
print(puzzle.get_description())
print("\n" + "="*70 + "\n")

# Get the initial context (stack frame facts)
context = puzzle.get_initial_context()
print(f"Stack trace loaded: {context['frame_count']} frames")
print(f"Total facts: {context['fact_count']}")
print(f"\nObjective: {context['objective']}")
```

### Example 2: Interactive Query Session

```python
def run_investigation_session(puzzle):
    """Run an interactive investigation session."""
    print("Memory Stack Investigation Terminal")
    print("Type 'hint' for guidance, 'quit' to exit")
    print("="*70)
    
    while not puzzle.completed:
        user_input = input("\n> ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            break
        
        if user_input.lower() == 'hint':
            hint = puzzle.get_hint(0)
            print(hint)
            continue
        
        # Process query or diagnosis
        result = puzzle.validate_solution(user_input)
        
        if result.is_valid:
            output = result.parsed_components.get("formatted_output", "")
            print(output)
            
            if puzzle.completed:
                print("\n" + "="*70)
                print("PUZZLE COMPLETE!")
                stats = puzzle.get_completion_statistics()
                print(f"Final Score: {stats['score_breakdown']['final_score']}")
                break
        else:
            print(f"Error: {result.error_message}")

# Usage
puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK)
run_investigation_session(puzzle)
```


### Example 3: Programmatic Query Execution

```python
from prologresurrected.game.memory_stack_puzzle import (
    QueryProcessor,
    StackFrameGenerator,
    FailureScenario
)

# Generate stack frames
generator = StackFrameGenerator(FailureScenario.NULL_POINTER, seed=123)
frames = generator.generate_stack_trace(num_frames=10)

# Create query processor
processor = QueryProcessor(frames, FailureScenario.NULL_POINTER)

# Execute various queries programmatically
queries = [
    "?- frame(X, Y, Z, W).",
    "?- status(FrameId, error).",
    "?- param(FrameId, ParamName, null).",
]

for query in queries:
    print(f"\nExecuting: {query}")
    result = processor.execute_query(query)
    
    if result.success:
        print(result.formatted_output)
        if result.is_significant:
            print(f"[SIGNIFICANT: {result.discovery_type}]")
    else:
        print(f"Error: {result.formatted_output}")
```

---

## Query Examples

### Example 4: Simple Queries

```python
# List all frames
query = "?- frame(X, Y, Z, W)."
# Returns all frames with variables bound to frame properties

# Find specific frame
query = "?- frame(1, FunctionName, Timestamp, Status)."
# Returns details for frame 1

# Find frames with error status
query = "?- status(FrameId, error)."
# Returns all frames that have error status

# Check memory allocation for a specific frame
query = "?- allocated(3, Bytes)."
# Returns memory allocated by frame 3
```

### Example 5: Compound Queries

```python
# Find frames with errors and their function names
query = "?- frame(Id, Name, Time, Status), status(Id, error)."

# Find frames with high memory allocation
query = "?- frame(Id, Name, Time, Status), allocated(Id, Bytes)."

# Find parameters for error frames
query = "?- status(Id, error), param(Id, ParamName, ParamValue)."

# Trace call relationships
query = "?- frame(Id1, caller_func, T1, S1), calls(Id1, Id2), frame(Id2, callee_func, T2, S2)."
```

### Example 6: Negation Queries

```python
# Check if frame 1 does NOT have error status
query = "?- \+ status(1, error)."

# Find frames that don't have null parameters
query = "?- \+ param(FrameId, ParamName, null)."
```

### Example 7: Relationship Queries

```python
from prologresurrected.game.memory_stack_puzzle import QueryProcessor

# Get call chain from a frame
processor = QueryProcessor(frames)

# Find all frames called by frame 3
callees = processor.find_call_chain(start_frame=3, direction="callees")
print(f"Frames called by frame 3: {callees}")

# Find all frames that called frame 5
callers = processor.find_call_chain(start_frame=5, direction="callers")
print(f"Frames that called frame 5: {callers}")

# Find path between two frames
path = processor.find_call_path(from_frame=1, to_frame=5)
if path:
    print(f"Call path from 1 to 5: {' -> '.join(map(str, path))}")

# Get comprehensive relationship info
rel_info = processor.get_relationship_info(frame_id=3)
formatted = processor.format_relationship_info(rel_info)
print(formatted)
```

---

## Custom Scenarios

### Example 8: Creating a Custom Failure Scenario

```python
from prologresurrected.game.memory_stack_puzzle import (
    StackFrameGenerator,
    StackFrame,
    FailureScenario
)
from enum import Enum

# Step 1: Extend the FailureScenario enum
class ExtendedFailureScenario(Enum):
    MEMORY_LEAK = "memory_leak"
    STACK_OVERFLOW = "stack_overflow"
    NULL_POINTER = "null_pointer"
    DEADLOCK = "deadlock"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    RACE_CONDITION = "race_condition"  # New scenario

# Step 2: Extend StackFrameGenerator
class CustomStackFrameGenerator(StackFrameGenerator):
    def generate_stack_trace(self, num_frames: int = 10):
        """Override to support custom scenario."""
        self.frames = []
        self.next_frame_id = 1
        self.current_timestamp = 1000
        
        # Generate normal frames
        self._generate_normal_frames(num_frames // 2)
        
        # Inject custom anomaly
        if self.scenario.value == "race_condition":
            self._inject_race_condition()
        else:
            # Fall back to parent implementation
            return super().generate_stack_trace(num_frames)
        
        # Generate remaining frames
        remaining = num_frames - len(self.frames)
        if remaining > 0:
            self._generate_normal_frames(remaining)
        
        return self.frames
    
    def _inject_race_condition(self):
        """Inject race condition anomaly."""
        # Frame 1: Read shared variable
        frame1 = StackFrame(
            frame_id=self.next_frame_id,
            function_name="read_shared_data",
            caller_id=self.frames[-1].frame_id if self.frames else None,
            timestamp=self.current_timestamp,
            memory_allocated=2048,
            status="active",
            parameters={"shared_var": "value_a", "thread_id": 1}
        )
        self.frames.append(frame1)
        self.next_frame_id += 1
        self.current_timestamp += 10
        
        # Frame 2: Write shared variable (different thread, same time)
        frame2 = StackFrame(
            frame_id=self.next_frame_id,
            function_name="write_shared_data",
            caller_id=self.frames[-1].frame_id if self.frames else None,
            timestamp=self.current_timestamp,  # Same timestamp!
            memory_allocated=2048,
            status="active",
            parameters={"shared_var": "value_b", "thread_id": 2}
        )
        self.frames.append(frame2)
        self.next_frame_id += 1
        self.current_timestamp += 10

# Usage
generator = CustomStackFrameGenerator(
    ExtendedFailureScenario.RACE_CONDITION
)
frames = generator.generate_stack_trace()
```


### Example 9: Custom Diagnosis Validator

```python
from prologresurrected.game.memory_stack_puzzle import DiagnosisValidator

# Extend DiagnosisValidator for custom scenario
class CustomDiagnosisValidator(DiagnosisValidator):
    DIAGNOSIS_PATTERNS = {
        **DiagnosisValidator.DIAGNOSIS_PATTERNS,
        "race_condition": {
            "required_keywords": [
                ["race", "condition"],
                ["concurrent", "access"],
                ["shared", "variable", "conflict"],
            ],
            "partial_keywords": [
                ["concurrent"],
                ["shared", "data"],
                ["thread", "conflict"],
            ],
            "correct_explanation": (
                "Correct! The system experienced a race condition.\n\n"
                "Two threads accessed the same shared variable simultaneously "
                "without proper synchronization. Thread 1 read the value while "
                "Thread 2 was writing to it, causing data corruption.\n\n"
                "In real debugging, you would look for:\n"
                "- Unsynchronized access to shared resources\n"
                "- Missing locks or mutexes\n"
                "- Concurrent operations on the same data"
            ),
            "incorrect_feedback": (
                "Not quite. Look at the timestamps and thread IDs.\n"
                "Hint: Check if multiple threads are accessing the same data."
            ),
            "partial_feedback": (
                "You've identified concurrent operations.\n"
                "But what specifically went wrong with the shared data access?"
            ),
        }
    }

# Usage
validator = CustomDiagnosisValidator("race_condition")
result = validator.validate_diagnosis("race condition on shared variable")
print(result.feedback)
```

---

## Integration Patterns

### Example 10: Integration with Game State

```python
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle
from prologresurrected.game.complexity import ComplexityLevel

class GameState:
    def __init__(self):
        self.current_puzzle = None
        self.complexity_level = ComplexityLevel.INTERMEDIATE
    
    def start_memory_stack_puzzle(self):
        """Initialize and start the memory stack puzzle."""
        self.current_puzzle = MemoryStackPuzzle()
        self.current_puzzle.set_complexity_level(self.complexity_level)
        
        # Display puzzle intro
        description = self.current_puzzle.get_description()
        self.display_message(description)
        
        # Show initial context
        context = self.current_puzzle.get_initial_context()
        self.display_message(f"\nStack trace loaded: {context['frame_count']} frames")
        
        if self.complexity_level == ComplexityLevel.BEGINNER:
            self.display_message("\nExample queries:")
            for example in context['example_queries']:
                self.display_message(f"  {example}")
    
    def handle_puzzle_input(self, user_input: str):
        """Handle user input during puzzle."""
        if not self.current_puzzle:
            return
        
        # Check for special commands
        if user_input.lower() == "hint":
            hint = self.current_puzzle.get_hint(0)
            self.display_message(hint)
            return
        
        if user_input.lower() == "progress":
            progress = self.current_puzzle.get_progress_summary()
            self.display_progress(progress)
            return
        
        # Process query or diagnosis
        result = self.current_puzzle.validate_solution(user_input)
        
        if result.is_valid:
            output = result.parsed_components.get("formatted_output", "")
            self.display_message(output)
            
            # Check for completion
            if self.current_puzzle.completed:
                self.handle_puzzle_completion()
        else:
            self.display_error(result.error_message)
    
    def handle_puzzle_completion(self):
        """Handle puzzle completion."""
        stats = self.current_puzzle.get_completion_statistics()
        
        # Display completion message
        self.display_message("\n" + "="*70)
        self.display_message("PUZZLE COMPLETE!")
        self.display_message("="*70)
        
        # Display score
        score_info = stats['score_breakdown']
        self.display_message(f"\nFinal Score: {score_info['final_score']} points")
        self.display_message(f"Queries Made: {stats['queries_made']}")
        self.display_message(f"Hints Used: {stats['hints_used']}")
        
        # Display educational summary
        edu_summary = stats['educational_summary']
        self.display_message(f"\nConcept Learned: {edu_summary['concept']}")
        self.display_message(f"\n{edu_summary['real_world_application']}")
        
        # Update player progress
        self.update_player_progress(stats)
        
        # Unlock next puzzle
        self.unlock_next_puzzle()
    
    def display_message(self, message: str):
        """Display message to player."""
        print(message)
    
    def display_error(self, error: str):
        """Display error message."""
        print(f"ERROR: {error}")
    
    def display_progress(self, progress: dict):
        """Display progress summary."""
        print(f"\nProgress Summary:")
        print(f"  Queries made: {progress['queries_made']}")
        print(f"  Discoveries: {', '.join(progress['discoveries']) if progress['discoveries'] else 'None'}")
        print(f"  Current phase: {progress['current_phase']}")
        print(f"  Hints used: {progress['hints_used']}")
    
    def update_player_progress(self, stats: dict):
        """Update player progress in game."""
        # Implementation depends on your game's progress system
        pass
    
    def unlock_next_puzzle(self):
        """Unlock the next puzzle."""
        # Implementation depends on your game's progression system
        pass

# Usage
game = GameState()
game.start_memory_stack_puzzle()

# Simulate player interaction
game.handle_puzzle_input("?- frame(X, Y, Z, W).")
game.handle_puzzle_input("?- status(FrameId, error).")
game.handle_puzzle_input("diagnose memory leak")
```

### Example 11: Complexity Level Management

```python
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle
from prologresurrected.game.complexity import ComplexityLevel

class PuzzleSession:
    def __init__(self):
        self.puzzle = MemoryStackPuzzle()
        self.complexity_level = ComplexityLevel.BEGINNER
        self.puzzle.set_complexity_level(self.complexity_level)
    
    def change_complexity(self, new_level: ComplexityLevel):
        """Change complexity level during puzzle."""
        old_level = self.complexity_level
        self.complexity_level = new_level
        self.puzzle.set_complexity_level(new_level)
        
        print(f"Complexity changed from {old_level.name} to {new_level.name}")
        print("Hint availability and guidance have been adjusted.")
        
        # Show adapted examples
        examples = self.puzzle.get_complexity_adapted_examples()
        if examples:
            print("\nExample queries for this level:")
            for example in examples:
                print(f"  {example}")
    
    def show_complexity_info(self):
        """Show information about current complexity level."""
        level_info = {
            ComplexityLevel.BEGINNER: {
                "description": "Detailed hints with examples and templates",
                "hints": "Unlimited",
                "examples": "Full examples with explanations",
            },
            ComplexityLevel.INTERMEDIATE: {
                "description": "Moderate guidance without templates",
                "hints": "Limited",
                "examples": "Basic examples only",
            },
            ComplexityLevel.ADVANCED: {
                "description": "Minimal guidance",
                "hints": "Very limited",
                "examples": "Minimal examples",
            },
            ComplexityLevel.EXPERT: {
                "description": "Conceptual guidance only",
                "hints": "Extremely limited",
                "examples": "No examples",
            },
        }
        
        info = level_info[self.complexity_level]
        print(f"\nCurrent Complexity: {self.complexity_level.name}")
        print(f"Description: {info['description']}")
        print(f"Hints: {info['hints']}")
        print(f"Examples: {info['examples']}")

# Usage
session = PuzzleSession()
session.show_complexity_info()

# Player wants more challenge
session.change_complexity(ComplexityLevel.ADVANCED)
```


---

## Testing Examples

### Example 12: Unit Testing Components

```python
import pytest
from prologresurrected.game.memory_stack_puzzle import (
    QueryValidator,
    QueryProcessor,
    DiagnosisValidator,
    StackFrameGenerator,
    FailureScenario,
)

class TestQueryValidator:
    """Test query validation."""
    
    def test_valid_simple_query(self):
        result = QueryValidator.validate_query("?- frame(X, Y, Z, W).")
        assert result.is_valid
        assert result.parsed_components["type"] == "simple"
        assert result.parsed_components["predicate"] == "frame"
    
    def test_invalid_missing_prefix(self):
        result = QueryValidator.validate_query("frame(X, Y, Z, W).")
        assert not result.is_valid
        assert "Missing query prefix" in result.error_message
    
    def test_valid_compound_query(self):
        query = "?- frame(Id, Name, Time, Status), status(Id, error)."
        result = QueryValidator.validate_query(query)
        assert result.is_valid
        assert result.parsed_components["type"] == "compound"
        assert result.parsed_components["condition_count"] == 2
    
    def test_valid_negation_query(self):
        result = QueryValidator.validate_query("?- \+ status(1, error).")
        assert result.is_valid
        assert result.parsed_components["type"] == "negation"

class TestQueryProcessor:
    """Test query execution."""
    
    @pytest.fixture
    def processor(self):
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK, seed=42)
        frames = generator.generate_stack_trace(num_frames=10)
        return QueryProcessor(frames, FailureScenario.MEMORY_LEAK)
    
    def test_execute_simple_query(self, processor):
        result = processor.execute_query("?- frame(X, Y, Z, W).")
        assert result.success
        assert len(result.results) > 0
    
    def test_execute_with_constants(self, processor):
        result = processor.execute_query("?- status(1, active).")
        assert result.success
    
    def test_find_call_chain(self, processor):
        chain = processor.find_call_chain(start_frame=1, direction="callees")
        assert isinstance(chain, list)

class TestDiagnosisValidator:
    """Test diagnosis validation."""
    
    def test_correct_diagnosis(self):
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("memory leak - allocated memory not freed")
        assert result.is_correct
        assert result.explanation is not None
    
    def test_partial_diagnosis(self):
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("memory problem")
        assert not result.is_correct
        assert result.is_partial
    
    def test_incorrect_diagnosis(self):
        validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
        result = validator.validate_diagnosis("stack overflow")
        assert not result.is_correct
        assert not result.is_partial
```

### Example 13: Integration Testing

```python
import pytest
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackPuzzle,
    FailureScenario
)
from prologresurrected.game.complexity import ComplexityLevel

class TestMemoryStackPuzzle:
    """Test complete puzzle workflow."""
    
    @pytest.fixture
    def puzzle(self):
        return MemoryStackPuzzle(
            scenario=FailureScenario.MEMORY_LEAK,
            seed=42
        )
    
    def test_puzzle_initialization(self, puzzle):
        assert puzzle.puzzle_id == "memory_stack_failure"
        assert not puzzle.completed
        assert len(puzzle.stack_frames) > 0
    
    def test_query_execution(self, puzzle):
        result = puzzle.validate_solution("?- frame(X, Y, Z, W).")
        assert result.is_valid
        assert "formatted_output" in result.parsed_components
    
    def test_diagnosis_submission(self, puzzle):
        # First make some queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- status(X, error).")
        
        # Submit diagnosis
        result = puzzle.validate_solution("diagnose memory leak")
        assert result.is_valid
        assert puzzle.completed
    
    def test_hint_system(self, puzzle):
        hint = puzzle.get_hint(0)
        assert isinstance(hint, str)
        assert len(hint) > 0
    
    def test_complexity_adaptation(self, puzzle):
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        context = puzzle.get_initial_context()
        assert "query_templates" in context
        
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        examples = puzzle.get_complexity_adapted_examples()
        assert len(examples) == 0  # No examples for expert
    
    def test_completion_statistics(self, puzzle):
        # Complete the puzzle
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("diagnose memory leak")
        
        stats = puzzle.get_completion_statistics()
        assert stats["completed"]
        assert "score_breakdown" in stats
        assert "educational_summary" in stats
    
    def test_reset(self, puzzle):
        # Make some progress
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.get_hint(0)
        
        # Reset
        puzzle.reset()
        
        assert len(puzzle.queries_made) == 0
        assert len(puzzle.discoveries) == 0
        assert not puzzle.completed
```

### Example 14: Property-Based Testing

```python
from hypothesis import given, strategies as st
from prologresurrected.game.memory_stack_puzzle import (
    StackFrameGenerator,
    FailureScenario,
    QueryValidator,
)

class TestStackFrameProperties:
    """Property-based tests for stack frames."""
    
    @given(st.integers(min_value=5, max_value=20))
    def test_frame_count_property(self, num_frames):
        """Property: Generated frames match requested count."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
        frames = generator.generate_stack_trace(num_frames)
        
        # Allow some variance due to anomaly injection
        assert len(frames) >= num_frames - 2
        assert len(frames) <= num_frames + 2
    
    @given(st.integers(min_value=5, max_value=20))
    def test_frame_completeness_property(self, num_frames):
        """Property: All frames have required fields."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
        frames = generator.generate_stack_trace(num_frames)
        
        for frame in frames:
            assert frame.frame_id > 0
            assert frame.function_name
            assert frame.timestamp > 0
            assert frame.memory_allocated > 0
            assert frame.status in ["active", "completed", "error"]
    
    @given(st.sampled_from(list(FailureScenario)))
    def test_scenario_generation_property(self, scenario):
        """Property: All scenarios generate valid frames."""
        generator = StackFrameGenerator(scenario, seed=42)
        frames = generator.generate_stack_trace(10)
        
        assert len(frames) > 0
        assert all(isinstance(f.frame_id, int) for f in frames)

class TestQueryValidationProperties:
    """Property-based tests for query validation."""
    
    @given(st.text(min_size=1, max_size=100))
    def test_validation_never_crashes(self, query_text):
        """Property: Validator never crashes on any input."""
        try:
            result = QueryValidator.validate_query(query_text)
            assert isinstance(result.is_valid, bool)
        except Exception as e:
            pytest.fail(f"Validator crashed on input: {query_text}\nError: {e}")
```

### Example 15: Performance Testing

```python
import time
import pytest
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackPuzzle,
    QueryProcessor,
    StackFrameGenerator,
    FailureScenario,
)

class TestPerformance:
    """Performance tests for puzzle components."""
    
    def test_puzzle_initialization_performance(self):
        """Test that puzzle initialization is fast."""
        start = time.time()
        puzzle = MemoryStackPuzzle()
        duration = time.time() - start
        
        assert duration < 0.1, f"Initialization took {duration}s (should be < 0.1s)"
    
    def test_query_execution_performance(self):
        """Test that query execution is fast."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
        frames = generator.generate_stack_trace(20)
        processor = QueryProcessor(frames)
        
        start = time.time()
        result = processor.execute_query("?- frame(X, Y, Z, W).")
        duration = time.time() - start
        
        assert duration < 0.05, f"Query took {duration}s (should be < 0.05s)"
    
    def test_large_stack_trace_performance(self):
        """Test performance with large stack traces."""
        generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
        
        start = time.time()
        frames = generator.generate_stack_trace(100)
        duration = time.time() - start
        
        assert duration < 0.5, f"Large trace generation took {duration}s"
        assert len(frames) >= 95  # Allow some variance
```

---

## Advanced Examples

### Example 16: Custom Hint System

```python
from prologresurrected.game.memory_stack_puzzle import MemoryStackHintSystem
from prologresurrected.game.complexity import ComplexityLevel

class CustomHintSystem(MemoryStackHintSystem):
    """Custom hint system with additional features."""
    
    def get_adaptive_hint(self) -> str:
        """Override to add custom hint logic."""
        # Check if player is stuck
        if self.queries_made > 10 and len(self.discoveries) == 0:
            return self._generate_stuck_hint()
        
        # Otherwise use parent implementation
        return super().get_adaptive_hint()
    
    def _generate_stuck_hint(self) -> str:
        """Generate hint when player is stuck."""
        return (
            ">>> MENTOR: \"You've made a lot of queries but haven't found "
            "the key clues yet. Let me give you a direct pointer:\n\n"
            "Try this query: ?- status(X, error).\n\n"
            "That'll show you which frames have errors. Start there.\""
        )
    
    def get_hint_with_cost(self) -> tuple[str, int]:
        """Get hint with associated point cost."""
        hint = self.get_adaptive_hint()
        
        # Calculate cost based on complexity level
        cost_map = {
            ComplexityLevel.BEGINNER: 5,
            ComplexityLevel.INTERMEDIATE: 10,
            ComplexityLevel.ADVANCED: 15,
            ComplexityLevel.EXPERT: 20,
        }
        
        cost = cost_map.get(self.current_complexity_level, 10)
        return hint, cost

# Usage
hint_system = CustomHintSystem(FailureScenario.MEMORY_LEAK)
hint_system.set_complexity_level(ComplexityLevel.INTERMEDIATE)
hint_system.update_progress(queries_made=12, discoveries=set())

hint, cost = hint_system.get_hint_with_cost()
print(f"Hint (costs {cost} points): {hint}")
```

---

**For more examples and detailed documentation, see:**
- `MEMORY_STACK_PUZZLE_DOCUMENTATION.md` - Comprehensive documentation
- `MEMORY_STACK_QUICK_START.md` - Quick start guide
- Test files in `tests/test_memory_stack_*.py` - Real test examples
