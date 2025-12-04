# Design Document: Memory Stack Failure Puzzle

## Overview

The Memory Stack Failure Puzzle is the first challenge in Logic Quest's main adventure mode, designed to teach players debugging concepts through Prolog-based investigation. Players take on the role of a junior programmer at Cyberdyne Systems investigating why the LOGIC-1 AI research computer crashed. The puzzle presents a simulated memory stack trace as Prolog facts, and players must write queries to examine the data, identify patterns, and diagnose the root cause of the failure.

This puzzle bridges the gap between the Hello World tutorial and more advanced challenges by introducing practical application of Prolog queries in a debugging context. It teaches players to think like debuggers while reinforcing their understanding of facts, queries, and variables.

### Learning Objectives

- Write Prolog queries to examine structured data
- Use variables to find patterns in data sets
- Combine multiple conditions in queries
- Interpret query results to identify anomalies
- Apply logical reasoning to diagnose problems
- Understand the relationship between Prolog and real-world debugging

### Integration with Existing System

The puzzle extends the `BasePuzzle` class from `prologresurrected/game/puzzles.py` and integrates with:
- The `PuzzleManager` for puzzle lifecycle management
- The `ComplexityManager` for adaptive difficulty
- The `StoryEngine` for narrative integration
- The validation system for query syntax checking

## Architecture

### Component Structure

```
MemoryStackPuzzle (extends BasePuzzle)
├── Stack Frame Data Generator
│   ├── Generates realistic stack frames
│   ├── Injects anomaly based on scenario
│   └── Formats as Prolog facts
├── Query Processor
│   ├── Validates query syntax
│   ├── Executes queries against fact database
│   ├── Formats results
│   └── Detects significant discoveries
├── Diagnosis Validator
│   ├── Checks submitted diagnosis
│   ├── Provides feedback
│   └── Triggers completion
├── Hint System (inherited + extended)
│   ├── Progress-aware hints
│   ├── Complexity-adapted guidance
│   └── Query suggestions
└── Narrative Integration
    ├── Story context
    ├── Progress feedback
    └── Completion narrative
```

### Data Flow

1. **Initialization**: Puzzle generates stack frame data with embedded anomaly
2. **Query Phase**: Player writes queries → Validation → Execution → Results → Feedback
3. **Discovery Phase**: Significant queries trigger acknowledgment and story progression
4. **Diagnosis Phase**: Player submits diagnosis → Validation → Completion or retry
5. **Completion**: Explanation, score calculation, progress update

## Components and Interfaces

### MemoryStackPuzzle Class

```python
class MemoryStackPuzzle(BasePuzzle):
    """
    First adventure mode puzzle teaching debugging through stack trace investigation.
    """
    
    def __init__(self):
        super().__init__(
            puzzle_id="memory_stack_failure",
            title="Memory Stack Investigation",
            difficulty=PuzzleDifficulty.BEGINNER
        )
        self.stack_frames: List[StackFrame] = []
        self.anomaly_type: str = ""
        self.queries_made: List[str] = []
        self.discoveries: Set[str] = []
        self.diagnosis_submitted: bool = False
        
    def get_description(self) -> str:
        """Returns puzzle description with narrative context."""
        
    def get_initial_context(self) -> Dict[str, Any]:
        """Returns stack frame facts and investigation objective."""
        
    def validate_solution(self, user_input: str) -> ValidationResult:
        """Validates queries or diagnosis submissions."""
        
    def execute_query(self, query: str) -> QueryResult:
        """Executes a validated query against stack frame facts."""
        
    def submit_diagnosis(self, diagnosis: str) -> DiagnosisResult:
        """Validates and processes a diagnosis submission."""
        
    def get_hint(self, hint_level: int) -> str:
        """Returns progress-aware, complexity-adapted hints."""
```

### StackFrame Data Model

