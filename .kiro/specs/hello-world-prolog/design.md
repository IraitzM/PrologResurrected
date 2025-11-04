# Hello World Prolog Challenge Design

## Overview

The Hello World Prolog Challenge is a standalone tutorial module that serves as an entry point to Logic Quest. It introduces absolute beginners to Prolog programming through a guided, interactive experience that maintains the game's 80s cyberpunk aesthetic while focusing purely on educational fundamentals.

## Architecture

### Component Integration
The challenge integrates with the existing Logic Quest architecture as a new puzzle type, but operates as a self-contained tutorial that can be accessed independently or as a prerequisite to the main game.

```
HelloWorldChallenge
├── Inherits from BasePuzzle
├── Uses Terminal for I/O and styling
├── Implements step-by-step tutorial flow
└── Provides completion tracking
```

### Tutorial Flow Architecture
The challenge follows a linear progression through five core concepts:
1. **Introduction** → What is Prolog?
2. **Facts** → Basic syntax and structure
3. **Fact Creation** → Hands-on practice
4. **Queries** → Asking questions
5. **Variables** → Dynamic queries
6. **Completion** → Summary and next steps

## Components and Interfaces

### HelloWorldPuzzle Class
```python
class HelloWorldPuzzle(BasePuzzle):
    def __init__(self):
        super().__init__("Hello World Prolog", "Prolog Basics")
        self.current_step = 0
        self.user_progress = {}
        self.validator = PrologValidator()
    
    def run(self, terminal: Terminal) -> bool:
        # Main tutorial orchestration with validation gates
    
    def step_introduction(self) -> bool:
        # Introduce Prolog concepts with active engagement requirement
    
    def step_facts_explanation(self) -> bool:
        # Explain fact syntax with component identification exercise
    
    def step_fact_creation(self) -> bool:
        # Interactive fact creation with validation gate
    
    def step_queries_explanation(self) -> bool:
        # Introduce query syntax with active practice requirement
    
    def step_variables_introduction(self) -> bool:
        # Explain variables with hands-on query creation
    
    def step_completion(self) -> bool:
        # Wrap up and celebrate
    
    def require_user_input(self, prompt: str, validator_func=None, expected_answer=None) -> str:
        # Generic method to require and validate specific user input before progression
        # MUST NOT accept "next" or "continue" as valid input
    
    def block_until_correct(self, exercise_func, max_attempts=None) -> bool:
        # Block progression until user completes exercise correctly with actual typed input
        # Provides progressive hints but requires demonstration of understanding
    
    def validate_interactive_input(self, user_input: str, exercise_type: str) -> ValidationResult:
        # Validates user input for specific exercise types (fact, query, component_id)
        # Rejects generic progression commands like "next"
```

### Tutorial Step Interface
Each tutorial step follows a consistent pattern with mandatory active participation:
- **Concept Introduction**: Brief explanation with examples
- **Active Engagement Gate**: User must provide specific input (NOT "next" or "continue") to proceed
- **Interactive Practice**: Hands-on exercise requiring typed answers (facts, queries, component identification)
- **Validation Gate**: System validates user input syntax and semantics, blocks progression until correct
- **Progressive Hints**: Increasingly specific hints for incorrect attempts, but still requires correct input
- **Progress Confirmation**: Ensure understanding through demonstrated competency before moving to next concept

### Input Validation System
```python
class PrologValidator:
    @staticmethod
    def validate_fact(user_input: str) -> ValidationResult:
        # Check fact syntax: predicate(args).
        # Must return validation result blocking progression if invalid
        # REJECTS "next", "continue", or other generic commands
    
    @staticmethod
    def validate_query(user_input: str) -> ValidationResult:
        # Check query syntax: ?- predicate(args).
        # Must return validation result blocking progression if invalid
        # REJECTS "next", "continue", or other generic commands
    
    @staticmethod
    def validate_component_identification(user_input: str, expected: str, question_type: str) -> ValidationResult:
        # Validate user's identification of fact/query components
        # Used for active learning exercises requiring specific answers
        # REJECTS "next", "continue", or other generic commands
    
    @staticmethod
    def validate_variable_query(user_input: str) -> ValidationResult:
        # Validate query with variables (uppercase letters)
        # Checks for proper variable naming and query syntax
    
    @staticmethod
    def is_generic_progression_command(user_input: str) -> bool:
        # Check if user is trying to skip with "next", "continue", etc.
        # Returns True for commands that should be rejected in interactive exercises
    
    @staticmethod
    def extract_components(fact: str) -> dict:
        # Parse predicate and arguments for validation
```

## Data Models

