# Logic Quest: A Prolog Learning Adventure

An 80s-style terminal game that teaches Prolog and logic programming through interactive storytelling and puzzles.

> **Development Status**: Core validation, tutorial content, puzzle management systems, and web interface with Reflex framework are complete and fully functional. Advanced puzzle implementation and story integration are in progress.

## Story
You are a junior programmer at Cyberdyne Systems in 1985. The company's AI research computer has malfunctioned, and its logic circuits are scrambled. You must navigate through the system's memory banks, solving logical puzzles to restore order and prevent a complete system meltdown.

## Features

### ✅ Implemented
- **Adaptive Difficulty System**: Four complexity levels that dynamically adjust puzzle parameters, hint availability, and scoring
- **Complexity-Aware Puzzles**: Automatic puzzle adaptation based on player skill level with type-specific modifications
- **Memory Stack Debugging Puzzle**: First adventure mode puzzle teaching system debugging through Prolog queries and stack trace analysis
- **Comprehensive Prolog Validation**: Robust syntax validation with detailed error messages and hints, including compound queries and negation
- **Hello World Tutorial Content**: Complete tutorial structure with step-by-step learning progression
- **Tutorial Management System**: Progress tracking, navigation, and session management
- **Puzzle Management Framework**: Complete base classes and management system for Prolog puzzles with complexity integration
- **Educational Content**: Rich explanations, examples, and practice exercises adapted to complexity level
- **Development Tooling**: Task runner, testing framework, and code quality tools

### ✅ Recently Implemented
- **Adaptive Complexity System**: Four difficulty levels (Beginner, Intermediate, Advanced, Expert) with dynamic puzzle adaptation, complexity-aware hints, and scoring multipliers
- **Complexity Configuration**: JSON-based configuration system for customizing difficulty parameters, hint frequency, and explanation depth
- **Adaptive Puzzle Factory**: Automatically adapts puzzles to selected complexity level with type-specific modifications for facts, queries, rules, patterns, and deductions
- **Memory Stack Failure Puzzle**: First adventure mode puzzle teaching debugging through Prolog-based investigation of simulated system failures with stack traces and diagnostic queries
- **Complexity-Aware Hint System**: Intelligent hint delivery that adapts to player skill level with configurable frequency and detail
- **Progress Tracking by Complexity**: Separate achievement tracking for each difficulty level with completion statistics and average scores
- **Comprehensive Error Handling System**: Advanced progressive hint system with escalating help levels, specific error messages for common Prolog syntax mistakes, encouraging tone throughout all interactions, and recovery mechanisms for stuck users
- **Hello World Prolog Tutorial**: Complete step-by-step tutorial implementation with interactive exercises, progress tracking, and educational content delivery
- **Advanced Validation Integration**: Seamless integration between error handling system and Prolog validation with structured error feedback
- **Web-Based Retro Terminal**: Modern web interface with authentic 80s terminal styling using Reflex framework
- **Enhanced Terminal Rendering**: Advanced color-coded terminal output with support for multiple text colors (green, cyan, yellow, red, white) and different output types including explanation boxes for educational content
- **Robust Terminal Display**: Defensive programming improvements with safe array bounds checking to prevent rendering errors
- **Interactive Tutorial System**: Web-based implementation of tutorial content with terminal interface
- **80s Cyberpunk Interface**: Complete visual styling with neon colors, glowing effects, and ASCII art
- **Reflex Application Structure**: Full web app with routing, state management, and responsive design
- **UI Component Library**: Custom cyberpunk-styled components (buttons, text, terminal windows, containers)
- **Optimized State Management**: Lazy initialization pattern for game objects to prevent serialization issues
- **Improved Terminal Layout**: Full-height terminal interface with optimized space utilization and fixed header/input areas

### 🚧 In Development
- **Advanced Puzzle Implementation**: Concrete puzzle classes for all Prolog concepts using the management framework
- **Complete Story Integration**: Full narrative progression with puzzle integration
- **End-to-End Testing**: Comprehensive Playwright-based browser automation tests

### 🎯 Planned
- Complete 80s cyberpunk atmosphere
- Advanced Prolog concepts (recursion, backtracking)
- Cross-platform web deployment

## Getting Started

### Prerequisites
- Python 3.13+
- uv package manager

### Installation
```bash
# Install dependencies
uv sync

# Run the web application
reflex run

# Alternative: Run with Python directly
python main.py
```

