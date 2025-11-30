# Complexity Level Configuration Files

This directory contains JSON configuration files for each complexity level in Logic Quest.

## Configuration Files

- `beginner.json` - Configuration for Beginner level
- `intermediate.json` - Configuration for Intermediate level
- `advanced.json` - Configuration for Advanced level
- `expert.json` - Configuration for Expert level

## Documentation

- `HELP_SYSTEM.md` - Comprehensive guide to the in-game help system
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `example_usage.py` - Example code for using the configuration system

## Configuration Structure

Each configuration file must contain the following fields:

### Required Fields

- **name** (string): Display name for the complexity level
- **description** (string): Detailed description of what this level provides
- **hint_frequency** (string): How often hints are available
  - Valid values: `"always"`, `"on_request"`, `"after_attempts"`, `"minimal"`, `"none"`
- **explanation_depth** (string): How detailed explanations should be
  - Valid values: `"detailed"`, `"moderate"`, `"brief"`, `"minimal"`
- **puzzle_parameters** (object): Parameters that control puzzle difficulty
  - **max_variables** (integer): Maximum number of variables in puzzles
  - **max_predicates** (integer): Maximum number of predicates in puzzles
  - **allow_complex_syntax** (boolean): Whether complex Prolog syntax is allowed
  - **provide_templates** (boolean): Whether to provide code templates
  - **show_examples** (boolean): Whether to show examples
  - Additional optional parameters can be included
- **ui_indicators** (object): Visual indicators for the UI
  - **color** (string): Color theme for this level
  - **icon** (string): Emoji or icon representing this level
  - **badge** (string): Badge text to display
- **scoring_multiplier** (number): Score multiplier for this difficulty level

## Example Configuration

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

## Validation

Configuration files are validated when loaded. If validation fails, the system will fall back to built-in default configurations.

### Validation Rules

1. All required fields must be present
2. `hint_frequency` must be one of the valid enum values
3. `explanation_depth` must be one of the valid enum values
4. `max_variables` and `max_predicates` must be positive integers
5. `scoring_multiplier` must be a positive number
6. All UI indicator fields must be strings

## Customization

You can customize these configuration files to adjust the difficulty and behavior of each complexity level. Changes will be loaded the next time the game starts.

### Tips for Customization

- **Beginner Level**: Focus on maximum guidance and simple problems
  - Keep `max_variables` and `max_predicates` low (2-3)
  - Enable all assistance features (`provide_templates`, `show_examples`, etc.)
  - Use `"always"` for `hint_frequency`
  - Use `"detailed"` for `explanation_depth`

- **Intermediate Level**: Balance guidance with challenge
  - Moderate `max_variables` and `max_predicates` (4-5)
  - Enable some assistance features
  - Use `"on_request"` for `hint_frequency`
  - Use `"moderate"` for `explanation_depth`

- **Advanced Level**: Minimal guidance, complex problems
  - Higher `max_variables` and `max_predicates` (6-8)
  - Disable most assistance features
  - Use `"after_attempts"` for `hint_frequency`
  - Use `"brief"` for `explanation_depth`

- **Expert Level**: No guidance, maximum challenge
  - Highest `max_variables` and `max_predicates` (8-12)
  - Disable all assistance features
  - Use `"none"` for `hint_frequency`
  - Use `"minimal"` for `explanation_depth`
  - Enable optimization and edge case requirements

## Programmatic Access

Configurations can be loaded programmatically using the `ComplexityConfigLoader`:

```python
from prologresurrected.game.complexity_config import load_complexity_configs

# Load all configurations
configs = load_complexity_configs()

# Access a specific level's configuration
beginner_config = configs[ComplexityLevel.BEGINNER]
```

## Creating Default Files

If configuration files are missing, you can regenerate them with defaults:

```python
from prologresurrected.game.complexity_config import create_default_config_files

# Create default configuration files
create_default_config_files()
```
