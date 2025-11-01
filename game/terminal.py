"""
Terminal Interface Module

Handles all terminal operations, styling, and user interaction
for the Logic Quest retro terminal interface.
"""

import reflex as rx
from typing import List


class Terminal(rx.State):
    """
    Terminal interface component with retro 80s styling.

    Manages terminal display, input handling, and cyberpunk aesthetics.
    """

    output_lines: List[str] = []
    current_input: str = ""
    is_typing: bool = False
    cursor_visible: bool = True

    # Terminal styling constants
    COLORS = {
        "green": "#00ff00",
        "cyan": "#00ffff",
        "yellow": "#ffff00",
        "red": "#ff0000",
        "white": "#ffffff",
        "black": "#000000",
    }

    def add_output(self, text: str, color: str = "green"):
        """Add a line to terminal output with specified color."""
        colored_text = f"<span style='color: {self.COLORS.get(color, self.COLORS['green'])}'>{text}</span>"
        self.output_lines.append(colored_text)

    def clear_terminal(self):
        """Clear all terminal output."""
        self.output_lines = []

    def handle_input(self, input_text: str):
        """Process user input and add to output."""
        self.add_output(f"> {input_text}", "cyan")
        self.current_input = ""
        # Input will be processed by game logic

    def typewriter_effect(self, text: str, delay: float = 0.05):
        """Add typewriter effect for dramatic text display."""
        # This will be implemented with JavaScript for real-time effect
        self.add_output(text, "green")

    def display_ascii_art(self, art: str):
        """Display ASCII art in the terminal."""
        for line in art.split("\n"):
            self.add_output(line, "cyan")

    def show_prompt(self, prompt_text: str = "LOGIC-1 > "):
        """Display the command prompt."""
        self.add_output(prompt_text, "yellow")


def terminal_component() -> rx.Component:
    """
    Create the main terminal interface component.

    Returns:
        Reflex component with retro terminal styling
    """
    return rx.vstack(
        # Terminal header
        rx.hstack(
            rx.text(
                "CYBERDYNE SYSTEMS - LOGIC-1 TERMINAL",
                color="#00ff00",
                font_family="monospace",
                font_weight="bold",
            ),
            rx.spacer(),
            rx.text(
                "1985",
                color="#ffff00",
                font_family="monospace",
            ),
            width="100%",
            padding="0.5rem",
            background="#000000",
            border="2px solid #00ff00",
        ),
        # Terminal output area
        rx.box(
            rx.foreach(
                Terminal.output_lines,
                lambda line: rx.text(
                    line,
                    font_family="monospace",
                    font_size="14px",
                    line_height="1.2",
                    white_space="pre-wrap",
                ),
            ),
            height="400px",
            overflow_y="auto",
            padding="1rem",
            background="#000000",
            border="2px solid #00ff00",
            color="#00ff00",
        ),
        # Input area
        rx.hstack(
            rx.text(
                "LOGIC-1 > ",
                color="#ffff00",
                font_family="monospace",
                font_weight="bold",
            ),
            rx.input(
                value=Terminal.current_input,
                on_change=Terminal.set_current_input,
                on_key_down=lambda key: Terminal.handle_input(Terminal.current_input)
                if key == "Enter"
                else None,
                placeholder="Enter command...",
                background="#000000",
                border="1px solid #00ff00",
                color="#00ff00",
                font_family="monospace",
                flex="1",
            ),
            width="100%",
            padding="0.5rem",
            background="#000000",
            border="2px solid #00ff00",
        ),
        width="100%",
        max_width="800px",
        margin="0 auto",
        spacing="0",
    )


# ASCII art for the game
CYBERDYNE_LOGO = """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ██╗███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝████╗  ██║██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║  ██║ ╚████╔╝ ██╔██╗ ██║█████╗  
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║  ██║  ╚██╔╝  ██║╚██╗██║██╔══╝  
╚██████╗   ██║   ██████╔╝███████╗██║  ██║██████╔╝   ██║   ██║ ╚████║███████╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝   ╚═╝  ╚═══╝╚══════╝
                                                                              
                    SYSTEMS LOGIC-1 TERMINAL v2.1
"""

LOGIC_CIRCUIT = """
    ┌─────────────────────────────────────────┐
    │  LOGIC CIRCUIT STATUS: MALFUNCTIONING   │
    │                                         │
    │  ┌─[AND]─┐    ┌─[OR]──┐    ┌─[NOT]─┐   │
    │  │   ⚡   │────│   ⚡   │────│   ⚡   │   │
    │  └───────┘    └───────┘    └───────┘   │
    │                                         │
    │  ERROR: Logic pathways corrupted        │
    │  SOLUTION: Restore logical reasoning    │
    └─────────────────────────────────────────┘
"""
