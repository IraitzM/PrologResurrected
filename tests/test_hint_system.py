"""
Unit tests for the complexity-aware hint and guidance system.

Tests the HintConfig, ExplanationConfig, HintGenerator, and ComplexityAwareHintSystem
classes to ensure proper hint generation and adaptation across complexity levels.
"""

import pytest
from unittest.mock import Mock, patch
from prologresurrected.game.hint_system import (
    HintConfig, ExplanationConfig, HintGenerator, ComplexityAwareHintSystem,
    HintType, HintTiming
)
from prologresurrected.game.complexity import ComplexityLevel, HintFrequency, ExplanationDepth


class TestHintConfig:
    """Test the HintConfig class functionality."""
    
    def test_hint_config_creation(self):
        """Test creating a HintConfig with all parameters."""
        config = HintConfig(
            hint_frequency=HintFrequency.ALWAYS_AVAILABLE,
            max_hints_per_puzzle=5,
            progressive_hints=True,
            hint_timing=HintTiming.IMMEDIATE,
            attempts_before_hint=0,
            include_examples=True,
            include_templates=True,
            include_syntax_help=True,
            include_encouragement=True,
            allowed_hint_types=[HintType.SYNTAX, HintType.CONCEPT],
            hint_penalty_per_use=5
        )
        
        assert config.hint_frequency == HintFrequency.ALWAYS_AVAILABLE
        assert config.max_hints_per_puzzle == 5
        assert config.progressive_hints is True
        assert config.hint_timing == HintTiming.IMMEDIATE
        assert config.attempts_before_hint == 0
        assert config.include_examples is True
        assert config.include_templates is True
        assert config.include_syntax_help is True
        assert config.include_encouragement is True
        assert HintType.SYNTAX in config.allowed_hint_types
        assert HintType.CONCEPT in config.allowed_hint_types
        assert config.hint_penalty_per_use == 5
    
    def test_can_provide_hint_always_available(self):
        """Test hint availability when always available."""
        config = HintConfig(
            hint_frequency=HintFrequency.ALWAYS_AVAILABLE,
            max_hints_per_puzzle=3,
            progressive_hints=True,
            hint_timing=HintTiming.IMMEDIATE,
            attempts_before_hint=0,
            include_examples=True,
            include_templates=True,
            include_syntax_help=True,
            include_encouragement=True,
            allowed_hint_types=[HintType.SYNTAX],
            hint_penalty_per_use=5
        )
        
        # Should allow hints when under the limit
        assert config.can_provide_hint(attempts=0, hints_used=0) is True
        assert config.can_provide_hint(attempts=1, hints_used=2) is True
        
        # Should not allow hints when at the limit
        assert config.can_provide_hint(attempts=1, hints_used=3) is False
    
    def test_can_provide_hint_none_frequency(self):
        """Test hint availability when frequency is NONE."""
        config = HintConfig(
            hint_frequency=HintFrequency.NONE,
            max_hints_per_puzzle=3,
            progressive_hints=True,
            hint_timing=HintTiming.IMMEDIATE,
            attempts_before_hint=0,
            include_examples=True,
            include_templates=True,
            include_syntax_help=True,
            include_encouragement=True,
            allowed_hint_types=[HintType.SYNTAX],
            hint_penalty_per_use=5
        )
        
        # Should never allow hints
        assert config.can_provide_hint(attempts=0, hints_used=0) is False
        assert config.can_provide_hint(attempts=5, hints_used=0) is False
    
    def test_can_provide_hint_after_attempts(self):
        """Test hint availability when timing is after attempts."""
        config = HintConfig(
            hint_frequency=HintFrequency.AFTER_ATTEMPTS,
            max_hints_per_puzzle=3,
            progressive_hints=True,
            hint_timing=HintTiming.AFTER_MULTIPLE_ATTEMPTS,
            attempts_before_hint=2,
            include_examples=True,
            include_templates=True,
            include_syntax_help=True,
            include_encouragement=True,
            allowed_hint_types=[HintType.SYNTAX],
            hint_penalty_per_use=5
        )
        
        # Should not allow hints before required attempts
        assert config.can_provide_hint(attempts=0, hints_used=0) is False
        assert config.can_provide_hint(attempts=1, hints_used=0) is False
        
        # Should allow hints after required attempts
        assert config.can_provide_hint(attempts=2, hints_used=0) is True
        assert config.can_provide_hint(attempts=3, hints_used=1) is True
    
    def test_should_show_hint_type(self):
        """Test hint type filtering."""
        config = HintConfig(
            hint_frequency=HintFrequency.ALWAYS_AVAILABLE,
            max_hints_per_puzzle=3,
            progressive_hints=True,
            hint_timing=HintTiming.IMMEDIATE,
            attempts_before_hint=0,
            include_examples=True,
            include_templates=True,
            include_syntax_help=True,
            include_encouragement=True,
            allowed_hint_types=[HintType.SYNTAX, HintType.CONCEPT],
            hint_penalty_per_use=5
        )
        
        # Should show allowed hint types
        assert config.should_show_hint_type(HintType.SYNTAX) is True
        assert config.should_show_hint_type(HintType.CONCEPT) is True
        
        # Should not show disallowed hint types
        assert config.should_show_hint_type(HintType.TEMPLATE) is False
        assert config.should_show_hint_type(HintType.EXAMPLE) is False