### Tutorial Progress
```python
@dataclass
class TutorialProgress:
    current_step: int
    completed_steps: List[str]
    user_facts: List[str]
    user_queries: List[str]
    mistakes_count: int
    hints_used: int
```

### Validation Result
```python
@dataclass
class ValidationResult:
    is_valid: bool
    error_message: Optional[str]
    hint: Optional[str]
    parsed_components: Optional[dict]
```

### Tutorial Content
```python
TUTORIAL_CONTENT = {
    "introduction": {
        "title": "Welcome to Prolog Programming",
        "explanation": [...],
        "examples": [...],
        "engagement_prompt": "Press Enter when you're ready to start learning Prolog..."
    },
    "facts": {
        "title": "Your First Prolog Fact",
        "explanation": [...],
        "examples": ["likes(alice, chocolate).", "parent(tom, bob)."],
        "identification_exercise": {
            "prompt": "In the fact 'likes(alice, chocolate).', what is the predicate?",
            "expected_answer": "likes",
            "hints": ["The predicate is the name that describes the relationship", "It comes before the parentheses"]
        },
        "practice_prompt": "Write a fact that says Bob likes pizza:",
        "expected_format": "likes(bob, pizza)."
    },
    "queries": {
        "title": "Asking Questions with Queries",
        "explanation": [...],
        "examples": ["?- likes(alice, chocolate).", "?- parent(tom, bob)."],
        "practice_exercise": {
            "prompt": "Write a query to ask if Alice likes chocolate:",
            "expected_answer": "?- likes(alice, chocolate).",
            "validation_rules": ["must_start_with_query_prefix", "must_end_with_period"]
        }
    },
    # ... additional steps with active exercises
}
```

## Error Handling

### Progressive Hint System
1. **First Error**: General syntax reminder
2. **Second Error**: Specific component identification
3. **Third Error**: Show correct format with blanks to fill
4. **Fourth Error**: Offer to show complete answer

### Error Categories
- **Syntax Errors**: Missing periods, incorrect parentheses, case issues
- **Semantic Errors**: Incorrect predicate usage, argument mismatch
- **Format Errors**: Query prefix missing, extra characters

### Recovery Mechanisms
- Allow unlimited retries with increasingly helpful hints
- Option to skip to explanation after multiple failures
- Ability to return to previous concepts for review

## Testing Strategy

### Unit Tests
- Validate each tutorial step independently
- Test input validation for all expected formats
- Verify error handling and hint progression
- Test progress tracking and state management

### Integration Tests
- Test complete tutorial flow from start to finish
- Verify integration with existing Terminal and BasePuzzle classes
- Test transition to main game after completion

### End-to-End Tests (Playwright)
```javascript
// Example E2E test structure
test('Hello World Tutorial Complete Flow', async ({ page }) => {
  // Navigate to hello world challenge
  // Complete introduction step
  // Create first fact successfully
  // Make intentional errors to test hint system
  // Complete query exercises
  // Verify completion and transition options
});
```

### Educational Effectiveness Tests
- Verify all Prolog concepts are clearly explained
- Test that examples are appropriate for beginners
- Ensure error messages are helpful, not discouraging
- Validate that progression feels natural and achievable

## User Experience Design

### Visual Consistency
- Maintain 80s cyberpunk terminal aesthetic
- Use consistent color coding (green=success, red=error, cyan=info, yellow=warning)
- Apply same ASCII art and box styling as main game

### Interaction Patterns
- Clear prompts with examples followed by mandatory specific user input (NOT "next")
- Immediate validation feedback blocking progression until correct typed answers
- Visual progress indicators showing tutorial completion through demonstrated competency
- Active engagement requirements at every major concept with hands-on exercises
- Validation gates preventing passive consumption - no "next" button progression
- Progressive hint system for incorrect attempts while still requiring correct input
- Explicit rejection of generic progression commands during interactive exercises

### Accessibility Considerations
- Clear, readable text with sufficient contrast
- Logical tab order for keyboard navigation
- Screen reader friendly content structure
- Responsive design for various screen sizes

## Performance Considerations

### Lightweight Implementation
- Minimal memory footprint for tutorial content
- Fast validation algorithms for real-time feedback
- Efficient state management for progress tracking

### Scalability
- Modular design allows easy addition of new tutorial steps
- Content externalization for easy updates
- Plugin architecture for additional beginner challenges

## Security Considerations

### Input Sanitization
- Validate all user input to prevent injection attacks
- Sanitize content before display in web interface
- Limit input length to prevent resource exhaustion

### Safe Execution Environment
- No actual Prolog interpreter execution (simulation only)
- Client-side validation with server-side verification
- Secure handling of user progress data