"""
Tests for Memory Stack Puzzle complexity level adaptation.

Validates Requirements: 1.5, 6.1, 6.2, 6.3, 6.4, 6.5
"""

import pytest
from prologresurrected.game.memory_stack_puzzle import (
    MemoryStackPuzzle,
    FailureScenario,
)
from prologresurrected.game.complexity import ComplexityLevel


class TestComplexityLevelAdaptation:
    """Test complexity level adaptation functionality."""
    
    def test_set_complexity_level_updates_puzzle(self):
        """Test that set_complexity_level updates the puzzle's complexity level."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Default should be BEGINNER
        assert puzzle.current_complexity_level == ComplexityLevel.BEGINNER
        
        # Change to INTERMEDIATE
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert puzzle.current_complexity_level == ComplexityLevel.INTERMEDIATE
        
        # Change to EXPERT
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert puzzle.current_complexity_level == ComplexityLevel.EXPERT
    
    def test_set_complexity_level_updates_hint_system(self):
        """Test that set_complexity_level updates the hint system."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        # Change complexity level
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Verify hint system was updated
        assert puzzle.memory_hint_system.current_complexity_level == ComplexityLevel.ADVANCED
    
    def test_beginner_level_provides_templates(self):
        """Test that BEGINNER level provides query templates in initial context."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        context = puzzle.get_initial_context()
        
        # Should have query templates
        assert "query_templates" in context
        assert len(context["query_templates"]) > 0
        
        # Should have template explanations
        assert "template_explanations" in context
        assert "variables" in context["template_explanations"]
        assert "constants" in context["template_explanations"]
    
    def test_intermediate_level_no_templates(self):
        """Test that INTERMEDIATE level does not provide query templates."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        context = puzzle.get_initial_context()
        
        # Should not have query templates
        assert "query_templates" not in context
        assert "template_explanations" not in context
    
    def test_advanced_level_no_templates(self):
        """Test that ADVANCED level does not provide query templates."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        context = puzzle.get_initial_context()
        
        # Should not have query templates
        assert "query_templates" not in context
    
    def test_expert_level_no_templates(self):
        """Test that EXPERT level does not provide query templates."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        context = puzzle.get_initial_context()
        
        # Should not have query templates
        assert "query_templates" not in context
    
    def test_beginner_description_includes_examples(self):
        """Test that BEGINNER level description includes example queries."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        description = puzzle.get_description()
        
        # Should include BEGINNER GUIDE section
        assert "BEGINNER GUIDE" in description
        assert "Example Queries:" in description
        
        # Should include example queries
        assert "?- frame(X, Y, Z, W)." in description
        assert "?- status(FrameId, error)." in description
    
    def test_intermediate_description_no_beginner_guide(self):
        """Test that INTERMEDIATE level description does not include BEGINNER GUIDE."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        description = puzzle.get_description()
        
        # Should not include BEGINNER GUIDE section
        assert "BEGINNER GUIDE" not in description
    
    def test_dynamic_complexity_change_during_puzzle(self):
        """Test that complexity can be changed dynamically during puzzle execution."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Make some queries
        puzzle.validate_solution("?- frame(X, Y, Z, W).")
        puzzle.validate_solution("?- status(1, error).")
        
        assert len(puzzle.queries_made) == 2
        
        # Change complexity level during puzzle
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Verify complexity changed
        assert puzzle.current_complexity_level == ComplexityLevel.EXPERT
        assert puzzle.memory_hint_system.current_complexity_level == ComplexityLevel.EXPERT
        
        # Queries should still be tracked
        assert len(puzzle.queries_made) == 2
    
    def test_complexity_adapted_examples_beginner(self):
        """Test that BEGINNER level provides detailed example queries."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        examples = puzzle.get_complexity_adapted_examples()
        
        # Should have multiple examples with comments
        assert len(examples) > 0
        assert any("#" in example for example in examples)  # Has explanatory comments
    
    def test_complexity_adapted_examples_intermediate(self):
        """Test that INTERMEDIATE level provides basic examples without comments."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        examples = puzzle.get_complexity_adapted_examples()
        
        # Should have some examples but fewer than BEGINNER
        assert len(examples) > 0
        assert len(examples) < 5
    
    def test_complexity_adapted_examples_advanced(self):
        """Test that ADVANCED level provides minimal examples."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        examples = puzzle.get_complexity_adapted_examples()
        
        # Should have very few examples
        assert len(examples) > 0
        assert len(examples) <= 2
    
    def test_complexity_adapted_examples_expert(self):
        """Test that EXPERT level provides no examples."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        examples = puzzle.get_complexity_adapted_examples()
        
        # Should have no examples
        assert len(examples) == 0
    
    def test_hint_system_resets_on_complexity_change(self):
        """Test that hint count resets when complexity level changes."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        # Request some hints
        puzzle.get_hint(1)
        puzzle.get_hint(1)
        
        assert puzzle.memory_hint_system.hint_count == 2
        
        # Change complexity level
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        # Hint count should be reset
        assert puzzle.memory_hint_system.hint_count == 0
    
    def test_template_structure_is_valid(self):
        """Test that query templates have the expected structure."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        templates = puzzle._get_beginner_query_templates()
        
        # Each template should have required fields
        for template in templates:
            assert "pattern" in template
            assert "description" in template
            assert "usage" in template
            
            # Pattern should be a valid query format
            assert template["pattern"].startswith("?-")
            assert template["pattern"].endswith(".")
    
    def test_template_explanations_cover_key_concepts(self):
        """Test that template explanations cover key Prolog concepts."""
        puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
        
        explanations = puzzle._get_template_explanations()
        
        # Should explain key concepts
        assert "variables" in explanations
        assert "constants" in explanations
        assert "compound_queries" in explanations
        assert "tips" in explanations
        
        # Explanations should be non-empty strings
        for key, value in explanations.items():
            assert isinstance(value, str)
            assert len(value) > 0
    
    def test_all_complexity_levels_work(self):
        """Test that puzzle works correctly at all complexity levels."""
        for level in ComplexityLevel:
            puzzle = MemoryStackPuzzle(scenario=FailureScenario.MEMORY_LEAK, seed=42)
            puzzle.set_complexity_level(level)
            
            # Should be able to get description
            description = puzzle.get_description()
            assert len(description) > 0
            
            # Should be able to get initial context
            context = puzzle.get_initial_context()
            assert "facts" in context
            
            # Should be able to execute queries
            result = puzzle.validate_solution("?- frame(X, Y, Z, W).")
            assert result.is_valid