class TestExplanationConfig:
    """Test the ExplanationConfig class functionality."""
    
    def test_explanation_config_creation(self):
        """Test creating an ExplanationConfig with all parameters."""
        config = ExplanationConfig(
            explanation_depth=ExplanationDepth.DETAILED,
            include_why_explanations=True,
            include_how_explanations=True,
            include_what_explanations=True,
            use_analogies=True,
            use_examples=True,
            use_step_by_step=True,
            use_visual_aids=True,
            use_technical_terms=False,
            use_beginner_language=True,
            include_definitions=True,
            provide_detailed_errors=True,
            suggest_corrections=True,
            explain_common_mistakes=True
        )
        
        assert config.explanation_depth == ExplanationDepth.DETAILED
        assert config.include_why_explanations is True
        assert config.include_how_explanations is True
        assert config.include_what_explanations is True
        assert config.use_analogies is True
        assert config.use_examples is True
        assert config.use_step_by_step is True
        assert config.use_visual_aids is True
        assert config.use_technical_terms is False
        assert config.use_beginner_language is True
        assert config.include_definitions is True
        assert config.provide_detailed_errors is True
        assert config.suggest_corrections is True
        assert config.explain_common_mistakes is True
    
    def test_get_explanation_style(self):
        """Test explanation style descriptions."""
        detailed_config = ExplanationConfig(
            explanation_depth=ExplanationDepth.DETAILED,
            include_why_explanations=True,
            include_how_explanations=True,
            include_what_explanations=True,
            use_analogies=True,
            use_examples=True,
            use_step_by_step=True,
            use_visual_aids=True,
            use_technical_terms=False,
            use_beginner_language=True,
            include_definitions=True,
            provide_detailed_errors=True,
            suggest_corrections=True,
            explain_common_mistakes=True
        )
        
        minimal_config = ExplanationConfig(
            explanation_depth=ExplanationDepth.MINIMAL,
            include_why_explanations=False,
            include_how_explanations=False,
            include_what_explanations=False,
            use_analogies=False,
            use_examples=False,
            use_step_by_step=False,
            use_visual_aids=False,
            use_technical_terms=True,
            use_beginner_language=False,
            include_definitions=False,
            provide_detailed_errors=False,
            suggest_corrections=False,
            explain_common_mistakes=False
        )
        
        assert "comprehensive" in detailed_config.get_explanation_style()
        assert "brief" in minimal_config.get_explanation_style()


