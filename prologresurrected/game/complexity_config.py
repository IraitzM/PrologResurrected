"""
Complexity level configuration management system.

This module provides functionality for loading, validating, and managing
complexity level configurations from external configuration files.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from .complexity import (
    ComplexityLevel, ComplexityConfig, HintFrequency, ExplanationDepth
)


class ComplexityConfigLoader:
    """Loads and validates complexity level configurations."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_dir: Directory containing configuration files.
                       Defaults to 'config/complexity' in the game directory.
        """
        if config_dir is None:
            # Default to config directory relative to this file
            self.config_dir = Path(__file__).parent / "config" / "complexity"
        else:
            self.config_dir = Path(config_dir)
        
        self.loaded_configs: Dict[ComplexityLevel, ComplexityConfig] = {}
        self.validation_errors: list[str] = []
    
    def load_all_configs(self) -> Dict[ComplexityLevel, ComplexityConfig]:
        """
        Load all complexity level configurations.
        
        Returns:
            Dictionary mapping complexity levels to their configurations
            
        Raises:
            FileNotFoundError: If configuration directory doesn't exist
            ValueError: If configurations are invalid
        """
        if not self.config_dir.exists():
            # Return default configurations if directory doesn't exist
            return self._get_default_configs()
        
        configs = {}
        self.validation_errors = []
        
        for level in ComplexityLevel:
            try:
                config = self.load_config(level)
                configs[level] = config
            except Exception as e:
                self.validation_errors.append(
                    f"Error loading {level.name} config: {str(e)}"
                )
        
        # If any errors occurred, fall back to defaults
        if self.validation_errors:
            return self._get_default_configs()
        
        self.loaded_configs = configs
        return configs
    
    def load_config(self, level: ComplexityLevel) -> ComplexityConfig:
        """
        Load configuration for a specific complexity level.
        
        Args:
            level: The complexity level to load
            
        Returns:
            ComplexityConfig for the specified level
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        config_file = self.config_dir / f"{level.name.lower()}.json"
        
        if not config_file.exists():
            # Return default config for this level
            return self._get_default_config(level)
        
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        
        # Validate and convert to ComplexityConfig
        validated_config = self._validate_and_convert(config_data, level)
        
        return validated_config
    
    def _validate_and_convert(
        self, 
        config_data: Dict[str, Any], 
        level: ComplexityLevel
    ) -> ComplexityConfig:
        """
        Validate configuration data and convert to ComplexityConfig.
        
        Args:
            config_data: Raw configuration dictionary
            level: The complexity level this config is for
            
        Returns:
            Validated ComplexityConfig instance
            
        Raises:
            ValueError: If configuration is invalid
        """
        required_fields = [
            "name", "description", "hint_frequency", "explanation_depth",
            "puzzle_parameters", "ui_indicators", "scoring_multiplier"
        ]
        
        # Check required fields
        missing_fields = [f for f in required_fields if f not in config_data]
        if missing_fields:
            raise ValueError(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Convert string enums to enum instances
        try:
            hint_frequency = HintFrequency(config_data["hint_frequency"])
        except ValueError:
            raise ValueError(
                f"Invalid hint_frequency: {config_data['hint_frequency']}"
            )
        
        try:
            explanation_depth = ExplanationDepth(config_data["explanation_depth"])
        except ValueError:
            raise ValueError(
                f"Invalid explanation_depth: {config_data['explanation_depth']}"
            )
        
        # Validate puzzle_parameters
        self._validate_puzzle_parameters(config_data["puzzle_parameters"])
        
        # Validate ui_indicators
        self._validate_ui_indicators(config_data["ui_indicators"])
        
        # Validate scoring_multiplier
        if not isinstance(config_data["scoring_multiplier"], (int, float)):
            raise ValueError("scoring_multiplier must be a number")
        if config_data["scoring_multiplier"] <= 0:
            raise ValueError("scoring_multiplier must be positive")
        
        # Create ComplexityConfig instance
        return ComplexityConfig(
            name=config_data["name"],
            description=config_data["description"],
            hint_frequency=hint_frequency,
            explanation_depth=explanation_depth,
            puzzle_parameters=config_data["puzzle_parameters"],
            ui_indicators=config_data["ui_indicators"],
            scoring_multiplier=float(config_data["scoring_multiplier"])
        )
    
    def _validate_puzzle_parameters(self, params: Dict[str, Any]) -> None:
        """Validate puzzle parameters dictionary."""
        required_params = ["max_variables", "max_predicates"]
        
        for param in required_params:
            if param not in params:
                raise ValueError(f"Missing required puzzle parameter: {param}")
            if not isinstance(params[param], int) or params[param] <= 0:
                raise ValueError(f"{param} must be a positive integer")
    
    def _validate_ui_indicators(self, indicators: Dict[str, str]) -> None:
        """Validate UI indicators dictionary."""
        required_indicators = ["color", "icon", "badge"]
        
        for indicator in required_indicators:
            if indicator not in indicators:
                raise ValueError(f"Missing required UI indicator: {indicator}")
            if not isinstance(indicators[indicator], str):
                raise ValueError(f"{indicator} must be a string")
    
    def _get_default_configs(self) -> Dict[ComplexityLevel, ComplexityConfig]:
        """Get default configurations for all complexity levels."""
        return {
            level: self._get_default_config(level)
            for level in ComplexityLevel
        }
    
    def _get_default_config(self, level: ComplexityLevel) -> ComplexityConfig:
        """Get default configuration for a specific complexity level."""
        defaults = {
            ComplexityLevel.BEGINNER: ComplexityConfig(
                name="Beginner",
                description="Maximum guidance with step-by-step explanations and simple problems",
                hint_frequency=HintFrequency.ALWAYS_AVAILABLE,
                explanation_depth=ExplanationDepth.DETAILED,
                puzzle_parameters={
                    "max_variables": 2,
                    "max_predicates": 3,
                    "allow_complex_syntax": False,
                    "provide_templates": True,
                    "show_examples": True
                },
                ui_indicators={"color": "neon_green", "icon": "🌱", "badge": "BEGINNER"},
                scoring_multiplier=1.0
            ),
            ComplexityLevel.INTERMEDIATE: ComplexityConfig(
                name="Intermediate",
                description="Moderate guidance with standard complexity problems",
                hint_frequency=HintFrequency.ON_REQUEST,
                explanation_depth=ExplanationDepth.MODERATE,
                puzzle_parameters={
                    "max_variables": 4,
                    "max_predicates": 5,
                    "allow_complex_syntax": True,
                    "provide_templates": False,
                    "show_examples": True
                },
                ui_indicators={"color": "cyan", "icon": "⚡", "badge": "INTERMEDIATE"},
                scoring_multiplier=1.2
            ),
            ComplexityLevel.ADVANCED: ComplexityConfig(
                name="Advanced",
                description="Minimal guidance with complex problems and multiple solution paths",
                hint_frequency=HintFrequency.AFTER_ATTEMPTS,
                explanation_depth=ExplanationDepth.BRIEF,
                puzzle_parameters={
                    "max_variables": 6,
                    "max_predicates": 8,
                    "allow_complex_syntax": True,
                    "provide_templates": False,
                    "show_examples": False,
                    "require_optimization": True
                },
                ui_indicators={"color": "yellow", "icon": "🔥", "badge": "ADVANCED"},
                scoring_multiplier=1.5
            ),
            ComplexityLevel.EXPERT: ComplexityConfig(
                name="Expert",
                description="No guidance with optimization challenges and edge cases",
                hint_frequency=HintFrequency.NONE,
                explanation_depth=ExplanationDepth.MINIMAL,
                puzzle_parameters={
                    "max_variables": 8,
                    "max_predicates": 12,
                    "allow_complex_syntax": True,
                    "provide_templates": False,
                    "show_examples": False,
                    "require_optimization": True,
                    "include_edge_cases": True
                },
                ui_indicators={"color": "red", "icon": "💀", "badge": "EXPERT"},
                scoring_multiplier=2.0
            )
        }
        
        return defaults[level]
    
    def save_config(self, level: ComplexityLevel, config: ComplexityConfig) -> None:
        """
        Save a configuration to file.
        
        Args:
            level: The complexity level
            config: The configuration to save
        """
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = self.config_dir / f"{level.name.lower()}.json"
        
        # Convert config to dictionary
        config_dict = {
            "name": config.name,
            "description": config.description,
            "hint_frequency": config.hint_frequency.value,
            "explanation_depth": config.explanation_depth.value,
            "puzzle_parameters": config.puzzle_parameters,
            "ui_indicators": config.ui_indicators,
            "scoring_multiplier": config.scoring_multiplier
        }
        
        # Write to file with pretty formatting
        with open(config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def save_all_configs(self, configs: Dict[ComplexityLevel, ComplexityConfig]) -> None:
        """
        Save all configurations to files.
        
        Args:
            configs: Dictionary of configurations to save
        """
        for level, config in configs.items():
            self.save_config(level, config)
    
    def get_validation_errors(self) -> list[str]:
        """Get any validation errors from the last load operation."""
        return self.validation_errors.copy()
    
    def has_validation_errors(self) -> bool:
        """Check if there were validation errors in the last load operation."""
        return len(self.validation_errors) > 0


def create_default_config_files(config_dir: Optional[Path] = None) -> None:
    """
    Create default configuration files for all complexity levels.
    
    Args:
        config_dir: Directory to create config files in.
                   Defaults to 'config/complexity' in the game directory.
    """
    loader = ComplexityConfigLoader(config_dir)
    default_configs = loader._get_default_configs()
    loader.save_all_configs(default_configs)


def load_complexity_configs(config_dir: Optional[Path] = None) -> Dict[ComplexityLevel, ComplexityConfig]:
    """
    Convenience function to load all complexity configurations.
    
    Args:
        config_dir: Directory containing configuration files
        
    Returns:
        Dictionary mapping complexity levels to their configurations
    """
    loader = ComplexityConfigLoader(config_dir)
    return loader.load_all_configs()
