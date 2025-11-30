"""
Example usage of the complexity configuration system.

This script demonstrates how to use the configuration loader and manager
to work with complexity level configurations.
"""

from pathlib import Path
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_config import (
    ComplexityConfigLoader,
    create_default_config_files,
    load_complexity_configs
)


def example_basic_usage():
    """Example: Basic usage of ComplexityManager."""
    print("=== Basic ComplexityManager Usage ===\n")
    
    # Create a manager (loads configs automatically)
    manager = ComplexityManager()
    
    # Get current level
    current = manager.get_current_level()
    print(f"Current level: {current.name}")
    
    # Get configuration for current level
    config = manager.get_current_config()
    print(f"Level name: {config.name}")
    print(f"Description: {config.description}")
    print(f"Hint frequency: {config.hint_frequency.value}")
    print(f"Max variables: {config.puzzle_parameters['max_variables']}")
    print(f"Scoring multiplier: {config.scoring_multiplier}")
    print()


def example_loading_configs():
    """Example: Loading configurations from files."""
    print("=== Loading Configurations ===\n")
    
    # Load all configurations
    configs = load_complexity_configs()
    
    # Display information about each level
    for level, config in configs.items():
        print(f"{level.name}:")
        print(f"  Name: {config.name}")
        print(f"  Icon: {config.ui_indicators['icon']}")
        print(f"  Badge: {config.ui_indicators['badge']}")
        print(f"  Max Variables: {config.puzzle_parameters['max_variables']}")
        print(f"  Scoring Multiplier: {config.scoring_multiplier}x")
        print()


def example_custom_config_directory():
    """Example: Using a custom configuration directory."""
    print("=== Custom Configuration Directory ===\n")
    
    import tempfile
    
    # Create a temporary directory for custom configs
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        
        # Create default config files in the temp directory
        print(f"Creating config files in: {config_dir}")
        create_default_config_files(config_dir)
        
        # Load configs from custom directory
        loader = ComplexityConfigLoader(config_dir)
        configs = loader.load_all_configs()
        
        print(f"Loaded {len(configs)} configurations")
        print()


def example_config_validation():
    """Example: Configuration validation."""
    print("=== Configuration Validation ===\n")
    
    loader = ComplexityConfigLoader()
    
    # Load all configs
    configs = loader.load_all_configs()
    
    # Check for validation errors
    if loader.has_validation_errors():
        print("Validation errors found:")
        for error in loader.get_validation_errors():
            print(f"  - {error}")
    else:
        print("All configurations are valid!")
    
    print()


def example_manager_methods():
    """Example: Using ComplexityManager methods."""
    print("=== ComplexityManager Methods ===\n")
    
    manager = ComplexityManager()
    
    # Get puzzle parameters for different levels
    print("Puzzle Parameters by Level:")
    for level in ComplexityLevel:
        params = manager.get_puzzle_parameters(level)
        print(f"  {level.name}: {params['max_variables']} vars, {params['max_predicates']} predicates")
    
    print()
    
    # Get hint frequencies
    print("Hint Frequencies:")
    for level in ComplexityLevel:
        freq = manager.get_hint_frequency(level)
        print(f"  {level.name}: {freq.value}")
    
    print()
    
    # Get scoring multipliers
    print("Scoring Multipliers:")
    for level in ComplexityLevel:
        mult = manager.get_scoring_multiplier(level)
        print(f"  {level.name}: {mult}x")
    
    print()


def example_changing_levels():
    """Example: Changing complexity levels."""
    print("=== Changing Complexity Levels ===\n")
    
    manager = ComplexityManager()
    
    print(f"Initial level: {manager.get_current_level().name}")
    
    # Change to intermediate
    manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
    print(f"Changed to: {manager.get_current_level().name}")
    
    # Get config for new level
    config = manager.get_current_config()
    print(f"New max variables: {config.puzzle_parameters['max_variables']}")
    print(f"New scoring multiplier: {config.scoring_multiplier}x")
    
    print()


def example_ui_indicators():
    """Example: Working with UI indicators."""
    print("=== UI Indicators ===\n")
    
    manager = ComplexityManager()
    
    for level in ComplexityLevel:
        indicators = manager.get_ui_indicators(level)
        name = manager.get_level_name(level)
        
        print(f"{indicators['icon']} {name} [{indicators['badge']}]")
        print(f"   Color: {indicators['color']}")
        print()


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Complexity Configuration System Examples")
    print("="*60 + "\n")
    
    example_basic_usage()
    example_loading_configs()
    example_custom_config_directory()
    example_config_validation()
    example_manager_methods()
    example_changing_levels()
    example_ui_indicators()
    
    print("="*60)
    print("Examples complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
