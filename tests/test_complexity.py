"""
Unit tests for the complexity management infrastructure.

Tests cover ComplexityLevel enum, ComplexityConfig dataclass, and ComplexityManager class
to ensure proper functionality of the adaptive complexity system.
"""

import pytest
from prologresurrected.game.complexity import (
    ComplexityLevel,
    ComplexityConfig,
    ComplexityManager,
    HintFrequency,
    ExplanationDepth
)


class TestComplexityLevel:
    """Test cases for the ComplexityLevel enum."""
    
    def test_complexity_level_values(self):
        """Test that complexity levels have correct values."""
        assert ComplexityLevel.BEGINNER.value == 1
        assert ComplexityLevel.INTERMEDIATE.value == 2
        assert ComplexityLevel.ADVANCED.value == 3
        assert ComplexityLevel.EXPERT.value == 4
    
    def test_complexity_level_ordering(self):
        """Test that complexity levels have correct ordering values."""
        assert ComplexityLevel.BEGINNER.value < ComplexityLevel.INTERMEDIATE.value
        assert ComplexityLevel.INTERMEDIATE.value < ComplexityLevel.ADVANCED.value
        assert ComplexityLevel.ADVANCED.value < ComplexityLevel.EXPERT.value


class TestComplexityConfig:
    """Test cases for the ComplexityConfig dataclass."""
    
    def test_complexity_config_creation(self):
        """Test creating a ComplexityConfig instance."""
        config = ComplexityConfig(
            name="Test Level",
            description="Test description",
            hint_frequency=HintFrequency.ON_REQUEST,
            explanation_depth=ExplanationDepth.MODERATE,
            puzzle_parameters={"max_variables": 3},
            ui_indicators={"color": "blue"},
            scoring_multiplier=1.5
        )
        
        assert config.name == "Test Level"
        assert config.description == "Test description"
        assert config.hint_frequency == HintFrequency.ON_REQUEST
        assert config.explanation_depth == ExplanationDepth.MODERATE
        assert config.puzzle_parameters == {"max_variables": 3}
        assert config.ui_indicators == {"color": "blue"}
        assert config.scoring_multiplier == 1.5


