"""
Integration tests for ComplexityManager with configuration file loading.

Tests that the ComplexityManager correctly integrates with the
ComplexityConfigLoader to load configurations from files.
"""

import pytest
import tempfile
from pathlib import Path
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_config import create_default_config_files


class TestComplexityManagerConfigIntegration:
    """Tests for ComplexityManager integration with config files."""
    
    def test_manager_loads_from_default_location(self):
        """Test that manager loads configs from default location."""
        manager = ComplexityManager()
        
        # Should have all four levels configured
        assert len(manager.level_configs) == 4
        
        # Verify each level has a valid config
        for level in ComplexityLevel:
            config = manager.get_config(level)
            assert config is not None
            assert config.name is not None
            assert config.description is not None
    
    def test_manager_loads_from_custom_directory(self):
        """Test that manager can load configs from custom directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            # Create default config files in temp directory
            create_default_config_files(config_dir)
            
            # Create manager with custom directory
            manager = ComplexityManager(config_dir=str(config_dir))
            
            # Should have loaded all configs
            assert len(manager.level_configs) == 4
            
            # Verify configs are loaded correctly
            beginner_config = manager.get_config(ComplexityLevel.BEGINNER)
            assert beginner_config.name == "Beginner"
    
    def test_manager_falls_back_to_defaults_on_error(self):
        """Test that manager falls back to defaults if config loading fails."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Use a non-existent directory
            non_existent_dir = Path(tmpdir) / "nonexistent"
            
            manager = ComplexityManager(config_dir=str(non_existent_dir))
            
            # Should still have all configs (from built-in defaults)
            assert len(manager.level_configs) == 4
            
            # Verify configs are valid
            for level in ComplexityLevel:
                config = manager.get_config(level)
                assert config is not None
    
    def test_manager_reload_configs(self):
        """Test that manager can reload configurations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            # Create default config files
            create_default_config_files(config_dir)
            
            # Create manager
            manager = ComplexityManager(config_dir=str(config_dir))
            
            # Get initial config
            initial_config = manager.get_config(ComplexityLevel.BEGINNER)
            initial_name = initial_config.name
            
            # Reload configs
            manager.reload_configs()
            
            # Config should still be loaded
            reloaded_config = manager.get_config(ComplexityLevel.BEGINNER)
            assert reloaded_config.name == initial_name
    
    def test_manager_with_actual_config_files(self):
        """Test manager with the actual config files in the project."""
        # This tests with the real config files if they exist
        manager = ComplexityManager()
        
        # Verify all levels are configured
        for level in ComplexityLevel:
            config = manager.get_config(level)
            
            # Check required fields
            assert config.name is not None
            assert config.description is not None
            assert config.hint_frequency is not None
            assert config.explanation_depth is not None
            assert config.puzzle_parameters is not None
            assert config.ui_indicators is not None
            assert config.scoring_multiplier > 0
            
            # Check puzzle parameters
            assert "max_variables" in config.puzzle_parameters
            assert "max_predicates" in config.puzzle_parameters
            assert config.puzzle_parameters["max_variables"] > 0
            assert config.puzzle_parameters["max_predicates"] > 0
            
            # Check UI indicators
            assert "color" in config.ui_indicators
            assert "icon" in config.ui_indicators
            assert "badge" in config.ui_indicators
    
    def test_manager_puzzle_parameters_progression(self):
        """Test that puzzle parameters progress appropriately across levels."""
        manager = ComplexityManager()
        
        beginner = manager.get_puzzle_parameters(ComplexityLevel.BEGINNER)
        intermediate = manager.get_puzzle_parameters(ComplexityLevel.INTERMEDIATE)
        advanced = manager.get_puzzle_parameters(ComplexityLevel.ADVANCED)
        expert = manager.get_puzzle_parameters(ComplexityLevel.EXPERT)
        
        # Variables should increase with complexity
        assert beginner["max_variables"] < intermediate["max_variables"]
        assert intermediate["max_variables"] < advanced["max_variables"]
        assert advanced["max_variables"] <= expert["max_variables"]
        
        # Predicates should increase with complexity
        assert beginner["max_predicates"] < intermediate["max_predicates"]
        assert intermediate["max_predicates"] < advanced["max_predicates"]
        assert advanced["max_predicates"] <= expert["max_predicates"]
    
    def test_manager_scoring_multiplier_progression(self):
        """Test that scoring multipliers progress appropriately."""
        manager = ComplexityManager()
        
        beginner_mult = manager.get_scoring_multiplier(ComplexityLevel.BEGINNER)
        intermediate_mult = manager.get_scoring_multiplier(ComplexityLevel.INTERMEDIATE)
        advanced_mult = manager.get_scoring_multiplier(ComplexityLevel.ADVANCED)
        expert_mult = manager.get_scoring_multiplier(ComplexityLevel.EXPERT)
        
        # Multipliers should increase with complexity
        assert beginner_mult < intermediate_mult
        assert intermediate_mult < advanced_mult
        assert advanced_mult < expert_mult
    
    def test_manager_hint_frequency_progression(self):
        """Test that hint frequency becomes more restrictive with complexity."""
        manager = ComplexityManager()
        
        from prologresurrected.game.complexity import HintFrequency
        
        beginner_hints = manager.get_hint_frequency(ComplexityLevel.BEGINNER)
        expert_hints = manager.get_hint_frequency(ComplexityLevel.EXPERT)
        
        # Beginner should have most available hints
        assert beginner_hints == HintFrequency.ALWAYS_AVAILABLE
        
        # Expert should have no hints
        assert expert_hints == HintFrequency.NONE
    
    def test_manager_explanation_depth_progression(self):
        """Test that explanation depth decreases with complexity."""
        manager = ComplexityManager()
        
        from prologresurrected.game.complexity import ExplanationDepth
        
        beginner_depth = manager.get_explanation_depth(ComplexityLevel.BEGINNER)
        expert_depth = manager.get_explanation_depth(ComplexityLevel.EXPERT)
        
        # Beginner should have detailed explanations
        assert beginner_depth == ExplanationDepth.DETAILED
        
        # Expert should have minimal explanations
        assert expert_depth == ExplanationDepth.MINIMAL


class TestComplexityManagerConfigValidation:
    """Tests for configuration validation in ComplexityManager."""
    
    def test_all_configs_have_consistent_structure(self):
        """Test that all loaded configs have consistent structure."""
        manager = ComplexityManager()
        
        required_puzzle_params = ["max_variables", "max_predicates"]
        required_ui_indicators = ["color", "icon", "badge"]
        
        for level in ComplexityLevel:
            config = manager.get_config(level)
            
            # Check puzzle parameters
            for param in required_puzzle_params:
                assert param in config.puzzle_parameters, \
                    f"{level.name} missing puzzle parameter: {param}"
            
            # Check UI indicators
            for indicator in required_ui_indicators:
                assert indicator in config.ui_indicators, \
                    f"{level.name} missing UI indicator: {indicator}"
    
    def test_configs_have_unique_names(self):
        """Test that each complexity level has a unique name."""
        manager = ComplexityManager()
        
        names = set()
        for level in ComplexityLevel:
            config = manager.get_config(level)
            assert config.name not in names, \
                f"Duplicate config name: {config.name}"
            names.add(config.name)
    
    def test_configs_have_unique_badges(self):
        """Test that each complexity level has a unique badge."""
        manager = ComplexityManager()
        
        badges = set()
        for level in ComplexityLevel:
            config = manager.get_config(level)
            badge = config.ui_indicators["badge"]
            assert badge not in badges, \
                f"Duplicate badge: {badge}"
            badges.add(badge)
