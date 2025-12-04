# Memory Stack Puzzle - Comprehensive Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Query System](#query-system)
5. [Diagnosis System](#diagnosis-system)
6. [Hint System](#hint-system)
7. [Integration Guide](#integration-guide)
8. [Extending the Puzzle](#extending-the-puzzle)
9. [API Reference](#api-reference)

---

## Overview

The Memory Stack Puzzle is the first adventure mode puzzle in Logic Quest, designed to teach debugging concepts through Prolog-based investigation of simulated system failures. Players examine stack traces, write queries to investigate the data, and diagnose the root cause of system failures.

### Learning Objectives

- Write Prolog queries to examine structured data
- Use variables to find patterns in data sets
- Combine multiple conditions in queries
- Interpret query results to identify anomalies
- Apply logical reasoning to diagnose problems
- Understand the relationship between Prolog and real-world debugging

### Key Features

- **Five Failure Scenarios**: Memory leak, stack overflow, null pointer, deadlock, and resource exhaustion
- **Adaptive Difficulty**: Adjusts hints and guidance based on complexity level (BEGINNER to EXPERT)
- **Progress-Aware Hints**: Hints adapt based on queries made and discoveries found
- **Narrative Integration**: Cyberpunk 1985 storyline with mentor character guidance
- **Educational Content**: Connects Prolog concepts to real-world debugging practices

---

## Architecture

### Component Hierarchy

```
MemoryStackPuzzle (extends BasePuzzle)
├── StackFrameGenerator
│   └── Generates realistic stack frames with embedded anomalies
├── QueryProcessor
│   ├── QueryValidator
│   ├── ResultFormatter
│   └── Executes queries against fact database
├── DiagnosisValidator
│   └── Validates player diagnosis submissions
└── MemoryStackHintSystem (extends ComplexityAwareHintSystem)
    └── Provides progress-aware, complexity-adapted hints
```

### Data Flow

1. **Initialization**: Puzzle generates stack frame data with embedded anomaly
2. **Query Phase**: Player writes queries → Validation → Execution → Results → Feedback
3. **Discovery Phase**: Significant queries trigger acknowledgment and story progression
4. **Diagnosis Phase**: Player submits diagnosis → Validation → Completion or retry
5. **Completion**: Explanation, score calculation, progress update

---

## Core Components

### StackFrame Data Model

Represents a single stack frame in the memory trace.

```python
@dataclass
class StackFrame:
    frame_id: int                    # Unique identifier for the frame
    function_name: str               # Name of the function
    caller_id: Optional[int]         # ID of the calling frame (None for root)
    timestamp: int                   # Timestamp of the call
    memory_allocated: int            # Memory allocated by this frame (bytes)
    status: str                      # "active", "completed", or "error"
    parameters: Dict[str, Any]       # Function parameters
```

**Prolog Representation:**

Stack frames are converted to Prolog facts using the `to_prolog_facts()` method:

```prolog
% Basic frame information
frame(frame_id, function_name, timestamp, status).

% Caller-callee relationships
calls(caller_frame_id, callee_frame_id).

% Memory allocation
allocated(frame_id, bytes).

% Function parameters
param(frame_id, param_name, param_value).

% Frame status
status(frame_id, status_value).
```

### StackFrameGenerator

Generates realistic stack frames with embedded anomalies for different failure scenarios.

**Usage:**

```python
from prologresurrected.game.memory_stack_puzzle import (
    StackFrameGenerator, 
    FailureScenario
)

# Create generator for a specific scenario
generator = StackFrameGenerator(
    scenario=FailureScenario.MEMORY_LEAK,
    seed=42  # Optional: for reproducible generation
)

# Generate stack trace
stack_frames = generator.generate_stack_trace(num_frames=12)
```

**Supported Scenarios:**

1. **MEMORY_LEAK**: Multiple allocations without corresponding deallocations
2. **STACK_OVERFLOW**: Excessive recursive calls exceeding depth limits
3. **NULL_POINTER**: Functions called with null/invalid parameters
4. **DEADLOCK**: Circular lock dependencies between frames
5. **RESOURCE_EXHAUSTION**: Excessive resource consumption across multiple frames

**Customization:**

To add a new failure scenario:

1. Add the scenario to the `FailureScenario` enum
2. Implement an `_inject_<scenario_name>()` method in `StackFrameGenerator`
3. Add the scenario to the injection logic in `generate_stack_trace()`
4. Update `DiagnosisValidator.DIAGNOSIS_PATTERNS` with validation patterns
5. Add narrative text to `MemoryStackPuzzle.get_description()` and completion narratives

---

## Query System

### QueryValidator

Validates Prolog query syntax with support for simple, compound, and negation queries.

**Supported Query Types:**

1. **Simple Queries**: Single predicate with arguments
   ```prolog
   ?- frame(X, Y, Z, W).
   ?- status(1, error).
   ```

2. **Compound Queries**: Multiple conditions with AND logic
   ```prolog
   ?- frame(Id, Name, Time, Status), status(Id, error).
   ```

3. **Negation Queries**: Check for absence of data
   ```prolog
   ?- \+ status(1, error).
   ```

**Valid Predicates:**

- `frame(FrameId, FunctionName, Timestamp, Status)`
- `calls(CallerFrameId, CalleeFrameId)`
- `allocated(FrameId, Bytes)`
- `param(FrameId, ParamName, ParamValue)`
- `status(FrameId, StatusValue)`

**Usage:**

```python
from prologresurrected.game.memory_stack_puzzle import QueryValidator

# Validate a query
result = QueryValidator.validate_query("?- frame(X, Y, Z, W).")

if result.is_valid:
    print("Valid query!")
    print(f"Parsed components: {result.parsed_components}")
else:
    print(f"Error: {result.error_message}")
    print(f"Hint: {result.hint}")
```

### QueryProcessor

Executes validated queries against the stack frame fact database.

**Features:**

- Exact matching for constants
- Variable binding for pattern matching
- Compound query evaluation (AND logic)
- Negation query support
- Relationship traversal (caller/callee chains)
- Significance detection for important discoveries

**Usage:**

```python
from prologresurrected.game.memory_stack_puzzle import (
    QueryProcessor,
    StackFrameGenerator,
    FailureScenario
)

# Generate stack frames
generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
frames = generator.generate_stack_trace()

# Create query processor
processor = QueryProcessor(frames, FailureScenario.MEMORY_LEAK)

# Execute a query
result = processor.execute_query("?- status(X, error).")

if result.success:
    print(result.formatted_output)
    if result.is_significant:
        print(f"Significant discovery: {result.discovery_type}")
```

**Relationship Queries:**

The QueryProcessor provides methods for analyzing frame relationships:

```python
# Get all frames called by frame 3
callee_chain = processor.find_call_chain(start_frame=3, direction="callees")

# Get all frames that called frame 5
caller_chain = processor.find_call_chain(start_frame=5, direction="callers")

# Find path between two frames
path = processor.find_call_path(from_frame=1, to_frame=5)

# Get comprehensive relationship info
rel_info = processor.get_relationship_info(frame_id=3)
formatted = processor.format_relationship_info(rel_info)
print(formatted)
```

### ResultFormatter

Formats query results for clear display with significance highlighting.

**Features:**

- Clear variable binding display
- Empty result handling with helpful suggestions
- Significance detection and highlighting
- Context-aware explanations

**Significance Detection:**

The formatter automatically detects significant discoveries:

- **error**: Error status in frames
- **memory_anomaly**: High memory allocation (>1MB)
- **recursion**: Many recursive calls (>10)
- **null_parameter**: Null values in parameters
- **deadlock**: Lock waiting patterns
- **pattern**: Large result sets (>5 matches)

---

## Diagnosis System

### DiagnosisValidator

Validates player diagnosis submissions with support for multiple phrasings and partial credit.

**Usage:**

```python
from prologresurrected.game.memory_stack_puzzle import (
    DiagnosisValidator,
    FailureScenario
)

# Create validator for a scenario
validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)

# Validate a diagnosis
result = validator.validate_diagnosis(
    "The system has a memory leak where allocated memory is not being freed"
)

if result.is_correct:
    print("Correct diagnosis!")
    print(result.explanation)
elif result.is_partial:
    print("Partially correct")
    print(result.feedback)
else:
    print("Incorrect")
    print(result.feedback)
```

**Diagnosis Patterns:**

Each scenario has multiple acceptable phrasings. For example, MEMORY_LEAK accepts:

- "memory leak"
- "allocated not freed"
- "allocated no release"
- "memory not released"
- "buffer not freed"

**Adding New Patterns:**

To add diagnosis patterns for a new scenario:

```python
# In DiagnosisValidator.DIAGNOSIS_PATTERNS
FailureScenario.NEW_SCENARIO: {
    "required_keywords": [
        ["keyword1", "keyword2"],  # All must appear
        ["alternative1", "alternative2"],  # OR this combination
    ],
    "partial_keywords": [
        ["partial1"],  # Indicates partial understanding
    ],
    "correct_explanation": "Detailed explanation...",
    "incorrect_feedback": "Hint for incorrect diagnosis...",
    "partial_feedback": "Guidance for partial diagnosis...",
}
```

---

## Hint System

### MemoryStackHintSystem

Provides adaptive hints based on progress and complexity level.

**Hint Progression:**

1. **Exploration Phase** (0-2 queries): Encourages initial investigation
2. **Investigation Phase** (3-5 queries): Guides deeper analysis
3. **Diagnosis Phase** (6+ queries): Helps synthesize findings

**Complexity Adaptation:**

- **BEGINNER**: Detailed hints with example queries and explanations
- **INTERMEDIATE**: Moderate guidance without specific examples
- **ADVANCED**: Minimal hints focusing on concepts
- **EXPERT**: Conceptual guidance only

**Usage:**

```python
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackHintSystem,
    FailureScenario
)
from prologresurrected.game.complexity import ComplexityLevel

# Create hint system
hint_system = MemoryStackHintSystem(FailureScenario.MEMORY_LEAK)
hint_system.set_complexity_level(ComplexityLevel.BEGINNER)

# Update progress
hint_system.update_progress(
    queries_made=3,
    discoveries={"memory_anomaly"}
)

# Get adaptive hint
hint = hint_system.get_adaptive_hint()
print(hint)

# Get query suggestion (BEGINNER only)
suggestion = hint_system.generate_query_suggestion("investigation")
if suggestion:
    print(f"Try: {suggestion}")
```

**Discovery-Specific Hints:**

The hint system provides context-specific guidance based on discoveries:

- `_generate_error_investigation_hint()`: When error status found
- `_generate_memory_investigation_hint()`: When memory anomaly found
- `_generate_recursion_investigation_hint()`: When recursion detected
- `_generate_null_investigation_hint()`: When null parameters found
- `_generate_deadlock_investigation_hint()`: When deadlock pattern found

---

## Integration Guide

### Integrating with PuzzleManager

The Memory Stack Puzzle integrates with the existing puzzle system:

```python
from prologresurrected.game.puzzles import PuzzleManager
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle

# In PuzzleManager.__init__()
self.puzzles["memory_stack_failure"] = MemoryStackPuzzle()
```

### Integrating with GameState

Handle puzzle interactions in the game state:

```python
# In GameState class

def handle_puzzle_input(self, user_input: str):
    """Handle input during puzzle gameplay."""
    current_puzzle = self.puzzle_manager.get_current_puzzle()
    
    if isinstance(current_puzzle, MemoryStackPuzzle):
        # Handle query or diagnosis
        result = current_puzzle.validate_solution(user_input)
        
        if result.is_valid:
            # Display results
            self.display_message(result.parsed_components["formatted_output"])
            
            # Check for completion
            if current_puzzle.completed:
                self.handle_puzzle_completion(current_puzzle)
        else:
            # Display error
            self.display_error(result.error_message)
```

### Complexity Level Integration

The puzzle respects the global complexity level:

```python
from prologresurrected.game.complexity import ComplexityManager

# Set complexity level
complexity_manager = ComplexityManager()
complexity_manager.set_level(ComplexityLevel.INTERMEDIATE)

# Puzzle automatically adapts
puzzle = MemoryStackPuzzle()
puzzle.set_complexity_level(complexity_manager.current_level)
```

---

## Extending the Puzzle

### Adding a New Failure Scenario

**Step 1: Define the Scenario**

```python
# In FailureScenario enum
class FailureScenario(Enum):
    # ... existing scenarios ...
    BUFFER_OVERFLOW = "buffer_overflow"
```

**Step 2: Implement Stack Frame Generation**

```python
# In StackFrameGenerator class
def _inject_buffer_overflow(self) -> None:
    """Inject buffer overflow anomaly."""
    # Create frame with oversized buffer write
    frame = StackFrame(
        frame_id=self.next_frame_id,
        function_name="write_buffer",
        caller_id=self.frames[-1].frame_id if self.frames else None,
        timestamp=self.current_timestamp,
        memory_allocated=4096,
        status="error",
        parameters={
            "buffer_size": 1024,
            "write_size": 2048,  # Exceeds buffer!
            "data": "overflow_data"
        }
    )
    self.frames.append(frame)
    self.next_frame_id += 1
    self.current_timestamp += 20
```

**Step 3: Add to Generation Logic**

```python
# In generate_stack_trace()
elif self.scenario == FailureScenario.BUFFER_OVERFLOW:
    self._inject_buffer_overflow()
```

**Step 4: Add Diagnosis Patterns**

```python
# In DiagnosisValidator.DIAGNOSIS_PATTERNS
FailureScenario.BUFFER_OVERFLOW: {
    "required_keywords": [
        ["buffer", "overflow"],
        ["write", "exceeds", "buffer"],
        ["buffer", "overrun"],
    ],
    "partial_keywords": [
        ["buffer", "problem"],
        ["write", "size"],
    ],
    "correct_explanation": (
        "Correct! The system experienced a buffer overflow.\n\n"
        "The write_buffer function attempted to write 2048 bytes into "
        "a buffer that was only 1024 bytes in size. This caused memory "
        "corruption and a system crash.\n\n"
        "In real debugging, you would look for:\n"
        "- Buffer size validation before writes\n"
        "- Bounds checking in array operations\n"
        "- Use of safe string functions"
    ),
    "incorrect_feedback": (
        "Not quite. Look at the buffer sizes and write operations.\n"
        "Hint: Compare the buffer_size and write_size parameters."
    ),
    "partial_feedback": (
        "You've identified a buffer-related issue.\n"
        "But what specifically went wrong with the buffer operation?"
    ),
}
```

**Step 5: Add Narrative Content**

```python
# In MemoryStackPuzzle.get_description()
scenario_narratives = {
    # ... existing narratives ...
    FailureScenario.BUFFER_OVERFLOW: (
        "At 03:12 hours, LOGIC-1 crashed with a memory corruption fault. "
        "A buffer write operation exceeded its bounds, smashing through "
        "adjacent memory and corrupting critical system data.\n\n"
        "Your mission: analyze the stack trace and identify which operation "
        "caused the buffer overflow."
    ),
}

# In _get_completion_narrative()
completion_narratives = {
    # ... existing narratives ...
    FailureScenario.BUFFER_OVERFLOW: (
        "SYSTEM STATUS UPDATE:\n"
        ">>> LOGIC-1 DIAGNOSTIC COMPLETE\n"
        ">>> ROOT CAUSE IDENTIFIED: BUFFER OVERFLOW\n"
        ">>> REPAIR PROTOCOL INITIATED\n\n"
        "You add bounds checking to the write_buffer function...\n"
        # ... rest of narrative ...
    ),
}
```

**Step 6: Add Educational Content**

```python
# In _get_educational_summary()
educational_content = {
    # ... existing content ...
    FailureScenario.BUFFER_OVERFLOW: {
        "concept": "Buffer Overflow Detection",
        "real_world_application": (
            "Buffer overflows are critical security vulnerabilities..."
        ),
        "debugging_techniques": [
            "Use bounds checking before buffer operations",
            "Employ memory-safe functions",
            "Enable compiler protections (stack canaries, ASLR)",
        ],
        "prolog_connection": (
            "Your Prolog queries compared buffer sizes with write sizes..."
        ),
    },
}
```

### Customizing Hint Behavior

To customize hints for specific scenarios:

```python
# In MemoryStackHintSystem class

def _generate_custom_investigation_hint(self) -> str:
    """Generate hint for custom scenario."""
    if self.current_complexity_level == ComplexityLevel.BEGINNER:
        return (
            ">>> MENTOR: \"Check the buffer parameters. "
            "Compare buffer_size with write_size:\n"
            "  ?- param(Id, buffer_size, Size1), "
            "param(Id, write_size, Size2).\n\n"
            "If write_size is bigger than buffer_size, "
            "you've found your problem.\""
        )
    else:
        return (
            ">>> MENTOR: \"Compare buffer sizes with write operations. "
            "Look for size mismatches.\""
        )

# Add to _generate_investigation_hint()
elif "buffer_overflow" in self.discoveries:
    return self._generate_custom_investigation_hint()
```

---

## API Reference

### MemoryStackPuzzle

Main puzzle class extending `BasePuzzle`.

#### Constructor

```python
def __init__(
    self,
    scenario: Optional[FailureScenario] = None,
    seed: Optional[int] = None
)
```

**Parameters:**
- `scenario`: Specific failure scenario to use (random if None)
- `seed`: Random seed for reproducible generation

#### Key Methods

```python
def get_description(self) -> str
```
Returns puzzle description with narrative context and complexity-adapted guidance.

```python
def get_initial_context(self) -> Dict[str, Any]
```
Returns stack frame facts and investigation context.

**Returns:**
- `facts`: List of Prolog fact strings
- `fact_count`: Total number of facts
- `frame_count`: Number of stack frames
- `scenario_type`: Scenario identifier
- `objective`: Investigation objective text
- `example_queries`: List of example queries
- `query_templates`: (BEGINNER only) Query templates with explanations

```python
def validate_solution(self, user_input: str) -> ValidationResult
```
Validates user input (query or diagnosis).

**Parameters:**
- `user_input`: User's query or diagnosis command

**Returns:** `ValidationResult` with:
- `is_valid`: Whether input was valid
- `error_message`: Error message if invalid
- `parsed_components`: Parsed query/diagnosis results

```python
def get_hint(self, hint_level: int) -> str
```
Returns progress-aware, complexity-adapted hint.

```python
def set_complexity_level(self, level: ComplexityLevel) -> None
```
Sets complexity level and updates hint system.

```python
def get_completion_statistics(self) -> Dict[str, Any]
```
Returns detailed completion statistics including score breakdown.

**Returns:**
- `completed`: Whether puzzle is complete
- `scenario_type`: Scenario identifier
- `complexity_level`: Current complexity level
- `queries_made`: Number of queries executed
- `discoveries_found`: Number of discoveries made
- `hints_used`: Number of hints requested
- `score_breakdown`: Detailed scoring information
- `efficiency_rating`: Performance ratings
- `educational_summary`: Educational content

```python
def reset(self) -> None
```
Resets puzzle state for a new attempt.

### QueryProcessor

Executes queries against stack frame data.

#### Constructor

```python
def __init__(
    self,
    stack_frames: List[StackFrame],
    scenario_type: Optional[FailureScenario] = None
)
```

#### Key Methods

```python
def execute_query(self, query: str) -> QueryResult
```
Executes a validated query.

**Returns:** `QueryResult` with:
- `success`: Whether query executed successfully
- `results`: List of variable binding dictionaries
- `formatted_output`: Formatted result string
- `is_significant`: Whether discovery is significant
- `discovery_type`: Type of discovery (if significant)

```python
def find_call_chain(
    self,
    start_frame: int,
    direction: str = "callees"
) -> List[int]
```
Finds complete call chain from a frame.

**Parameters:**
- `start_frame`: Starting frame ID
- `direction`: "callees" or "callers"

**Returns:** List of frame IDs in the chain

```python
def get_relationship_info(self, frame_id: int) -> Dict[str, Any]
```
Gets comprehensive relationship information for a frame.

**Returns:**
- `frame_id`: The frame ID
- `direct_caller`: Direct caller frame ID
- `direct_callees`: List of direct callee frame IDs
- `caller_chain`: Complete caller chain
- `callee_chain`: Complete callee chain

### DiagnosisValidator

Validates diagnosis submissions.

#### Constructor

```python
def __init__(self, scenario_type: FailureScenario)
```

#### Key Methods

```python
def validate_diagnosis(self, diagnosis: str) -> DiagnosisResult
```
Validates a diagnosis submission.

**Returns:** `DiagnosisResult` with:
- `is_correct`: Whether diagnosis is correct
- `is_partial`: Whether diagnosis is partially correct
- `feedback`: Feedback message
- `explanation`: Detailed explanation (if correct)

```python
def get_hint_for_diagnosis(
    self,
    queries_made: int,
    discoveries: set
) -> str
```
Generates hint for formulating diagnosis.

### MemoryStackHintSystem

Provides adaptive hints.

#### Constructor

```python
def __init__(self, scenario_type: FailureScenario)
```

#### Key Methods

```python
def update_progress(
    self,
    queries_made: int,
    discoveries: Set[str]
) -> None
```
Updates progress tracking for adaptive hints.

```python
def get_adaptive_hint(self) -> str
```
Returns hint adapted to progress and complexity level.

```python
def generate_query_suggestion(self, phase: str) -> Optional[str]
```
Generates suggested query for current phase (BEGINNER only).

**Parameters:**
- `phase`: "exploration", "investigation", or "diagnosis"

**Returns:** Suggested query string or None

```python
def reset_progress(self) -> None
```
Resets progress tracking for new attempt.

---

## Best Practices

### For Players

1. **Start Broad**: Use variables to explore the data before narrowing down
2. **Look for Patterns**: Multiple similar results often indicate the problem
3. **Follow Relationships**: Use `calls/2` to trace execution flow
4. **Check Status First**: Error status is often a smoking gun
5. **Examine Parameters**: Bad data often shows up in parameters

### For Developers

1. **Test All Scenarios**: Ensure each failure scenario is discoverable
2. **Validate Queries**: Always validate before execution
3. **Provide Context**: Use story messages to maintain immersion
4. **Adapt to Complexity**: Respect the player's chosen difficulty level
5. **Track Progress**: Use discoveries to provide relevant hints

### For Educators

1. **Connect to Reality**: Emphasize real-world debugging applications
2. **Encourage Exploration**: Let students discover patterns themselves
3. **Provide Scaffolding**: Use BEGINNER level for initial learning
4. **Progress Gradually**: Move from BEGINNER to EXPERT as skills develop
5. **Discuss Findings**: Use completion statistics to review performance

---

## Troubleshooting

### Common Issues

**Issue**: Queries not returning expected results

**Solution**: Check that:
- Query syntax is valid (use `QueryValidator.validate_query()`)
- Predicate names match exactly (case-sensitive)
- Arguments are in correct order
- Variables are uppercase, constants are lowercase

**Issue**: Hints not adapting to progress

**Solution**: Ensure:
- `update_progress()` is called after each query
- Discoveries are being tracked correctly
- Complexity level is set properly

**Issue**: Diagnosis not being accepted

**Solution**: Verify:
- Diagnosis contains required keywords
- Keywords are spelled correctly
- Diagnosis is specific enough (not just partial keywords)

### Debug Mode

Enable debug output for development:

```python
# In QueryProcessor
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug output
logger = logging.getLogger(__name__)
logger.debug(f"Executing query: {query}")
logger.debug(f"Matches found: {len(matches)}")
```

---

## Performance Considerations

### Query Execution

- Fact database is built once during initialization
- Queries are executed in O(n) time where n is the number of facts
- Relationship queries use caching to avoid redundant traversals
- Compound queries short-circuit on first failed condition

### Memory Usage

- Stack frames are stored in memory (typically 10-15 frames)
- Fact database is a dictionary of lists (efficient lookup)
- Query results are not cached (to save memory)
- Relationship cache is cleared on reset

### Optimization Tips

1. **Limit Stack Frames**: Keep frame count reasonable (10-15)
2. **Cache Relationships**: Use `_relationship_cache` for repeated queries
3. **Early Termination**: Compound queries stop on first failure
4. **Lazy Evaluation**: Generate facts only when needed

---

## Testing

### Unit Testing

Test individual components:

```python
import pytest
from prologresurrected.game.memory_stack_puzzle import *

def test_query_validation():
    result = QueryValidator.validate_query("?- frame(X, Y, Z, W).")
    assert result.is_valid
    assert result.parsed_components["type"] == "simple"

def test_diagnosis_validation():
    validator = DiagnosisValidator(FailureScenario.MEMORY_LEAK)
    result = validator.validate_diagnosis("memory leak")
    assert result.is_correct
```

### Integration Testing

Test puzzle workflow:

```python
def test_puzzle_workflow():
    puzzle = MemoryStackPuzzle(
        scenario=FailureScenario.MEMORY_LEAK,
        seed=42
    )
    
    # Execute queries
    result1 = puzzle.validate_solution("?- frame(X, Y, Z, W).")
    assert result1.is_valid
    
    # Submit diagnosis
    result2 = puzzle.validate_solution(
        "diagnose memory leak - allocated memory not freed"
    )
    assert result2.is_valid
    assert puzzle.completed
```

### Property-Based Testing

Use Hypothesis for property testing:

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=100))
def test_stack_frame_generation(num_frames):
    generator = StackFrameGenerator(FailureScenario.MEMORY_LEAK)
    frames = generator.generate_stack_trace(num_frames)
    
    # Property: All frames have required fields
    for frame in frames:
        assert frame.frame_id > 0
        assert frame.function_name
        assert frame.timestamp > 0
        assert frame.memory_allocated > 0
        assert frame.status in ["active", "completed", "error"]
```

---

## Changelog

### Version 1.0.0 (Initial Release)

- Five failure scenarios implemented
- Full query system with validation
- Diagnosis validation with multiple phrasings
- Adaptive hint system with complexity levels
- Narrative integration with cyberpunk 1985 theme
- Educational content connecting to real-world debugging
- Comprehensive scoring system
- Integration with existing puzzle framework

---

## License

This documentation is part of the Logic Quest project.

---

## Support

For questions or issues:
- Check the troubleshooting section above
- Review the API reference for method signatures
- Examine the test files for usage examples
- Consult the main project documentation

---

**Last Updated**: November 30, 2025
**Version**: 1.0.0
