"""
Core complexity management infrastructure for adaptive difficulty levels.

This module provides the foundational components for managing complexity levels
throughout the Logic Quest game, including level definitions, configurations,
and the central complexity manager.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class ComplexityLevel(Enum):
    """Defines the available complexity levels for the game."""
    BEGINNER = 1      # Maximum guidance, simple problems
    INTERMEDIATE = 2  # Moderate guidance, standard problems  
    ADVANCED = 3      # Minimal guidance, complex problems
    EXPERT = 4        # No guidance, optimization challenges


class HintFrequency(Enum):
    """Defines how frequently hints are available."""
    ALWAYS_AVAILABLE = "always"
    ON_REQUEST = "on_request"
    AFTER_ATTEMPTS = "after_attempts"
    MINIMAL = "minimal"
    NONE = "none"


class ExplanationDepth(Enum):
    """Defines the depth of explanations provided."""
    DETAILED = "detailed"
    MODERATE = "moderate"
    BRIEF = "brief"
    MINIMAL = "minimal"


@dataclass
class ComplexityConfig:
    """Configuration settings for a specific complexity level."""
    name: str
    description: str
    hint_frequency: HintFrequency
    explanation_depth: ExplanationDepth
    puzzle_parameters: Dict[str, Any]
    ui_indicators: Dict[str, str]
    scoring_multiplier: float


class ComplexityManager:
    """Central coordinator for complexity-related functionality."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the complexity manager with default settings.
        
        Args:
            config_dir: Optional directory containing configuration files.
                       If None, uses default location or built-in defaults.
        """
        self.current_level: ComplexityLevel = ComplexityLevel.BEGINNER
        self.config_dir = config_dir
        self.level_configs: Dict[ComplexityLevel, ComplexityConfig] = self._initialize_configs()
    
    def _initialize_configs(self) -> Dict[ComplexityLevel, ComplexityConfig]:
        """
        Initialize the configuration for each complexity level.
        
        Attempts to load from configuration files first, falls back to
        built-in defaults if files are not available or invalid.
        """
        try:
            # Try to load from configuration files
            from .complexity_config import load_complexity_configs
            from pathlib import Path
            
            config_path = Path(self.config_dir) if self.config_dir else None
            configs = load_complexity_configs(config_path)
            return configs
        except Exception:
            # Fall back to built-in defaults if loading fails
            return self._get_builtin_defaults()
    
    def _get_builtin_defaults(self) -> Dict[ComplexityLevel, ComplexityConfig]:
        """Get built-in default configurations as fallback."""
        return {
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
    
    def reload_configs(self, config_dir: Optional[str] = None) -> None:
        """
        Reload configurations from files.
        
        Args:
            config_dir: Optional directory containing configuration files.
                       If None, uses the previously set directory.
        """
        if config_dir is not None:
            self.config_dir = config_dir
        self.level_configs = self._initialize_configs()
    
    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """
        Set the current complexity level.
        
        Args:
            level: The complexity level to set
            
        Raises:
            ValueError: If level is not a valid ComplexityLevel
        """
        if not isinstance(level, ComplexityLevel):
            raise ValueError(f"Invalid complexity level: {level}. Must be a ComplexityLevel enum value.")
        self.current_level = level
    
    def get_current_level(self) -> ComplexityLevel:
        """Get the current complexity level."""
        return self.current_level
    
    def get_current_config(self) -> ComplexityConfig:
        """Get the configuration for the current complexity level."""
        return self.level_configs[self.current_level]
    
    def get_config(self, level: ComplexityLevel) -> ComplexityConfig:
        """Get the configuration for a specific complexity level."""
        if level not in self.level_configs:
            raise ValueError(f"No configuration found for level: {level}")
        return self.level_configs[level]
    
    def get_puzzle_parameters(self, level: Optional[ComplexityLevel] = None) -> Dict[str, Any]:
        """Get puzzle parameters for the specified level (or current level if None)."""
        target_level = level if level is not None else self.current_level
        return self.get_config(target_level).puzzle_parameters.copy()
    
    def get_hint_frequency(self, level: Optional[ComplexityLevel] = None) -> HintFrequency:
        """Get hint frequency for the specified level (or current level if None)."""
        target_level = level if level is not None else self.current_level
        return self.get_config(target_level).hint_frequency
    
    def get_explanation_depth(self, level: Optional[ComplexityLevel] = None) -> ExplanationDepth:
        """Get explanation depth for the specified level (or current level if None)."""
        target_level = level if level is not None else self.current_level
        return self.get_config(target_level).explanation_depth
    
    def get_scoring_multiplier(self, level: Optional[ComplexityLevel] = None) -> float:
        """Get scoring multiplier for the specified level (or current level if None)."""
        target_level = level if level is not None else self.current_level
        return self.get_config(target_level).scoring_multiplier
    
    def get_ui_indicators(self, level: Optional[ComplexityLevel] = None) -> Dict[str, str]:
        """Get UI indicators for the specified level (or current level if None)."""
        target_level = level if level is not None else self.current_level
        return self.get_config(target_level).ui_indicators.copy()
    
    def should_show_advanced_concepts(self, level: Optional[ComplexityLevel] = None) -> bool:
        """Determine if advanced concepts should be shown for the specified level."""
        target_level = level if level is not None else self.current_level
        return target_level in [ComplexityLevel.ADVANCED, ComplexityLevel.EXPERT]
    
    def get_available_levels(self) -> list[ComplexityLevel]:
        """Get all available complexity levels."""
        return list(ComplexityLevel)
    
    def get_level_description(self, level: ComplexityLevel) -> str:
        """Get the description for a specific complexity level."""
        return self.get_config(level).description
    
    def get_level_name(self, level: ComplexityLevel) -> str:
        """Get the display name for a specific complexity level."""
        return self.get_config(level).name