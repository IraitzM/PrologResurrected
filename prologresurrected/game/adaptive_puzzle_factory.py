"""
Adaptive Puzzle Factory Module

Creates and adapts puzzles based on complexity levels, ensuring that all puzzles
provide appropriate challenge and guidance for the selected difficulty level.
"""

from typing import Dict, Any, Optional, Type, List
from copy import deepcopy
from .puzzles import BasePuzzle, PuzzleDifficulty, PuzzleType
from .complexity import ComplexityLevel, ComplexityManager
from .hello_world_puzzle import HelloWorldPuzzle


class AdaptivePuzzleFactory:
    """
    Factory class for creating complexity-adapted puzzles.
    
    This factory takes base puzzle instances and adapts them according to
    the selected complexity level, modifying parameters like hint availability,
    explanation depth, and puzzle constraints.
    """
    
    def __init__(self):
        """Initialize the adaptive puzzle factory."""
        self.complexity_manager = ComplexityManager()
        self.adaptation_strategies = self._initialize_adaptation_strategies()
        self.puzzle_type_mappings = self._initialize_puzzle_type_mappings()
    
    def _initialize_adaptation_strategies(self) -> Dict[ComplexityLevel, Dict[str, Any]]:
        """Initialize adaptation strategies for each complexity level."""
        return {
            ComplexityLevel.BEGINNER: {
                "max_variables": 2,
                "max_predicates": 3,
                "allow_complex_syntax": False,
                "provide_templates": True,
                "show_examples": True,
                "include_step_by_step": True,
                "hint_frequency": "always",
                "explanation_detail": "detailed",
                "error_recovery": "guided",
                "syntax_assistance": True,
                "concept_reinforcement": True
            },
            ComplexityLevel.INTERMEDIATE: {
                "max_variables": 4,
                "max_predicates": 5,
                "allow_complex_syntax": True,
                "provide_templates": False,
                "show_examples": True,
                "include_step_by_step": False,
                "hint_frequency": "on_request",
                "explanation_detail": "moderate",
                "error_recovery": "standard",
                "syntax_assistance": True,
                "concept_reinforcement": False
            },
            ComplexityLevel.ADVANCED: {
                "max_variables": 6,
                "max_predicates": 8,
                "allow_complex_syntax": True,
                "provide_templates": False,
                "show_examples": False,
                "include_step_by_step": False,
                "hint_frequency": "after_attempts",
                "explanation_detail": "brief",
                "error_recovery": "minimal",
                "syntax_assistance": False,
                "concept_reinforcement": False,
                "require_optimization": True,
                "multiple_solutions": True
            },
            ComplexityLevel.EXPERT: {
                "max_variables": 8,
                "max_predicates": 12,
                "allow_complex_syntax": True,
                "provide_templates": False,
                "show_examples": False,
                "include_step_by_step": False,
                "hint_frequency": "none",
                "explanation_detail": "minimal",
                "error_recovery": "none",
                "syntax_assistance": False,
                "concept_reinforcement": False,
                "require_optimization": True,
                "multiple_solutions": True,
                "include_edge_cases": True,
                "performance_constraints": True
            }
        }
    
    def _initialize_puzzle_type_mappings(self) -> Dict[str, PuzzleType]:
        """Initialize mappings from puzzle IDs to puzzle types."""
        return {
            "hello_world_prolog": PuzzleType.FACT_CREATION,
            "simple_fact_1": PuzzleType.FACT_CREATION,
            "basic_query_1": PuzzleType.QUERY_WRITING,
            "rule_definition_1": PuzzleType.RULE_DEFINITION,
            "pattern_match_1": PuzzleType.PATTERN_MATCHING,
            "logical_deduction_1": PuzzleType.LOGICAL_DEDUCTION
        }
    
    def create_adapted_puzzle(
        self, 
        base_puzzle: BasePuzzle, 
        complexity_level: ComplexityLevel
    ) -> BasePuzzle:
        """
        Create an adapted version of a puzzle for the specified complexity level.
        
        Args:
            base_puzzle: The base puzzle to adapt
            complexity_level: The target complexity level
            
        Returns:
            Adapted puzzle instance
            
        Raises:
            ValueError: If base_puzzle or complexity_level is invalid
            RuntimeError: If adaptation fails critically
        """
        # Validate inputs
        if not isinstance(base_puzzle, BasePuzzle):
            raise ValueError(f"base_puzzle must be a BasePuzzle instance, got {type(base_puzzle)}")
        
        if not isinstance(complexity_level, ComplexityLevel):
            raise ValueError(f"complexity_level must be a ComplexityLevel enum, got {type(complexity_level)}")
        
        try:
            # Create a deep copy to avoid modifying the original
            adapted_puzzle = deepcopy(base_puzzle)
            
            # Set the complexity level on the puzzle
            adapted_puzzle.set_complexity_level(complexity_level)
            
            # Get the puzzle type for specific adaptations
            puzzle_type = self._get_puzzle_type(base_puzzle)
            
            # Apply general adaptations
            self._apply_general_adaptations(adapted_puzzle, complexity_level)
            
            # Apply type-specific adaptations with error handling
            try:
                if puzzle_type == PuzzleType.FACT_CREATION:
                    self._adapt_fact_puzzle(adapted_puzzle, complexity_level)
                elif puzzle_type == PuzzleType.QUERY_WRITING:
                    self._adapt_query_puzzle(adapted_puzzle, complexity_level)
                elif puzzle_type == PuzzleType.RULE_DEFINITION:
                    self._adapt_rule_puzzle(adapted_puzzle, complexity_level)
                elif puzzle_type == PuzzleType.PATTERN_MATCHING:
                    self._adapt_pattern_puzzle(adapted_puzzle, complexity_level)
                elif puzzle_type == PuzzleType.LOGICAL_DEDUCTION:
                    self._adapt_deduction_puzzle(adapted_puzzle, complexity_level)
            except Exception as e:
                # Log the error but continue with general adaptations only
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Type-specific adaptation failed for {puzzle_type}: {e}")
                # Puzzle still has general adaptations applied
            
            return adapted_puzzle
            
        except Exception as e:
            # If deep copy or basic adaptation fails, return original puzzle
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Critical failure in puzzle adaptation: {e}")
            # Return original puzzle as last resort
            return base_puzzle
    
    def _get_puzzle_type(self, puzzle: BasePuzzle) -> PuzzleType:
        """Determine the puzzle type from the puzzle instance."""
        puzzle_id = puzzle.puzzle_id
        return self.puzzle_type_mappings.get(puzzle_id, PuzzleType.FACT_CREATION)
    
    def _apply_general_adaptations(self, puzzle: BasePuzzle, level: ComplexityLevel) -> None:
        """Apply general adaptations that affect all puzzle types."""
        strategy = self.adaptation_strategies[level]
        
        # Store adaptation parameters on the puzzle for use by methods
        if not hasattr(puzzle, '_adaptation_params'):
            puzzle._adaptation_params = {}
        
        puzzle._adaptation_params.update(strategy)
        
        # Don't modify max_score - let the complexity multiplier handle scoring differences
        # The complexity multiplier in the scoring calculation will provide the appropriate scaling
    
    def _adapt_fact_puzzle(self, puzzle: BasePuzzle, level: ComplexityLevel) -> None:
        """Apply adaptations specific to fact creation puzzles."""
        strategy = self.adaptation_strategies[level]
        
        if level == ComplexityLevel.BEGINNER:
            # Add template and examples for beginners
            puzzle._beginner_template = "predicate(argument1, argument2)."
            puzzle._show_syntax_help = True
            puzzle._provide_examples = True
            
        elif level == ComplexityLevel.INTERMEDIATE:
            # Standard fact creation with moderate guidance
            puzzle._show_syntax_help = True
            puzzle._provide_examples = True
            
        elif level == ComplexityLevel.ADVANCED:
            # More complex facts with multiple arguments
            puzzle._allow_multiple_predicates = True
            puzzle._require_complex_relationships = True
            
        elif level == ComplexityLevel.EXPERT:
            # Complex facts with optimization requirements
            puzzle._require_optimization = True
            puzzle._include_edge_cases = True
            puzzle._multiple_valid_solutions = True
    
    def _adapt_query_puzzle(self, puzzle: BasePuzzle, level: ComplexityLevel) -> None:
        """Apply adaptations specific to query writing puzzles."""
        strategy = self.adaptation_strategies[level]
        
        if level == ComplexityLevel.BEGINNER:
            # Simple queries with clear examples
            puzzle._show_query_syntax = True
            puzzle._provide_query_templates = True
            puzzle._explain_variable_usage = True
            
        elif level == ComplexityLevel.INTERMEDIATE:
            # Standard queries with some guidance
            puzzle._show_query_syntax = True
            puzzle._allow_simple_variables = True
            
        elif level == ComplexityLevel.ADVANCED:
            # Complex queries with multiple variables
            puzzle._require_multiple_variables = True
            puzzle._allow_complex_conditions = True
            
        elif level == ComplexityLevel.EXPERT:
            # Advanced queries with optimization
            puzzle._require_optimization = True
            puzzle._multiple_solution_paths = True
            puzzle._performance_constraints = True
    
    def _adapt_rule_puzzle(self, puzzle: BasePuzzle, level: ComplexityLevel) -> None:
        """Apply adaptations specific to rule definition puzzles."""
        strategy = self.adaptation_strategies[level]
        
        if level == ComplexityLevel.BEGINNER:
            # Simple rules with clear structure
            puzzle._show_rule_syntax = True
            puzzle._provide_rule_templates = True
            puzzle._explain_implication = True
            puzzle._max_conditions = 2
            
        elif level == ComplexityLevel.INTERMEDIATE:
            # Standard rules with moderate complexity
            puzzle._show_rule_syntax = True
            puzzle._max_conditions = 3
            puzzle._allow_conjunctions = True
            
        elif level == ComplexityLevel.ADVANCED:
            # Complex rules with multiple conditions
            puzzle._max_conditions = 5
            puzzle._allow_disjunctions = True
            puzzle._require_multiple_rules = True
            
        elif level == ComplexityLevel.EXPERT:
            # Advanced rules with optimization
            puzzle._require_optimization = True
            puzzle._allow_recursion = True
            puzzle._performance_constraints = True
    
    def _adapt_pattern_puzzle(self, puzzle: BasePuzzle, level: ComplexityLevel) -> None:
        """Apply adaptations specific to pattern matching puzzles."""
        strategy = self.adaptation_strategies[level]
        
        if level == ComplexityLevel.BEGINNER:
            # Simple patterns with clear examples
            puzzle._show_pattern_examples = True
            puzzle._explain_unification = True
            puzzle._max_pattern_complexity = 2
            
        elif level == ComplexityLevel.INTERMEDIATE:
            # Standard patterns with moderate complexity
            puzzle._max_pattern_complexity = 3
            puzzle._allow_nested_patterns = True
            
        elif level == ComplexityLevel.ADVANCED:
            # Complex patterns with multiple variables
            puzzle._max_pattern_complexity = 5
            puzzle._require_complex_unification = True
            
        elif level == ComplexityLevel.EXPERT:
            # Advanced patterns with optimization
            puzzle._require_optimization = True
            puzzle._include_edge_cases = True
            puzzle._performance_constraints = True
    
    def _adapt_deduction_puzzle(self, puzzle: BasePuzzle, level: ComplexityLevel) -> None:
        """Apply adaptations specific to logical deduction puzzles."""
        strategy = self.adaptation_strategies[level]
        
        if level == ComplexityLevel.BEGINNER:
            # Simple deductions with clear reasoning
            puzzle._show_reasoning_steps = True
            puzzle._explain_backtracking = True
            puzzle._max_inference_depth = 2
            
        elif level == ComplexityLevel.INTERMEDIATE:
            # Standard deductions with moderate complexity
            puzzle._max_inference_depth = 3
            puzzle._allow_multiple_paths = True
            
        elif level == ComplexityLevel.ADVANCED:
            # Complex deductions with multiple inference paths
            puzzle._max_inference_depth = 5
            puzzle._require_complex_reasoning = True
            
        elif level == ComplexityLevel.EXPERT:
            # Advanced deductions with optimization
            puzzle._require_optimization = True
            puzzle._include_edge_cases = True
            puzzle._performance_constraints = True
    
    def get_complexity_parameters(self, level: ComplexityLevel) -> Dict[str, Any]:
        """Get the adaptation parameters for a specific complexity level."""
        return self.adaptation_strategies.get(level, {}).copy()
    
    def get_supported_puzzle_types(self) -> List[PuzzleType]:
        """Get the list of puzzle types supported by this factory."""
        return list(PuzzleType)
    
    def can_adapt_puzzle(self, puzzle: BasePuzzle) -> bool:
        """Check if a puzzle can be adapted by this factory."""
        puzzle_type = self._get_puzzle_type(puzzle)
        return puzzle_type in self.get_supported_puzzle_types()
    
    def create_complexity_specific_puzzle(
        self, 
        puzzle_type: PuzzleType, 
        level: ComplexityLevel,
        **kwargs
    ) -> Optional[BasePuzzle]:
        """
        Create a new puzzle specifically designed for a complexity level.
        
        Args:
            puzzle_type: The type of puzzle to create
            level: The target complexity level
            **kwargs: Additional parameters for puzzle creation
            
        Returns:
            New puzzle instance or None if type not supported
        """
        # This would be expanded to create new puzzles from scratch
        # For now, we focus on adapting existing puzzles
        return None
    
    def validate_adaptation(self, puzzle: BasePuzzle, level: ComplexityLevel) -> bool:
        """
        Validate that a puzzle has been properly adapted for a complexity level.
        
        Args:
            puzzle: The adapted puzzle to validate
            level: The target complexity level
            
        Returns:
            True if adaptation is valid
        """
        # Check that the puzzle has the complexity level set
        if puzzle.get_complexity_level() != level:
            return False
        
        # Check that adaptation parameters are present
        if not hasattr(puzzle, '_adaptation_params'):
            return False
        
        # Validate that required parameters are set
        strategy = self.adaptation_strategies.get(level, {})
        for key, expected_value in strategy.items():
            if key not in puzzle._adaptation_params:
                return False
        
        return True
    
    def get_adaptation_summary(self, puzzle: BasePuzzle) -> Dict[str, Any]:
        """
        Get a summary of adaptations applied to a puzzle.
        
        Args:
            puzzle: The adapted puzzle
            
        Returns:
            Dictionary containing adaptation details
        """
        if not hasattr(puzzle, '_adaptation_params'):
            return {"error": "No adaptations found"}
        
        level = puzzle.get_complexity_level()
        return {
            "complexity_level": level.name,
            "puzzle_id": puzzle.puzzle_id,
            "puzzle_type": self._get_puzzle_type(puzzle).value,
            "adaptations": puzzle._adaptation_params.copy(),
            "max_score": puzzle.max_score,
            "is_valid": self.validate_adaptation(puzzle, level)
        }