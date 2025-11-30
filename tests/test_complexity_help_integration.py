"""
Integration tests for complexity help system with game state.

Tests that the help system properly integrates with the main game
and provides correct information based on game state.
"""

import pytest
from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_help import ComplexityHelpSystem


class TestComplexityHelpGameIntegration:
    """Test integration of help system with game mechanics."""
    
    @pytest.fixture
    def manager(self):
        """Create a complexity manager."""
        return ComplexityManager()
    
    @pytest.fixture
    def help_system(self, manager):
        """Create a help system."""
        return ComplexityHelpSystem(manager)
    
    def test_help_reflects_current_level(self, manager, help_system):
        """Test that help reflects the current complexity level."""
        # Set to beginner
        manager.set_complexity_level(ComplexityLevel.BEGINNER)
        contextual = help_system.get_contextual_help(ComplexityLevel.BEGINNER, "general")
        assert "BEGINNER" in contextual
        
        # Set to expert
        manager.set_complexity_level(ComplexityLevel.EXPERT)
        contextual = help_system.get_contextual_help(ComplexityLevel.EXPERT, "general")
        assert "EXPERT" in contextual
    
    def test_help_provides_accurate_config_info(self, manager, help_system):
        """Test that help provides accurate configuration information."""
        for level in ComplexityLevel:
            config = manager.get_config(level)
            quick_ref = help_system.get_quick_reference(level)
            
            # Check that quick reference includes accurate config info
            assert str(config.scoring_multiplier) in quick_ref
            assert config.hint_frequency.value in quick_ref
            assert config.explanation_depth.value in quick_ref
    
    def test_contextual_help_for_all_game_contexts(self, help_system):
        """Test that contextual help works for all game contexts."""
        contexts = ["puzzle", "selection", "change", "general"]
        
        for level in ComplexityLevel:
            for context in contexts:
                help_text = help_system.get_contextual_help(level, context)
                
                # Should return non-empty help text
                assert help_text
                assert len(help_text) > 0
                
                # Should include level name
                assert level.name in help_text
    
    def test_help_system_commands_coverage(self, help_system):
        """Test that help system covers all expected commands."""
        # Overview
        overview = help_system.get_complexity_overview()
        assert "complexity compare" in overview
        assert "complexity tips" in overview
        
        # Tips
        tips = help_system.get_complexity_tips()
        assert "complexity help" in tips.lower()
        
        # FAQ
        faq = help_system.get_faq()
        assert "complexity help" in faq.lower()
    
    def test_level_specific_help_progression(self, help_system):
        """Test that level-specific help shows appropriate progression guidance."""
        # Beginner should mention moving up
        beginner = help_system.get_level_specific_help(ComplexityLevel.BEGINNER)
        assert "MOVE UP" in beginner or "INTERMEDIATE" in beginner
        
        # Intermediate should mention both directions
        intermediate = help_system.get_level_specific_help(ComplexityLevel.INTERMEDIATE)
        assert "MOVE" in intermediate
        
        # Expert should mention moving down
        expert = help_system.get_level_specific_help(ComplexityLevel.EXPERT)
        assert "MOVE DOWN" in expert or "ADVANCED" in expert
    
    def test_help_system_educational_content(self, help_system):
        """Test that help system provides educational content."""
        overview = help_system.get_complexity_overview()
        
        # Should explain key concepts
        assert "hints" in overview.lower()
        assert "guidance" in overview.lower()
        assert "scoring" in overview.lower()
        
        # Should mention all levels
        for level in ComplexityLevel:
            assert level.name in overview
    
    def test_comparison_shows_progression(self, help_system):
        """Test that comparison shows clear progression across levels."""
        comparison = help_system.get_complexity_comparison()
        
        # Should show progression in key metrics
        assert "BEGINNER" in comparison
        assert "INTERMEDIATE" in comparison
        assert "ADVANCED" in comparison
        assert "EXPERT" in comparison
        
        # Should show different values for different levels
        assert "1.0x" in comparison  # Beginner multiplier
        assert "2.0x" in comparison  # Expert multiplier
    
    def test_tips_provide_actionable_guidance(self, help_system):
        """Test that tips provide actionable guidance."""
        tips = help_system.get_complexity_tips()
        
        # Should have clear recommendations
        assert "CHOOSE BEGINNER IF" in tips
        assert "CHOOSE INTERMEDIATE IF" in tips
        assert "CHOOSE ADVANCED IF" in tips
        assert "CHOOSE EXPERT IF" in tips
        
        # Should have general tips
        assert "GENERAL TIPS" in tips
    
    def test_faq_answers_common_questions(self, help_system):
        """Test that FAQ answers common questions."""
        faq = help_system.get_faq()
        
        # Should have Q&A format
        assert "Q:" in faq
        assert "A:" in faq
        
        # Should cover key topics
        assert "change" in faq.lower()
        assert "score" in faq.lower()
        assert "level" in faq.lower()
    
    def test_quick_reference_completeness(self, help_system):
        """Test that quick reference includes all essential information."""
        for level in ComplexityLevel:
            quick_ref = help_system.get_quick_reference(level)
            
            # Should include key sections
            assert "DESCRIPTION" in quick_ref
            assert "FEATURES" in quick_ref
            assert "BEST FOR" in quick_ref
            
            # Should include level name
            assert level.name in quick_ref


