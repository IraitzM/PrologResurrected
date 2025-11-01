"""
Puzzle System Tests

Tests for the puzzle management system, including base puzzle classes,
puzzle manager, and example puzzle implementations.
"""

from game.puzzles import (
    PuzzleDifficulty,
    PuzzleType,
    PuzzleResult,
    BasePuzzle,
    PuzzleManager,
    SimpleFactPuzzle,
)
from game.validation import ValidationResult


class TestPuzzleDifficulty:
    """Test cases for PuzzleDifficulty enum."""

    def test_difficulty_values(self):
        """Test that difficulty levels have correct values."""
        assert PuzzleDifficulty.BEGINNER.value == 1
        assert PuzzleDifficulty.INTERMEDIATE.value == 2
        assert PuzzleDifficulty.ADVANCED.value == 3
        assert PuzzleDifficulty.EXPERT.value == 4

    def test_difficulty_ordering(self):
        """Test that difficulties are properly ordered."""
        difficulties = list(PuzzleDifficulty)
        values = [diff.value for diff in difficulties]
        assert values == [1, 2, 3, 4]


class TestPuzzleType:
    """Test cases for PuzzleType enum."""

    def test_puzzle_type_values(self):
        """Test that puzzle types have correct string values."""
        assert PuzzleType.FACT_CREATION.value == "fact_creation"
        assert PuzzleType.QUERY_WRITING.value == "query_writing"
        assert PuzzleType.RULE_DEFINITION.value == "rule_definition"
        assert PuzzleType.PATTERN_MATCHING.value == "pattern_matching"
        assert PuzzleType.LOGICAL_DEDUCTION.value == "logical_deduction"


class TestPuzzleResult:
    """Test cases for PuzzleResult dataclass."""

    def test_puzzle_result_creation(self):
        """Test creating a puzzle result with required fields."""
        result = PuzzleResult(
            success=True, score=85, feedback="Great job!", hints_used=1, attempts=2
        )

        assert result.success is True
        assert result.score == 85
        assert result.feedback == "Great job!"
        assert result.hints_used == 1
        assert result.attempts == 2
        assert result.time_taken is None  # Default value

    def test_puzzle_result_with_time(self):
        """Test creating a puzzle result with time taken."""
        result = PuzzleResult(
            success=False,
            score=0,
            feedback="Try again",
            hints_used=0,
            attempts=1,
            time_taken=45.5,
        )

        assert result.time_taken == 45.5


class MockPuzzle(BasePuzzle):
    """Mock puzzle implementation for testing BasePuzzle."""

    def __init__(
        self,
        puzzle_id="test_puzzle",
        title="Test Puzzle",
        difficulty=PuzzleDifficulty.BEGINNER,
    ):
        super().__init__(puzzle_id, title, difficulty)
        self.description = "Test puzzle description"
        self.context = {"facts": [], "rules": []}
        self.expected_solution = "test_solution"
        self.hints = ["Hint 1", "Hint 2", "Hint 3"]
        self.validation_result = ValidationResult(is_valid=True)

    def get_description(self):
        return self.description

    def get_initial_context(self):
        return self.context

    def validate_solution(self, user_input):
        if user_input == self.expected_solution:
            return ValidationResult(is_valid=True)
        else:
            return ValidationResult(
                is_valid=False, error_message="Incorrect solution", hint="Try again"
            )

    def get_hint(self, hint_level):
        if 1 <= hint_level <= len(self.hints):
            return self.hints[hint_level - 1]
        return "No more hints available"

    def get_expected_solution(self):
        return self.expected_solution


