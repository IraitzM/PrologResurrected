# Technology Stack & Build System

## Tech Stack
- **Language**: Python 3.13+
- **Web Framework**: Reflex for retro terminal deployment
- **Package Manager**: uv for dependency management
- **Linting**: ruff for code quality
- **Testing**: playwright for end-to-end tests
- **Platform**: Cross-platform web deployment

## Project Structure
- Reflex-based web application with retro terminal interface
- Modular architecture with separate concerns (terminal, story, puzzles, concepts)
- Object-oriented design with base classes and inheritance
- Type hints used throughout for better code clarity
- Comprehensive E2E test coverage for all puzzles and challenges

## Common Commands

### Task Runner
This project uses [Task](https://taskfile.dev/) for command management. Install with: `go install github.com/go-task/task/v3/cmd/task@latest`

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

# Check code format without changes
task lint-check

# Run all validation checks
task validate

# Run development server (when ready)
task dev

# Clean build artifacts
task clean

# Build package
task build

# Run CI pipeline
task ci

# Demo validation utilities
task demo
```

### Direct Commands (if Task not available)
```bash
# Install dependencies
uv sync

# Run development server
reflex run

# Run linting
ruff check .
ruff format .

# Run unit tests
uv run pytest tests/ -v

# Run end-to-end tests
playwright test
```

### Production Deployment
```bash
# Build for production
reflex export

# Deploy
reflex deploy
```

### Testing
- All puzzles must have corresponding E2E tests
- Tests should cover successful completion paths
- Tests should verify educational content delivery
- Tests should validate retro terminal styling and interactions

#### Unit Testing Requirements
- **All new code must have passing unit tests before being considered complete**
- Use pytest for unit testing framework
- Test files should be placed in `tests/` directory
- Run tests with: `uv run pytest tests/ -v`
- All validation utilities, game logic, and core functionality must be tested
- Tests must pass in CI/CD pipeline before merging

## Reflex Terminal Features
- Web-based retro terminal interface with CSS styling
- 80s cyberpunk color scheme (green, cyan, yellow, red)
- Typewriter effect animations
- ASCII art rendering in browser
- Interactive input components with retro styling
- Responsive design for various screen sizes

## Code Organization
- `main.py`: Reflex app entry point and routing
- `components/`: Reflex UI components
  - `terminal.py`: Web terminal component
  - `retro_ui.py`: 80s styling components including explanation boxes
- `game/`: Core game logic modules
  - `story.py`: Narrative and story progression
  - `puzzles.py`: Puzzle management system
  - `prolog_concepts.py`: Individual puzzle implementations
- `tests/`: End-to-end test suites
  - `test_puzzles.py`: Tests for all puzzle implementations
  - `test_story.py`: Story progression tests
  - `test_terminal.py`: UI interaction tests

## Dependencies
- `reflex`: Web framework for Python
- `ruff`: Fast Python linter and formatter
- `pytest`: Unit testing framework
- `playwright`: Browser automation for E2E testing
- `task`: Task runner for development commands (optional but recommended)
- Additional dependencies managed via `pyproject.toml` and `uv.lock`