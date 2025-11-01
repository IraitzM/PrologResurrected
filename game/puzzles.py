"""
Puzzle Management Module

Base classes and management system for Prolog concept puzzles.
Coordinates puzzle selection, execution, and progress tracking.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from game.validation import ValidationResult, PrologValidator


class PuzzleDifficulty(Enum):
    """Puzzle difficulty levels."""

    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class PuzzleType(Enum):
    """Types of Prolog puzzles."""

    FACT_CREATION = "fact_creation"
    QUERY_WRITING = "query_writing"
    RULE_DEFINITION = "rule_definition"
    PATTERN_MATCHING = "pattern_matching"
    LOGICAL_DEDUCTION = "logical_deduction"


@dataclass
class PuzzleResult:
    """Result of a puzzle attempt."""

    success: bool
    score: int
    feedback: str
    hints_used: int
    attempts: int
    time_taken: Optional[float] = None


class BasePuzzle(ABC):
    """
    Abstract base class for all Prolog puzzles.

    Defines the interface that all puzzle implementations must follow.
    """

    def __init__(self, puzzle_id: str, title: str, difficulty: PuzzleDifficulty):
        """
        Initialize a puzzle.

        Args:
            puzzle_id: Unique identifier for the puzzle
            title: Human-readable puzzle title
            difficulty: Difficulty level of the puzzle
        """
        self.puzzle_id = puzzle_id
        self.title = title
        self.difficulty = difficulty
        self.attempts = 0
        self.hints_used = 0
        self.completed = False
        self.max_score = 100

    @abstractmethod
    def get_description(self) -> str:
        """Get the puzzle description and instructions."""
        pass

    @abstractmethod
    def get_initial_context(self) -> Dict[str, Any]:
        """Get initial context (facts, rules) for the puzzle."""
        pass

    @abstractmethod
    def validate_solution(self, user_input: str) -> ValidationResult:
        """
        Validate the user's solution attempt.

        Args:
            user_input: The user's solution string

        Returns:
            ValidationResult with success status and feedback
        """
        pass

    @abstractmethod
    def get_hint(self, hint_level: int) -> str:
        """
        Get a hint for the puzzle.

        Args:
            hint_level: Level of hint (1 = gentle, higher = more specific)

        Returns:
            Hint text appropriate for the level
        """
        pass

    @abstractmethod
    def get_expected_solution(self) -> str:
        """Get the expected solution for the puzzle."""
        pass

    def attempt_solution(self, user_input: str) -> PuzzleResult:
        """
        Process a solution attempt.

        Args:
            user_input: The user's solution attempt

        Returns:
            PuzzleResult with outcome and feedback
        """
        self.attempts += 1
        validation = self.validate_solution(user_input)

        if validation.is_valid:
            self.completed = True
            score = self._calculate_score()
            return PuzzleResult(
                success=True,
                score=score,
                feedback=self._get_success_feedback(),
                hints_used=self.hints_used,
                attempts=self.attempts,
            )
        else:
            return PuzzleResult(
                success=False,
                score=0,
                feedback=validation.error_message or "Incorrect solution. Try again!",
                hints_used=self.hints_used,
                attempts=self.attempts,
            )

    def request_hint(self) -> str:
        """
        Request a hint for the puzzle.

        Returns:
            Hint text
        """
        self.hints_used += 1
        return self.get_hint(self.hints_used)

    def reset(self):
        """Reset puzzle state for a new attempt."""
        self.attempts = 0
        self.hints_used = 0
        self.completed = False

    def _calculate_score(self) -> int:
        """Calculate score based on attempts and hints used."""
        base_score = self.max_score

        # Deduct points for multiple attempts
        attempt_penalty = max(0, (self.attempts - 1) * 10)

        # Deduct points for hints
        hint_penalty = self.hints_used * 15

        final_score = max(10, base_score - attempt_penalty - hint_penalty)
        return final_score

    def _get_success_feedback(self) -> str:
        """Get encouraging feedback for successful completion."""
        if self.attempts == 1 and self.hints_used == 0:
            return "Perfect! You solved it on the first try without hints!"
        elif self.attempts <= 2:
            return "Excellent work! You got it quickly."
        elif self.hints_used == 0:
            return "Great job solving it without hints!"
        else:
            return "Well done! You persevered and found the solution."


class PuzzleManager:
    """
    Manages puzzle selection, progression, and state tracking.

    Coordinates the overall puzzle experience and maintains
    player progress across different puzzle types and levels.
    """

    def __init__(self):
        """Initialize the puzzle manager."""
        self.available_puzzles: Dict[str, BasePuzzle] = {}
        self.completed_puzzles: List[str] = []
        self.current_puzzle: Optional[BasePuzzle] = None
        self.player_stats = {
            "total_score": 0,
            "puzzles_completed": 0,
            "total_attempts": 0,
            "total_hints_used": 0,
            "concepts_mastered": set(),
        }

    def register_puzzle(self, puzzle: BasePuzzle):
        """
        Register a puzzle with the manager.

        Args:
            puzzle: The puzzle instance to register
        """
        self.available_puzzles[puzzle.puzzle_id] = puzzle

    def get_puzzle(self, puzzle_id: str) -> Optional[BasePuzzle]:
        """
        Get a puzzle by ID.

        Args:
            puzzle_id: The puzzle identifier

        Returns:
            The puzzle instance or None if not found
        """
        return self.available_puzzles.get(puzzle_id)

    def get_puzzles_by_difficulty(
        self, difficulty: PuzzleDifficulty
    ) -> List[BasePuzzle]:
        """
        Get all puzzles of a specific difficulty.

        Args:
            difficulty: The difficulty level to filter by

        Returns:
            List of puzzles matching the difficulty
        """
        return [
            puzzle
            for puzzle in self.available_puzzles.values()
            if puzzle.difficulty == difficulty
        ]

    def get_next_puzzle(self, current_level: int) -> Optional[BasePuzzle]:
        """
        Get the next appropriate puzzle based on player level.

        Args:
            current_level: Player's current level

        Returns:
            Next puzzle to attempt or None if no suitable puzzle
        """
        # Simple progression: start with beginner puzzles
        available = [
            puzzle
            for puzzle in self.available_puzzles.values()
            if puzzle.puzzle_id not in self.completed_puzzles
        ]

        if not available:
            return None

        # Sort by difficulty and return the easiest uncompleted puzzle
        available.sort(key=lambda p: p.difficulty.value)
        return available[0]

    def start_puzzle(self, puzzle_id: str) -> bool:
        """
        Start a specific puzzle.

        Args:
            puzzle_id: ID of the puzzle to start

        Returns:
            True if puzzle started successfully
        """
        puzzle = self.get_puzzle(puzzle_id)
        if puzzle:
            self.current_puzzle = puzzle
            puzzle.reset()
            return True
        return False

    def submit_solution(self, user_input: str) -> Optional[PuzzleResult]:
        """
        Submit a solution for the current puzzle.

        Args:
            user_input: The user's solution attempt

        Returns:
            PuzzleResult or None if no current puzzle
        """
        if not self.current_puzzle:
            return None

        result = self.current_puzzle.attempt_solution(user_input)

        if result.success:
            self._complete_puzzle(self.current_puzzle, result)

        return result

    def get_hint(self) -> Optional[str]:
        """
        Get a hint for the current puzzle.

        Returns:
            Hint text or None if no current puzzle
        """
        if not self.current_puzzle:
            return None

        return self.current_puzzle.request_hint()

    def get_player_stats(self) -> Dict[str, Any]:
        """Get current player statistics."""
        return self.player_stats.copy()

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of player progress."""
        total_puzzles = len(self.available_puzzles)
        completed_count = len(self.completed_puzzles)

        return {
            "puzzles_completed": completed_count,
            "total_puzzles": total_puzzles,
            "completion_percentage": (completed_count / total_puzzles * 100)
            if total_puzzles > 0
            else 0,
            "total_score": self.player_stats["total_score"],
            "average_score": (
                self.player_stats["total_score"] / completed_count
                if completed_count > 0
                else 0
            ),
            "concepts_mastered": list(self.player_stats["concepts_mastered"]),
        }

    def _complete_puzzle(self, puzzle: BasePuzzle, result: PuzzleResult):
        """
        Handle puzzle completion and update statistics.

        Args:
            puzzle: The completed puzzle
            result: The result of the completion
        """
        if puzzle.puzzle_id not in self.completed_puzzles:
            self.completed_puzzles.append(puzzle.puzzle_id)
            self.player_stats["puzzles_completed"] += 1

        self.player_stats["total_score"] += result.score
        self.player_stats["total_attempts"] += result.attempts
        self.player_stats["total_hints_used"] += result.hints_used

        # For now, just mark general completion
        # This would be expanded to map puzzles to concepts based on type
        self.player_stats["concepts_mastered"].add("basic_prolog")


