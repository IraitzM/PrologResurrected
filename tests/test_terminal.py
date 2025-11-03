"""
Terminal Interface Tests

Tests for the terminal interface component, including UI interactions,
styling, and terminal operations for the Logic Quest retro interface.
"""

from unittest.mock import Mock, patch
from prologresurrected.game.terminal import Terminal, terminal_component, CYBERDYNE_LOGO, LOGIC_CIRCUIT


class TestTerminal:
    """Test cases for the Terminal state class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.terminal = Terminal()

    def test_terminal_initialization(self):
        """Test that terminal initializes with correct default state."""
        assert self.terminal.output_lines == []
        assert self.terminal.current_input == ""
        assert self.terminal.is_typing is False
        assert self.terminal.cursor_visible is True

    def test_color_constants(self):
        """Test that terminal has correct color scheme constants."""
        expected_colors = {
            "green": "#00ff00",
            "cyan": "#00ffff",
            "yellow": "#ffff00",
            "red": "#ff0000",
            "white": "#ffffff",
            "black": "#000000",
        }

        assert self.terminal.COLORS == expected_colors

    def test_add_output_default_color(self):
        """Test adding output with default green color."""
        test_text = "System online"
        self.terminal.add_output(test_text)

        expected_output = (
            f"<span style='color: {self.terminal.COLORS['green']}'>{test_text}</span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output

    def test_add_output_custom_color(self):
        """Test adding output with custom color."""
        test_text = "Warning: Logic circuits unstable"
        color = "red"
        self.terminal.add_output(test_text, color)

        expected_output = (
            f"<span style='color: {self.terminal.COLORS[color]}'>{test_text}</span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output

    def test_add_output_invalid_color_fallback(self):
        """Test that invalid color falls back to green."""
        test_text = "Fallback test"
        invalid_color = "purple"
        self.terminal.add_output(test_text, invalid_color)

        expected_output = (
            f"<span style='color: {self.terminal.COLORS['green']}'>{test_text}</span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output

    def test_add_multiple_outputs(self):
        """Test adding multiple output lines."""
        lines = [("Line 1", "green"), ("Line 2", "cyan"), ("Line 3", "yellow")]

        for text, color in lines:
            self.terminal.add_output(text, color)

        assert len(self.terminal.output_lines) == 3

        for i, (text, color) in enumerate(lines):
            expected = (
                f"<span style='color: {self.terminal.COLORS[color]}'>{text}</span>"
            )
            assert self.terminal.output_lines[i] == expected

    def test_clear_terminal(self):
        """Test clearing terminal output."""
        # Add some output first
        self.terminal.add_output("Test line 1")
        self.terminal.add_output("Test line 2")
        assert len(self.terminal.output_lines) == 2

        # Clear and verify
        self.terminal.clear_terminal()
        assert self.terminal.output_lines == []

    def test_handle_input(self):
        """Test handling user input."""
        test_input = "likes(alice, chocolate)."

        self.terminal.handle_input(test_input)

        # Should add input to output with cyan color and reset current_input
        expected_output = (
            f"<span style='color: {self.terminal.COLORS['cyan']}'>> {test_input}</span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output
        assert self.terminal.current_input == ""

    def test_typewriter_effect(self):
        """Test typewriter effect adds text to output."""
        test_text = "Initializing LOGIC-1 system..."

        self.terminal.typewriter_effect(test_text)

        expected_output = (
            f"<span style='color: {self.terminal.COLORS['green']}'>{test_text}</span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output

    def test_typewriter_effect_with_delay(self):
        """Test typewriter effect with custom delay parameter."""
        test_text = "Loading neural pathways..."
        custom_delay = 0.1

        self.terminal.typewriter_effect(test_text, custom_delay)

        # Should still add to output (delay would be handled by JS in real implementation)
        expected_output = (
            f"<span style='color: {self.terminal.COLORS['green']}'>{test_text}</span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output

    def test_display_ascii_art(self):
        """Test displaying ASCII art."""
        test_art = "  ╔══════╗\n  ║ TEST ║\n  ╚══════╝"

        self.terminal.display_ascii_art(test_art)

        # Should add each line separately with cyan color
        lines = test_art.split("\n")
        assert len(self.terminal.output_lines) == len(lines)

        for i, line in enumerate(lines):
            expected = (
                f"<span style='color: {self.terminal.COLORS['cyan']}'>{line}</span>"
            )
            assert self.terminal.output_lines[i] == expected

    def test_show_prompt_default(self):
        """Test showing default prompt."""
        self.terminal.show_prompt()

        expected_output = (
            f"<span style='color: {self.terminal.COLORS['yellow']}'>LOGIC-1 > </span>"
        )
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output

    def test_show_prompt_custom(self):
        """Test showing custom prompt."""
        custom_prompt = "CYBERDYNE > "
        self.terminal.show_prompt(custom_prompt)

        expected_output = f"<span style='color: {self.terminal.COLORS['yellow']}'>{custom_prompt}</span>"
        assert len(self.terminal.output_lines) == 1
        assert self.terminal.output_lines[0] == expected_output


class TestTerminalComponent:
    """Test cases for the terminal component function."""

    @patch("game.terminal.rx")
    def test_terminal_component_structure(self, mock_rx):
        """Test that terminal component has correct structure."""
        # Mock the rx components
        mock_rx.vstack.return_value = Mock()
        mock_rx.hstack.return_value = Mock()
        mock_rx.box.return_value = Mock()
        mock_rx.text.return_value = Mock()
        mock_rx.spacer.return_value = Mock()
        mock_rx.foreach.return_value = Mock()
        mock_rx.input.return_value = Mock()

        # Call the function
        terminal_component()

        # Verify that rx.vstack was called (main container)
        mock_rx.vstack.assert_called()

        # Verify that rx.hstack was called (for header and input areas)
        assert mock_rx.hstack.call_count >= 2

        # Verify that rx.box was called (for output area)
        mock_rx.box.assert_called()

        # Verify that rx.input was called (for user input)
        mock_rx.input.assert_called()

    @patch("game.terminal.rx")
    def test_terminal_component_styling(self, mock_rx):
        """Test that terminal component applies correct cyberpunk styling."""
        mock_rx.vstack.return_value = Mock()
        mock_rx.hstack.return_value = Mock()
        mock_rx.box.return_value = Mock()
        mock_rx.text.return_value = Mock()
        mock_rx.spacer.return_value = Mock()
        mock_rx.foreach.return_value = Mock()
        mock_rx.input.return_value = Mock()

        terminal_component()

        # Check that styling parameters are used
        # This verifies that the component applies retro terminal styling
        calls = mock_rx.hstack.call_args_list + mock_rx.box.call_args_list

        # Look for styling parameters in the calls
        styling_found = False
        for call in calls:
            if call.kwargs:
                if any(
                    key in call.kwargs
                    for key in ["background", "border", "color", "font_family"]
                ):
                    styling_found = True
                    break

        assert styling_found, "Terminal component should apply cyberpunk styling"


class TestASCIIArt:
    """Test cases for ASCII art constants."""

    def test_cyberdyne_logo_exists(self):
        """Test that Cyberdyne logo ASCII art is defined."""
        assert CYBERDYNE_LOGO is not None
        assert isinstance(CYBERDYNE_LOGO, str)
        assert len(CYBERDYNE_LOGO) > 0
        assert "SYSTEMS" in CYBERDYNE_LOGO

    def test_cyberdyne_logo_structure(self):
        """Test that Cyberdyne logo has proper ASCII art structure."""
        lines = CYBERDYNE_LOGO.strip().split("\n")

        # Should have multiple lines for ASCII art
        assert len(lines) > 5

        # Should contain box drawing characters or similar ASCII art elements
        art_chars = ["█", "╗", "╔", "╝", "╚", "║", "═"]
        has_art_chars = any(char in CYBERDYNE_LOGO for char in art_chars)
        assert has_art_chars, "Logo should contain ASCII art characters"

    def test_logic_circuit_exists(self):
        """Test that logic circuit ASCII art is defined."""
        assert LOGIC_CIRCUIT is not None
        assert isinstance(LOGIC_CIRCUIT, str)
        assert len(LOGIC_CIRCUIT) > 0
        assert "LOGIC CIRCUIT" in LOGIC_CIRCUIT

    def test_logic_circuit_structure(self):
        """Test that logic circuit has proper ASCII art structure."""
        lines = LOGIC_CIRCUIT.strip().split("\n")

        # Should have multiple lines for the circuit diagram
        assert len(lines) > 5

        # Should contain circuit-related terms
        circuit_terms = ["AND", "OR", "NOT", "ERROR", "LOGIC"]
        has_circuit_terms = any(term in LOGIC_CIRCUIT for term in circuit_terms)
        assert has_circuit_terms, "Circuit should contain logic gate terms"

        # Should contain box drawing characters for the circuit
        box_chars = ["┌", "┐", "└", "┘", "─", "│"]
        has_box_chars = any(char in LOGIC_CIRCUIT for char in box_chars)
        assert has_box_chars, "Circuit should contain box drawing characters"


class TestTerminalIntegration:
    """Integration tests for terminal functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.terminal = Terminal()

    def test_cyberpunk_session_simulation(self):
        """Test a simulated cyberpunk terminal session."""
        # Simulate system startup
        self.terminal.display_ascii_art(CYBERDYNE_LOGO)
        self.terminal.add_output("SYSTEM INITIALIZATION COMPLETE", "green")
        self.terminal.add_output("LOGIC-1 NEURAL INTERFACE ONLINE", "cyan")

        # Simulate user interaction
        self.terminal.show_prompt()
        self.terminal.handle_input("status")
        self.terminal.add_output("SYSTEM STATUS: CRITICAL ERROR DETECTED", "red")

        # Verify the session flow
        assert len(self.terminal.output_lines) > 10  # Logo + messages + prompt + input

        # Check that different colors are used
        output_text = " ".join(self.terminal.output_lines)
        assert "#00ff00" in output_text  # green
        assert "#00ffff" in output_text  # cyan
        assert "#ff0000" in output_text  # red
        assert "#ffff00" in output_text  # yellow (prompt)

    def test_error_handling_display(self):
        """Test displaying error messages with appropriate styling."""
        error_messages = [
            "CRITICAL: Logic pathways corrupted",
            "WARNING: Memory bank Alpha unstable",
            "ERROR: Inference engine offline",
        ]

        for msg in error_messages:
            self.terminal.add_output(msg, "red")

        assert len(self.terminal.output_lines) == len(error_messages)

        # All should be red colored
        for line in self.terminal.output_lines:
            assert f"color: {self.terminal.COLORS['red']}" in line

    def test_prolog_interaction_flow(self):
        """Test a typical Prolog learning interaction."""
        # Display tutorial introduction
        self.terminal.add_output("Welcome to Prolog Programming", "cyan")
        self.terminal.add_output("Let's create your first fact:", "green")

        # Show prompt and handle user input
        self.terminal.show_prompt()
        user_fact = "likes(alice, chocolate)."
        self.terminal.handle_input(user_fact)

        # Provide feedback
        self.terminal.add_output("✅ Excellent! Valid Prolog fact created.", "green")

        # Verify the interaction
        assert len(self.terminal.output_lines) == 5

        # Check that user input is properly formatted
        input_line = self.terminal.output_lines[3]  # After intro, prompt, then input
        assert f"> {user_fact}" in input_line
        assert f"color: {self.terminal.COLORS['cyan']}" in input_line

    def test_terminal_state_persistence(self):
        """Test that terminal state persists across operations."""
        # Add initial content
        self.terminal.add_output("Initial message", "green")
        initial_count = len(self.terminal.output_lines)

        # Perform various operations
        self.terminal.show_prompt()
        self.terminal.handle_input("test command")
        self.terminal.typewriter_effect("Processing...")

        # Verify state is maintained and accumulated
        assert len(self.terminal.output_lines) > initial_count

        # Original message should still be there
        assert "Initial message" in self.terminal.output_lines[0]

        # New content should be added
        assert any("test command" in line for line in self.terminal.output_lines)
        assert any("Processing..." in line for line in self.terminal.output_lines)


