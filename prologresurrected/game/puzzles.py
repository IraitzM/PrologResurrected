"""
Puzzle Management Module

Base classes and management system for Prolog concept puzzles.
Coordinates puzzle selection, execution, and progress tracking.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from .validation import ValidationResult, PrologValidator
from .complexity import ComplexityLevel, ComplexityManager, HintFrequency, ExplanationDepth
from .hint_system import ComplexityAwareHintSystem, HintConfig, ExplanationConfig


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
    next_puzzle_unlocked: Optional[str] = None  # ID of next puzzle unlocked on completion


class BasePuzzle(ABC):
    """
    Abstract base class for all Prolog puzzles.

    Defines the interface that all puzzle implementations must follow.
    Now includes complexity-aware functionality for adaptive difficulty.
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
        self.complexity_manager = ComplexityManager()
        self.current_complexity_level = ComplexityLevel.BEGINNER
        self.hint_system = ComplexityAwareHintSystem()

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

    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """
        Set the complexity level for this puzzle instance.
        
        Args:
            level: The complexity level to set
        """
        self.current_complexity_level = level
        self.complexity_manager.set_complexity_level(level)
        self.hint_system.set_complexity_level(level)

    def get_complexity_level(self) -> ComplexityLevel:
        """Get the current complexity level for this puzzle."""
        return self.current_complexity_level

    def get_complexity_adapted_hint(self, hint_level: int) -> str:
        """
        Get a hint adapted to the current complexity level.
        
        Args:
            hint_level: Level of hint requested
            
        Returns:
            Hint text adapted to complexity level, or empty string if hints not allowed
        """
        # Create context for the hint system
        puzzle_context = {
            "attempts": self.attempts,
            "hints_used": self.hints_used,
            "puzzle_id": self.puzzle_id,
            "expected_predicate": getattr(self, 'expected_predicate', None),
            "expected_args": getattr(self, 'expected_args', None)
        }
        
        # Use the new hint system to generate adaptive hints
        return self.hint_system.get_hint(hint_level, puzzle_context)

    def get_complexity_adapted_feedback(self, validation_result: ValidationResult) -> str:
        """
        Get feedback adapted to the current complexity level.
        
        Args:
            validation_result: The validation result to provide feedback for
            
        Returns:
            Feedback text adapted to complexity level
        """
        if not validation_result.is_valid:
            # Get error explanation from hint system
            error_context = {
                "error_message": validation_result.error_message,
                "hint": validation_result.hint,
                "attempts": self.attempts
            }
            
            base_feedback = validation_result.error_message or "Incorrect solution."
            explanation = self.hint_system.get_explanation("syntax_error", error_context)
            
            # Combine base feedback with complexity-adapted explanation
            explanation_config = self.hint_system.get_explanation_config()
            
            if explanation_config.provide_detailed_errors:
                detailed_feedback = explanation
                if validation_result.hint and explanation_config.suggest_corrections:
                    detailed_feedback += f"\n\n💡 Suggestion: {validation_result.hint}"
                return detailed_feedback
            elif explanation_config.suggest_corrections and validation_result.hint:
                return f"{base_feedback}\n\nSuggestion: {validation_result.hint}"
            else:
                return base_feedback
        else:
            # Success feedback adapted to complexity
            return self._get_complexity_adapted_success_feedback()

    def _get_complexity_adapted_success_feedback(self) -> str:
        """Get success feedback adapted to the current complexity level."""
        base_feedback = self._get_success_feedback()
        explanation_depth = self.complexity_manager.get_explanation_depth()
        
        if explanation_depth == ExplanationDepth.DETAILED:
            return f"🎉 {base_feedback}\n\n✨ You're making great progress in your Prolog journey!"
        elif explanation_depth == ExplanationDepth.MODERATE:
            return f"✅ {base_feedback}"
        elif explanation_depth == ExplanationDepth.BRIEF:
            return base_feedback
        else:  # MINIMAL
            return "Correct."

    def get_complexity_parameters(self) -> Dict[str, Any]:
        """Get the puzzle parameters for the current complexity level."""
        return self.complexity_manager.get_puzzle_parameters()

    def should_provide_template(self) -> bool:
        """Check if a template should be provided based on complexity level."""
        params = self.get_complexity_parameters()
        return params.get("provide_templates", False)

    def should_show_examples(self) -> bool:
        """Check if examples should be shown based on complexity level."""
        params = self.get_complexity_parameters()
        return params.get("show_examples", True)

    def get_max_variables_allowed(self) -> int:
        """Get the maximum number of variables allowed for this complexity level."""
        params = self.get_complexity_parameters()
        return params.get("max_variables", 4)

    def get_max_predicates_allowed(self) -> int:
        """Get the maximum number of predicates allowed for this complexity level."""
        params = self.get_complexity_parameters()
        return params.get("max_predicates", 5)

    def allows_complex_syntax(self) -> bool:
        """Check if complex syntax is allowed at this complexity level."""
        params = self.get_complexity_parameters()
        return params.get("allow_complex_syntax", True)

    def requires_optimization(self) -> bool:
        """Check if optimization is required at this complexity level."""
        params = self.get_complexity_parameters()
        return params.get("require_optimization", False)

    def includes_edge_cases(self) -> bool:
        """Check if edge cases should be included at this complexity level."""
        params = self.get_complexity_parameters()
        return params.get("include_edge_cases", False)

    def get_hint_config(self) -> HintConfig:
        """Get the hint configuration for the current complexity level."""
        return self.hint_system.get_hint_config()

    def get_explanation_config(self) -> ExplanationConfig:
        """Get the explanation configuration for the current complexity level."""
        return self.hint_system.get_explanation_config()

    def can_request_hint(self) -> bool:
        """Check if a hint can be requested at the current state."""
        return self.hint_system.can_provide_hint(self.attempts, self.hints_used)

    def get_hint_availability_message(self) -> str:
        """Get a message about hint availability."""
        puzzle_context = {
            "attempts": self.attempts,
            "hints_used": self.hints_used
        }
        return self.hint_system.hint_generator.get_hint_availability_message(
            self.current_complexity_level, self.attempts, self.hints_used
        )

    def get_complexity_explanation(self, topic: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Get an explanation for a topic adapted to the current complexity level."""
        return self.hint_system.get_explanation(topic, context)

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
                feedback=self.get_complexity_adapted_feedback(validation),
                hints_used=self.hints_used,
                attempts=self.attempts,
            )
        else:
            return PuzzleResult(
                success=False,
                score=0,
                feedback=self.get_complexity_adapted_feedback(validation),
                hints_used=self.hints_used,
                attempts=self.attempts,
            )

    def request_hint(self) -> str:
        """
        Request a hint for the puzzle.

        Returns:
            Hint text adapted to complexity level
        """
        # Check if hint can be provided before incrementing counter
        if self.hint_system.can_provide_hint(self.attempts, self.hints_used):
            self.hints_used += 1
            return self.get_complexity_adapted_hint(self.hints_used)
        else:
            # Return availability message without incrementing counter
            puzzle_context = {
                "attempts": self.attempts,
                "hints_used": self.hints_used
            }
            return self.hint_system.get_hint(1, puzzle_context)

    def reset(self):
        """Reset puzzle state for a new attempt."""
        self.attempts = 0
        self.hints_used = 0
        self.completed = False

    def _calculate_score(self) -> int:
        """Calculate score based on attempts, hints used, and complexity level."""
        base_score = self.max_score

        # Deduct points for multiple attempts
        attempt_penalty = max(0, (self.attempts - 1) * 10)

        # Use hint system to calculate hint penalty based on complexity level
        hint_penalty = self.hint_system.calculate_hint_penalty(self.hints_used)

        # Apply complexity multiplier
        complexity_multiplier = self.complexity_manager.get_scoring_multiplier()
        
        final_score = max(10, base_score - attempt_penalty - hint_penalty)
        final_score = int(final_score * complexity_multiplier)
        
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
    Now includes complexity-aware puzzle management.
    """

    def __init__(self):
        """Initialize the puzzle manager."""
        self.available_puzzles: Dict[str, BasePuzzle] = {}
        self.completed_puzzles: List[str] = []
        self.current_puzzle: Optional[BasePuzzle] = None
        self.complexity_manager = ComplexityManager()
        # Import here to avoid circular imports
        from .adaptive_puzzle_factory import AdaptivePuzzleFactory
        self.adaptive_factory = AdaptivePuzzleFactory()
        self.player_stats = {
            "total_score": 0,
            "puzzles_completed": 0,
            "total_attempts": 0,
            "total_hints_used": 0,
            "concepts_mastered": set(),
            "hello_world_completed": False,  # Track hello world tutorial completion
            "complexity_achievements": {
                ComplexityLevel.BEGINNER: {"puzzles_completed": 0, "total_score": 0},
                ComplexityLevel.INTERMEDIATE: {"puzzles_completed": 0, "total_score": 0},
                ComplexityLevel.ADVANCED: {"puzzles_completed": 0, "total_score": 0},
                ComplexityLevel.EXPERT: {"puzzles_completed": 0, "total_score": 0},
            },
            "puzzle_completion_history": [],  # Track each puzzle completion with complexity level
        }
        
        # Register the Hello World tutorial as level 0
        self._register_hello_world_puzzle()
        
        # Register the Memory Stack Failure puzzle as first adventure mode puzzle
        self._register_memory_stack_puzzle()

    def _register_hello_world_puzzle(self):
        """Register the Hello World Prolog tutorial puzzle."""
        try:
            from .hello_world_puzzle import HelloWorldPuzzle
            hello_world = HelloWorldPuzzle()
            self.available_puzzles[hello_world.puzzle_id] = hello_world
        except ImportError:
            # HelloWorldPuzzle not available, skip registration
            pass
    
    def _register_memory_stack_puzzle(self):
        """Register the Memory Stack Failure puzzle as first adventure mode puzzle."""
        try:
            from .memory_stack_puzzle import MemoryStackPuzzle
            memory_stack = MemoryStackPuzzle()
            self.available_puzzles[memory_stack.puzzle_id] = memory_stack
        except ImportError:
            # MemoryStackPuzzle not available, skip registration
            pass

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
        
        Ensures that core Prolog concepts are covered regardless of complexity level
        by selecting puzzles that teach fundamental concepts.

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
        # This ensures core concepts are taught in order regardless of complexity level
        available.sort(key=lambda p: p.difficulty.value)
        return available[0]
    
    def get_concept_coverage(self) -> Dict[str, bool]:
        """
        Get coverage of core Prolog concepts across all complexity levels.
        
        Returns:
            Dictionary mapping concept names to whether they've been covered
        """
        core_concepts = {
            "prolog_basics": False,
            "facts": False,
            "queries": False,
            "variables": False,
            "rules": False,
            "unification": False,
            "backtracking": False,
            "recursion": False,
        }
        
        # Mark concepts as covered if they're in the mastered set
        for concept in self.player_stats["concepts_mastered"]:
            if concept in core_concepts:
                core_concepts[concept] = True
        
        return core_concepts
    
    def ensures_concept_coverage(self, puzzle_id: str) -> List[str]:
        """
        Get the list of core concepts that a puzzle covers.
        
        This ensures that puzzles at any complexity level teach the same
        fundamental concepts, just with different levels of guidance.
        
        Args:
            puzzle_id: The puzzle to check
            
        Returns:
            List of concept names covered by this puzzle
        """
        # Map puzzles to the concepts they cover
        puzzle_concepts = {
            "hello_world_prolog": ["prolog_basics", "facts", "queries", "variables"],
            "simple_fact_1": ["facts", "prolog_basics"],
            "basic_query_1": ["queries", "variables"],
            "rule_definition_1": ["rules", "facts"],
            "pattern_match_1": ["unification", "variables"],
            "logical_deduction_1": ["backtracking", "rules"],
        }
        
        return puzzle_concepts.get(puzzle_id, [])

    def start_puzzle(self, puzzle_id: str) -> bool:
        """
        Start a specific puzzle.

        Args:
            puzzle_id: ID of the puzzle to start

        Returns:
            True if puzzle started successfully
        """
        base_puzzle = self.get_puzzle(puzzle_id)
        if base_puzzle:
            # Set complexity level on the original puzzle for backward compatibility
            current_level = self.complexity_manager.get_current_level()
            base_puzzle.set_complexity_level(current_level)
            
            # Create an adapted version of the puzzle for the current complexity level
            self.current_puzzle = self.adaptive_factory.create_adapted_puzzle(
                base_puzzle, 
                current_level
            )
            self.current_puzzle.reset()
            return True
        return False

    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """
        Set the complexity level for all puzzles.
        
        Args:
            level: The complexity level to set
        """
        self.complexity_manager.set_complexity_level(level)
        
        # Update complexity level on all registered puzzles for backward compatibility
        for puzzle in self.available_puzzles.values():
            puzzle.set_complexity_level(level)
        
        # If there's a current puzzle, re-adapt it to the new complexity level
        if self.current_puzzle:
            # Find the base puzzle for re-adaptation
            base_puzzle_id = self.current_puzzle.puzzle_id
            base_puzzle = self.available_puzzles.get(base_puzzle_id)
            if base_puzzle:
                # Preserve current state
                attempts = self.current_puzzle.attempts
                hints_used = self.current_puzzle.hints_used
                completed = self.current_puzzle.completed
                
                # Create new adapted puzzle
                self.current_puzzle = self.adaptive_factory.create_adapted_puzzle(
                    base_puzzle, 
                    level
                )
                
                # Restore state
                self.current_puzzle.attempts = attempts
                self.current_puzzle.hints_used = hints_used
                self.current_puzzle.completed = completed

    def get_complexity_level(self) -> ComplexityLevel:
        """Get the current complexity level."""
        return self.complexity_manager.get_current_level()

    def get_complexity_config(self) -> Dict[str, Any]:
        """Get the current complexity configuration."""
        config = self.complexity_manager.get_current_config()
        return {
            "name": config.name,
            "description": config.description,
            "level": self.complexity_manager.get_current_level(),
            "ui_indicators": config.ui_indicators,
            "scoring_multiplier": config.scoring_multiplier
        }

    def get_adapted_puzzle(self, puzzle_id: str, level: ComplexityLevel) -> Optional[BasePuzzle]:
        """
        Get an adapted version of a puzzle for a specific complexity level.
        
        Args:
            puzzle_id: ID of the puzzle to adapt
            level: Target complexity level
            
        Returns:
            Adapted puzzle instance or None if puzzle not found
        """
        base_puzzle = self.get_puzzle(puzzle_id)
        if base_puzzle:
            return self.adaptive_factory.create_adapted_puzzle(base_puzzle, level)
        return None

    def get_adaptation_summary(self, puzzle_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a summary of adaptations for the current puzzle.
        
        Args:
            puzzle_id: ID of the puzzle to get summary for
            
        Returns:
            Adaptation summary or None if puzzle not found
        """
        if self.current_puzzle and self.current_puzzle.puzzle_id == puzzle_id:
            return self.adaptive_factory.get_adaptation_summary(self.current_puzzle)
        return None

    def can_adapt_puzzle(self, puzzle_id: str) -> bool:
        """
        Check if a puzzle can be adapted by the factory.
        
        Args:
            puzzle_id: ID of the puzzle to check
            
        Returns:
            True if puzzle can be adapted
        """
        puzzle = self.get_puzzle(puzzle_id)
        if puzzle:
            return self.adaptive_factory.can_adapt_puzzle(puzzle)
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
            current_puzzle_id = self.current_puzzle.puzzle_id
            self._complete_puzzle(self.current_puzzle, result)
            
            # Unlock next puzzle in progression
            next_puzzle_id = self.unlock_next_puzzle(current_puzzle_id)
            if next_puzzle_id:
                # Store the unlocked puzzle ID for display to player
                result.next_puzzle_unlocked = next_puzzle_id

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
    
    def get_complexity_achievements(self, level: ComplexityLevel) -> Dict[str, Any]:
        """
        Get achievements for a specific complexity level.
        
        Args:
            level: The complexity level to get achievements for
            
        Returns:
            Dictionary containing puzzles completed and scores for that level
        """
        achievements = self.player_stats["complexity_achievements"][level]
        return {
            "level": level.name,
            "puzzles_completed": achievements["puzzles_completed"],
            "total_score": achievements["total_score"],
            "average_score": (
                achievements["total_score"] / achievements["puzzles_completed"]
                if achievements["puzzles_completed"] > 0
                else 0
            ),
        }
    
    def get_all_complexity_achievements(self) -> Dict[str, Dict[str, Any]]:
        """
        Get achievements for all complexity levels.
        
        Returns:
            Dictionary mapping complexity level names to their achievements
        """
        achievements = {}
        for level in ComplexityLevel:
            achievements[level.name] = self.get_complexity_achievements(level)
        return achievements

    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of player progress including complexity-level achievements."""
        total_puzzles = len(self.available_puzzles)
        completed_count = len(self.completed_puzzles)

        # Format complexity achievements for display
        complexity_achievements = {}
        for level, achievements in self.player_stats["complexity_achievements"].items():
            complexity_achievements[level.name] = {
                "puzzles_completed": achievements["puzzles_completed"],
                "total_score": achievements["total_score"],
                "average_score": (
                    achievements["total_score"] / achievements["puzzles_completed"]
                    if achievements["puzzles_completed"] > 0
                    else 0
                ),
            }

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
            "hello_world_completed": self.player_stats["hello_world_completed"],
            "complexity_achievements": complexity_achievements,
            "completion_history": self.player_stats["puzzle_completion_history"].copy(),
        }

    def is_hello_world_completed(self) -> bool:
        """Check if the Hello World tutorial has been completed."""
        return self.player_stats.get("hello_world_completed", False)

    def get_hello_world_puzzle(self) -> Optional[BasePuzzle]:
        """Get the Hello World tutorial puzzle."""
        return self.get_puzzle("hello_world_prolog")

    def should_recommend_hello_world(self) -> bool:
        """Check if Hello World tutorial should be recommended to the player."""
        # Recommend if not completed and no other puzzles have been completed
        return (
            not self.is_hello_world_completed() 
            and len(self.completed_puzzles) == 0
        )

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

        # Track complexity-specific achievements
        complexity_level = puzzle.get_complexity_level()
        self.player_stats["complexity_achievements"][complexity_level]["puzzles_completed"] += 1
        self.player_stats["complexity_achievements"][complexity_level]["total_score"] += result.score
        
        # Record completion in history with complexity information
        completion_record = {
            "puzzle_id": puzzle.puzzle_id,
            "puzzle_title": puzzle.title,
            "complexity_level": complexity_level.name,
            "score": result.score,
            "attempts": result.attempts,
            "hints_used": result.hints_used,
        }
        self.player_stats["puzzle_completion_history"].append(completion_record)

        # Track hello world tutorial completion
        if puzzle.puzzle_id == "hello_world_prolog":
            self.player_stats["hello_world_completed"] = True
            self.player_stats["concepts_mastered"].add("prolog_basics")
            self.player_stats["concepts_mastered"].add("facts")
            self.player_stats["concepts_mastered"].add("queries")
            self.player_stats["concepts_mastered"].add("variables")
        # Track memory stack puzzle completion and debugging concepts
        elif puzzle.puzzle_id == "memory_stack_failure":
            self._track_memory_stack_concepts(puzzle)
        else:
            # For now, just mark general completion
            # This would be expanded to map puzzles to concepts based on type
            self.player_stats["concepts_mastered"].add("basic_prolog")
    
    def _track_memory_stack_concepts(self, puzzle: BasePuzzle):
        """
        Track concept mastery for the Memory Stack Failure puzzle.
        
        Records debugging skills and Prolog concepts learned through
        the puzzle completion.
        
        Args:
            puzzle: The completed Memory Stack puzzle
            
        Validates: Requirements 5.5
        """
        # Core debugging concepts learned
        self.player_stats["concepts_mastered"].add("debugging_methodology")
        self.player_stats["concepts_mastered"].add("stack_trace_analysis")
        self.player_stats["concepts_mastered"].add("root_cause_analysis")
        self.player_stats["concepts_mastered"].add("logical_investigation")
        
        # Prolog concepts reinforced
        self.player_stats["concepts_mastered"].add("prolog_queries")
        self.player_stats["concepts_mastered"].add("variable_binding")
        self.player_stats["concepts_mastered"].add("compound_queries")
        self.player_stats["concepts_mastered"].add("pattern_matching")
        
        # Get puzzle-specific completion statistics if available
        if hasattr(puzzle, 'get_completion_statistics'):
            stats = puzzle.get_completion_statistics()
            
            # Track scenario-specific concepts
            if stats.get("completed"):
                scenario_type = stats.get("scenario_type", "")
                
                # Add scenario-specific debugging concepts
                if scenario_type == "memory_leak":
                    self.player_stats["concepts_mastered"].add("memory_leak_detection")
                    self.player_stats["concepts_mastered"].add("resource_management")
                elif scenario_type == "stack_overflow":
                    self.player_stats["concepts_mastered"].add("recursion_analysis")
                    self.player_stats["concepts_mastered"].add("stack_overflow_detection")
                elif scenario_type == "null_pointer":
                    self.player_stats["concepts_mastered"].add("null_pointer_detection")
                    self.player_stats["concepts_mastered"].add("parameter_validation")
                elif scenario_type == "deadlock":
                    self.player_stats["concepts_mastered"].add("deadlock_detection")
                    self.player_stats["concepts_mastered"].add("concurrency_debugging")
                elif scenario_type == "resource_exhaustion":
                    self.player_stats["concepts_mastered"].add("resource_exhaustion_detection")
                    self.player_stats["concepts_mastered"].add("capacity_analysis")
                
                # Track advanced Prolog concepts based on discoveries
                discoveries = stats.get("discoveries", [])
                if "pattern" in discoveries:
                    self.player_stats["concepts_mastered"].add("pattern_recognition")
                if len(discoveries) >= 3:
                    self.player_stats["concepts_mastered"].add("systematic_investigation")
    
    def unlock_next_puzzle(self, current_puzzle_id: str) -> Optional[str]:
        """
        Unlock the next puzzle in the progression after completing current puzzle.
        
        Determines which puzzle should be unlocked next based on the
        completed puzzle and player progress.
        
        Args:
            current_puzzle_id: ID of the puzzle just completed
            
        Returns:
            ID of the next unlocked puzzle, or None if no next puzzle
            
        Validates: Requirements 5.5
        """
        # Define puzzle progression order
        puzzle_progression = {
            "hello_world_prolog": "memory_stack_failure",  # Tutorial -> First adventure puzzle
            "memory_stack_failure": None,  # Currently the last puzzle (more to be added)
        }
        
        next_puzzle_id = puzzle_progression.get(current_puzzle_id)
        
        if next_puzzle_id and next_puzzle_id not in self.completed_puzzles:
            # Puzzle is unlocked and not yet completed
            return next_puzzle_id
        
        return None
    
    def is_puzzle_unlocked(self, puzzle_id: str) -> bool:
        """
        Check if a puzzle is unlocked and available to play.
        
        A puzzle is unlocked if:
        - It's the hello world tutorial (always available)
        - Its prerequisite puzzle has been completed
        
        Args:
            puzzle_id: ID of the puzzle to check
            
        Returns:
            True if puzzle is unlocked, False otherwise
            
        Validates: Requirements 5.5
        """
        # Hello world tutorial is always unlocked
        if puzzle_id == "hello_world_prolog":
            return True
        
        # Memory stack puzzle is unlocked after hello world
        if puzzle_id == "memory_stack_failure":
            return self.player_stats.get("hello_world_completed", False)
        
        # Future puzzles would have their own unlock conditions here
        
        return False
    
    def get_unlocked_puzzles(self) -> List[str]:
        """
        Get list of all currently unlocked puzzle IDs.
        
        Returns:
            List of puzzle IDs that are unlocked and available
            
        Validates: Requirements 5.5
        """
        unlocked = []
        
        for puzzle_id in self.available_puzzles.keys():
            if self.is_puzzle_unlocked(puzzle_id):
                unlocked.append(puzzle_id)
        
        return unlocked
    
    def get_next_recommended_puzzle(self) -> Optional[str]:
        """
        Get the next recommended puzzle for the player.
        
        Recommends the next uncompleted puzzle in the progression
        that is currently unlocked.
        
        Returns:
            Puzzle ID of recommended next puzzle, or None if all complete
            
        Validates: Requirements 5.5
        """
        # Recommend hello world if not completed
        if not self.is_hello_world_completed() and "hello_world_prolog" not in self.completed_puzzles:
            return "hello_world_prolog"
        
        # Get all unlocked puzzles
        unlocked = self.get_unlocked_puzzles()
        
        # Find first unlocked puzzle that's not completed
        for puzzle_id in unlocked:
            if puzzle_id not in self.completed_puzzles:
                return puzzle_id
        
        return None  # All unlocked puzzles are completed


# Example puzzle implementation with complexity awareness
class SimpleFactPuzzle(BasePuzzle):
    """A simple puzzle for creating Prolog facts with complexity adaptation."""

    def __init__(self):
        super().__init__(
            puzzle_id="simple_fact_1",
            title="Create Your First Fact",
            difficulty=PuzzleDifficulty.BEGINNER,
        )
        self.expected_predicate = "likes"
        self.expected_args = ["alice", "chocolate"]

    def get_description(self) -> str:
        """Get puzzle description adapted to complexity level."""
        base_description = "Create a Prolog fact that states 'Alice likes chocolate'."
        
        if self.should_show_examples():
            base_description += "\nRemember: facts follow the pattern predicate(arg1, arg2)."
        
        if self.should_provide_template():
            base_description += "\nTemplate: likes(?, ?)."
        
        return base_description

    def get_initial_context(self) -> Dict[str, Any]:
        context = {
            "facts": [],
            "rules": [],
            "instructions": "Write a fact using the 'likes' predicate.",
        }
        
        if self.should_show_examples():
            context["examples"] = [
                "Example fact: loves(john, mary).",
                "Example fact: owns(sarah, car)."
            ]
        
        return context

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

        # Provide complexity-appropriate error messages
        explanation_depth = self.complexity_manager.get_explanation_depth()
        
        if explanation_depth == ExplanationDepth.DETAILED:
            error_msg = "The fact is syntactically correct but doesn't match the requirement. Make sure you're stating that Alice likes chocolate using the exact format."
            hint_msg = "Check that you're using 'likes' as the predicate and 'alice' and 'chocolate' as the arguments."
        elif explanation_depth == ExplanationDepth.MODERATE:
            error_msg = "The fact is syntactically correct but doesn't match the requirement."
            hint_msg = "Make sure you're stating that Alice likes chocolate."
        else:  # BRIEF or MINIMAL
            error_msg = "Incorrect fact."
            hint_msg = "Check the predicate and arguments."

        return ValidationResult(
            is_valid=False,
            error_message=error_msg,
            hint=hint_msg,
        )

    def get_hint(self, hint_level: int) -> str:
        """Get base hints that will be adapted by complexity level."""
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