The application will start a local web server (typically at http://localhost:3000) where you can access the retro terminal interface.

**Note**: The application follows proper Reflex structure with the main app in the `prologresurrected` package. It can be run with either `reflex run` (recommended) or `python main.py`. The interface features a dual-panel layout with terminal on the left and information panel on the right, providing an optimal learning experience with interactive tutorial content.

### Quick Demo
```bash
# Demo validation utilities and puzzle system
task demo
```

### Development

#### Using Task Runner (Recommended)
This project uses [Task](https://taskfile.dev/) for command management:

```bash
# Show all available tasks
task

# Set up development environment
task setup

# Run unit tests
task test

# Run tests in watch mode
task test-watch

# Run linting and formatting
task lint

# Run development server
task dev

# Run all validation checks (tests + linting)
task validate

# Run CI pipeline
task ci

# Demo validation utilities and puzzle system
task demo
```

#### Direct Commands
```bash
# Run the web application
reflex run

# Run unit tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_validation.py -v

# Run linting and formatting
uv run ruff check .
uv run ruff format .

# Run end-to-end tests (when implemented)
uv run playwright test
```

## Project Structure
```
├── main.py                   # Simple entry point that imports from prologresurrected package
├── prologresurrected/        # Main Reflex application package
│   ├── __init__.py          # Package initialization
│   └── prologresurrected.py # Main Reflex app with interactive tutorial system
├── game/                     # Core game logic modules
│   ├── __init__.py
│   ├── complexity.py         # Core complexity level definitions and management
│   ├── complexity_config.py  # Configuration loading and validation system
│   ├── complexity_help.py    # Complexity-aware help and hint system
│   ├── complexity_error_handling.py # Error handling with complexity adaptation
│   ├── adaptive_puzzle_factory.py # Factory for creating complexity-adapted puzzles
│   ├── validation.py         # Prolog syntax validation utilities
│   ├── tutorial_content.py   # Tutorial content, navigation, and progress tracking
│   ├── puzzles.py           # Puzzle management framework with complexity integration
│   ├── hello_world_puzzle.py # Complete Hello World tutorial with complexity adaptation
│   ├── memory_stack_puzzle.py # Memory Stack Failure debugging puzzle
│   ├── error_handling.py    # Comprehensive error handling system with progressive hints
│   ├── hint_system.py       # Complexity-aware hint generation system
│   ├── terminal.py          # Terminal interface and styling (Reflex-based)
│   ├── story.py             # Narrative engine and story progression
│   └── config/
│       └── complexity/       # JSON configuration files for complexity levels
│           ├── beginner.json
│           ├── intermediate.json
│           ├── advanced.json
│           └── expert.json
├── components/               # Reflex UI components
│   ├── __init__.py
│   └── retro_ui.py          # 80s cyberpunk styling components (neon colors, terminal windows, ASCII art, explanation boxes)
├── tests/                    # Comprehensive test suite
│   ├── test_complexity.py    # Complexity system tests
│   ├── test_complexity_config.py # Configuration loading tests
│   ├── test_adaptive_puzzle_factory.py # Puzzle adaptation tests
│   ├── test_memory_stack_puzzle.py # Memory Stack puzzle tests
│   ├── test_validation.py    # Validation system tests
│   ├── test_tutorial_content.py # Tutorial content tests
│   ├── test_puzzles.py       # Puzzle management tests
│   ├── test_story.py         # Story engine tests
│   ├── test_terminal.py      # Terminal interface tests
│   ├── test_error_handling.py # Error handling system tests (27 tests)
│   ├── test_error_handling_integration.py # Error handling integration tests (10 tests)
│   ├── test_hello_world_puzzle.py # Hello World tutorial tests
│   └── e2e/                  # End-to-end browser tests
│       ├── test_welcome_screen.py
│       ├── test_tutorial_flow.py
│       ├── test_adventure_mode.py
│       ├── test_complexity_selection_interface.py
│       └── test_full_user_journey.py
├── .kiro/
│   └── specs/
│       └── hello-world-prolog/  # Tutorial specification documents
├── docs/                     # Documentation (Quarto-based)
├── rxconfig.py               # Reflex configuration file
├── demo.py                   # Quick demo of validation features
├── pyproject.toml            # Project configuration with Reflex dependencies
├── Taskfile.yml              # Task runner configuration
└── README.md
```

## Tutorial System Features

### Hello World Prolog Tutorial
The game includes a comprehensive beginner tutorial that teaches Prolog fundamentals:

- **Step-by-Step Learning**: Six structured tutorial steps from introduction to completion
- **Interactive Exercises**: Hands-on practice with fact creation and query writing
- **Progress Tracking**: Complete session management with user progress persistence
- **Content Navigation**: Forward/backward navigation through tutorial steps
- **Educational Content**: Rich explanations, examples, and practice exercises

### Tutorial Content Structure
- **Introduction**: Overview of Prolog and logic programming concepts
- **Facts Explanation**: Understanding Prolog fact syntax and structure
- **Fact Creation**: Interactive exercise to create your first Prolog fact
- **Queries Explanation**: Learning to ask questions with Prolog queries
- **Variables Introduction**: Using variables to find multiple solutions
- **Completion**: Summary and transition to advanced concepts

### Tutorial Management Classes
- **TutorialStep**: Enumeration of tutorial steps for type-safe navigation
- **TutorialProgress**: Tracks user advancement, mistakes, hints, and completion times
- **TutorialNavigator**: Handles step navigation and content loading
- **TutorialSession**: Manages complete tutorial sessions with progress persistence

## Adaptive Complexity System

Logic Quest features a sophisticated adaptive difficulty system that tailors the learning experience to your skill level:

### Four Complexity Levels

#### 🌱 Beginner
- **Maximum guidance** with step-by-step explanations
- **Always-available hints** with detailed feedback
- **Templates and examples** for every exercise
- **Scoring multiplier**: 1.0x
- **UI Indicator**: Green 🌱

#### ⚡ Intermediate
- **Moderate guidance** with standard complexity
- **Hints on request** with moderate detail
- **Examples provided** but no templates
- **Scoring multiplier**: 1.2x
- **UI Indicator**: Cyan ⚡

#### 🔥 Advanced
- **Minimal guidance** with complex problems
- **Hints after attempts** with brief explanations
- **No templates or examples**
- **Requires optimization** and multiple solution paths
- **Scoring multiplier**: 1.5x
- **UI Indicator**: Yellow 🔥

#### 💀 Expert
- **No guidance** with optimization challenges
- **No hints available**
- **Edge cases and performance constraints**
- **Requires mastery** of all concepts
- **Scoring multiplier**: 2.0x
- **UI Indicator**: Red 💀

### Adaptive Features

#### Dynamic Puzzle Adaptation
- **Automatic adjustment** of puzzle parameters based on complexity level
- **Type-specific modifications** for facts, queries, rules, patterns, and deductions
- **Variable limits** and predicate complexity scaled to skill level
- **Syntax assistance** and templates provided at lower levels

#### Complexity-Aware Hints
- **Hint frequency** adapts to complexity level (always, on-request, after-attempts, minimal, none)
- **Explanation depth** varies from detailed to minimal
- **Progressive guidance** with escalating specificity
- **Context-sensitive** help based on puzzle type and player progress

#### Separate Progress Tracking
- **Per-level achievements** track puzzles completed and scores at each complexity
- **Average scores** calculated separately for each difficulty level
- **Completion history** records which puzzles were solved at which complexity
- **Concept mastery** tracked across all complexity levels

### Configuration System

The complexity system uses JSON configuration files for easy customization:

```json
{
  "name": "Beginner",
  "description": "Maximum guidance with step-by-step explanations",
  "hint_frequency": "always",
  "explanation_depth": "detailed",
  "puzzle_parameters": {
    "max_variables": 2,
    "max_predicates": 3,
    "allow_complex_syntax": false,
    "provide_templates": true,
    "show_examples": true
  },
  "ui_indicators": {
    "color": "neon_green",
    "icon": "🌱",
    "badge": "BEGINNER"
  },
  "scoring_multiplier": 1.0
}
```

Configuration files are located in `prologresurrected/game/config/complexity/` and can be customized to create custom difficulty profiles.

### Complexity Selection

Players select their complexity level at the start of each game mode:
- **Tutorial mode**: Complexity selection before starting Hello World tutorial
- **Adventure mode**: Complexity selection before entering main game
- **In-game changes**: Players can change complexity level during gameplay with confirmation
- **Visual indicators**: Current complexity level displayed with color-coded badges

## Puzzle Management System

The game includes a comprehensive puzzle management framework that provides the foundation for all Prolog learning challenges:

### Core Components

#### BasePuzzle Abstract Class
All puzzles inherit from `BasePuzzle`, which provides:
- **Puzzle Metadata**: ID, title, difficulty level tracking
- **Attempt Tracking**: Counts attempts, hints used, completion status
- **Scoring System**: Dynamic scoring based on performance (attempts, hints)
- **Solution Validation**: Abstract interface for validating user solutions
- **Hint System**: Progressive hint delivery with escalating specificity
- **Progress Management**: Reset functionality and state tracking

#### Puzzle Classification System
- **PuzzleDifficulty**: BEGINNER, INTERMEDIATE, ADVANCED, EXPERT levels
- **PuzzleType**: Categorizes puzzles by concept (FACT_CREATION, QUERY_WRITING, RULE_DEFINITION, PATTERN_MATCHING, LOGICAL_DEDUCTION)
- **PuzzleResult**: Structured results with success status, score, feedback, and performance metrics

#### PuzzleManager
Centralized management system that handles:
- **Puzzle Registration**: Dynamic puzzle loading and organization
- **Progress Tracking**: Player statistics, completion tracking, concept mastery
- **Puzzle Selection**: Intelligent next-puzzle recommendation based on player level
- **Session Management**: Current puzzle state, solution submission, hint delivery
- **Performance Analytics**: Comprehensive statistics and progress summaries

### Puzzle Framework Features

#### Scoring Algorithm
- **Base Score**: 100 points maximum per puzzle
- **Attempt Penalty**: -10 points per additional attempt (beyond first)
- **Hint Penalty**: -15 points per hint used
- **Minimum Score**: 10 points guaranteed for completion

#### Validation Integration
- Seamless integration with the Prolog validation system
- Structured error feedback through ValidationResult
- Component extraction for advanced puzzle checking
- Custom validation logic per puzzle type

#### Progress Tracking
- **Player Statistics**: Total score, puzzles completed, attempts, hints used
- **Concept Mastery**: Tracks which Prolog concepts have been learned
- **Completion Percentage**: Overall progress through available puzzles
- **Performance Metrics**: Average scores and learning analytics

#### Architectural Benefits
- **Extensible Design**: Easy addition of new puzzle types through inheritance
- **Separation of Concerns**: Clear distinction between puzzle logic, validation, and presentation
- **Type Safety**: Comprehensive use of enums and dataclasses for robust state management
- **Testability**: Abstract base class enables comprehensive unit testing of puzzle behavior
- **Scalability**: Manager pattern supports large numbers of puzzles with efficient organization

### Example Puzzle Implementation

The framework includes multiple reference implementations:

#### SimpleFactPuzzle
- Validates creation of specific Prolog facts
- Progressive hint system with 4 levels of assistance
- Integration with PrologValidator for syntax checking
- Semantic validation for puzzle-specific requirements

#### Memory Stack Failure Puzzle
First adventure mode puzzle teaching debugging concepts:
- **Stack trace analysis**: Examine simulated system failures with realistic stack frames
- **Prolog-based investigation**: Write queries to diagnose root causes
- **Multiple failure scenarios**: Memory leaks, stack overflows, null pointers, deadlocks, resource exhaustion
- **Compound query support**: Use complex queries with multiple conditions and negation
- **Educational feedback**: Significance detection highlights important discoveries
- **Complexity adaptation**: Puzzle difficulty scales with selected complexity level

## State Management Architecture

The application uses an optimized state management pattern specifically designed for Reflex applications:

### Key Features
- **Lazy Initialization**: Game objects (TutorialSession, StoryEngine, PuzzleManager) are created only when needed
- **Serialization Safety**: Prevents issues with Reflex's state serialization by avoiding direct object instantiation in state
- **Property-Based Access**: Clean, transparent interface for accessing game components
- **Memory Efficiency**: Objects are instantiated on-demand, reducing initial memory footprint

### Implementation Pattern
```python
class GameState(rx.State):
    # Initialize as None to avoid serialization issues
    _tutorial_session = None
    _story_engine = None
    _puzzle_manager = None

    @property
    def tutorial_session(self):
        if self._tutorial_session is None:
            self._tutorial_session = TutorialSession()
        return self._tutorial_session
```

This pattern ensures that complex game objects are properly managed within Reflex's state system while maintaining clean, readable code.

## Error Handling & Validation Features

### Comprehensive Error Handling System
The game includes an advanced error handling system that provides exceptional learning support:

#### Progressive Hint System
- **Escalating Help Levels**: 5 levels of hints from gentle encouragement to complete solutions
- **Attempt-Based Progression**: Hints become more specific as users make more attempts
- **Intelligent Error Detection**: Automatic categorization of common Prolog syntax mistakes
- **Contextual Guidance**: Hints tailored to the specific type of error and exercise

#### Specific Error Messages
- **Missing Period Errors**: Detects and explains when facts/queries lack required periods
- **Uppercase Predicate Errors**: Identifies incorrect capitalization in predicate names
- **Missing Parentheses**: Catches omitted or mismatched parentheses around arguments
- **Query Prefix Issues**: Detects missing `?-` prefix in Prolog queries
- **Variable Capitalization**: Identifies lowercase variables that should be uppercase
- **Syntax Pattern Matching**: Comprehensive detection of malformed Prolog syntax

#### Encouraging Learning Environment
- **Positive Tone**: All error messages maintain supportive, encouraging language
- **Motivational Messaging**: Uses phrases like "Great attempt!", "You're learning!", "Don't give up!"
- **Learning-Focused**: Frames mistakes as natural parts of the learning process
- **Visual Elements**: Includes emojis and visual cues to maintain engagement

#### Recovery Mechanisms for Stuck Users
- **Multiple Help Options**: Continue, get hints, see examples, show answers, skip exercises
- **Alternative Explanations**: Different ways to understand the same concept
- **Adaptive Support**: More recovery options become available after multiple attempts
- **Concept Review**: Quick refreshers on key Prolog concepts when needed

### Robust Prolog Validation System
- **Fact Validation**: Validates Prolog facts with detailed error messages and hints
- **Query Validation**: Validates Prolog queries with comprehensive syntax checking
- **Component Extraction**: Parses predicates, arguments, and statement structure
- **Error Analysis**: Specific feedback for common syntax mistakes with helpful suggestions
- **Structured Results**: ValidationResult dataclass with detailed feedback components
- **Integration Ready**: Seamless integration with the progressive hint system

### Key Validation Capabilities
- Checks for proper fact syntax: `predicate(arg1, arg2).`
- Validates query syntax: `?- predicate(arg1, arg2).`
- Detects common errors: missing periods, incorrect capitalization, malformed parentheses
- Provides specific hints for each type of error
- Extracts and validates predicate names and arguments
- Supports atoms, variables, and numbers in arguments
- Returns structured ValidationResult with detailed feedback

### ValidationResult Structure
The validation system returns a `ValidationResult` dataclass containing:
- `is_valid`: Boolean indicating if the input is syntactically correct
- `error_message`: Human-readable error description (if invalid)
- `hint`: Helpful suggestion for fixing the error (if invalid)  
- `parsed_components`: Dictionary of extracted syntax components (if valid)

### Example Usage

#### Complexity System
```python
from game.complexity import ComplexityLevel, ComplexityManager
from game.adaptive_puzzle_factory import AdaptivePuzzleFactory
from game.puzzles import PuzzleManager

# Initialize complexity manager
complexity_mgr = ComplexityManager()

# Set complexity level
complexity_mgr.set_complexity_level(ComplexityLevel.INTERMEDIATE)

# Get current configuration
config = complexity_mgr.get_current_config()
print(f"Level: {config.name}")
print(f"Hint Frequency: {config.hint_frequency.value}")
print(f"Scoring Multiplier: {config.scoring_multiplier}x")

# Create adaptive puzzle factory
factory = AdaptivePuzzleFactory()

# Adapt a puzzle to current complexity level
from game.hello_world_puzzle import HelloWorldPuzzle
base_puzzle = HelloWorldPuzzle()
adapted_puzzle = factory.create_adapted_puzzle(base_puzzle, ComplexityLevel.ADVANCED)

# Get adaptation summary
summary = factory.get_adaptation_summary(adapted_puzzle)
print(f"Adapted for: {summary['complexity_level']}")
print(f"Adaptations: {summary['adaptations']}")

# Use with puzzle manager
manager = PuzzleManager()
manager.set_complexity_level(ComplexityLevel.EXPERT)

# Get complexity-specific achievements
achievements = manager.get_complexity_achievements(ComplexityLevel.INTERMEDIATE)
print(f"Puzzles completed at Intermediate: {achievements['puzzles_completed']}")
print(f"Average score: {achievements['average_score']}")
```

#### Memory Stack Puzzle
```python
from game.memory_stack_puzzle import MemoryStackPuzzle, FailureScenario

# Create memory stack puzzle
puzzle = MemoryStackPuzzle()

# Get puzzle description
description = puzzle.get_description()
print(description)

# Get initial context (stack trace facts)
context = puzzle.get_initial_context()
print(context['facts'])  # Prolog facts representing stack frames

# Validate a diagnostic query
result = puzzle.validate_solution("?- frame(X, process_request, Y, error).")
if result.is_valid:
    print("Valid query!")
    print(f"Results: {result.parsed_components}")

# Use compound queries
compound_query = "?- allocated(X, Y), Y > 1000000."
result = puzzle.validate_solution(compound_query)

# Use negation queries
negation_query = "?- \\+ status(X, completed)."
result = puzzle.validate_solution(negation_query)

# Get complexity-adapted hints
hint = puzzle.get_complexity_adapted_hint(1)
print(hint)
```

#### Error Handling System
```python
from game.error_handling import (
    ProgressiveHintSystem, RecoveryMechanisms, ErrorContext, 
    ErrorCategory, HintLevel
)
from game.validation import PrologValidator

# Validate user input with comprehensive error handling
user_input = "likes(bob, pizza)"  # Missing period
expected_answer = "likes(bob, pizza)."

# Get validation result
validation_result = PrologValidator.validate_fact(user_input)

# Create error context
error_context = ErrorContext(
    user_input=user_input,
    expected_answer=expected_answer,
    attempt_count=2,  # Second attempt
    error_category=ErrorCategory.MISSING_PERIOD,
    validation_result=validation_result,
    exercise_type="fact"
)

# Generate progressive hint response
response = ProgressiveHintSystem.generate_error_response(error_context)

print(f"Hint Level: {response.hint_level}")  # HintLevel.SPECIFIC
print(f"Message: {response.message_lines[0]}")  # "You're showing great persistence!"
print(f"Error: {response.message_lines[2]}")   # "❌ Error: Missing period at the end."
print(f"Hint: {response.message_lines[4]}")    # "💡 All Prolog facts must end with a period (.)."

# Get recovery options for stuck users
help_options = RecoveryMechanisms.offer_help_options(attempt_count=4, exercise_type="fact")
print(help_options)
# {
#     "continue": "Keep trying (I can do this!)",
#     "hint": "Give me a more specific hint", 
#     "example": "Show me a similar example",
#     "answer": "Show me the correct answer",
#     "skip": "Skip this exercise for now"
# }

# Get alternative explanations
explanation = RecoveryMechanisms.provide_alternative_explanation("fact", "syntax")
print(explanation)
# [
#     "🎯 Think of facts like entries in a database:",
#     "• Each fact is a piece of information",
#     "• It states something that is always true",
#     "• Format: relationship(thing1, thing2).",
#     ...
# ]
```

#### Hello World Tutorial Integration
```python
from game.hello_world_puzzle import HelloWorldPuzzle
from game.terminal import Terminal

# Create tutorial instance
tutorial = HelloWorldPuzzle()
terminal = Terminal()

# Run complete tutorial with error handling
success = tutorial.run(terminal)

# The tutorial automatically uses the comprehensive error handling system:
# - Progressive hints for syntax errors
# - Encouraging messages throughout
# - Recovery options for stuck users
# - Alternative explanations when needed
# - Complete answer explanations after multiple attempts
```

#### Puzzle Management System
```python
from game.puzzles import PuzzleManager, SimpleFactPuzzle, PuzzleDifficulty

# Initialize puzzle manager
manager = PuzzleManager()

# Register puzzles
simple_puzzle = SimpleFactPuzzle()
manager.register_puzzle(simple_puzzle)

# Start a puzzle
success = manager.start_puzzle("simple_fact_1")
if success:
    # Get puzzle description
    description = manager.current_puzzle.get_description()
    print(description)  # "Create a Prolog fact that states 'Alice likes chocolate'..."
    
    # Submit a solution
    result = manager.submit_solution("likes(alice, chocolate).")
    print(f"Success: {result.success}")  # True
    print(f"Score: {result.score}")      # 100 (perfect score)
    print(f"Feedback: {result.feedback}") # "Perfect! You solved it on the first try..."

# Get player progress
stats = manager.get_player_stats()
print(f"Total Score: {stats['total_score']}")
print(f"Puzzles Completed: {stats['puzzles_completed']}")

# Get progress summary
summary = manager.get_progress_summary()
print(f"Completion: {summary['completion_percentage']}%")
print(f"Average Score: {summary['average_score']}")
```

#### Custom Puzzle Creation
```python
from game.puzzles import BasePuzzle, PuzzleDifficulty, ValidationResult
from game.validation import PrologValidator

class CustomQueryPuzzle(BasePuzzle):
    def __init__(self):
        super().__init__(
            puzzle_id="custom_query_1",
            title="Write Your First Query",
            difficulty=PuzzleDifficulty.BEGINNER
        )
    
    def get_description(self) -> str:
        return "Write a query to ask if Alice likes chocolate."
    
    def validate_solution(self, user_input: str) -> ValidationResult:
        # Use the validation system
        result = PrologValidator.validate_query(user_input)
        if not result.is_valid:
            return result
        
        # Check semantic correctness
        components = result.parsed_components
        if (components.get("predicate") == "likes" and 
            "alice" in components.get("arguments", []) and
            "chocolate" in components.get("arguments", [])):
            return ValidationResult(is_valid=True)
        
        return ValidationResult(
            is_valid=False,
            error_message="Query is syntactically correct but doesn't ask about Alice and chocolate.",
            hint="Try: ?- likes(alice, chocolate)."
        )
    
    def get_hint(self, hint_level: int) -> str:
        hints = [
            "Queries start with '?-'",
            "Use the 'likes' predicate",
            "Include both 'alice' and 'chocolate' as arguments",
            "The complete answer is: ?- likes(alice, chocolate)."
        ]
        return hints[min(hint_level - 1, len(hints) - 1)]
    
    def get_expected_solution(self) -> str:
        return "?- likes(alice, chocolate)."
```

#### Tutorial System
```python
from game.tutorial_content import TutorialSession, TutorialStep

# Start a new tutorial session
session = TutorialSession()
session.start_session()

# Get current step content
content = session.get_current_content()
print(content['title'])  # "🚀 Welcome to Prolog Programming"

# Navigate through tutorial
session.advance_step()  # Move to next step
session.go_back_step()  # Go back to previous step

# Track user progress
session.record_user_input('fact', 'likes(bob, pizza).')
session.record_mistake()  # Track errors for analytics
session.record_hint_used()  # Track when hints are shown

# Get session summary
summary = session.get_session_summary()
print(f"Completion: {summary['completion_percentage']}%")
print(f"Facts created: {summary['facts_created']}")
```

#### Validation System
```python
from game.validation import PrologValidator, get_encouraging_message

# Validate a fact
result = PrologValidator.validate_fact("likes(alice, chocolate).")
print(result.is_valid)  # True
print(result.parsed_components)  # {'predicate': 'likes', 'arguments': ['alice', 'chocolate'], 'full_fact': '...'}

# Validate a query
result = PrologValidator.validate_query("?- likes(alice, X).")
print(result.is_valid)  # True

# Handle validation errors with helpful feedback
result = PrologValidator.validate_fact("likes(alice, chocolate)")  # Missing period
print(result.error_message)  # "Missing period at the end."
print(result.hint)  # "All Prolog facts must end with a period (.)."

# Get encouraging messages for learners
message = get_encouraging_message()
print(message)  # Random supportive message
```

## Web Interface Features

### Cyberpunk Visual Design
- **Neon Color Palette**: Green, cyan, yellow, red, and pink neon colors with glow effects
- **Retro Terminal Windows**: Authentic terminal styling with title bars and window controls
- **ASCII Art Display**: Cyberdyne Systems logo and decorative elements
- **Gradient Backgrounds**: Dark cyberpunk gradients with subtle lighting effects
- **Glowing Borders**: Neon border effects with box shadows for depth

### Interactive Components
- **Cyberpunk Buttons**: Hover effects with color transitions and glow animations
- **Enhanced Terminal Display**: Multi-color terminal output with proper color coding for different message types and robust error handling
- **Full-Height Terminal Interface**: Optimized layout that utilizes full browser viewport with fixed header (60px) and input area (50px)
- **Scrollable Output Area**: Terminal output area automatically scrolls and adapts to available screen space
- **Terminal Input**: Real-time command input with monospace font styling
- **Explanation Boxes**: Centered content boxes with retro styling for displaying educational content and explanations
- **Defensive Programming**: Safe array bounds checking prevents rendering errors and ensures stable terminal display
- **Responsive Layout**: Adapts to different screen sizes and devices with dynamic height calculations
- **State Management**: Persistent game state across browser sessions
- **Dynamic Content**: Real-time updates without page refreshes

### Reflex Framework Integration
- **Component-Based Architecture**: Reusable UI components for consistent styling including explanation boxes for educational content
- **Server-Side State**: Python-based state management with automatic synchronization
- **Lazy Initialization**: Game objects (TutorialSession, StoryEngine, PuzzleManager) are initialized on-demand to prevent serialization issues
- **Property-Based Access**: Clean interface for accessing game components through Python properties
- **Hot Reload**: Development server with automatic updates on code changes
- **Cross-Platform**: Runs on any device with a modern web browser

## Technology Stack
- **Framework**: Reflex (Python web framework)
- **Language**: Python 3.13+
- **Package Manager**: uv for fast dependency management
- **Testing**: pytest for unit tests, Playwright for end-to-end testing
- **Code Quality**: Ruff for linting and formatting
- **Task Runner**: Task for development workflow automation
- **Database**: SQLite for development (configured in rxconfig.py)
- **State Management**: Lazy initialization pattern for optimal Reflex performance
- **Deployment**: Web-based with cross-platform support

## Deployment

### Local Development
```bash
# Run development server
reflex run
```

### Production Deployment
```bash
# Build for production
reflex export

# Deploy to hosting platform
reflex deploy
```

The application uses SQLite for development data storage and provides cross-platform access through any modern web browser.

### State Management Architecture

The application uses an optimized state management pattern for Reflex:

- **Lazy Initialization**: Game objects are created on-demand using Python properties
- **Serialization Safety**: Prevents issues with Reflex's state serialization by avoiding direct object instantiation
- **Clean Interface**: Properties provide transparent access to game components
- **Memory Efficiency**: Objects are only created when actually needed

```python
# Example of the lazy initialization pattern
@property
def tutorial_session(self):
    if self._tutorial_session is None:
        self._tutorial_session = TutorialSession()
    return self._tutorial_session
```

## Testing
The project includes comprehensive unit tests covering:

### Error Handling System Tests (37 total tests)
- **Progressive Hint System Tests**: Verify hint level progression, error categorization, and response generation
- **Recovery Mechanism Tests**: Validate help options, alternative explanations, and adaptive support
- **Encouraging Tone Tests**: Ensure positive language throughout all error messages
- **Integration Tests**: Test complete error handling flows from user input to recovery
- **Specific Error Scenario Tests**: Cover all common Prolog syntax mistakes with appropriate responses

### Hello World Tutorial Tests
- Complete tutorial flow from introduction to completion
- Interactive exercise validation and feedback
- Step navigation and progress tracking
- Integration with error handling system
- Educational content delivery and presentation

### Puzzle Management System Tests
- BasePuzzle abstract class functionality
- PuzzleManager registration and selection
- Scoring algorithm accuracy
- Progress tracking and statistics
- Puzzle result generation and feedback
- Hint system progression
- Custom puzzle implementation patterns

### Tutorial System Tests
- Tutorial content structure and navigation
- Progress tracking and session management
- Step advancement and completion logic
- Content loading and step enumeration
- Tutorial session state management
- Lazy initialization patterns for Reflex compatibility

### Validation System Tests
- Basic validation functionality
- Comprehensive fact validation scenarios
- Comprehensive query validation scenarios
- Component extraction and parsing
- Error message generation
- Encouraging message system
- ValidationResult data structure

Run tests with:
```bash
# Using Task runner (recommended)
task test

# Or directly with pytest
uv run pytest tests/ -v

# Run specific test files
uv run pytest tests/test_error_handling.py -v          # 27 error handling tests
uv run pytest tests/test_error_handling_integration.py -v  # 10 integration tests
uv run pytest tests/test_hello_world_puzzle.py -v     # Hello World tutorial tests
uv run pytest tests/test_tutorial_content.py -v       # Tutorial system tests
uv run pytest tests/test_validation.py -v             # Validation system tests
uv run pytest tests/test_puzzles.py -v                # Puzzle management tests

# Run all validation checks (tests + linting)
task validate
```

## Learning Objectives

### Hello World Tutorial Objectives
- Understanding what Prolog is and how it differs from other programming languages
- Learning to create and understand Prolog facts with proper syntax
- Writing your first Prolog fact with guided practice
- Understanding how to ask questions using Prolog queries
- Using variables in queries to find multiple solutions
- Building confidence for advanced Prolog concepts

### Interactive Tutorial Requirements
**Important**: The tutorial system requires active participation and correct Prolog syntax:

- ❌ **Cannot progress with "next" or "continue" commands**
- ✅ **Must type correct Prolog commands to advance**
- ✅ **Each exercise requires specific answers (facts, queries, component identification)**
- ✅ **Progressive hint system provides guidance when stuck**
- ✅ **Comprehensive error messages help fix syntax mistakes**

The tutorial is designed to ensure hands-on learning rather than passive reading. You'll write actual Prolog code and receive immediate feedback on your syntax and understanding.

### Advanced Game Objectives
- **Progressive Skill Building**: Structured learning path from beginner to expert level puzzles
- **Concept Mastery**: Facts, rules, unification, pattern matching, backtracking, and recursion
- **Problem-Solving Skills**: Complex logical reasoning through interactive challenges
- **Performance Tracking**: Score-based progression with detailed feedback and analytics
- **Adaptive Learning**: Hint systems and difficulty progression based on player performance
- **Logic Programming Paradigms**: Deep understanding of declarative programming concepts

## Tutorial Content
The Hello World tutorial includes rich educational content:

- **Engaging Explanations**: Clear, beginner-friendly explanations of each concept
- **Interactive Examples**: Hands-on practice with immediate feedback
- **Progressive Difficulty**: Concepts build naturally from simple to more complex
- **Cyberpunk Theme**: 80s-style narrative woven throughout the learning experience
- **Practice Exercises**: Guided exercises with validation and hints
- **Encouraging Feedback**: Supportive messages to maintain learner motivation