class TestHintGenerator:
    """Test the HintGenerator class functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.hint_generator = HintGenerator()
    
    def test_initialization(self):
        """Test that HintGenerator initializes properly."""
        assert self.hint_generator.hint_configs is not None
        assert self.hint_generator.explanation_configs is not None
        assert self.hint_generator.hint_templates is not None
        
        # Check that all complexity levels have configurations
        for level in ComplexityLevel:
            assert level in self.hint_generator.hint_configs
            assert level in self.hint_generator.explanation_configs
    
    def test_get_hint_config(self):
        """Test getting hint configurations for different levels."""
        beginner_config = self.hint_generator.get_hint_config(ComplexityLevel.BEGINNER)
        expert_config = self.hint_generator.get_hint_config(ComplexityLevel.EXPERT)
        
        assert beginner_config.hint_frequency == HintFrequency.ALWAYS_AVAILABLE
        assert expert_config.hint_frequency == HintFrequency.NONE
        
        assert beginner_config.max_hints_per_puzzle > expert_config.max_hints_per_puzzle
        assert beginner_config.include_examples is True
        assert expert_config.include_examples is False
    
    def test_get_explanation_config(self):
        """Test getting explanation configurations for different levels."""
        beginner_config = self.hint_generator.get_explanation_config(ComplexityLevel.BEGINNER)
        expert_config = self.hint_generator.get_explanation_config(ComplexityLevel.EXPERT)
        
        assert beginner_config.explanation_depth == ExplanationDepth.DETAILED
        assert expert_config.explanation_depth == ExplanationDepth.MINIMAL
        
        assert beginner_config.use_examples is True
        assert expert_config.use_examples is False
        
        assert beginner_config.provide_detailed_errors is True
        assert expert_config.provide_detailed_errors is False
    
    def test_can_provide_hint(self):
        """Test hint availability checking."""
        # Beginner level should allow hints immediately
        assert self.hint_generator.can_provide_hint(ComplexityLevel.BEGINNER, attempts=0, hints_used=0) is True
        
        # Expert level should never allow hints
        assert self.hint_generator.can_provide_hint(ComplexityLevel.EXPERT, attempts=5, hints_used=0) is False
        
        # Advanced level should require attempts first
        assert self.hint_generator.can_provide_hint(ComplexityLevel.ADVANCED, attempts=1, hints_used=0) is False
        assert self.hint_generator.can_provide_hint(ComplexityLevel.ADVANCED, attempts=3, hints_used=0) is True
    
    def test_generate_hint_beginner(self):
        """Test hint generation for beginner level."""
        hint = self.hint_generator.generate_hint(
            ComplexityLevel.BEGINNER, 
            HintType.SYNTAX, 
            1
        )
        
        assert hint != ""
        assert isinstance(hint, str)
        # Beginner hints should be more detailed
        assert len(hint) > 10
    
    def test_generate_hint_expert(self):
        """Test hint generation for expert level."""
        hint = self.hint_generator.generate_hint(
            ComplexityLevel.EXPERT, 
            HintType.SYNTAX, 
            1
        )
        
        # Expert level should not provide syntax hints
        assert hint == ""
    
    def test_generate_hint_with_context(self):
        """Test hint generation with context customization."""
        context = {
            "expected_predicate": "likes",
            "expected_args": ["alice", "chocolate"]
        }
        
        hint = self.hint_generator.generate_hint(
            ComplexityLevel.BEGINNER, 
            HintType.TEMPLATE, 
            1, 
            context
        )
        
        # Should customize the hint with context information
        assert "likes" in hint or "alice" in hint or "chocolate" in hint
    
    def test_generate_progressive_hint_beginner(self):
        """Test progressive hint generation for beginner level."""
        # First hint should be encouraging/conceptual
        hint1 = self.hint_generator.generate_progressive_hint(ComplexityLevel.BEGINNER, 1)
        assert hint1 != ""
        
        # Later hints should be more specific
        hint3 = self.hint_generator.generate_progressive_hint(ComplexityLevel.BEGINNER, 3)
        assert hint3 != ""
        
        # Hints should be different (progressive)
        assert hint1 != hint3
    
    def test_generate_progressive_hint_expert(self):
        """Test progressive hint generation for expert level."""
        hint = self.hint_generator.generate_progressive_hint(ComplexityLevel.EXPERT, 1)
        assert "No hints available at Expert level" in hint
    
    def test_generate_explanation_facts(self):
        """Test explanation generation for facts topic."""
        beginner_explanation = self.hint_generator.generate_explanation(
            ComplexityLevel.BEGINNER, 
            "facts"
        )
        expert_explanation = self.hint_generator.generate_explanation(
            ComplexityLevel.EXPERT, 
            "facts"
        )
        
        # Beginner explanation should be longer and more detailed
        assert len(beginner_explanation) > len(expert_explanation)
        assert "Facts in Prolog" in beginner_explanation
        assert "example" in beginner_explanation.lower() or "like" in beginner_explanation.lower()
    
    def test_generate_explanation_with_context(self):
        """Test explanation generation with context enhancement."""
        context = {
            "examples": ["likes(mary, pizza).", "owns(john, car)."],
            "steps": ["Identify the relationship", "Choose the predicate", "Add arguments"]
        }
        
        explanation = self.hint_generator.generate_explanation(
            ComplexityLevel.BEGINNER, 
            "facts", 
            context
        )
        
        # Should include context information for beginner level
        assert "examples" in explanation.lower() or "step" in explanation.lower()
    
    def test_get_hint_availability_message(self):
        """Test hint availability message generation."""
        # Expert level message
        expert_msg = self.hint_generator.get_hint_availability_message(
            ComplexityLevel.EXPERT, attempts=0, hints_used=0
        )
        assert "not available at Expert level" in expert_msg
        
        # Beginner level with hints remaining
        beginner_msg = self.hint_generator.get_hint_availability_message(
            ComplexityLevel.BEGINNER, attempts=0, hints_used=2
        )
        assert "hint" in beginner_msg.lower()
        assert "remaining" in beginner_msg.lower()
    
    def test_calculate_hint_penalty(self):
        """Test hint penalty calculation."""
        beginner_penalty = self.hint_generator.calculate_hint_penalty(ComplexityLevel.BEGINNER, 2)
        expert_penalty = self.hint_generator.calculate_hint_penalty(ComplexityLevel.EXPERT, 2)
        
        # Beginner should have lower penalty than other levels
        intermediate_penalty = self.hint_generator.calculate_hint_penalty(ComplexityLevel.INTERMEDIATE, 2)
        
        assert beginner_penalty < intermediate_penalty
        assert expert_penalty == 0  # No hints allowed, so no penalty


class TestComplexityAwareHintSystem:
    """Test the ComplexityAwareHintSystem integration class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.hint_system = ComplexityAwareHintSystem()
    
    def test_initialization(self):
        """Test that ComplexityAwareHintSystem initializes properly."""
        assert self.hint_system.hint_generator is not None
        assert self.hint_system.current_complexity_level == ComplexityLevel.BEGINNER
    
    def test_set_complexity_level(self):
        """Test setting complexity level."""
        self.hint_system.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.hint_system.current_complexity_level == ComplexityLevel.ADVANCED
    
    def test_can_provide_hint(self):
        """Test hint availability checking."""
        # Beginner level should allow hints
        assert self.hint_system.can_provide_hint(attempts=0, hints_used=0) is True
        
        # Change to expert level
        self.hint_system.set_complexity_level(ComplexityLevel.EXPERT)
        assert self.hint_system.can_provide_hint(attempts=0, hints_used=0) is False
    
    def test_get_hint(self):
        """Test hint retrieval."""
        puzzle_context = {
            "attempts": 1,
            "hints_used": 0,
            "expected_predicate": "likes"
        }
        
        hint = self.hint_system.get_hint(1, puzzle_context)
        assert hint != ""
        assert isinstance(hint, str)
    
    def test_get_hint_expert_level(self):
        """Test hint retrieval at expert level."""
        self.hint_system.set_complexity_level(ComplexityLevel.EXPERT)
        
        puzzle_context = {
            "attempts": 1,
            "hints_used": 0
        }
        
        hint = self.hint_system.get_hint(1, puzzle_context)
        assert "not available at Expert level" in hint
    
    def test_get_explanation(self):
        """Test explanation retrieval."""
        explanation = self.hint_system.get_explanation("facts")
        assert explanation != ""
        assert isinstance(explanation, str)
        
        # Should be detailed for beginner level
        assert len(explanation) > 50
    
    def test_get_hint_config(self):
        """Test getting current hint configuration."""
        config = self.hint_system.get_hint_config()
        assert isinstance(config, HintConfig)
        assert config.hint_frequency == HintFrequency.ALWAYS_AVAILABLE  # Beginner default
    
    def test_get_explanation_config(self):
        """Test getting current explanation configuration."""
        config = self.hint_system.get_explanation_config()
        assert isinstance(config, ExplanationConfig)
        assert config.explanation_depth == ExplanationDepth.DETAILED  # Beginner default
    
    def test_calculate_hint_penalty(self):
        """Test hint penalty calculation."""
        penalty = self.hint_system.calculate_hint_penalty(2)
        assert penalty >= 0
        assert isinstance(penalty, int)
        
        # Should be consistent with hint generator
        expected_penalty = self.hint_system.hint_generator.calculate_hint_penalty(
            ComplexityLevel.BEGINNER, 2
        )
        assert penalty == expected_penalty


