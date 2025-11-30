# Memory Stack Puzzle Documentation

## Overview

The Memory Stack Puzzle is a comprehensive educational puzzle that teaches debugging concepts through Prolog-based investigation. This directory contains complete documentation for understanding, using, and extending the puzzle.

## Documentation Files

### 1. MEMORY_STACK_PUZZLE_DOCUMENTATION.md
**Comprehensive technical documentation** covering all aspects of the puzzle.

**Contents:**
- Complete architecture overview
- Detailed component descriptions
- API reference for all classes and methods
- Integration guide with existing systems
- Step-by-step guide for extending with new scenarios
- Best practices and troubleshooting

**Use this when:**
- You need detailed technical information
- You're extending the puzzle with new features
- You're integrating the puzzle into the game
- You need API reference documentation

### 2. MEMORY_STACK_QUICK_START.md
**Quick reference guide** for getting started quickly.

**Contents:**
- 5-minute quick start
- Common query examples
- Failure scenario reference table
- Complexity level comparison
- Simple integration example
- Quick troubleshooting tips

**Use this when:**
- You want to get started immediately
- You need a quick reference
- You're looking for common usage patterns
- You need a refresher on syntax

### 3. MEMORY_STACK_EXAMPLES.md
**Practical code examples** demonstrating real usage patterns.

**Contents:**
- Basic usage examples
- Query execution patterns
- Custom scenario creation
- Integration with game state
- Testing examples (unit, integration, property-based)
- Advanced customization examples

**Use this when:**
- You want to see working code
- You're implementing similar functionality
- You need testing examples
- You're learning how to use the puzzle

## Quick Navigation

### I want to...

**...understand how the puzzle works**
→ Start with `MEMORY_STACK_PUZZLE_DOCUMENTATION.md` - Overview and Architecture sections

**...use the puzzle in my game**
→ Check `MEMORY_STACK_QUICK_START.md` - Basic Usage and Integration Example

**...see working code examples**
→ Look at `MEMORY_STACK_EXAMPLES.md` - Basic Usage and Integration Patterns

**...add a new failure scenario**
→ See `MEMORY_STACK_PUZZLE_DOCUMENTATION.md` - Extending the Puzzle section
→ Then `MEMORY_STACK_EXAMPLES.md` - Custom Scenarios section

**...write tests**
→ Check `MEMORY_STACK_EXAMPLES.md` - Testing Examples section

**...understand the API**
→ See `MEMORY_STACK_PUZZLE_DOCUMENTATION.md` - API Reference section

**...troubleshoot an issue**
→ Check `MEMORY_STACK_QUICK_START.md` - Troubleshooting section
→ Or `MEMORY_STACK_PUZZLE_DOCUMENTATION.md` - Troubleshooting section

## Key Components

### Core Classes

1. **MemoryStackPuzzle** - Main puzzle class
   - Extends `BasePuzzle`
   - Coordinates all puzzle components
   - Handles player interaction

2. **StackFrameGenerator** - Generates stack traces
   - Creates realistic stack frames
   - Injects scenario-specific anomalies
   - Supports five failure scenarios

3. **QueryProcessor** - Executes Prolog queries
   - Validates query syntax
   - Executes against fact database
   - Detects significant discoveries

4. **DiagnosisValidator** - Validates diagnoses
   - Supports multiple phrasings
   - Provides partial credit
   - Generates contextual feedback

5. **MemoryStackHintSystem** - Provides adaptive hints
   - Progress-aware hints
   - Complexity-level adaptation
   - Scenario-specific guidance

### Supported Scenarios

1. **MEMORY_LEAK** - Allocated memory not freed
2. **STACK_OVERFLOW** - Excessive recursion depth
3. **NULL_POINTER** - Invalid parameters passed
4. **DEADLOCK** - Circular lock dependency
5. **RESOURCE_EXHAUSTION** - Excessive resource consumption

## Quick Start Example

```python
from prologresurrected.game.memory_stack_puzzle import MemoryStackPuzzle

# Create puzzle
puzzle = MemoryStackPuzzle()

# Get description
print(puzzle.get_description())

# Execute query
result = puzzle.validate_solution("?- frame(X, Y, Z, W).")
if result.is_valid:
    print(result.parsed_components["formatted_output"])

# Submit diagnosis
result = puzzle.validate_solution("diagnose memory leak")
if puzzle.completed:
    stats = puzzle.get_completion_statistics()
    print(f"Score: {stats['score_breakdown']['final_score']}")
```

## File Structure

```
prologresurrected/game/
├── memory_stack_puzzle.py              # Main implementation
├── MEMORY_STACK_README.md              # This file
├── MEMORY_STACK_PUZZLE_DOCUMENTATION.md # Comprehensive docs
├── MEMORY_STACK_QUICK_START.md         # Quick reference
└── MEMORY_STACK_EXAMPLES.md            # Code examples
```

## Related Files

- **Implementation**: `memory_stack_puzzle.py`
- **Tests**: `tests/test_memory_stack_*.py`
- **Design Document**: `.kiro/specs/memory-stack-puzzle/design.md`
- **Requirements**: `.kiro/specs/memory-stack-puzzle/requirements.md`
- **Tasks**: `.kiro/specs/memory-stack-puzzle/tasks.md`

## Testing

Run tests with:
```bash
# All memory stack tests
pytest tests/test_memory_stack_*.py -v

# Specific test file
pytest tests/test_memory_stack_data_models.py -v

# With coverage
pytest tests/test_memory_stack_*.py --cov=prologresurrected.game.memory_stack_puzzle
```

## Integration Points

The puzzle integrates with:
- **PuzzleManager** - Puzzle lifecycle management
- **ComplexityManager** - Difficulty adaptation
- **HintSystem** - Hint generation and tracking
- **StoryEngine** - Narrative progression
- **GameState** - Player interaction and progress

## Educational Value

The puzzle teaches:
- **Prolog Concepts**: Facts, queries, variables, unification
- **Debugging Skills**: Pattern recognition, root cause analysis
- **Logical Reasoning**: Hypothesis formation and testing
- **Real-World Connection**: Debugging techniques applicable to actual software development

## Support

For questions or issues:
1. Check the troubleshooting sections in the documentation
2. Review the code examples for similar use cases
3. Examine the test files for working examples
4. Consult the design and requirements documents

## Version

**Current Version**: 1.0.0
**Last Updated**: November 30, 2025

## License

Part of the Logic Quest project.

---

**Start here**: If you're new, begin with `MEMORY_STACK_QUICK_START.md` for a quick introduction, then move to `MEMORY_STACK_PUZZLE_DOCUMENTATION.md` for comprehensive details.