```python
@dataclass
class StackFrame:
    """Represents a single stack frame in the memory trace."""
    frame_id: int
    function_name: str
    caller_id: Optional[int]
    timestamp: int
    memory_allocated: int
    status: str  # "active", "completed", "error"
    parameters: Dict[str, Any]
    
    def to_prolog_facts(self) -> List[str]:
        """Converts stack frame to Prolog fact representation."""
```

### QueryResult Data Model

```python
@dataclass
class QueryResult:
    """Result of executing a query."""
    success: bool
    results: List[Dict[str, Any]]
    formatted_output: str
    is_significant: bool  # True if query reveals important information
    discovery_type: Optional[str]  # Type of discovery made, if any
```

### Query Processor

```python
class QueryProcessor:
    """Processes Prolog queries against stack frame data."""
    
    def __init__(self, stack_frames: List[StackFrame]):
        self.facts = self._build_fact_database(stack_frames)
        
    def validate_query(self, query: str) -> ValidationResult:
        """Validates Prolog query syntax."""
        
    def execute_query(self, query: str) -> QueryResult:
        """Executes query and returns results."""
        
    def format_results(self, results: List[Dict]) -> str:
        """Formats query results for display."""
        
    def detect_significance(self, query: str, results: List[Dict]) -> Tuple[bool, Optional[str]]:
        """Determines if query reveals significant information."""
```

### Diagnosis Validator

```python
class DiagnosisValidator:
    """Validates player diagnosis of root cause."""
    
    def __init__(self, anomaly_type: str):
        self.correct_diagnosis = anomaly_type
        self.diagnosis_patterns = self._load_diagnosis_patterns()
        
    def validate_diagnosis(self, diagnosis: str) -> DiagnosisResult:
        """Checks if diagnosis correctly identifies the root cause."""
        
    def get_feedback(self, diagnosis: str, is_correct: bool) -> str:
        """Provides feedback on diagnosis attempt."""
```

## Data Models

### Stack Frame Scenarios

The puzzle supports multiple failure scenarios, each with a different anomaly type:

1. **Memory Leak**: A function allocates memory but never releases it
2. **Stack Overflow**: Recursive calls exceed stack depth limit
3. **Null Pointer**: A function is called with invalid parameters
4. **Deadlock**: Two functions waiting on each other
5. **Resource Exhaustion**: System runs out of available resources

Each scenario generates appropriate stack frame data with the anomaly embedded in a discoverable way.

### Prolog Fact Schema

Stack frames are represented as Prolog facts:

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

### Example Stack Frame Data