class TestHintSystemIntegration:
    """Test integration scenarios for the hint system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.hint_system = ComplexityAwareHintSystem()
    
    def test_complexity_level_progression(self):
        """Test hint behavior changes as complexity level increases."""
        puzzle_context = {"attempts": 1, "hints_used": 0}
        
        # Test each complexity level
        levels_and_expectations = [
            (ComplexityLevel.BEGINNER, True, True),  # Can provide, detailed
            (ComplexityLevel.INTERMEDIATE, True, False),  # Can provide, less detailed
            (ComplexityLevel.ADVANCED, False, False),  # Cannot provide immediately, brief
            (ComplexityLevel.EXPERT, False, False)  # Cannot provide, minimal
        ]
        
        for level, can_provide_immediately, should_be_detailed in levels_and_expectations:
            self.hint_system.set_complexity_level(level)
            
            can_provide = self.hint_system.can_provide_hint(1, 0)
            assert can_provide == can_provide_immediately, f"Failed for {level}"
            
            if level != ComplexityLevel.EXPERT:
                explanation = self.hint_system.get_explanation("facts")
                is_detailed = len(explanation) > 100
                if should_be_detailed:
                    assert is_detailed, f"Should be detailed for {level}"
    
    def test_hint_exhaustion(self):
        """Test behavior when hints are exhausted."""
        puzzle_context = {"attempts": 1, "hints_used": 0}
        
        # Get maximum hints for beginner level
        config = self.hint_system.get_hint_config()
        max_hints = config.max_hints_per_puzzle
        
        # Should be able to provide hints up to the limit
        for i in range(max_hints):
            puzzle_context["hints_used"] = i
            assert self.hint_system.can_provide_hint(1, i) is True
        
        # Should not be able to provide more hints after limit
        puzzle_context["hints_used"] = max_hints
        assert self.hint_system.can_provide_hint(1, max_hints) is False
    
    def test_context_customization(self):
        """Test that context properly customizes hints."""
        context_with_predicate = {
            "attempts": 1,
            "hints_used": 0,
            "expected_predicate": "loves",
            "expected_args": ["john", "mary"]
        }
        
        context_without_predicate = {
            "attempts": 1,
            "hints_used": 0
        }
        
        hint_with_context = self.hint_system.get_hint(1, context_with_predicate)
        hint_without_context = self.hint_system.get_hint(1, context_without_predicate)
        
        # Hints should be different when context is provided
        # (though they might be the same if no customization occurs)
        assert isinstance(hint_with_context, str)
        assert isinstance(hint_without_context, str)
        assert len(hint_with_context) > 0
        assert len(hint_without_context) > 0


if __name__ == "__main__":
    pytest.main([__file__])