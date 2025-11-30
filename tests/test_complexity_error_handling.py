"""
Unit tests for complexity error handling and recovery mechanisms.

Tests error handling for invalid complexity level selections, puzzle adaptation
failures, complexity transition errors, and user-friendly error messages.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_error_handling import (
    ComplexityErrorType,
    ComplexityError,
    ComplexityErrorHandler,
    ComplexityLevelValidator,
    SafeComplexityManager,
    PuzzleAdaptationErrorHandler,
    create_safe_complexity_system,
    format_error_for_user,
)
from prologresurrected.game.puzzles import BasePuzzle


class TestComplexityErrorHandler:
    """Test the ComplexityErrorHandler class."""
    
    def test_handle_error_creates_error_object(self):
        """Test that handle_error creates a ComplexityError object."""
        handler = ComplexityErrorHandler()
        
        error = handler.handle_error(
            ComplexityErrorType.INVALID_LEVEL_SELECTION,
            "Test error message",
            details="Test details"
        )
        
        assert isinstance(error, ComplexityError)
        assert error.error_type == ComplexityErrorType.INVALID_LEVEL_SELECTION
        assert error.message == "Test error message"
        assert error.details == "Test details"
        assert error.recoverable is True
    
    def test_handle_error_tracks_history(self):
        """Test that errors are tracked in history."""
        handler = ComplexityErrorHandler()
        
        handler.handle_error(
            ComplexityErrorType.INVALID_LEVEL_SELECTION,
            "Error 1"
        )
        handler.handle_error(
            ComplexityErrorType.CONFIG_LOAD_FAILURE,
            "Error 2"
        )
        
        history = handler.get_error_history()
        assert len(history) == 2
        assert history[0].message == "Error 1"
        assert history[1].message == "Error 2"
    
    def test_handle_error_tracks_recovery_attempts(self):
        """Test that recovery attempts are tracked."""
        handler = ComplexityErrorHandler()
        
        handler.handle_error(
            ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE,
            "Attempt 1"
        )
        handler.handle_error(
            ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE,
            "Attempt 2"
        )
        
        count = handler.get_recovery_count(ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE)
        assert count == 2
    
    def test_clear_error_history(self):
        """Test clearing error history."""
        handler = ComplexityErrorHandler()
        
        handler.handle_error(
            ComplexityErrorType.INVALID_LEVEL_SELECTION,
            "Error"
        )
        
        assert len(handler.get_error_history()) == 1
        
        handler.clear_error_history()
        
        assert len(handler.get_error_history()) == 0
        assert handler.get_recovery_count(ComplexityErrorType.INVALID_LEVEL_SELECTION) == 0


class TestComplexityLevelValidator:
    """Test the ComplexityLevelValidator class."""
    
    def test_validate_level_selection_with_enum(self):
        """Test validation with ComplexityLevel enum."""
        is_valid, error = ComplexityLevelValidator.validate_level_selection(
            ComplexityLevel.BEGINNER
        )
        
        assert is_valid is True
        assert error is None
    
    def test_validate_level_selection_with_valid_string(self):
        """Test validation with valid string."""
        is_valid, error = ComplexityLevelValidator.validate_level_selection("BEGINNER")
        
        assert is_valid is True
        assert error is None
    
    def test_validate_level_selection_with_invalid_string(self):
        """Test validation with invalid string."""
        is_valid, error = ComplexityLevelValidator.validate_level_selection("INVALID")
        
        assert is_valid is False
        assert "Invalid complexity level name" in error
    
    def test_validate_level_selection_with_valid_int(self):
        """Test validation with valid integer."""
        is_valid, error = ComplexityLevelValidator.validate_level_selection(1)
        
        assert is_valid is True
        assert error is None
    
    def test_validate_level_selection_with_invalid_int(self):
        """Test validation with invalid integer."""
        is_valid, error = ComplexityLevelValidator.validate_level_selection(99)
        
        assert is_valid is False
        assert "Invalid complexity level value" in error
    
    def test_validate_level_selection_with_invalid_type(self):
        """Test validation with invalid type."""
        is_valid, error = ComplexityLevelValidator.validate_level_selection([1, 2, 3])
        
        assert is_valid is False
        assert "Invalid complexity level type" in error
    
    def test_validate_level_transition_valid(self):
        """Test valid level transition."""
        is_valid, error = ComplexityLevelValidator.validate_level_transition(
            ComplexityLevel.BEGINNER,
            ComplexityLevel.INTERMEDIATE
        )
        
        assert is_valid is True
        assert error is None
    
    def test_validate_level_transition_same_level_not_allowed(self):
        """Test transition to same level when not allowed."""
        is_valid, error = ComplexityLevelValidator.validate_level_transition(
            ComplexityLevel.BEGINNER,
            ComplexityLevel.BEGINNER,
            allow_same=False
        )
        
        assert is_valid is False
        assert "Already at BEGINNER level" in error
    
    def test_validate_level_transition_same_level_allowed(self):
        """Test transition to same level when allowed."""
        is_valid, error = ComplexityLevelValidator.validate_level_transition(
            ComplexityLevel.BEGINNER,
            ComplexityLevel.BEGINNER,
            allow_same=True
        )
        
        assert is_valid is True
        assert error is None


class TestSafeComplexityManager:
    """Test the SafeComplexityManager class."""
    
    def test_initialization_succeeds(self):
        """Test that SafeComplexityManager initializes successfully."""
        manager = SafeComplexityManager()
        
        assert manager.manager is not None
        assert manager.error_handler is not None
    
    def test_set_complexity_level_with_valid_enum(self):
        """Test setting complexity level with valid enum."""
        manager = SafeComplexityManager()
        
        success, error = manager.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        assert success is True
        assert error is None
        assert manager.get_current_level() == ComplexityLevel.INTERMEDIATE
    
    def test_set_complexity_level_with_valid_string(self):
        """Test setting complexity level with valid string."""
        manager = SafeComplexityManager()
        
        success, error = manager.set_complexity_level("ADVANCED")
        
        assert success is True
        assert error is None
        assert manager.get_current_level() == ComplexityLevel.ADVANCED
    
    def test_set_complexity_level_with_invalid_string(self):
        """Test setting complexity level with invalid string."""
        manager = SafeComplexityManager()
        
        success, error = manager.set_complexity_level("INVALID")
        
        assert success is False
        assert error is not None
        assert error.error_type == ComplexityErrorType.INVALID_LEVEL_SELECTION
        # Level should remain at default (BEGINNER)
        assert manager.get_current_level() == ComplexityLevel.BEGINNER
    
    def test_set_complexity_level_with_invalid_type(self):
        """Test setting complexity level with invalid type."""
        manager = SafeComplexityManager()
        
        success, error = manager.set_complexity_level([1, 2, 3])
        
        assert success is False
        assert error is not None
        # Level should remain at default
        assert manager.get_current_level() == ComplexityLevel.BEGINNER
    
    def test_set_complexity_level_without_validation(self):
        """Test setting complexity level without validation."""
        manager = SafeComplexityManager()
        
        # This should still work because we pass a valid enum
        success, error = manager.set_complexity_level(
            ComplexityLevel.EXPERT,
            validate=False
        )
        
        assert success is True
        assert error is None
    
    def test_get_current_level_returns_fallback_on_error(self):
        """Test that get_current_level returns fallback on error."""
        manager = SafeComplexityManager()
        manager.manager = None  # Simulate manager failure
        
        level = manager.get_current_level()
        
        assert level == manager.fallback_level
    
    def test_get_config_returns_none_on_error(self):
        """Test that get_config returns None on error."""
        manager = SafeComplexityManager()
        manager.manager = None  # Simulate manager failure
        
        config = manager.get_config()
        
        assert config is None


class TestPuzzleAdaptationErrorHandler:
    """Test the PuzzleAdaptationErrorHandler class."""
    
    def test_safe_adapt_puzzle_success(self):
        """Test successful puzzle adaptation."""
        handler = PuzzleAdaptationErrorHandler()
        
        # Create a mock puzzle
        from prologresurrected.game.puzzles import PuzzleDifficulty
        from prologresurrected.game.validation import ValidationResult
        
        class MockPuzzle(BasePuzzle):
            def __init__(self):
                super().__init__(
                    puzzle_id="test",
                    title="Test",
                    difficulty=PuzzleDifficulty.BEGINNER
                )
            
            def get_description(self):
                return "Test description"
            
            def get_expected_solution(self):
                return "test_solution"
            
            def get_hint(self, hint_level: int):
                return "Test hint"
            
            def get_initial_context(self):
                return {}
            
            def validate_solution(self, solution):
                return ValidationResult(is_valid=solution == "test_solution", message="Test")
        
        puzzle = MockPuzzle()
        
        # Mock adaptation function
        def adapt_func(p, level):
            p.set_complexity_level(level)
            return p
        
        adapted, error = handler.safe_adapt_puzzle(
            adapt_func,
            puzzle,
            ComplexityLevel.INTERMEDIATE
        )
        
        assert error is None
        assert adapted.get_complexity_level() == ComplexityLevel.INTERMEDIATE
    
    def test_safe_adapt_puzzle_with_failure_returns_fallback(self):
        """Test that adaptation failure returns fallback puzzle."""
        handler = PuzzleAdaptationErrorHandler()
        
        from prologresurrected.game.puzzles import PuzzleDifficulty
        from prologresurrected.game.validation import ValidationResult
        
        class MockPuzzle(BasePuzzle):
            def __init__(self):
                super().__init__(
                    puzzle_id="test",
                    title="Test",
                    difficulty=PuzzleDifficulty.BEGINNER
                )
            
            def get_description(self):
                return "Test description"
            
            def get_expected_solution(self):
                return "test_solution"
            
            def get_hint(self, hint_level: int):
                return "Test hint"
            
            def get_initial_context(self):
                return {}
            
            def validate_solution(self, solution):
                return ValidationResult(is_valid=solution == "test_solution", message="Test")
        
        puzzle = MockPuzzle()
        fallback = MockPuzzle()
        
        # Mock adaptation function that fails
        def failing_adapt_func(p, level):
            raise RuntimeError("Adaptation failed")
        
        adapted, error = handler.safe_adapt_puzzle(
            failing_adapt_func,
            puzzle,
            ComplexityLevel.INTERMEDIATE,
            fallback_puzzle=fallback
        )
        
        assert error is not None
        assert error.error_type == ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE
        assert adapted == fallback
    
    def test_safe_adapt_puzzle_with_failure_returns_original(self):
        """Test that adaptation failure returns original puzzle if no fallback."""
        handler = PuzzleAdaptationErrorHandler()
        
        from prologresurrected.game.puzzles import PuzzleDifficulty
        from prologresurrected.game.validation import ValidationResult
        
        class MockPuzzle(BasePuzzle):
            def __init__(self):
                super().__init__(
                    puzzle_id="test",
                    title="Test",
                    difficulty=PuzzleDifficulty.BEGINNER
                )
            
            def get_description(self):
                return "Test description"
            
            def get_expected_solution(self):
                return "test_solution"
            
            def get_hint(self, hint_level: int):
                return "Test hint"
            
            def get_initial_context(self):
                return {}
            
            def validate_solution(self, solution):
                return ValidationResult(is_valid=solution == "test_solution", message="Test")
        
        puzzle = MockPuzzle()
        
        # Mock adaptation function that fails
        def failing_adapt_func(p, level):
            raise RuntimeError("Adaptation failed")
        
        adapted, error = handler.safe_adapt_puzzle(
            failing_adapt_func,
            puzzle,
            ComplexityLevel.INTERMEDIATE
        )
        
        assert error is not None
        assert adapted == puzzle
    
    def test_validate_adapted_puzzle_success(self):
        """Test successful puzzle validation."""
        handler = PuzzleAdaptationErrorHandler()
        
        from prologresurrected.game.puzzles import PuzzleDifficulty
        from prologresurrected.game.validation import ValidationResult
        
        class MockPuzzle(BasePuzzle):
            def __init__(self):
                super().__init__(
                    puzzle_id="test",
                    title="Test",
                    difficulty=PuzzleDifficulty.BEGINNER
                )
            
            def get_description(self):
                return "Test description"
            
            def get_expected_solution(self):
                return "test_solution"
            
            def get_hint(self, hint_level: int):
                return "Test hint"
            
            def get_initial_context(self):
                return {}
            
            def validate_solution(self, solution):
                return ValidationResult(is_valid=solution == "test_solution", message="Test")
        
        puzzle = MockPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        is_valid, error = handler.validate_adapted_puzzle(
            puzzle,
            ComplexityLevel.ADVANCED
        )
        
        assert is_valid is True
        assert error is None
    
    def test_validate_adapted_puzzle_level_mismatch(self):
        """Test puzzle validation with level mismatch."""
        handler = PuzzleAdaptationErrorHandler()
        
        from prologresurrected.game.puzzles import PuzzleDifficulty
        from prologresurrected.game.validation import ValidationResult
        
        class MockPuzzle(BasePuzzle):
            def __init__(self):
                super().__init__(
                    puzzle_id="test",
                    title="Test",
                    difficulty=PuzzleDifficulty.BEGINNER
                )
            
            def get_description(self):
                return "Test description"
            
            def get_expected_solution(self):
                return "test_solution"
            
            def get_hint(self, hint_level: int):
                return "Test hint"
            
            def get_initial_context(self):
                return {}
            
            def validate_solution(self, solution):
                return ValidationResult(is_valid=solution == "test_solution", message="Test")
        
        puzzle = MockPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        is_valid, error = handler.validate_adapted_puzzle(
            puzzle,
            ComplexityLevel.ADVANCED
        )
        
        assert is_valid is False
        assert "level mismatch" in error.lower()


class TestComplexityError:
    """Test the ComplexityError dataclass."""
    
    def test_error_generates_user_message(self):
        """Test that ComplexityError generates user message."""
        error = ComplexityError(
            error_type=ComplexityErrorType.INVALID_LEVEL_SELECTION,
            message="Test error"
        )
        
        assert error.user_message != ""
        assert "Invalid complexity level" in error.user_message
    
    def test_error_with_custom_user_message(self):
        """Test ComplexityError with custom user message."""
        custom_message = "Custom error message for user"
        error = ComplexityError(
            error_type=ComplexityErrorType.CONFIG_LOAD_FAILURE,
            message="Test error",
            user_message=custom_message
        )
        
        assert error.user_message == custom_message
    
    def test_error_recoverable_flag(self):
        """Test ComplexityError recoverable flag."""
        error = ComplexityError(
            error_type=ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE,
            message="Test error",
            recoverable=True
        )
        
        assert error.recoverable is True
    
    def test_error_fallback_level(self):
        """Test ComplexityError fallback level."""
        error = ComplexityError(
            error_type=ComplexityErrorType.STATE_TRANSITION_FAILURE,
            message="Test error",
            fallback_level=ComplexityLevel.INTERMEDIATE
        )
        
        assert error.fallback_level == ComplexityLevel.INTERMEDIATE


class TestFormatErrorForUser:
    """Test the format_error_for_user function."""
    
    def test_format_recoverable_error(self):
        """Test formatting a recoverable error."""
        error = ComplexityError(
            error_type=ComplexityErrorType.CONFIG_LOAD_FAILURE,
            message="Test error",
            recoverable=True,
            fallback_level=ComplexityLevel.BEGINNER
        )
        
        lines = format_error_for_user(error)
        
        assert len(lines) > 0
        assert any("SYSTEM NOTICE" in line for line in lines)
        assert any("automatically recovered" in line.lower() for line in lines)
        assert any("BEGINNER" in line for line in lines)
    
    def test_format_non_recoverable_error(self):
        """Test formatting a non-recoverable error."""
        error = ComplexityError(
            error_type=ComplexityErrorType.MANAGER_INITIALIZATION_FAILURE,
            message="Test error",
            recoverable=False
        )
        
        lines = format_error_for_user(error)
        
        assert len(lines) > 0
        assert any("requires attention" in line.lower() for line in lines)
    
    def test_format_error_with_details(self):
        """Test formatting error with technical details."""
        error = ComplexityError(
            error_type=ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE,
            message="Test error",
            details="Technical details here",
            recoverable=True
        )
        
        lines = format_error_for_user(error, include_details=True)
        
        assert any("Technical details here" in line for line in lines)
    
    def test_format_error_without_details(self):
        """Test formatting error without technical details."""
        error = ComplexityError(
            error_type=ComplexityErrorType.PUZZLE_ADAPTATION_FAILURE,
            message="Test error",
            details="Technical details here",
            recoverable=True
        )
        
        lines = format_error_for_user(error, include_details=False)
        
        assert not any("Technical details here" in line for line in lines)


class TestCreateSafeComplexitySystem:
    """Test the create_safe_complexity_system factory function."""
    
    def test_creates_all_components(self):
        """Test that factory creates all required components."""
        system = create_safe_complexity_system()
        
        assert "manager" in system
        assert "error_handler" in system
        assert "validator" in system
        assert "puzzle_adapter" in system
        
        assert isinstance(system["manager"], SafeComplexityManager)
        assert isinstance(system["error_handler"], ComplexityErrorHandler)
        assert isinstance(system["validator"], ComplexityLevelValidator)
        assert isinstance(system["puzzle_adapter"], PuzzleAdaptationErrorHandler)
    
    def test_components_are_functional(self):
        """Test that created components are functional."""
        system = create_safe_complexity_system()
        
        # Test manager
        success, error = system["manager"].set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert success is True
        
        # Test validator
        is_valid, error_msg = system["validator"].validate_level_selection(ComplexityLevel.ADVANCED)
        assert is_valid is True
        
        # Test error handler
        error = system["error_handler"].handle_error(
            ComplexityErrorType.CONFIG_LOAD_FAILURE,
            "Test"
        )
        assert isinstance(error, ComplexityError)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
