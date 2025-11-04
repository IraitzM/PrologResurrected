# Project Structure & Architecture

## Directory Layout
```
├── main.py                   # Entry point - imports and runs Reflex app
├── pyproject.toml            # Project dependencies and configuration
├── rxconfig.py               # Reflex configuration
├── Taskfile.yml              # Task runner commands
├── README.md                 # Project documentation
├── docs/                     # Quarto documentation
├── tests/                    # Unit and integration tests
│   ├── e2e/                  # End-to-end tests
│   ├── test_*.py             # Individual test modules
│   └── ...
└── prologresurrected/        # Main Reflex package
    └── prologresurrected/    # Nested package structure (Reflex convention)
        ├── __init__.py       # Package marker
        ├── prologresurrected.py # Main Reflex app and state management
        ├── components/       # Reflex UI components
        │   ├── __init__.py
        │   └── retro_ui.py   # 80s styling and UI components
        └── game/             # Core game logic modules
            ├── __init__.py
            ├── terminal.py   # Terminal interface and styling
            ├── story.py      # Narrative engine and story progression
            ├── puzzles.py    # Puzzle management and base classes
            ├── hello_world_puzzle.py # Hello World tutorial puzzle (main puzzle)
            ├── hello_world_puzzle.py # Hello World tutorial puzzle
            ├── tutorial_content.py # Tutorial text and content
            ├── validation.py # Input validation utilities
            └── error_handling.py # Error handling utilities
```

## Architecture Patterns

### Separation of Concerns
- **Reflex App Layer**: Web interface, state management, and routing (`prologresurrected.py`)
- **UI Component Layer**: Retro styling and web components (`components/retro_ui.py`)
- **Terminal Layer**: Terminal utilities and styling helpers (`game/terminal.py`)
- **Story Layer**: Narrative flow, level progression, and story text (`game/story.py`)
- **Puzzle Layer**: Game logic, puzzle management, and base classes (`game/puzzles.py`)
- **Concept Layer**: Tutorial puzzle implementation (`game/hello_world_puzzle.py`)
- **Validation Layer**: Input validation and error handling (`game/validation.py`, `game/error_handling.py`)
- **Content Layer**: Tutorial content and text management (`game/tutorial_content.py`)

### Class Hierarchy
- `State`: Main Reflex state class in `prologresurrected.py` managing game state
- `BasePuzzle`: Abstract base class for all puzzles in `puzzles.py`
- Individual puzzle classes inherit from `BasePuzzle` (in `hello_world_puzzle.py`)
- `Terminal`: Handles terminal operations and styling utilities in `terminal.py`
- `StoryEngine`: Manages narrative flow and story progression in `story.py`
- `PuzzleManager`: Coordinates puzzle selection and execution in `puzzles.py`
- UI Components: Reflex components in `components/retro_ui.py` for web interface

### Game State Management
- Player progress tracked in dictionary format
- Level-based progression (1-5)
- Score tracking and concept completion tracking
- Simple state persistence within game session

## Code Conventions
- Use type hints for function parameters and return values
- Class names use PascalCase
- Method names use snake_case
- Constants use UPPER_CASE
- Docstrings for all classes and public methods
- Clear separation between game logic and presentation