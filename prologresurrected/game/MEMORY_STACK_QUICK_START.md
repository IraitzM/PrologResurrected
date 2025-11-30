# Memory Stack Puzzle - Quick Start Guide

## 5-Minute Quick Start

### Basic Usage

```python
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackPuzzle,
    FailureScenario
)

# Create puzzle (random scenario)
puzzle = MemoryStackPuzzle()

# Or specify a scenario
puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)

# Get puzzle description
print(puzzle.get_description())

# Get initial context (stack frame facts)
context = puzzle.get_initial_context()
print(f"Facts available: {context['fact_count']}")

# Player writes a query
user_query = "?- frame(X, Y, Z, W)."
result = puzzle.validate_solution(user_query)

if result.is_valid:
    print(result.parsed_components["formatted_output"])

# Player submits diagnosis
diagnosis = "diagnose memory leak - allocated memory not freed"
result = puzzle.validate_solution(diagnosis)

if result.is_valid and puzzle.completed:
    print("Puzzle solved!")
    stats = puzzle.get_completion_statistics()
    print(f"Score: {stats['score_breakdown']['final_score']}")
```

## Common Queries

### List All Frames
```prolog
?- frame(X, Y, Z, W).
```

### Find Frames with Errors
```prolog
?- status(FrameId, error).
```

### Check Memory Allocations
```prolog
?- allocated(FrameId, Bytes).
```

### View Parameters
```prolog
?- param(FrameId, ParamName, ParamValue).
```

### See Call Relationships
```prolog
?- calls(Caller, Callee).
```

### Compound Query (Find Error Frames)
```prolog
?- frame(Id, Name, Time, Status), status(Id, error).
```

## Failure Scenarios

| Scenario | Key Indicators | Example Diagnosis |
|----------|---------------|-------------------|
| MEMORY_LEAK | Multiple allocations, no cleanup | "memory leak - allocated memory not freed" |
| STACK_OVERFLOW | Excessive recursion depth | "stack overflow - excessive recursion" |
| NULL_POINTER | Null parameters | "null pointer - invalid parameters" |
| DEADLOCK | Circular lock dependencies | "deadlock - circular lock dependency" |
| RESOURCE_EXHAUSTION | High total memory usage | "resource exhaustion - excessive memory" |

## Complexity Levels

| Level | Hints | Examples | Templates |
|-------|-------|----------|-----------|
| BEGINNER | Detailed with examples | Yes | Yes |
| INTERMEDIATE | Moderate guidance | Basic | No |
| ADVANCED | Minimal hints | Minimal | No |
| EXPERT | Conceptual only | None | No |

## Integration Example

```python
from prologresurrected.game.puzzles import PuzzleManager
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle
from prologresurrected.game.complexity import ComplexityLevel

# Register puzzle
puzzle_manager = PuzzleManager()
puzzle = MemoryStackPuzzle()
puzzle_manager.register_puzzle(puzzle)

# Set complexity
puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)

# Game loop
while not puzzle.completed:
    user_input = input("> ")
    
    if user_input == "hint":
        print(puzzle.get_hint(0))
    else:
        result = puzzle.validate_solution(user_input)
        if result.is_valid:
            print(result.parsed_components.get("formatted_output", ""))
        else:
            print(result.error_message)

# Show completion stats
if puzzle.completed:
    stats = puzzle.get_completion_statistics()
    print(f"\nFinal Score: {stats['score_breakdown']['final_score']}")
    print(f"Queries Made: {stats['queries_made']}")
    print(f"Hints Used: {stats['hints_used']}")
```

## Adding a New Scenario (Quick Version)

1. **Add to enum:**
```python
class FailureScenario(Enum):
    NEW_SCENARIO = "new_scenario"
```

2. **Implement injection:**
```python
def _inject_new_scenario(self) -> None:
    frame = StackFrame(
        frame_id=self.next_frame_id,
        function_name="problem_function",
        # ... set anomaly properties
    )
    self.frames.append(frame)
```

3. **Add diagnosis patterns:**
```python
FailureScenario.NEW_SCENARIO: {
    "required_keywords": [["keyword1", "keyword2"]],
    "correct_explanation": "...",
    "incorrect_feedback": "...",
}
```

4. **Add narratives:**
```python
# In get_description() and _get_completion_narrative()
scenario_narratives[FailureScenario.NEW_SCENARIO] = "..."
```

## Testing Quick Reference

```python
import pytest
from prologresurrected.game.memory_stack_puzzle import *

# Test query validation
def test_query():
    result = QueryValidator.validate_query("?- frame(X, Y, Z, W).")
    assert result.is_valid

# Test query execution
def test_execution():
    generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
    frames = generator.generate_stack_trace()
    processor = QueryProcessor(frames)
    result = processor.execute_query("?- frame(X, Y, Z, W).")
    assert result.success
    assert len(result.results) > 0

# Test diagnosis
def test_diagnosis():
    validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
    result = validator.validate_diagnosis("memory leak")
    assert result.is_correct

# Test full puzzle
def test_puzzle():
    puzzle = MemoryStackPuzzle(
        scenario=FailureScenario.MEMORY_LEAK,
        seed=42
    )
    
    # Query
    result = puzzle.validate_solution("?- status(X, error).")
    assert result.is_valid
    
    # Diagnose
    result = puzzle.validate_solution("diagnose memory leak")
    assert puzzle.completed
```

## Troubleshooting

### Query Not Working?
- Check syntax: Must start with `?-` and end with `.`
- Variables must be uppercase: `X`, `FrameId`
- Constants must be lowercase: `error`, `active`
- Predicates are case-sensitive: `frame`, not `Frame`

### Diagnosis Not Accepted?
- Include key terms: "memory leak", "stack overflow", etc.
- Be specific: "memory leak" not just "memory problem"
- Check spelling of technical terms

### Hints Not Showing?
- Check complexity level (EXPERT has minimal hints)
- Ensure progress is being tracked
- Call `update_progress()` after queries

## API Quick Reference

### MemoryStackPuzzle
- `__init__(scenario, seed)` - Create puzzle
- `get_description()` - Get narrative intro
- `get_initial_context()` - Get stack frame facts
- `validate_solution(input)` - Process query/diagnosis
- `get_hint(level)` - Get adaptive hint
- `set_complexity_level(level)` - Set difficulty
- `get_completion_statistics()` - Get final stats

### QueryProcessor
- `execute_query(query)` - Execute validated query
- `find_call_chain(frame, direction)` - Get call chain
- `get_relationship_info(frame)` - Get frame relationships

### DiagnosisValidator
- `validate_diagnosis(text)` - Check diagnosis
- `get_hint_for_diagnosis(queries, discoveries)` - Get hint

### MemoryStackHintSystem
- `update_progress(queries, discoveries)` - Update state
- `get_adaptive_hint()` - Get context-aware hint
- `generate_query_suggestion(phase)` - Get query example

## Resources

- Full documentation: `MEMORY_STACK_PUZZLE_DOCUMENTATION.md`
- Test examples: `tests/test_memory_stack_*.py`
- Design document: `.kiro/specs/memory-stack-puzzle/design.md`
- Requirements: `.kiro/specs/memory-stack-puzzle/requirements.md`

---

**Need more details?** See the comprehensive documentation in `MEMORY_STACK_PUZZLE_DOCUMENTATION.md`