class TestTerminalAccessibility:
    """Test accessibility features of the terminal interface."""

    def setup_method(self):
        """Set up test fixtures."""
        self.terminal = Terminal()

    def test_color_contrast(self):
        """Test that terminal uses high contrast colors for accessibility."""
        # Cyberpunk colors should provide good contrast against black background
        colors = self.terminal.COLORS

        # All neon colors should be bright (high values)
        bright_colors = ["green", "cyan", "yellow", "red", "white"]
        for color_name in bright_colors:
            color_value = colors[color_name]
            # Neon colors should be at maximum brightness (#00ff00, #ffff00, etc.)
            assert "ff" in color_value.lower(), (
                f"{color_name} should be bright for accessibility"
            )

    def test_text_formatting_consistency(self):
        """Test that text formatting is consistent and readable."""
        test_messages = [
            "System message",
            "User input",
            "Error notification",
            "Success confirmation",
        ]

        colors = ["green", "cyan", "red", "yellow"]

        for msg, color in zip(test_messages, colors):
            self.terminal.add_output(msg, color)

        # All output should use consistent HTML span formatting
        for line in self.terminal.output_lines:
            assert line.startswith("<span style='color:")
            assert line.endswith("</span>")
            assert (
                "font-family" not in line
            )  # Font should be handled by CSS, not inline

    def test_screen_reader_compatibility(self):
        """Test that terminal output is compatible with screen readers."""
        # Add various types of content
        self.terminal.add_output("Welcome to Logic Quest", "green")
        self.terminal.display_ascii_art("┌─────┐\n│ BOX │\n└─────┘")
        self.terminal.show_prompt()

        # All content should be in text format (no images or complex formatting)
        for line in self.terminal.output_lines:
            # Should be plain text wrapped in simple HTML spans
            assert "<span" in line and "</span>" in line
            # Should not contain complex HTML structures
            assert "<div" not in line and "<img" not in line
