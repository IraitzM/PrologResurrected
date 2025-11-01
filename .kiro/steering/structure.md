# Project Structure & Architecture

## Directory Layout
```
├── main.py              # Entry point and main game loop
├── demo.py              # Quick demo of game features
├── requirements.txt     # Dependencies (empty - stdlib only)
├── README.md           # Project documentation
└── game/               # Core game package
    ├── __init__.py     # Package marker
    ├── terminal.py     # Terminal interface and styling
    ├── story.py        # Narrative engine and story progression
    ├── puzzles.py      # Puzzle management and base classes
    └── prolog_concepts.py # Individual puzzle implementations
```

## Architecture Patterns

### Separation of Concerns
- **Terminal Layer**: All I/O, styling, and user interaction
- **Story Layer**: Narrative flow, level progression, and story text
- **Puzzle Layer**: Game logic, puzzle management, and concept teaching
- **Concept Layer**: Individual puzzle implementations for each Prolog concept

### Class Hierarchy
- `BasePuzzle`: Abstract base class for all puzzles
- Individual puzzle classes inherit from `BasePuzzle`
- `Terminal`: Handles all terminal operations and styling
- `StoryEngine`: Manages narrative flow and story progression
- `PuzzleManager`: Coordinates puzzle selection and execution

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