class TestBasePuzzle:
    """Test cases for BasePuzzle abstract base class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle = MockPuzzle()

    def test_puzzle_initialization(self):
        """Test that puzzle initializes with correct default state."""
        assert self.puzzle.puzzle_id == "test_puzzle"
        assert self.puzzle.title == "Test Puzzle"
        assert self.puzzle.difficulty == PuzzleDifficulty.BEGINNER
        assert self.puzzle.attempts == 0
        assert self.puzzle.hints_used == 0
        assert self.puzzle.completed is False
        assert self.puzzle.max_score == 100

    def test_successful_solution_attempt(self):
        """Test attempting a correct solution."""
        result = self.puzzle.attempt_solution("test_solution")

        assert result.success is True
        assert result.score > 0
        assert result.attempts == 1
        assert result.hints_used == 0
        assert self.puzzle.completed is True

    def test_failed_solution_attempt(self):
        """Test attempting an incorrect solution."""
        result = self.puzzle.attempt_solution("wrong_solution")

        assert result.success is False
        assert result.score == 0
        assert result.attempts == 1
        assert result.hints_used == 0
        assert self.puzzle.completed is False

    def test_multiple_attempts_score_penalty(self):
        """Test that multiple attempts reduce the score."""
        # First attempt (wrong)
        result1 = self.puzzle.attempt_solution("wrong1")
        assert result1.success is False

        # Second attempt (wrong)
        result2 = self.puzzle.attempt_solution("wrong2")
        assert result2.success is False

        # Third attempt (correct)
        result3 = self.puzzle.attempt_solution("test_solution")
        assert result3.success is True

        # Score should be reduced due to multiple attempts
        assert result3.score < 100  # Less than max score
        assert result3.attempts == 3

    def test_hint_usage_score_penalty(self):
        """Test that using hints reduces the score."""
        # Use some hints
        hint1 = self.puzzle.request_hint()
        hint2 = self.puzzle.request_hint()

        assert hint1 == "Hint 1"
        assert hint2 == "Hint 2"
        assert self.puzzle.hints_used == 2

        # Solve correctly
        result = self.puzzle.attempt_solution("test_solution")

        assert result.success is True
        assert result.score < 100  # Reduced due to hints
        assert result.hints_used == 2

    def test_score_calculation_minimum(self):
        """Test that score never goes below minimum value."""
        # Use many hints and attempts to try to get score below 10
        for _ in range(10):
            self.puzzle.request_hint()

        for _ in range(10):
            self.puzzle.attempt_solution("wrong")

        # Final correct attempt
        result = self.puzzle.attempt_solution("test_solution")

        assert result.success is True
        assert result.score >= 10  # Should not go below minimum

    def test_perfect_score(self):
        """Test getting perfect score with first attempt and no hints."""
        result = self.puzzle.attempt_solution("test_solution")

        assert result.success is True
        assert result.score == 100  # Perfect score
        assert result.attempts == 1
        assert result.hints_used == 0

    def test_puzzle_reset(self):
        """Test resetting puzzle state."""
        # Modify puzzle state
        self.puzzle.attempt_solution("wrong")
        self.puzzle.request_hint()

        assert self.puzzle.attempts > 0
        assert self.puzzle.hints_used > 0

        # Reset and verify
        self.puzzle.reset()

        assert self.puzzle.attempts == 0
        assert self.puzzle.hints_used == 0
        assert self.puzzle.completed is False

    def test_success_feedback_messages(self):
        """Test different success feedback messages based on performance."""
        # Perfect performance
        puzzle1 = MockPuzzle("p1")
        result1 = puzzle1.attempt_solution("test_solution")
        assert "Perfect!" in result1.feedback

        # Quick solution
        puzzle2 = MockPuzzle("p2")
        puzzle2.attempt_solution("wrong")  # One failed attempt
        result2 = puzzle2.attempt_solution("test_solution")
        assert "Excellent" in result2.feedback

        # Solution without hints
        puzzle3 = MockPuzzle("p3")
        for _ in range(3):
            puzzle3.attempt_solution("wrong")
        result3 = puzzle3.attempt_solution("test_solution")
        assert "without hints" in result3.feedback

        # General success
        puzzle4 = MockPuzzle("p4")
        puzzle4.request_hint()
        puzzle4.attempt_solution("wrong")
        result4 = puzzle4.attempt_solution("test_solution")
        # Should get "Excellent work" since it's only 2 attempts
        assert "Excellent" in result4.feedback


class TestPuzzleManager:
    """Test cases for PuzzleManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = PuzzleManager()
        self.puzzle1 = MockPuzzle("puzzle1", "Easy Puzzle", PuzzleDifficulty.BEGINNER)
        self.puzzle2 = MockPuzzle("puzzle2", "Hard Puzzle", PuzzleDifficulty.ADVANCED)

    def test_manager_initialization(self):
        """Test that puzzle manager initializes correctly."""
        assert len(self.manager.available_puzzles) == 0
        assert len(self.manager.completed_puzzles) == 0
        assert self.manager.current_puzzle is None

        stats = self.manager.player_stats
        assert stats["total_score"] == 0
        assert stats["puzzles_completed"] == 0
        assert stats["total_attempts"] == 0
        assert stats["total_hints_used"] == 0
        assert isinstance(stats["concepts_mastered"], set)

    def test_register_puzzle(self):
        """Test registering puzzles with the manager."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.register_puzzle(self.puzzle2)

        assert len(self.manager.available_puzzles) == 2
        assert "puzzle1" in self.manager.available_puzzles
        assert "puzzle2" in self.manager.available_puzzles

    def test_get_puzzle(self):
        """Test retrieving puzzles by ID."""
        self.manager.register_puzzle(self.puzzle1)

        retrieved = self.manager.get_puzzle("puzzle1")
        assert retrieved is self.puzzle1

        not_found = self.manager.get_puzzle("nonexistent")
        assert not_found is None

    def test_get_puzzles_by_difficulty(self):
        """Test filtering puzzles by difficulty."""
        self.manager.register_puzzle(self.puzzle1)  # BEGINNER
        self.manager.register_puzzle(self.puzzle2)  # ADVANCED

        beginner_puzzles = self.manager.get_puzzles_by_difficulty(
            PuzzleDifficulty.BEGINNER
        )
        assert len(beginner_puzzles) == 1
        assert beginner_puzzles[0] is self.puzzle1

        advanced_puzzles = self.manager.get_puzzles_by_difficulty(
            PuzzleDifficulty.ADVANCED
        )
        assert len(advanced_puzzles) == 1
        assert advanced_puzzles[0] is self.puzzle2

        intermediate_puzzles = self.manager.get_puzzles_by_difficulty(
            PuzzleDifficulty.INTERMEDIATE
        )
        assert len(intermediate_puzzles) == 0

    def test_get_next_puzzle(self):
        """Test getting the next appropriate puzzle."""
        self.manager.register_puzzle(self.puzzle2)  # ADVANCED
        self.manager.register_puzzle(self.puzzle1)  # BEGINNER

        # Should return the easiest uncompleted puzzle
        next_puzzle = self.manager.get_next_puzzle(current_level=1)
        assert next_puzzle is self.puzzle1  # BEGINNER comes first

    def test_start_puzzle(self):
        """Test starting a specific puzzle."""
        self.manager.register_puzzle(self.puzzle1)

        # Start the puzzle
        result = self.manager.start_puzzle("puzzle1")
        assert result is True
        assert self.manager.current_puzzle is self.puzzle1

        # Puzzle should be reset when started
        assert self.puzzle1.attempts == 0
        assert self.puzzle1.hints_used == 0
        assert self.puzzle1.completed is False

    def test_start_nonexistent_puzzle(self):
        """Test starting a puzzle that doesn't exist."""
        result = self.manager.start_puzzle("nonexistent")
        assert result is False
        assert self.manager.current_puzzle is None

    def test_submit_solution_success(self):
        """Test submitting a successful solution."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.start_puzzle("puzzle1")

        result = self.manager.submit_solution("test_solution")

        assert result is not None
        assert result.success is True
        assert "puzzle1" in self.manager.completed_puzzles
        assert self.manager.player_stats["puzzles_completed"] == 1
        assert self.manager.player_stats["total_score"] > 0

    def test_submit_solution_failure(self):
        """Test submitting an incorrect solution."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.start_puzzle("puzzle1")

        result = self.manager.submit_solution("wrong_solution")

        assert result is not None
        assert result.success is False
        assert "puzzle1" not in self.manager.completed_puzzles
        assert self.manager.player_stats["puzzles_completed"] == 0

    def test_submit_solution_no_current_puzzle(self):
        """Test submitting solution when no puzzle is active."""
        result = self.manager.submit_solution("any_solution")
        assert result is None

    def test_get_hint(self):
        """Test getting hints for current puzzle."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.start_puzzle("puzzle1")

        hint = self.manager.get_hint()
        assert hint == "Hint 1"
        assert (
            self.manager.player_stats["total_hints_used"] == 0
        )  # Not updated until completion

    def test_get_hint_no_current_puzzle(self):
        """Test getting hint when no puzzle is active."""
        hint = self.manager.get_hint()
        assert hint is None

    def test_get_progress_summary(self):
        """Test getting progress summary."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.register_puzzle(self.puzzle2)

        # Complete one puzzle
        self.manager.start_puzzle("puzzle1")
        self.manager.submit_solution("test_solution")

        summary = self.manager.get_progress_summary()

        assert summary["puzzles_completed"] == 1
        assert summary["total_puzzles"] == 2
        assert summary["completion_percentage"] == 50.0
        assert summary["total_score"] > 0
        assert summary["average_score"] > 0
        assert isinstance(summary["concepts_mastered"], list)

    def test_statistics_tracking(self):
        """Test that statistics are properly tracked."""
        self.manager.register_puzzle(self.puzzle1)
        self.manager.start_puzzle("puzzle1")

        # Use hints and make attempts
        self.manager.get_hint()
        self.manager.submit_solution("wrong1")
        self.manager.submit_solution("wrong2")
        result = self.manager.submit_solution("test_solution")

        stats = self.manager.player_stats
        assert stats["puzzles_completed"] == 1
        assert stats["total_score"] == result.score
        assert stats["total_attempts"] == 3
        assert stats["total_hints_used"] == 1


