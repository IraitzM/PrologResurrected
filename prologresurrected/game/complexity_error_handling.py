"""
Comprehensive Error Handling and Recovery for Complexity Level System

This module provides robust error handling, graceful fallbacks, and recovery
mechanisms for all complexity-related operations in Logic Quest.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable
import logging
from pathlib import Path

from .complexity import ComplexityLevel, ComplexityConfig, ComplexityManager


# Configure logging for error tracking
logger = logging.getLogger(__name__)


class ComplexityErrorType(Enum):
    """Types of errors that can occur in the complexity system."""
    INVALID_LEVEL_SELECTION = "invalid_level_selection"
    CONFIG_LOAD_FAILURE = "config_load_failure"
    CONFIG_VALIDATION_FAILURE = "config_validation_failure"
    PUZZLE_ADAPTATION_FAILURE = "puzzle_adaptation_failure"
    STATE_TRANSITION_FAILURE = "state_transition_failure"
    PERSISTENCE_FAILURE = "persistence_failure"
    MANAGER_INITIALIZATION_FAILURE = "manager_initialization_failure"


@dataclass
class ComplexityError:
    """Represents an error in the complexity system."""
    error_type: ComplexityErrorType
    message: str
    details: Optional[str] = None
    recoverable: bool = True
    fallback_level: Optional[ComplexityLevel] = None
    user_message: str = ""
    
    def __post_init__(self):
        """Generate user-friendly message if not provided."""
        if not self.user_message:
            self.user_message = self._generate_user_message()
    
    def _generate_user_message(self) -> str:
        """Generate a user-friendly error message."""
        messages = {
            ComplexityErrorType.INVALID_LEVEL_SELECTION: 
                "Invalid complexity level selected. Using default level instead.",
            ComplexityErrorType.CONFIG_LOAD_FAILURE:
                "Could not load complexity configuration. Using built-in defaults.",
            ComplexityErrorType.CONFIG_VALIDATION_FAILURE:
                "Configuration validation failed. Using safe defaults.",
            ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE:
                "Could not adapt puzzle to complexity level. Using standard puzzle.",
            ComplexityErrorType.STATE_TRANSITION_FAILURE:
                "Could not change complexity level. Keeping current level.",
            ComplexityErrorType.PERSISTENCE_FAILURE:
                "Could not save complexity settings. Changes may not persist.",
            ComplexityErrorType.MANAGER_INITIALIZATION_FAILURE:
                "Could not initialize complexity manager. Using default settings.",
        }
        return messages.get(self.error_type, "An error occurred in the complexity system.")


class ComplexityErrorHandler:
    """
    Centralized error handler for complexity-related operations.
    
    Provides consistent error handling, logging, and recovery mechanisms
    across the complexity system.
    """
    
    def __init__(self, enable_logging: bool = True):
        """
        Initialize the error handler.
        
        Args:
            enable_logging: Whether to enable error logging
        """
        self.enable_logging = enable_logging
        self.error_history: list[ComplexityError] = []
        self.recovery_attempts: Dict[ComplexityErrorType, int] = {}
        
    def handle_error(
        self, 
        error_type: ComplexityErrorType,
        message: str,
        details: Optional[str] = None,
        exception: Optional[Exception] = None,
        recoverable: bool = True,
        fallback_level: Optional[ComplexityLevel] = None
    ) -> ComplexityError:
        """
        Handle an error in the complexity system.
        
        Args:
            error_type: Type of error that occurred
            message: Error message for logging
            details: Additional error details
            exception: Original exception if available
            recoverable: Whether the error is recoverable
            fallback_level: Fallback complexity level if applicable
            
        Returns:
            ComplexityError object with error information
        """
        # Create error object
        error = ComplexityError(
            error_type=error_type,
            message=message,
            details=details or (str(exception) if exception else None),
            recoverable=recoverable,
            fallback_level=fallback_level or ComplexityLevel.BEGINNER
        )
        
        # Log the error
        if self.enable_logging:
            log_message = f"Complexity Error [{error_type.value}]: {message}"
            if details:
                log_message += f" | Details: {details}"
            if exception:
                log_message += f" | Exception: {str(exception)}"
            
            if recoverable:
                logger.warning(log_message)
            else:
                logger.error(log_message)
        
        # Track error history
        self.error_history.append(error)
        
        # Track recovery attempts
        if error_type not in self.recovery_attempts:
            self.recovery_attempts[error_type] = 0
        self.recovery_attempts[error_type] += 1
        
        return error
    
    def get_error_history(self) -> list[ComplexityError]:
        """Get the history of errors."""
        return self.error_history.copy()
    
    def clear_error_history(self) -> None:
        """Clear the error history."""
        self.error_history.clear()
        self.recovery_attempts.clear()
    
    def get_recovery_count(self, error_type: ComplexityErrorType) -> int:
        """Get the number of recovery attempts for an error type."""
        return self.recovery_attempts.get(error_type, 0)


class ComplexityLevelValidator:
    """Validates complexity level selections and transitions."""
    
    @staticmethod
    def validate_level_selection(level: Any) -> tuple[bool, Optional[str]]:
        """
        Validate a complexity level selection.
        
        Args:
            level: The level to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if it's a ComplexityLevel enum
        if isinstance(level, ComplexityLevel):
            return True, None
        
        # Check if it's a valid string representation
        if isinstance(level, str):
            try:
                ComplexityLevel[level.upper()]
                return True, None
            except KeyError:
                return False, f"Invalid complexity level name: {level}"
        
        # Check if it's a valid integer value
        if isinstance(level, int):
            try:
                ComplexityLevel(level)
                return True, None
            except ValueError:
                return False, f"Invalid complexity level value: {level}"
        
        return False, f"Invalid complexity level type: {type(level)}"
    
    @staticmethod
    def validate_level_transition(
        current_level: ComplexityLevel,
        new_level: ComplexityLevel,
        allow_same: bool = False
    ) -> tuple[bool, Optional[str]]:
        """
        Validate a complexity level transition.
        
        Args:
            current_level: Current complexity level
            new_level: New complexity level to transition to
            allow_same: Whether to allow transition to the same level
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(current_level, ComplexityLevel):
            return False, "Current level is not a valid ComplexityLevel"
        
        if not isinstance(new_level, ComplexityLevel):
            return False, "New level is not a valid ComplexityLevel"
        
        if current_level == new_level and not allow_same:
            return False, f"Already at {current_level.name} level"
        
        return True, None


class SafeComplexityManager:
    """
    Wrapper around ComplexityManager with comprehensive error handling.
    
    Provides safe operations with automatic fallbacks and recovery.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the safe complexity manager.
        
        Args:
            config_dir: Optional configuration directory
        """
        self.error_handler = ComplexityErrorHandler()
        self.manager: Optional[ComplexityManager] = None
        self.fallback_level = ComplexityLevel.BEGINNER
        
        # Initialize the manager with error handling
        self._initialize_manager(config_dir)
    
    def _initialize_manager(self, config_dir: Optional[str]) -> None:
        """Initialize the complexity manager with error handling."""
        try:
            self.manager = ComplexityManager(config_dir)
        except Exception as e:
            error = self.error_handler.handle_error(
                ComplexityErrorType.MANAGER_INITIALIZATION_FAILURE,
                "Failed to initialize ComplexityManager",
                exception=e,
                recoverable=True,
                fallback_level=self.fallback_level
            )
            
            # Create a minimal manager with defaults
            try:
                self.manager = ComplexityManager()
            except Exception as e2:
                # Last resort: create a completely minimal manager
                self.manager = None
                logger.critical(f"Could not create fallback manager: {e2}")
    
    def set_complexity_level(
        self, 
        level: Any,
        validate: bool = True
    ) -> tuple[bool, Optional[ComplexityError]]:
        """
        Safely set the complexity level with validation and error handling.
        
        Args:
            level: The complexity level to set
            validate: Whether to validate the level before setting
            
        Returns:
            Tuple of (success, error)
        """
        # Validate the level if requested
        if validate:
            is_valid, error_msg = ComplexityLevelValidator.validate_level_selection(level)
            if not is_valid:
                error = self.error_handler.handle_error(
                    ComplexityErrorType.INVALID_LEVEL_SELECTION,
                    error_msg or "Invalid level selection",
                    recoverable=True,
                    fallback_level=self.fallback_level
                )
                return False, error
        
        # Convert to ComplexityLevel if needed
        try:
            if isinstance(level, str):
                level = ComplexityLevel[level.upper()]
            elif isinstance(level, int):
                level = ComplexityLevel(level)
        except (KeyError, ValueError) as e:
            error = self.error_handler.handle_error(
                ComplexityErrorType.INVALID_LEVEL_SELECTION,
                f"Could not convert to ComplexityLevel: {level}",
                exception=e,
                recoverable=True,
                fallback_level=self.fallback_level
            )
            return False, error
        
        # Attempt to set the level
        try:
            if self.manager:
                self.manager.set_complexity_level(level)
                return True, None
            else:
                error = self.error_handler.handle_error(
                    ComplexityErrorType.STATE_TRANSITION_FAILURE,
                    "Manager not initialized",
                    recoverable=False
                )
                return False, error
        except Exception as e:
            error = self.error_handler.handle_error(
                ComplexityErrorType.STATE_TRANSITION_FAILURE,
                f"Failed to set complexity level to {level.name}",
                exception=e,
                recoverable=True,
                fallback_level=self.manager.get_current_level() if self.manager else self.fallback_level
            )
            return False, error
    
    def get_current_level(self) -> ComplexityLevel:
        """
        Safely get the current complexity level.
        
        Returns:
            Current complexity level (fallback if error)
        """
        try:
            if self.manager:
                return self.manager.get_current_level()
            else:
                return self.fallback_level
        except Exception as e:
            self.error_handler.handle_error(
                ComplexityErrorType.STATE_TRANSITION_FAILURE,
                "Failed to get current level",
                exception=e,
                recoverable=True
            )
            return self.fallback_level
    
    def get_config(self, level: Optional[ComplexityLevel] = None) -> Optional[ComplexityConfig]:
        """
        Safely get configuration for a complexity level.
        
        Args:
            level: Complexity level (None for current)
            
        Returns:
            ComplexityConfig or None if error
        """
        try:
            if self.manager:
                if level is None:
                    return self.manager.get_current_config()
                else:
                    return self.manager.get_config(level)
            else:
                return None
        except Exception as e:
            self.error_handler.handle_error(
                ComplexityErrorType.CONFIG_LOAD_FAILURE,
                f"Failed to get config for level {level}",
                exception=e,
                recoverable=True
            )
            return None
    
    def reload_configs(self, config_dir: Optional[str] = None) -> tuple[bool, Optional[ComplexityError]]:
        """
        Safely reload configurations with error handling.
        
        Args:
            config_dir: Optional configuration directory
            
        Returns:
            Tuple of (success, error)
        """
        try:
            if self.manager:
                self.manager.reload_configs(config_dir)
                return True, None
            else:
                error = self.error_handler.handle_error(
                    ComplexityErrorType.CONFIG_LOAD_FAILURE,
                    "Manager not initialized",
                    recoverable=False
                )
                return False, error
        except Exception as e:
            error = self.error_handler.handle_error(
                ComplexityErrorType.CONFIG_LOAD_FAILURE,
                "Failed to reload configurations",
                exception=e,
                recoverable=True
            )
            return False, error


class PuzzleAdaptationErrorHandler:
    """Handles errors during puzzle adaptation with graceful fallbacks."""
    
    def __init__(self):
        """Initialize the puzzle adaptation error handler."""
        self.error_handler = ComplexityErrorHandler()
    
    def safe_adapt_puzzle(
        self,
        adaptation_func: Callable,
        puzzle: Any,
        level: ComplexityLevel,
        fallback_puzzle: Optional[Any] = None
    ) -> tuple[Any, Optional[ComplexityError]]:
        """
        Safely adapt a puzzle with error handling and fallback.
        
        Args:
            adaptation_func: Function to adapt the puzzle
            puzzle: Puzzle to adapt
            level: Target complexity level
            fallback_puzzle: Fallback puzzle if adaptation fails
            
        Returns:
            Tuple of (adapted_puzzle, error)
        """
        try:
            adapted_puzzle = adaptation_func(puzzle, level)
            return adapted_puzzle, None
        except Exception as e:
            error = self.error_handler.handle_error(
                ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE,
                f"Failed to adapt puzzle to {level.name}",
                exception=e,
                recoverable=True,
                fallback_level=level
            )
            
            # Return fallback puzzle or original puzzle
            return fallback_puzzle if fallback_puzzle is not None else puzzle, error
    
    def validate_adapted_puzzle(
        self,
        puzzle: Any,
        level: ComplexityLevel,
        validation_func: Optional[Callable] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Validate that a puzzle has been properly adapted.
        
        Args:
            puzzle: Adapted puzzle to validate
            level: Target complexity level
            validation_func: Optional custom validation function
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check basic puzzle attributes
            if not hasattr(puzzle, 'get_complexity_level'):
                return False, "Puzzle missing get_complexity_level method"
            
            if puzzle.get_complexity_level() != level:
                return False, f"Puzzle level mismatch: expected {level.name}, got {puzzle.get_complexity_level().name}"
            
            # Run custom validation if provided
            if validation_func:
                return validation_func(puzzle, level)
            
            return True, None
        except Exception as e:
            return False, f"Validation error: {str(e)}"


def create_safe_complexity_system(config_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Factory function to create a complete safe complexity system.
    
    Args:
        config_dir: Optional configuration directory
        
    Returns:
        Dictionary containing all safe complexity components
    """
    return {
        "manager": SafeComplexityManager(config_dir),
        "error_handler": ComplexityErrorHandler(),
        "validator": ComplexityLevelValidator(),
        "puzzle_adapter": PuzzleAdaptationErrorHandler(),
    }


def format_error_for_user(error: ComplexityError, include_details: bool = False) -> list[str]:
    """
    Format an error for display to the user.
    
    Args:
        error: ComplexityError to format
        include_details: Whether to include technical details
        
    Returns:
        List of formatted message lines
    """
    lines = [
        "⚠️  SYSTEM NOTICE",
        "",
        error.user_message,
    ]
    
    if error.recoverable:
        lines.extend([
            "",
            "✅ The system has automatically recovered.",
            "You can continue playing without interruption.",
        ])
        
        if error.fallback_level:
            lines.extend([
                "",
                f"Using {error.fallback_level.name} complexity level as fallback.",
            ])
    else:
        lines.extend([
            "",
            "❌ This error requires attention.",
            "Please restart the game or contact support.",
        ])
    
    if include_details and error.details:
        lines.extend([
            "",
            "Technical Details:",
            f"  {error.details}",
        ])
    
    return lines
