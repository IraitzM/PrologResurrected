"""
Tests for HelloWorldPuzzle complexity adaptation.

Validates that the HelloWorldPuzzle adapts correctly to different complexity levels,
providing appropriate guidance, examples, and challenges for each level.
"""

import pytest
from prologresurrected.game.hello_world_puzzle import HelloWorldPuzzle
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.terminal import Terminal


class MockTerminal:
    """Mock terminal for testing."""
    
    def __init__(self):
        self.outputs = []
        self.cleared = False
    
    def add_output(self, text: str, color: str = "white"):
        """Record output."""
        self.outputs.append((text, color))
    
    def clear_terminal(self):
        """Record terminal clear."""
        self.cleared = True
        self.outputs = []
    
    def get_output_text(self) -> str:
        """Get all output as text."""
        return "\n".join([text for text, _ in self.outputs])


class TestHelloWorldComplexityAdaptation:
    """Test suite for HelloWorldPuzzle complexity adaptation."""
    
    def test_puzzle_initializes_with_beginner_level(self):
        """Test that puzzle initializes with BEGINNER level by default."""
        puzzle = HelloWorldPuzzle()
        assert puzzle.get_complexity_level() == ComplexityLevel.BEGINNER
        assert puzzle._complexity_adapted is True
    
    def test_set_complexity_level_reapplies_adaptations(self):
        """Test that setting complexity level reapplies adaptations."""
        puzzle = HelloWorldPuzzle()
        
        # Change to EXPERT level
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        assert puzzle.get_complexity_level() == ComplexityLevel.EXPERT
        assert puzzle._tutorial_pace == "minimal"
        assert puzzle._hint_frequency == "none"
        assert puzzle._error_detail_level == "minimal"
    
    def test_beginner_level_configuration(self):
        """Test BEGINNER level has appropriate configuration."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        
        assert puzzle._tutorial_pace == "slow"
        assert puzzle._hint_frequency == "always"
        assert puzzle._error_detail_level == "detailed"
        assert puzzle._show_detailed_explanations is True
        assert puzzle._provide_step_by_step is True
        assert puzzle._max_attempts_per_exercise == 5
    
    def test_intermediate_level_configuration(self):
        """Test INTERMEDIATE level has appropriate configuration."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        
        assert puzzle._tutorial_pace == "moderate"
        assert puzzle._hint_frequency == "on_request"
        assert puzzle._error_detail_level == "moderate"
        assert puzzle._show_detailed_explanations is True
    
    def test_advanced_level_configuration(self):
        """Test ADVANCED level has appropriate configuration."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        assert puzzle._tutorial_pace == "fast"
        assert puzzle._hint_frequency == "minimal"
        assert puzzle._error_detail_level == "brief"
        assert puzzle._show_detailed_explanations is False
    
    def test_expert_level_configuration(self):
        """Test EXPERT level has appropriate configuration."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        assert puzzle._tutorial_pace == "minimal"
        assert puzzle._hint_frequency == "none"
        assert puzzle._error_detail_level == "minimal"
        assert puzzle._show_detailed_explanations is False
        assert puzzle._provide_step_by_step is False
    
    def test_max_attempts_varies_by_complexity(self):
        """Test that max attempts varies by complexity level."""
        puzzle = HelloWorldPuzzle()
        
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert puzzle._get_max_attempts_for_exercise() == 5
        
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert puzzle._get_max_attempts_for_exercise() == 4
        
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        assert puzzle._get_max_attempts_for_exercise() == 3
        
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert puzzle._get_max_attempts_for_exercise() == 2
    
    def test_component_exercise_shown_for_beginner_intermediate(self):
        """Test component identification exercise shown for BEGINNER and INTERMEDIATE."""
        puzzle = HelloWorldPuzzle()
        
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert puzzle._should_show_component_exercise() is True
        
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert puzzle._should_show_component_exercise() is True
        
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        assert puzzle._should_show_component_exercise() is False
        
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert puzzle._should_show_component_exercise() is False
    
    def test_detailed_syntax_breakdown_for_beginner_intermediate(self):
        """Test detailed syntax breakdown shown for BEGINNER and INTERMEDIATE."""
        puzzle = HelloWorldPuzzle()
        
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert puzzle._should_show_detailed_syntax_breakdown() is True
        
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert puzzle._should_show_detailed_syntax_breakdown() is True
        
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        assert puzzle._should_show_detailed_syntax_breakdown() is False
        
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert puzzle._should_show_detailed_syntax_breakdown() is False
    
    def test_hint_detail_level_varies_by_complexity(self):
        """Test hint detail level varies by complexity."""
        puzzle = HelloWorldPuzzle()
        
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        assert puzzle._get_hint_detail_level() == "detailed"
        
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        assert puzzle._get_hint_detail_level() == "moderate"
        
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        assert puzzle._get_hint_detail_level() == "brief"
        
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        assert puzzle._get_hint_detail_level() == "minimal"
    
    def test_introduction_step_adapts_to_beginner(self):
        """Test introduction step shows full content for BEGINNER."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        terminal = MockTerminal()
        
        result = puzzle.step_introduction(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for beginner-specific content
        assert "Welcome to Prolog Programming" in output
        assert "Your Journey into Logic Programming Begins" in output
        assert "CYBERDYNE SYSTEMS" in output
        assert "THE THREE PILLARS OF PROLOG" in output
        assert "READY TO BEGIN?" in output
        assert "future logic programmer" in output
    
    def test_introduction_step_adapts_to_expert(self):
        """Test introduction step shows minimal content for EXPERT."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        terminal = MockTerminal()
        
        result = puzzle.step_introduction(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for expert-specific content
        assert "Prolog Programming Challenge" in output
        assert "Expert-Level Prolog" in output
        
        # Check that beginner-specific content is NOT present
        assert "CYBERDYNE SYSTEMS" not in output
        assert "THE THREE PILLARS OF PROLOG" not in output
        assert "READY TO BEGIN?" not in output
        assert "future logic programmer" not in output
    
    def test_introduction_step_adapts_to_intermediate(self):
        """Test introduction step shows moderate content for INTERMEDIATE."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.INTERMEDIATE)
        terminal = MockTerminal()
        
        result = puzzle.step_introduction(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for intermediate-specific content
        assert "Welcome to Prolog Programming" in output
        assert "CYBERDYNE SYSTEMS" in output
        assert "THE THREE PILLARS OF PROLOG" in output
        
        # Check for simplified prompts
        assert "Press ENTER to start the tutorial" in output
    
    def test_introduction_step_adapts_to_advanced(self):
        """Test introduction step shows brief content for ADVANCED."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        terminal = MockTerminal()
        
        result = puzzle.step_introduction(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for advanced-specific content
        assert "Advanced Logic Programming" in output
        
        # Check that detailed beginner content is reduced
        assert "CYBERDYNE SYSTEMS" not in output
        assert "Core Prolog Elements" in output  # Brief version
    
    def test_completion_step_adapts_to_beginner(self):
        """Test completion step shows full celebration for BEGINNER."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        terminal = MockTerminal()
        
        result = puzzle.step_completion(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for beginner-specific content (check for key phrases that appear in the output)
        # The output includes ASCII art and celebration messages
        assert "COMPLETE" in output or "SUCCESS" in output
        assert "Welcome to the world of logic programming!" in output
        # Check that detailed celebration content is present (not minimal)
        assert len(output) > 1000  # Beginner has more verbose output
    
    def test_completion_step_adapts_to_expert(self):
        """Test completion step shows minimal content for EXPERT."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        terminal = MockTerminal()
        
        result = puzzle.step_completion(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for expert-specific content
        assert "Complete" in output
        assert "Fundamentals Reviewed" in output
        
        # Check that beginner-specific content is NOT present
        assert "Congratulations, Logic Programmer!" not in output
        assert "MISSION ACCOMPLISHED" not in output
        assert "Welcome to the world of logic programming!" not in output
    
    def test_variables_step_adapts_to_beginner(self):
        """Test variables step shows full content for BEGINNER."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        terminal = MockTerminal()
        
        result = puzzle.step_variables_introduction(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for beginner-specific content (check for key phrases)
        assert "VARIABLES" in output.upper()  # Check case-insensitive
        assert "VARIABLE SYNTAX RULES" in output or "VARIABLE RULES" in output
        assert "VARIABLE QUERY EXAMPLES" in output or "VARIABLE EXAMPLES" in output
        assert "mastered" in output.lower() or "MASTERED" in output
        # Check that detailed content is present (not minimal)
        assert len(output) > 1000  # Beginner has more verbose output
    
    def test_variables_step_adapts_to_expert(self):
        """Test variables step shows minimal content for EXPERT."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        terminal = MockTerminal()
        
        result = puzzle.step_variables_introduction(terminal)
        
        assert result is True
        output = terminal.get_output_text()
        
        # Check for expert-specific content
        assert "Variables" in output
        assert "Pattern Matching" in output
        
        # Check that beginner-specific content is NOT present
        assert "Variables: The Power of 'What If?'" not in output
        assert "VARIABLE SYNTAX RULES" not in output
        assert "VARIABLE QUERY EXAMPLES" not in output
    
    def test_content_adaptation_condenses_for_advanced(self):
        """Test that content adaptation condenses explanations for ADVANCED."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.ADVANCED)
        
        # Test with long content
        long_content = [f"Line {i}" for i in range(10)]
        adapted = puzzle._get_complexity_adapted_content(long_content, "explanation")
        
        # Should be condensed
        assert len(adapted) < len(long_content)
        assert "..." in adapted
    
    def test_content_adaptation_minimal_for_expert(self):
        """Test that content adaptation is minimal for EXPERT."""
        puzzle = HelloWorldPuzzle()
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        
        # Test with long content
        long_content = [f"Line {i}" for i in range(10)]
        adapted = puzzle._get_complexity_adapted_content(long_content, "explanation")
        
        # Should be very brief
        assert len(adapted) <= 3
    
    def test_complexity_parameters_inherited_from_base(self):
        """Test that complexity parameters are inherited from BasePuzzle."""
        puzzle = HelloWorldPuzzle()
        
        puzzle.set_complexity_level(ComplexityLevel.BEGINNER)
        params = puzzle.get_complexity_parameters()
        
        assert params["provide_templates"] is True
        assert params["show_examples"] is True
        assert params["max_variables"] == 2
        
        puzzle.set_complexity_level(ComplexityLevel.EXPERT)
        params = puzzle.get_complexity_parameters()
        
        assert params["provide_templates"] is False
        assert params.get("require_optimization", False) is True
        assert params["max_variables"] == 8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
