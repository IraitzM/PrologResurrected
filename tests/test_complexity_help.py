"""
Unit tests for the complexity help system.

Tests the comprehensive help, documentation, and guidance features
for complexity levels.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_help import ComplexityHelpSystem, format_help_for_terminal


class TestComplexityHelpSystem:
    """Test the ComplexityHelpSystem class."""
    
    @pytest.fixture
    def complexity_manager(self):
        """Create a complexity manager for testing."""
        return ComplexityManager()
    
    @pytest.fixture
    def help_system(self, complexity_manager):
        """Create a help system for testing."""
        return ComplexityHelpSystem(complexity_manager)
    
    def test_initialization(self, complexity_manager):
        """Test help system initialization."""
        help_system = ComplexityHelpSystem(complexity_manager)
        assert help_system.complexity_manager is complexity_manager
    
    def test_get_complexity_overview(self, help_system):
        """Test getting the complexity overview."""
        overview = help_system.get_complexity_overview()
        
        # Check that overview contains key information
        assert "COMPLEXITY LEVEL SYSTEM OVERVIEW" in overview
        assert "BEGINNER" in overview
        assert "INTERMEDIATE" in overview
        assert "ADVANCED" in overview
        assert "EXPERT" in overview
        assert "scoring multiplier" in overview.lower()
        assert "hints" in overview.lower()
    
    def test_get_complexity_comparison(self, help_system):
        """Test getting the complexity comparison."""
        comparison = help_system.get_complexity_comparison()
        
        # Check that comparison contains comparison table
        assert "COMPLEXITY LEVEL COMPARISON" in comparison
        assert "FEATURE COMPARISON" in comparison
        assert "Hint Frequency" in comparison
        assert "Explanations" in comparison
        assert "Score Multiplier" in comparison
        
        # Check all levels are included
        assert "BEGINNER" in comparison
        assert "INTERMEDIATE" in comparison
        assert "ADVANCED" in comparison
        assert "EXPERT" in comparison
    
    def test_get_complexity_tips(self, help_system):
        """Test getting complexity tips."""
        tips = help_system.get_complexity_tips()
        
        # Check that tips contain recommendations
        assert "TIPS & RECOMMENDATIONS" in tips
        assert "CHOOSE BEGINNER IF" in tips
        assert "CHOOSE INTERMEDIATE IF" in tips
        assert "CHOOSE ADVANCED IF" in tips
        assert "CHOOSE EXPERT IF" in tips
        assert "GENERAL TIPS" in tips
    
    def test_get_level_specific_help_beginner(self, help_system):
        """Test getting help for beginner level."""
        help_text = help_system.get_level_specific_help(ComplexityLevel.BEGINNER)
        
        assert "BEGINNER LEVEL" in help_text
        assert "WHAT TO EXPECT" in help_text
        assert "BEST PRACTICES" in help_text
        assert "WHEN TO MOVE UP" in help_text
        assert "MAXIMUM GUIDANCE" in help_text
    
    def test_get_level_specific_help_intermediate(self, help_system):
        """Test getting help for intermediate level."""
        help_text = help_system.get_level_specific_help(ComplexityLevel.INTERMEDIATE)
        
        assert "INTERMEDIATE LEVEL" in help_text
        assert "WHAT TO EXPECT" in help_text
        assert "BEST PRACTICES" in help_text
        assert "MODERATE GUIDANCE" in help_text
    
    def test_get_level_specific_help_advanced(self, help_system):
        """Test getting help for advanced level."""
        help_text = help_system.get_level_specific_help(ComplexityLevel.ADVANCED)
        
        assert "ADVANCED LEVEL" in help_text
        assert "WHAT TO EXPECT" in help_text
        assert "BEST PRACTICES" in help_text
        assert "MINIMAL GUIDANCE" in help_text
        assert "OPTIMIZATION" in help_text
    
    def test_get_level_specific_help_expert(self, help_system):
        """Test getting help for expert level."""
        help_text = help_system.get_level_specific_help(ComplexityLevel.EXPERT)
        
        assert "EXPERT LEVEL" in help_text
        assert "WHAT TO EXPECT" in help_text
        assert "BEST PRACTICES" in help_text
        assert "NO GUIDANCE" in help_text
        assert "NO HINTS" in help_text
    
    def test_get_contextual_help_puzzle(self, help_system):
        """Test getting contextual help for puzzle context."""
        help_text = help_system.get_contextual_help(ComplexityLevel.BEGINNER, "puzzle")
        
        assert "PUZZLE HELP" in help_text
        assert "BEGINNER" in help_text
        assert "HINTS" in help_text
    
    def test_get_contextual_help_selection(self, help_system):
        """Test getting contextual help for selection context."""
        help_text = help_system.get_contextual_help(ComplexityLevel.INTERMEDIATE, "selection")
        
        assert "COMPLEXITY SELECTION HELP" in help_text
        assert "INTERMEDIATE" in help_text
        assert "CHOOSING A LEVEL" in help_text
    
    def test_get_contextual_help_change(self, help_system):
        """Test getting contextual help for change context."""
        help_text = help_system.get_contextual_help(ComplexityLevel.ADVANCED, "change")
        
        assert "COMPLEXITY CHANGE HELP" in help_text
        assert "ADVANCED" in help_text
        assert "CHANGING LEVELS" in help_text
    
    def test_get_contextual_help_general(self, help_system):
        """Test getting general contextual help."""
        help_text = help_system.get_contextual_help(ComplexityLevel.EXPERT, "general")
        
        assert "COMPLEXITY SYSTEM HELP" in help_text
        assert "EXPERT" in help_text
        assert "COMMANDS" in help_text
    
    def test_get_quick_reference(self, help_system):
        """Test getting quick reference for a level."""
        quick_ref = help_system.get_quick_reference(ComplexityLevel.BEGINNER)
        
        assert "BEGINNER LEVEL" in quick_ref
        assert "QUICK REFERENCE" in quick_ref
        assert "DESCRIPTION" in quick_ref
        assert "FEATURES" in quick_ref
        assert "BEST FOR" in quick_ref
    
    def test_get_quick_reference_all_levels(self, help_system):
        """Test getting quick reference for all levels."""
        for level in ComplexityLevel:
            quick_ref = help_system.get_quick_reference(level)
            
            assert level.name in quick_ref
            assert "QUICK REFERENCE" in quick_ref
            assert "DESCRIPTION" in quick_ref
            assert "FEATURES" in quick_ref
    
    def test_get_faq(self, help_system):
        """Test getting FAQ."""
        faq = help_system.get_faq()
        
        assert "FREQUENTLY ASKED QUESTIONS" in faq
        assert "Q:" in faq
        assert "A:" in faq
        assert "change complexity levels" in faq.lower()
        assert "score" in faq.lower()
    
    def test_format_help_for_terminal(self):
        """Test formatting help text for terminal display."""
        help_text = "Line 1\nLine 2\nLine 3"
        lines = format_help_for_terminal(help_text)
        
        assert isinstance(lines, list)
        assert len(lines) == 3
        assert lines[0] == "Line 1"
        assert lines[1] == "Line 2"
        assert lines[2] == "Line 3"
    
    def test_format_help_for_terminal_empty(self):
        """Test formatting empty help text."""
        help_text = ""
        lines = format_help_for_terminal(help_text)
        
        assert isinstance(lines, list)
        assert len(lines) == 1
        assert lines[0] == ""
    
    def test_contextual_help_includes_level_info(self, help_system):
        """Test that contextual help includes current level information."""
        for level in ComplexityLevel:
            help_text = help_system.get_contextual_help(level, "general")
            assert level.name in help_text
    
    def test_level_specific_help_includes_when_to_move(self, help_system):
        """Test that level-specific help includes guidance on when to change levels."""
        # Beginner should have "when to move up"
        beginner_help = help_system.get_level_specific_help(ComplexityLevel.BEGINNER)
        assert "WHEN TO MOVE UP" in beginner_help
        
        # Intermediate should have both directions
        intermediate_help = help_system.get_level_specific_help(ComplexityLevel.INTERMEDIATE)
        assert "WHEN TO MOVE" in intermediate_help
        
        # Advanced should have both directions
        advanced_help = help_system.get_level_specific_help(ComplexityLevel.ADVANCED)
        assert "WHEN TO MOVE" in advanced_help
        
        # Expert should have "when to move down"
        expert_help = help_system.get_level_specific_help(ComplexityLevel.EXPERT)
        assert "WHEN TO MOVE DOWN" in expert_help
    
    def test_tips_include_all_levels(self, help_system):
        """Test that tips include recommendations for all levels."""
        tips = help_system.get_complexity_tips()
        
        assert "CHOOSE BEGINNER IF" in tips
        assert "CHOOSE INTERMEDIATE IF" in tips
        assert "CHOOSE ADVANCED IF" in tips
        assert "CHOOSE EXPERT IF" in tips
    
    def test_comparison_includes_all_features(self, help_system):
        """Test that comparison includes all important features."""
        comparison = help_system.get_complexity_comparison()
        
        # Check for key features
        assert "Hint Frequency" in comparison
        assert "Explanations" in comparison
        assert "Templates" in comparison
        assert "Examples" in comparison
        assert "Max Variables" in comparison
        assert "Max Predicates" in comparison
        assert "Score Multiplier" in comparison
    
    def test_overview_includes_key_features(self, help_system):
        """Test that overview includes key features of the system."""
        overview = help_system.get_complexity_overview()
        
        assert "Change complexity level anytime" in overview
        assert "progress and score are always preserved" in overview.lower()
        assert "achievements separately" in overview.lower()
        assert "scoring multipliers" in overview.lower()
    
    def test_faq_covers_common_questions(self, help_system):
        """Test that FAQ covers common questions."""
        faq = help_system.get_faq()
        
        # Check for common questions
        assert "change complexity levels" in faq.lower()
        assert "affect my score" in faq.lower()
        assert "same concepts" in faq.lower()
        assert "which level should i start" in faq.lower()
        assert "too hard" in faq.lower()
        assert "too easy" in faq.lower()


class TestComplexityHelpIntegration:
    """Test integration of help system with complexity manager."""
    
    def test_help_system_uses_manager_configs(self):
        """Test that help system uses complexity manager configurations."""
        manager = ComplexityManager()
        help_system = ComplexityHelpSystem(manager)
        
        # Get quick reference for each level
        for level in ComplexityLevel:
            quick_ref = help_system.get_quick_reference(level)
            config = manager.get_config(level)
            
            # Check that quick reference includes config information (case-insensitive)
            assert config.name.upper() in quick_ref.upper()
            assert str(config.scoring_multiplier) in quick_ref
    
    def test_contextual_help_reflects_current_level(self):
        """Test that contextual help reflects the current complexity level."""
        manager = ComplexityManager()
        help_system = ComplexityHelpSystem(manager)
        
        # Test for each level
        for level in ComplexityLevel:
            manager.set_complexity_level(level)
            help_text = help_system.get_contextual_help(level, "general")
            
            # Should include current level name
            assert level.name in help_text
    
    def test_help_system_handles_all_levels(self):
        """Test that help system provides help for all complexity levels."""
        manager = ComplexityManager()
        help_system = ComplexityHelpSystem(manager)
        
        for level in ComplexityLevel:
            # Should not raise any exceptions
            overview = help_system.get_complexity_overview()
            comparison = help_system.get_complexity_comparison()
            tips = help_system.get_complexity_tips()
            level_help = help_system.get_level_specific_help(level)
            contextual = help_system.get_contextual_help(level, "general")
            quick_ref = help_system.get_quick_reference(level)
            
            # All should return non-empty strings
            assert overview
            assert comparison
            assert tips
            assert level_help
            assert contextual
            assert quick_ref