class TestComplexityManager:
    """Test cases for the ComplexityManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = ComplexityManager()
    
    def test_initial_state(self):
        """Test that manager initializes with correct default state."""
        assert self.manager.get_current_level() == ComplexityLevel.BEGINNER
        assert len(self.manager.level_configs) == 4
        
        # Verify all levels have configurations
        for level in ComplexityLevel:
            assert level in self.manager.level_configs
    
    def test_set_complexity_level(self):
        """Test setting complexity level."""
        self.manager.set_complexity_level(ComplexityLevel.ADVANCED)
        assert self.manager.get_current_level() == ComplexityLevel.ADVANCED
        
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        assert self.manager.get_current_level() == ComplexityLevel.EXPERT
    
    def test_set_invalid_complexity_level(self):
        """Test that setting invalid complexity level raises error."""
        with pytest.raises(ValueError, match="Invalid complexity level"):
            self.manager.set_complexity_level("invalid")
        
        with pytest.raises(ValueError, match="Invalid complexity level"):
            self.manager.set_complexity_level(5)
    
    def test_get_current_config(self):
        """Test getting current configuration."""
        config = self.manager.get_current_config()
        assert config.name == "Beginner"
        assert config.hint_frequency == HintFrequency.ALWAYS_AVAILABLE
        
        self.manager.set_complexity_level(ComplexityLevel.EXPERT)
        config = self.manager.get_current_config()
        assert config.name == "Expert"
        assert config.hint_frequency == HintFrequency.NONE
    
    def test_get_config_for_specific_level(self):
        """Test getting configuration for specific level."""
        config = self.manager.get_config(ComplexityLevel.INTERMEDIATE)
        assert config.name == "Intermediate"
        assert config.hint_frequency == HintFrequency.ON_REQUEST
        
        # Current level should remain unchanged
        assert self.manager.get_current_level() == ComplexityLevel.BEGINNER
    
    def test_get_config_invalid_level(self):
        """Test that getting config for invalid level raises error."""
        # This shouldn't happen in practice since we use enum, but test defensive programming
        with pytest.raises(ValueError, match="No configuration found for level"):
            # Simulate invalid level by directly accessing with non-existent key
            self.manager.level_configs = {}
            self.manager.get_config(ComplexityLevel.BEGINNER)
    
    def test_get_puzzle_parameters(self):
        """Test getting puzzle parameters."""
        # Test current level (BEGINNER)
        params = self.manager.get_puzzle_parameters()
        assert params["max_variables"] == 2
        assert params["provide_templates"] is True
        
        # Test specific level
        params = self.manager.get_puzzle_parameters(ComplexityLevel.EXPERT)
        assert params["max_variables"] == 8
        assert params["include_edge_cases"] is True
        
        # Verify we get a copy (modifications don't affect original)
        params["new_key"] = "test"
        original_params = self.manager.get_puzzle_parameters()
        assert "new_key" not in original_params
    
    def test_get_hint_frequency(self):
        """Test getting hint frequency."""
        # Test current level
        freq = self.manager.get_hint_frequency()
        assert freq == HintFrequency.ALWAYS_AVAILABLE
        
        # Test specific level
        freq = self.manager.get_hint_frequency(ComplexityLevel.ADVANCED)
        assert freq == HintFrequency.AFTER_ATTEMPTS
    
    def test_get_explanation_depth(self):
        """Test getting explanation depth."""
        # Test current level
        depth = self.manager.get_explanation_depth()
        assert depth == ExplanationDepth.DETAILED
        
        # Test specific level
        depth = self.manager.get_explanation_depth(ComplexityLevel.EXPERT)
        assert depth == ExplanationDepth.MINIMAL
    
    def test_get_scoring_multiplier(self):
        """Test getting scoring multiplier."""
        # Test current level
        multiplier = self.manager.get_scoring_multiplier()
        assert multiplier == 1.0
        
        # Test specific level
        multiplier = self.manager.get_scoring_multiplier(ComplexityLevel.EXPERT)
        assert multiplier == 2.0
    
    def test_get_ui_indicators(self):
        """Test getting UI indicators."""
        # Test current level
        indicators = self.manager.get_ui_indicators()
        assert indicators["color"] == "neon_green"
        assert indicators["icon"] == "🌱"
        
        # Test specific level
        indicators = self.manager.get_ui_indicators(ComplexityLevel.EXPERT)
        assert indicators["color"] == "red"
        assert indicators["icon"] == "💀"
        
        # Verify we get a copy
        indicators["new_key"] = "test"
        original_indicators = self.manager.get_ui_indicators()
        assert "new_key" not in original_indicators
    
    def test_should_show_advanced_concepts(self):
        """Test advanced concepts visibility logic."""
        # Test current level (BEGINNER)
        assert not self.manager.should_show_advanced_concepts()
        
        # Test specific levels
        assert not self.manager.should_show_advanced_concepts(ComplexityLevel.BEGINNER)
        assert not self.manager.should_show_advanced_concepts(ComplexityLevel.INTERMEDIATE)
        assert self.manager.should_show_advanced_concepts(ComplexityLevel.ADVANCED)
        assert self.manager.should_show_advanced_concepts(ComplexityLevel.EXPERT)
    
    def test_get_available_levels(self):
        """Test getting all available levels."""
        levels = self.manager.get_available_levels()
        assert len(levels) == 4
        assert ComplexityLevel.BEGINNER in levels
        assert ComplexityLevel.INTERMEDIATE in levels
        assert ComplexityLevel.ADVANCED in levels
        assert ComplexityLevel.EXPERT in levels
    
    def test_get_level_description(self):
        """Test getting level descriptions."""
        desc = self.manager.get_level_description(ComplexityLevel.BEGINNER)
        assert "Maximum guidance" in desc
        assert "step-by-step" in desc
        
        desc = self.manager.get_level_description(ComplexityLevel.EXPERT)
        assert "No guidance" in desc
        assert "optimization" in desc
    
    def test_get_level_name(self):
        """Test getting level names."""
        assert self.manager.get_level_name(ComplexityLevel.BEGINNER) == "Beginner"
        assert self.manager.get_level_name(ComplexityLevel.INTERMEDIATE) == "Intermediate"
        assert self.manager.get_level_name(ComplexityLevel.ADVANCED) == "Advanced"
        assert self.manager.get_level_name(ComplexityLevel.EXPERT) == "Expert"
    
    def test_level_configurations_completeness(self):
        """Test that all level configurations are complete and valid."""
        for level in ComplexityLevel:
            config = self.manager.get_config(level)
            
            # Verify all required fields are present
            assert config.name
            assert config.description
            assert isinstance(config.hint_frequency, HintFrequency)
            assert isinstance(config.explanation_depth, ExplanationDepth)
            assert isinstance(config.puzzle_parameters, dict)
            assert isinstance(config.ui_indicators, dict)
            assert isinstance(config.scoring_multiplier, (int, float))
            assert config.scoring_multiplier > 0
            
            # Verify UI indicators have required keys
            assert "color" in config.ui_indicators
            assert "icon" in config.ui_indicators
            assert "badge" in config.ui_indicators
    
    def test_complexity_progression_logic(self):
        """Test that complexity increases appropriately across levels."""
        beginner_params = self.manager.get_puzzle_parameters(ComplexityLevel.BEGINNER)
        expert_params = self.manager.get_puzzle_parameters(ComplexityLevel.EXPERT)
        
        # Expert should have higher limits than beginner
        assert expert_params["max_variables"] > beginner_params["max_variables"]
        assert expert_params["max_predicates"] > beginner_params["max_predicates"]
        
        # Expert should have fewer aids than beginner
        assert not expert_params.get("provide_templates", False)
        assert beginner_params.get("provide_templates", False)
        
        # Scoring multipliers should increase with difficulty
        beginner_multiplier = self.manager.get_scoring_multiplier(ComplexityLevel.BEGINNER)
        expert_multiplier = self.manager.get_scoring_multiplier(ComplexityLevel.EXPERT)
        assert expert_multiplier > beginner_multiplier


class TestHintFrequency:
    """Test cases for the HintFrequency enum."""
    
    def test_hint_frequency_values(self):
        """Test that hint frequency enum has correct values."""
        assert HintFrequency.ALWAYS_AVAILABLE.value == "always"
        assert HintFrequency.ON_REQUEST.value == "on_request"
        assert HintFrequency.AFTER_ATTEMPTS.value == "after_attempts"
        assert HintFrequency.MINIMAL.value == "minimal"
        assert HintFrequency.NONE.value == "none"


class TestExplanationDepth:
    """Test cases for the ExplanationDepth enum."""
    
    def test_explanation_depth_values(self):
        """Test that explanation depth enum has correct values."""
        assert ExplanationDepth.DETAILED.value == "detailed"
        assert ExplanationDepth.MODERATE.value == "moderate"
        assert ExplanationDepth.BRIEF.value == "brief"
        assert ExplanationDepth.MINIMAL.value == "minimal"