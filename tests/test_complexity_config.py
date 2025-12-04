"""
Unit tests for complexity configuration loading and validation.

Tests the ComplexityConfigLoader class and related functionality for
loading, validating, and managing complexity level configurations.
"""

import pytest
import json
import tempfile
from pathlib import Path
from prologresurrected.game.complexity import ComplexityLevel, HintFrequency, ExplanationDepth
from prologresurrected.game.complexity_config import (
    ComplexityConfigLoader,
    create_default_config_files,
    load_complexity_configs
)


class TestComplexityConfigLoader:
    """Tests for the ComplexityConfigLoader class."""
    
    def test_loader_initialization(self):
        """Test that loader initializes correctly."""
        loader = ComplexityConfigLoader()
        assert loader.config_dir is not None
        assert loader.loaded_configs == {}
        assert loader.validation_errors == []
    
    def test_loader_with_custom_directory(self):
        """Test loader with custom configuration directory."""
        custom_dir = Path("/custom/config/path")
        loader = ComplexityConfigLoader(custom_dir)
        assert loader.config_dir == custom_dir
    
    def test_load_default_configs_when_directory_missing(self):
        """Test that default configs are returned when directory doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            non_existent_dir = Path(tmpdir) / "nonexistent"
            loader = ComplexityConfigLoader(non_existent_dir)
            configs = loader.load_all_configs()
            
            # Should return all four complexity levels
            assert len(configs) == 4
            assert ComplexityLevel.BEGINNER in configs
            assert ComplexityLevel.INTERMEDIATE in configs
            assert ComplexityLevel.ADVANCED in configs
            assert ComplexityLevel.EXPERT in configs
    
    def test_load_valid_config_file(self):
        """Test loading a valid configuration file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            # Create a valid config file
            config_data = {
                "name": "Test Level",
                "description": "Test description",
                "hint_frequency": "always",
                "explanation_depth": "detailed",
                "puzzle_parameters": {
                    "max_variables": 3,
                    "max_predicates": 4,
                    "allow_complex_syntax": False,
                    "provide_templates": True
                },
                "ui_indicators": {
                    "color": "green",
                    "icon": "🎯",
                    "badge": "TEST"
                },
                "scoring_multiplier": 1.5
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            config = loader.load_config(ComplexityLevel.BEGINNER)
            
            assert config.name == "Test Level"
            assert config.description == "Test description"
            assert config.hint_frequency == HintFrequency.ALWAYS_AVAILABLE
            assert config.explanation_depth == ExplanationDepth.DETAILED
            assert config.puzzle_parameters["max_variables"] == 3
            assert config.scoring_multiplier == 1.5
    
    def test_load_config_with_missing_required_field(self):
        """Test that loading fails gracefully with missing required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            # Create an invalid config file (missing description)
            config_data = {
                "name": "Test Level",
                "hint_frequency": "always",
                "explanation_depth": "detailed",
                "puzzle_parameters": {
                    "max_variables": 3,
                    "max_predicates": 4
                },
                "ui_indicators": {
                    "color": "green",
                    "icon": "🎯",
                    "badge": "TEST"
                },
                "scoring_multiplier": 1.5
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            
            # Should raise ValueError
            with pytest.raises(ValueError, match="Missing required fields"):
                loader.load_config(ComplexityLevel.BEGINNER)
    
    def test_load_config_with_invalid_hint_frequency(self):
        """Test that loading fails with invalid hint_frequency value."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            config_data = {
                "name": "Test Level",
                "description": "Test description",
                "hint_frequency": "invalid_value",
                "explanation_depth": "detailed",
                "puzzle_parameters": {
                    "max_variables": 3,
                    "max_predicates": 4
                },
                "ui_indicators": {
                    "color": "green",
                    "icon": "🎯",
                    "badge": "TEST"
                },
                "scoring_multiplier": 1.5
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            
            with pytest.raises(ValueError, match="Invalid hint_frequency"):
                loader.load_config(ComplexityLevel.BEGINNER)
    
    def test_load_config_with_invalid_explanation_depth(self):
        """Test that loading fails with invalid explanation_depth value."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            config_data = {
                "name": "Test Level",
                "description": "Test description",
                "hint_frequency": "always",
                "explanation_depth": "invalid_value",
                "puzzle_parameters": {
                    "max_variables": 3,
                    "max_predicates": 4
                },
                "ui_indicators": {
                    "color": "green",
                    "icon": "🎯",
                    "badge": "TEST"
                },
                "scoring_multiplier": 1.5
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            
            with pytest.raises(ValueError, match="Invalid explanation_depth"):
                loader.load_config(ComplexityLevel.BEGINNER)
    
    def test_load_config_with_missing_puzzle_parameters(self):
        """Test that loading fails with missing puzzle parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            config_data = {
                "name": "Test Level",
                "description": "Test description",
                "hint_frequency": "always",
                "explanation_depth": "detailed",
                "puzzle_parameters": {
                    "max_variables": 3
                    # Missing max_predicates
                },
                "ui_indicators": {
                    "color": "green",
                    "icon": "🎯",
                    "badge": "TEST"
                },
                "scoring_multiplier": 1.5
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            
            with pytest.raises(ValueError, match="Missing required puzzle parameter"):
                loader.load_config(ComplexityLevel.BEGINNER)
    
    def test_load_config_with_invalid_scoring_multiplier(self):
        """Test that loading fails with invalid scoring multiplier."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            config_data = {
                "name": "Test Level",
                "description": "Test description",
                "hint_frequency": "always",
                "explanation_depth": "detailed",
                "puzzle_parameters": {
                    "max_variables": 3,
                    "max_predicates": 4
                },
                "ui_indicators": {
                    "color": "green",
                    "icon": "🎯",
                    "badge": "TEST"
                },
                "scoring_multiplier": -1.0  # Invalid: negative
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            
            with pytest.raises(ValueError, match="scoring_multiplier must be positive"):
                loader.load_config(ComplexityLevel.BEGINNER)
    
    def test_save_config(self):
        """Test saving a configuration to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            loader = ComplexityConfigLoader(config_dir)
            
            # Get a default config
            default_config = loader._get_default_config(ComplexityLevel.BEGINNER)
            
            # Save it
            loader.save_config(ComplexityLevel.BEGINNER, default_config)
            
            # Verify file was created
            config_file = config_dir / "beginner.json"
            assert config_file.exists()
            
            # Load and verify content
            with open(config_file, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data["name"] == default_config.name
            assert saved_data["description"] == default_config.description
            assert saved_data["hint_frequency"] == default_config.hint_frequency.value
    
    def test_save_all_configs(self):
        """Test saving all configurations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            loader = ComplexityConfigLoader(config_dir)
            
            # Get default configs
            configs = loader._get_default_configs()
            
            # Save all
            loader.save_all_configs(configs)
            
            # Verify all files were created
            assert (config_dir / "beginner.json").exists()
            assert (config_dir / "intermediate.json").exists()
            assert (config_dir / "advanced.json").exists()
            assert (config_dir / "expert.json").exists()
    
    def test_load_all_configs_with_valid_files(self):
        """Test loading all configurations from valid files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            loader = ComplexityConfigLoader(config_dir)
            
            # Create default config files
            default_configs = loader._get_default_configs()
            loader.save_all_configs(default_configs)
            
            # Load all configs
            loaded_configs = loader.load_all_configs()
            
            assert len(loaded_configs) == 4
            assert not loader.has_validation_errors()
    
    def test_validation_errors_tracking(self):
        """Test that validation errors are tracked correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            # Create an invalid config file
            config_data = {
                "name": "Test",
                # Missing required fields
            }
            
            config_file = config_dir / "beginner.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            loader = ComplexityConfigLoader(config_dir)
            configs = loader.load_all_configs()
            
            # Should have validation errors
            assert loader.has_validation_errors()
            errors = loader.get_validation_errors()
            assert len(errors) > 0
            
            # Should fall back to defaults
            assert len(configs) == 4


class TestDefaultConfigCreation:
    """Tests for default configuration file creation."""
    
    def test_create_default_config_files(self):
        """Test creating default configuration files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            create_default_config_files(config_dir)
            
            # Verify all files were created
            assert (config_dir / "beginner.json").exists()
            assert (config_dir / "intermediate.json").exists()
            assert (config_dir / "advanced.json").exists()
            assert (config_dir / "expert.json").exists()
            
            # Verify files are valid JSON
            for level in ["beginner", "intermediate", "advanced", "expert"]:
                config_file = config_dir / f"{level}.json"
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    assert "name" in data
                    assert "description" in data
                    assert "hint_frequency" in data


class TestConvenienceFunction:
    """Tests for the convenience function."""
    
    def test_load_complexity_configs(self):
        """Test the convenience function for loading configs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            
            # Create default files
            create_default_config_files(config_dir)
            
            # Load using convenience function
            configs = load_complexity_configs(config_dir)
            
            assert len(configs) == 4
            assert all(level in configs for level in ComplexityLevel)


class TestDefaultConfigurations:
    """Tests for default configuration values."""
    
    def test_beginner_default_config(self):
        """Test that beginner default config has appropriate values."""
        loader = ComplexityConfigLoader()
        config = loader._get_default_config(ComplexityLevel.BEGINNER)
        
        assert config.name == "Beginner"
        assert config.hint_frequency == HintFrequency.ALWAYS_AVAILABLE
        assert config.explanation_depth == ExplanationDepth.DETAILED
        assert config.puzzle_parameters["max_variables"] == 2
        assert config.puzzle_parameters["provide_templates"] is True
        assert config.scoring_multiplier == 1.0
    
    def test_intermediate_default_config(self):
        """Test that intermediate default config has appropriate values."""
        loader = ComplexityConfigLoader()
        config = loader._get_default_config(ComplexityLevel.INTERMEDIATE)
        
        assert config.name == "Intermediate"
        assert config.hint_frequency == HintFrequency.ON_REQUEST
        assert config.explanation_depth == ExplanationDepth.MODERATE
        assert config.puzzle_parameters["max_variables"] == 4
        assert config.scoring_multiplier == 1.2
    
    def test_advanced_default_config(self):
        """Test that advanced default config has appropriate values."""
        loader = ComplexityConfigLoader()
        config = loader._get_default_config(ComplexityLevel.ADVANCED)
        
        assert config.name == "Advanced"
        assert config.hint_frequency == HintFrequency.AFTER_ATTEMPTS
        assert config.explanation_depth == ExplanationDepth.BRIEF
        assert config.puzzle_parameters["max_variables"] == 6
        assert config.scoring_multiplier == 1.5
    
    def test_expert_default_config(self):
        """Test that expert default config has appropriate values."""
        loader = ComplexityConfigLoader()
        config = loader._get_default_config(ComplexityLevel.EXPERT)
        
        assert config.name == "Expert"
        assert config.hint_frequency == HintFrequency.NONE
        assert config.explanation_depth == ExplanationDepth.MINIMAL
        assert config.puzzle_parameters["max_variables"] == 8
        assert config.scoring_multiplier == 2.0
    
    def test_all_default_configs_have_required_fields(self):
        """Test that all default configs have required fields."""
        loader = ComplexityConfigLoader()
        
        for level in ComplexityLevel:
            config = loader._get_default_config(level)
            
            assert config.name is not None
            assert config.description is not None
            assert config.hint_frequency is not None
            assert config.explanation_depth is not None
            assert config.puzzle_parameters is not None
            assert "max_variables" in config.puzzle_parameters
            assert "max_predicates" in config.puzzle_parameters
            assert config.ui_indicators is not None
            assert "color" in config.ui_indicators
            assert "icon" in config.ui_indicators
            assert "badge" in config.ui_indicators
            assert config.scoring_multiplier > 0