class TestSimpleFactPuzzle:
    """Test cases for the SimpleFactPuzzle implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.puzzle = SimpleFactPuzzle()

    def test_puzzle_properties(self):
        """Test that puzzle has correct properties."""
        assert self.puzzle.puzzle_id == "simple_fact_1"
        assert self.puzzle.title == "Create Your First Fact"
        assert self.puzzle.difficulty == PuzzleDifficulty.BEGINNER
        assert self.puzzle.expected_predicate == "likes"
        assert self.puzzle.expected_args == ["alice", "chocolate"]

    def test_get_description(self):
        """Test getting puzzle description."""
        description = self.puzzle.get_description()

        assert "Alice likes chocolate" in description
        assert "predicate(arg1, arg2)" in description
        assert isinstance(description, str)
        assert len(description) > 50  # Should be substantial

    def test_get_initial_context(self):
        """Test getting initial context."""
        context = self.puzzle.get_initial_context()

        assert "facts" in context
        assert "rules" in context
        assert "instructions" in context
        assert context["facts"] == []
        assert context["rules"] == []
        assert "likes" in context["instructions"]

    def test_validate_correct_solution(self):
        """Test validating the correct solution."""
        result = self.puzzle.validate_solution("likes(alice, chocolate).")

        assert result.is_valid is True

    def test_validate_incorrect_solution(self):
        """Test validating incorrect solutions."""
        # Wrong predicate
        result1 = self.puzzle.validate_solution("enjoys(alice, chocolate).")
        assert result1.is_valid is False
        assert "doesn't match the requirement" in result1.error_message

        # Wrong arguments
        result2 = self.puzzle.validate_solution("likes(bob, pizza).")
        assert result2.is_valid is False

        # Syntax error
        result3 = self.puzzle.validate_solution("likes(alice, chocolate)")
        assert result3.is_valid is False

    def test_get_hints(self):
        """Test getting hints at different levels."""
        hints = []
        for level in range(1, 5):
            hint = self.puzzle.get_hint(level)
            hints.append(hint)
            assert isinstance(hint, str)
            assert len(hint) > 10

        # Hints should be progressively more specific
        assert "relationship" in hints[0].lower()
        assert "likes" in hints[1].lower()
        assert "likes(alice, chocolate)" in hints[2]
        assert "period" in hints[3].lower()

    def test_get_hint_beyond_available(self):
        """Test getting hints beyond available levels."""
        hint = self.puzzle.get_hint(10)  # Beyond available hints

        assert isinstance(hint, str)
        assert "very close" in hint.lower()

    def test_get_expected_solution(self):
        """Test getting the expected solution."""
        solution = self.puzzle.get_expected_solution()
        assert solution == "likes(alice, chocolate)."

    def test_complete_puzzle_workflow(self):
        """Test a complete puzzle solving workflow."""
        # Get description and context
        description = self.puzzle.get_description()
        context = self.puzzle.get_initial_context()

        assert "Alice likes chocolate" in description
        assert isinstance(context, dict)

        # Try wrong solution first
        result1 = self.puzzle.attempt_solution("wrong_answer")
        assert result1.success is False

        # Get a hint
        hint = self.puzzle.request_hint()
        assert isinstance(hint, str)

        # Try correct solution
        result2 = self.puzzle.attempt_solution("likes(alice, chocolate).")
        assert result2.success is True
        assert result2.score < 100  # Reduced due to failed attempt and hint
        assert result2.attempts == 2
        assert result2.hints_used == 1


class TestPuzzleIntegration:
    """Integration tests for the puzzle system."""

    def test_full_puzzle_session(self):
        """Test a complete puzzle session from start to finish."""
        manager = PuzzleManager()
        puzzle = SimpleFactPuzzle()

        # Register and start puzzle
        manager.register_puzzle(puzzle)
        assert manager.start_puzzle("simple_fact_1") is True

        # Get initial information
        description = puzzle.get_description()
        context = puzzle.get_initial_context()

        assert "Alice likes chocolate" in description
        assert isinstance(context, dict)

        # Make some attempts with hints
        result1 = manager.submit_solution("wrong1")
        assert result1.success is False

        hint1 = manager.get_hint()
        assert isinstance(hint1, str)

        result2 = manager.submit_solution("wrong2")
        assert result2.success is False

        hint2 = manager.get_hint()
        assert isinstance(hint2, str)

        # Final correct solution
        result3 = manager.submit_solution("likes(alice, chocolate).")
        assert result3.success is True

        # Check final statistics
        stats = manager.get_player_stats()
        assert stats["puzzles_completed"] == 1
        assert stats["total_attempts"] == 3
        assert stats["total_hints_used"] == 2
        assert stats["total_score"] > 0

        # Check progress summary
        summary = manager.get_progress_summary()
        assert summary["completion_percentage"] == 100.0  # Only one puzzle
        assert summary["average_score"] > 0