class TestComplexityHelpUserExperience:
    """Test user experience aspects of the help system."""
    
    @pytest.fixture
    def help_system(self):
        """Create a help system."""
        manager = ComplexityManager()
        return ComplexityHelpSystem(manager)
    
    def test_help_text_is_readable(self, help_system):
        """Test that help text is well-formatted and readable."""
        overview = help_system.get_complexity_overview()
        
        # Should have clear structure
        assert "═" in overview  # Section dividers
        assert "\n" in overview  # Line breaks
        
        # Should not be too long per line (rough check)
        lines = overview.split("\n")
        for line in lines:
            # Most lines should be reasonable length (allowing for some long lines)
            if len(line) > 100:
                # Should be a divider or special formatting
                assert "═" in line or "─" in line or "│" in line
    
    def test_help_uses_consistent_terminology(self, help_system):
        """Test that help uses consistent terminology."""
        overview = help_system.get_complexity_overview()
        comparison = help_system.get_complexity_comparison()
        tips = help_system.get_complexity_tips()
        
        # All should use same level names
        for level in ComplexityLevel:
            level_name = level.name
            assert level_name in overview
            assert level_name in comparison
            assert level_name in tips
    
    def test_help_provides_examples(self, help_system):
        """Test that help provides concrete examples."""
        tips = help_system.get_complexity_tips()
        
        # Should have example commands
        assert "complexity help" in tips.lower()
        
        # Should have specific guidance
        assert "if" in tips.lower()  # "Choose X if..."
    
    def test_help_is_encouraging(self, help_system):
        """Test that help uses encouraging language."""
        tips = help_system.get_complexity_tips()
        
        # Should have positive language
        assert "can" in tips.lower()
        
        # Should not be discouraging
        assert "can't" not in tips.lower() or "cannot" not in tips.lower()
    
    def test_contextual_help_is_relevant(self, help_system):
        """Test that contextual help is relevant to the context."""
        puzzle_help = help_system.get_contextual_help(ComplexityLevel.BEGINNER, "puzzle")
        selection_help = help_system.get_contextual_help(ComplexityLevel.BEGINNER, "selection")
        
        # Puzzle help should mention puzzle-related things
        assert "PUZZLE" in puzzle_help or "hint" in puzzle_help.lower()
        
        # Selection help should mention selection-related things
        assert "SELECTION" in selection_help or "choosing" in selection_help.lower()
        
        # They should be different
        assert puzzle_help != selection_help


class TestComplexityHelpErrorHandling:
    """Test error handling in the help system."""
    
    def test_help_system_handles_all_levels(self):
        """Test that help system handles all complexity levels without errors."""
        manager = ComplexityManager()
        help_system = ComplexityHelpSystem(manager)
        
        for level in ComplexityLevel:
            # Should not raise any exceptions
            try:
                help_system.get_level_specific_help(level)
                help_system.get_contextual_help(level, "general")
                help_system.get_quick_reference(level)
            except Exception as e:
                pytest.fail(f"Help system failed for level {level.name}: {e}")
    
    def test_help_system_handles_all_contexts(self):
        """Test that help system handles all contexts without errors."""
        manager = ComplexityManager()
        help_system = ComplexityHelpSystem(manager)
        
        contexts = ["puzzle", "selection", "change", "general", "unknown"]
        
        for context in contexts:
            # Should not raise any exceptions
            try:
                help_system.get_contextual_help(ComplexityLevel.BEGINNER, context)
            except Exception as e:
                pytest.fail(f"Help system failed for context {context}: {e}")