```prolog
% Normal frames
frame(1, init_system, 1000, completed).
frame(2, load_config, 1050, completed).
frame(3, start_ai_core, 1100, active).

% Anomalous frame (memory leak example)
frame(4, allocate_buffer, 1150, active).
allocated(4, 1048576).  % 1MB allocated
frame(5, allocate_buffer, 1200, active).
allocated(5, 1048576).  % Another 1MB allocated
frame(6, allocate_buffer, 1250, active).
allocated(6, 1048576).  % Another 1MB allocated
% No corresponding deallocation facts

% Relationships
calls(1, 2).
calls(2, 3).
calls(3, 4).
calls(3, 5).
calls(3, 6).
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, the following redundancies were identified and consolidated:

- **Redundant**: 6.1 (duplicate of 1.5), 6.4 (duplicate of 4.5), 7.4 (duplicate of 5.4), 8.2 (duplicate of 3.3), 9.2 (duplicate of 2.3), 9.4 (duplicate of 2.5), 10.1 (duplicate of 1.1)
- **Consolidated**: Query validation properties (2.1, 2.5) combined into comprehensive validation property
- **Consolidated**: Result formatting properties (2.3, 9.2) combined into single formatting property
- **Consolidated**: Hint properties (4.1, 4.2, 4.3) combined into adaptive hint property

The following properties represent unique validation requirements:

### Property 1: Stack frame data structure completeness
*For any* generated stack frame, it must include all required properties: frame_id, function_name, timestamp, status, memory_allocated, and parameters.
**Validates: Requirements 7.1**

### Property 2: Query syntax validation
*For any* string input, the query validator must correctly identify whether it is syntactically valid Prolog or not, and provide specific error messages for invalid syntax.
**Validates: Requirements 2.1, 2.5**

### Property 3: Query execution correctness
*For any* syntactically valid query and fact database, executing the query must return all and only the facts that match the query conditions.
**Validates: Requirements 2.2, 3.1**

### Property 4: Result formatting consistency
*For any* query result set, the formatted output must include all result bindings in a clear, structured format.
**Validates: Requirements 2.3**

### Property 5: Variable binding completeness
*For any* query containing variables, the system must return all valid variable bindings that satisfy the query.
**Validates: Requirements 3.3**

### Property 6: Relationship query evaluation
*For any* query about frame relationships (caller/callee), the system must correctly evaluate the relationships based on the calls/2 facts.
**Validates: Requirements 3.2**

### Property 7: Compound query evaluation
*For any* query with multiple conditions (logical AND), the system must return only results that satisfy all conditions.
**Validates: Requirements 8.3**

### Property 8: Diagnosis validation correctness
*For any* diagnosis submission, the validator must correctly identify whether it matches the root cause, regardless of exact wording variations.
**Validates: Requirements 5.1, 5.3**

### Property 9: Adaptive hint progression
*For any* puzzle state (number of queries made, discoveries found), the hint system must provide hints appropriate to that progress level.
**Validates: Requirements 4.1**

### Property 10: Complexity-adapted hint detail
*For any* complexity level, hints must match the expected detail level: BEGINNER includes examples, INTERMEDIATE provides moderate guidance, ADVANCED provides minimal guidance, EXPERT provides conceptual guidance only.
**Validates: Requirements 4.4, 4.5, 6.2, 6.3**

### Property 11: Complexity level adaptation
*For any* complexity level change during the puzzle, the hint availability and explanation depth must immediately reflect the new level's configuration.
**Validates: Requirements 6.5**

### Property 12: Empty result feedback
*For any* valid query that returns no results, the system must provide an explanation of why no matches were found and suggest alternative query approaches.
**Validates: Requirements 9.5**

### Property 13: Negation query support
*For any* query checking for the absence of data (negation), the system must correctly identify when expected facts are missing.
**Validates: Requirements 8.4**

## Error Handling

### Query Validation Errors

- **Syntax Errors**: Missing periods, incorrect predicate format, unmatched parentheses
- **Semantic Errors**: Undefined predicates, incorrect arity, type mismatches
- **Feedback**: Specific error messages with suggestions for correction

### Diagnosis Validation Errors

- **Incomplete Diagnosis**: Player identifies symptoms but not root cause
- **Incorrect Diagnosis**: Player misidentifies the problem
- **Feedback**: Guidance on what was missed or misunderstood

### Edge Cases

- Empty query results: Provide explanation and suggestions
- Ambiguous diagnosis: Ask for clarification
- Complex queries: Validate step-by-step and provide detailed feedback

## Testing Strategy

### Unit Testing

Unit tests will verify specific behaviors and edge cases:

- Stack frame generation produces valid data structures
- Query validator correctly identifies syntax errors
- Diagnosis validator accepts correct variations of the answer
- Hint system provides appropriate hints for each progress state
- Complexity level changes update hint behavior
- Empty result handling provides helpful feedback
- Narrative integration includes required story elements

### Property-Based Testing

Property-based tests will verify universal properties across many inputs using the Hypothesis library for Python. Each test will run a minimum of 100 iterations with randomly generated inputs.

**Configuration**: Use Hypothesis library with 100 minimum iterations per test.

**Test Organization**: Each correctness property will be implemented as a single property-based test, tagged with the property number and requirement reference.

**Property Test 1**: Stack frame data structure completeness
- Generate random stack frames with various properties
- Verify all required fields are present and valid
- **Feature: memory-stack-puzzle, Property 1: Stack frame data structure completeness**
- **Validates: Requirements 7.1**

**Property Test 2**: Query syntax validation
- Generate random strings (valid and invalid Prolog queries)
- Verify validator correctly identifies validity
- Verify invalid queries receive specific error messages
- **Feature: memory-stack-puzzle, Property 2: Query syntax validation**
- **Validates: Requirements 2.1, 2.5**

**Property Test 3**: Query execution correctness
- Generate random fact databases and queries
- Verify query results match expected facts
- Verify no incorrect facts are returned
- **Feature: memory-stack-puzzle, Property 3: Query execution correctness**
- **Validates: Requirements 2.2, 3.1**

**Property Test 4**: Result formatting consistency
- Generate random query results
- Verify formatted output includes all bindings
- Verify formatting is consistent and clear
- **Feature: memory-stack-puzzle, Property 4: Result formatting consistency**
- **Validates: Requirements 2.3**

**Property Test 5**: Variable binding completeness
- Generate random queries with variables
- Verify all valid bindings are returned
- Verify no invalid bindings are returned
- **Feature: memory-stack-puzzle, Property 5: Variable binding completeness**
- **Validates: Requirements 3.3**

**Property Test 6**: Relationship query evaluation
- Generate random frame relationships
- Generate queries about relationships
- Verify relationship queries return correct results
- **Feature: memory-stack-puzzle, Property 6: Relationship query evaluation**
- **Validates: Requirements 3.2**

**Property Test 7**: Compound query evaluation
- Generate random queries with multiple conditions
- Verify results satisfy all conditions
- Verify results that fail any condition are excluded
- **Feature: memory-stack-puzzle, Property 7: Compound query evaluation**
- **Validates: Requirements 8.3**

**Property Test 8**: Diagnosis validation correctness
- Generate various phrasings of correct and incorrect diagnoses
- Verify correct diagnoses are accepted regardless of wording
- Verify incorrect diagnoses are rejected with feedback
- **Feature: memory-stack-puzzle, Property 8: Diagnosis validation correctness**
- **Validates: Requirements 5.1, 5.3**

**Property Test 9**: Adaptive hint progression
- Generate random puzzle states (queries made, discoveries)
- Verify hints adapt to progress level
- Verify early hints suggest exploration, later hints are more specific
- **Feature: memory-stack-puzzle, Property 9: Adaptive hint progression**
- **Validates: Requirements 4.1**

**Property Test 10**: Complexity-adapted hint detail
- Test hint generation at each complexity level
- Verify BEGINNER includes examples
- Verify INTERMEDIATE provides moderate guidance
- Verify ADVANCED provides minimal guidance
- Verify EXPERT provides conceptual guidance only
- **Feature: memory-stack-puzzle, Property 10: Complexity-adapted hint detail**
- **Validates: Requirements 4.4, 4.5, 6.2, 6.3**

**Property Test 11**: Complexity level adaptation
- Generate random complexity level changes
- Verify hint behavior immediately reflects new level
- Verify explanation depth matches new level
- **Feature: memory-stack-puzzle, Property 11: Complexity level adaptation**
- **Validates: Requirements 6.5**

**Property Test 12**: Empty result feedback
- Generate queries that return no results
- Verify explanation is provided
- Verify alternative approaches are suggested
- **Feature: memory-stack-puzzle, Property 12: Empty result feedback**
- **Validates: Requirements 9.5**

**Property Test 13**: Negation query support
- Generate fact databases with missing expected facts
- Generate negation queries
- Verify negation queries correctly identify missing facts
- **Feature: memory-stack-puzzle, Property 13: Negation query support**
- **Validates: Requirements 8.4**

### Integration Testing

- Test puzzle integration with PuzzleManager
- Test complexity level changes during active puzzle
- Test story progression triggers
- Test completion and progress updates
- Test transition to next puzzle

### End-to-End Testing

- Complete puzzle walkthrough at each complexity level
- Test hint system throughout puzzle progression
- Test diagnosis submission and feedback
- Test narrative integration and story advancement