# Example puzzle implementation
class SimpleFactPuzzle(BasePuzzle):
    """A simple puzzle for creating Prolog facts."""

    def __init__(self):
        super().__init__(
            puzzle_id="simple_fact_1",
            title="Create Your First Fact",
            difficulty=PuzzleDifficulty.BEGINNER,
        )
        self.expected_predicate = "likes"
        self.expected_args = ["alice", "chocolate"]

    def get_description(self) -> str:
        return (
            "Create a Prolog fact that states 'Alice likes chocolate'.\n"
            "Remember: facts follow the pattern predicate(arg1, arg2)."
        )

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": [],
            "rules": [],
            "instructions": "Write a fact using the 'likes' predicate.",
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # First validate basic syntax
        result = PrologValidator.validate_fact(user_input)

        if not result.is_valid:
            return result

        # Check if it matches the expected solution
        components = result.parsed_components
        if (
            components
            and components.get("predicate") == self.expected_predicate
            and components.get("arguments") == self.expected_args
        ):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The fact is syntactically correct but doesn't match the requirement.",
            hint="Make sure you're stating that Alice likes chocolate.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = [
            "Think about the relationship between Alice and chocolate.",
            "Use 'likes' as the predicate name.",
            "The format should be: likes(alice, chocolate).",
            "Don't forget the period at the end!",
        ]

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "You're very close! Check the exact format required."

    def get_expected_solution(self) -> str:
        return "likes(alice, chocolate)."
