"""
Logic Quest - Main Entry Point

Reflex-based web application entry point for the Prolog learning game.
Provides retro terminal interface with 80s cyberpunk styling.
"""

import reflex as rx
from game.terminal import CYBERDYNE_LOGO
from game.story import StoryEngine
from game.puzzles import PuzzleManager
from game.tutorial_content import TutorialSession
from components.retro_ui import (
    retro_container,
    neon_text,
    cyberpunk_button,
    ascii_art_display,
    terminal_window,
    explanation_panel,
)


class GameState(rx.State):
    """Main application state for Logic Quest."""

    # Game state
    current_screen: str = "welcome"
    game_mode: str = "menu"  # menu, tutorial, adventure

    # Tutorial state
    tutorial_active: bool = False
    tutorial_step: int = 0

    # Story and puzzle state
    player_level: int = 1
    player_score: int = 0
    concepts_learned: list[str] = []

    # Terminal state
    terminal_output: list[str] = []
    terminal_colors: list[str] = []
    user_input: str = ""
    
    # Right panel state
    right_panel_content: str = "Welcome to Logic Quest!\n\nType 'hint' for guidance."
    right_panel_color: str = "neon_green"
    right_panel_title: str = "SYSTEM INFO"

    # Initialize non-serializable objects as class attributes
    _tutorial_session = None
    _story_engine = None
    _puzzle_manager = None

    @property
    def tutorial_session(self):
        if self._tutorial_session is None:
            self._tutorial_session = TutorialSession()
        return self._tutorial_session

    @property
    def story_engine(self):
        if self._story_engine is None:
            self._story_engine = StoryEngine()
        return self._story_engine

    @property
    def puzzle_manager(self):
        if self._puzzle_manager is None:
            self._puzzle_manager = PuzzleManager()
        return self._puzzle_manager

    def start_tutorial(self):
        """Start the Hello World Prolog tutorial."""
        self.game_mode = "tutorial"
        self.tutorial_active = True
        self.tutorial_session.start_session()
        self.current_screen = "tutorial"

        # Initialize HelloWorldPuzzle for interactive exercises
        from game.hello_world_puzzle import HelloWorldPuzzle
        self._hello_world_puzzle = HelloWorldPuzzle()
        self._hello_world_puzzle.initialize_for_interactive_mode(self)

        # Add welcome message to terminal
        self.terminal_output = []
        self.add_terminal_output("🚀 Starting Interactive Hello World Prolog Tutorial...", "cyan")
        self.add_terminal_output("", "green")

        # Get first tutorial content
        content = self.tutorial_session.get_current_content()
        self.add_terminal_output(content.get("title", "Tutorial"), "yellow")
        self.add_terminal_output("", "green")
        
        # Display introduction content
        for line in content.get("explanation", []):
            self.add_terminal_output(line, "cyan")
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("💡 This tutorial requires active participation!", "yellow")
        self.add_terminal_output("Type 'begin', 'start', or 'ready' to show you're engaged.", "green")
        self.add_terminal_output("Type 'hint' for guidance or 'menu' to return.", "cyan")

        # Set explanation in right panel
        explanation_text = "\n".join(content.get("explanation", []))
        if explanation_text.strip():
            self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")

    def start_adventure(self):
        """Start the main Logic Quest adventure."""
        self.game_mode = "adventure"
        self.current_screen = "adventure"

        # Add intro story to terminal
        self.terminal_output = []
        self.add_terminal_output("🌆 INITIALIZING LOGIC QUEST...", "cyan")
        self.add_terminal_output("", "green")

        # Display ASCII art
        for line in CYBERDYNE_LOGO.split("\n"):
            self.add_terminal_output(line, "cyan")

        # Get intro story
        intro = self.story_engine.get_intro_story()
        self.add_terminal_output("", "green")
        self.add_terminal_output(intro.title, "yellow")
        self.add_terminal_output("Type 'help' for commands or 'hint' for guidance.", "cyan")

        # Set story content in right panel
        story_text = "\n".join(intro.content)
        if story_text.strip():
            self.set_right_panel(story_text, "neon_cyan", "MISSION BRIEFING")

    def return_to_menu(self):
        """Return to the main menu."""
        self.game_mode = "menu"
        self.current_screen = "welcome"
        self.tutorial_active = False
        self.terminal_output = []

    def handle_terminal_input(self, input_text: str):
        """Handle user input from terminal."""
        if not input_text.strip():
            return

        self.add_terminal_output(f"> {input_text}", "cyan")

        if self.game_mode == "tutorial":
            self._handle_tutorial_input(input_text)
        elif self.game_mode == "adventure":
            self._handle_adventure_input(input_text)

        # Clear input
        self.user_input = ""

    def _handle_tutorial_input(self, input_text: str):
        """Handle input during tutorial mode with interactive exercises."""
        # Handle global commands first
        if input_text.lower() == "hint":
            self._show_tutorial_hint()
            return
        elif input_text.lower() == "menu":
            self.return_to_menu()
            return
        elif input_text.lower() == "adventure" and self.tutorial_session.is_complete():
            # Transition to main adventure after tutorial completion
            self._transition_to_adventure()
            return
        
        # Get current tutorial step to determine if we're in an interactive exercise
        current_step = self.tutorial_session.current_step
        
        # Route input based on current tutorial step
        if current_step == 0:  # Introduction step
            self._handle_introduction_input(input_text)
        elif current_step == 1:  # Facts explanation with component identification
            self._handle_facts_explanation_input(input_text)
        elif current_step == 2:  # Fact creation exercise
            self._handle_fact_creation_input(input_text)
        elif current_step == 3:  # Query explanation and practice
            self._handle_query_explanation_input(input_text)
        elif current_step == 4:  # Variable introduction and practice
            self._handle_variable_introduction_input(input_text)
        elif current_step == 5:  # Completion
            self._handle_completion_input(input_text)
        else:
            # Fallback for unknown steps
            self.add_terminal_output("Unknown tutorial step. Type 'menu' to return.", "red")

    def _handle_introduction_input(self, input_text: str):
        """Handle input during introduction step."""
        # Require specific engagement command, not "next"
        if input_text.lower() in ["begin", "start", "ready"]:
            if self.tutorial_session.advance_step():
                content = self.tutorial_session.get_current_content()
                self.add_terminal_output("", "green")
                self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                
                # Set explanation in right panel
                explanation_text = "\n".join(content.get("explanation", []))
                if explanation_text.strip():
                    self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")
                
                # Show first interactive exercise prompt
                self.add_terminal_output("", "green")
                self.add_terminal_output("Now let's test your understanding with an interactive exercise!", "cyan")
        elif input_text.lower() in ["next", "continue"]:
            self.add_terminal_output("❌ This tutorial requires active participation!", "red")
            self.add_terminal_output("Type 'begin', 'start', or 'ready' to show you're engaged.", "yellow")
        else:
            self.add_terminal_output("Type 'begin', 'start', or 'ready' to continue, or 'hint' for guidance.", "yellow")

    def _handle_facts_explanation_input(self, input_text: str):
        """Handle input during facts explanation with component identification."""
        # This step requires component identification - route to HelloWorldPuzzle
        if hasattr(self, '_hello_world_puzzle') and self._hello_world_puzzle:
            result = self._hello_world_puzzle.handle_component_identification_input(input_text)
            if result == "completed":
                # Exercise completed, advance to next step
                if self.tutorial_session.advance_step():
                    content = self.tutorial_session.get_current_content()
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                    
                    explanation_text = "\n".join(content.get("explanation", []))
                    if explanation_text.strip():
                        self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")
            elif result == "invalid":
                # Invalid input handled by puzzle
                pass
        else:
            # Fallback if puzzle not initialized
            self.add_terminal_output("Tutorial system error. Type 'menu' to return.", "red")

    def _handle_fact_creation_input(self, input_text: str):
        """Handle input during fact creation exercise."""
        if hasattr(self, '_hello_world_puzzle') and self._hello_world_puzzle:
            result = self._hello_world_puzzle.handle_fact_creation_input(input_text)
            if result == "completed":
                if self.tutorial_session.advance_step():
                    content = self.tutorial_session.get_current_content()
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                    
                    explanation_text = "\n".join(content.get("explanation", []))
                    if explanation_text.strip():
                        self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")
        else:
            self.add_terminal_output("Tutorial system error. Type 'menu' to return.", "red")

    def _handle_query_explanation_input(self, input_text: str):
        """Handle input during query explanation and practice."""
        if hasattr(self, '_hello_world_puzzle') and self._hello_world_puzzle:
            result = self._hello_world_puzzle.handle_query_practice_input(input_text)
            if result == "completed":
                if self.tutorial_session.advance_step():
                    content = self.tutorial_session.get_current_content()
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                    
                    explanation_text = "\n".join(content.get("explanation", []))
                    if explanation_text.strip():
                        self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")
        else:
            self.add_terminal_output("Tutorial system error. Type 'menu' to return.", "red")

    def _handle_variable_introduction_input(self, input_text: str):
        """Handle input during variable introduction and practice."""
        if hasattr(self, '_hello_world_puzzle') and self._hello_world_puzzle:
            result = self._hello_world_puzzle.handle_variable_practice_input(input_text)
            if result == "completed":
                if self.tutorial_session.advance_step():
                    # Tutorial completed - mark completion and offer transition
                    self._complete_hello_world_tutorial()
        else:
            self.add_terminal_output("Tutorial system error. Type 'menu' to return.", "red")

    def _handle_completion_input(self, input_text: str):
        """Handle input during completion step."""
        if input_text.lower() == "adventure":
            self._transition_to_adventure()
        elif input_text.lower() in ["next", "continue"]:
            self.add_terminal_output("Type 'adventure' to start the main game or 'menu' to return.", "yellow")
        else:
            self.add_terminal_output("Type 'adventure' to start the main game or 'menu' to return.", "yellow")

    def _handle_adventure_input(self, input_text: str):
        """Handle input during adventure mode."""
        if input_text.lower() == "menu":
            self.return_to_menu()
        elif input_text.lower() == "help":
            self.add_terminal_output("Available commands:", "yellow")
            self.add_terminal_output("  help - Show this help", "green")
            self.add_terminal_output("  hint - Get guidance on what to do next", "green")
            self.add_terminal_output("  status - Show game status", "green")
            self.add_terminal_output("  menu - Return to main menu", "green")
            if not self.story_engine.is_hello_world_completed():
                self.add_terminal_output("", "green")
                self.add_terminal_output("💡 New to Prolog? Consider starting with the", "yellow")
                self.add_terminal_output("   Hello World tutorial from the main menu!", "yellow")
        elif input_text.lower() == "hint":
            self._show_adventure_hint()
        elif input_text.lower() == "status":
            progress = self.story_engine.get_player_progress()
            self.add_terminal_output(f"Current Level: {progress['level']}", "green")
            self.add_terminal_output(f"Score: {progress['score']}", "green")
            self.add_terminal_output(
                f"Concepts Learned: {len(progress['concepts_learned'])}", "green"
            )
            self.add_terminal_output(
                f"Hello World Tutorial: {'✅ Completed' if progress.get('hello_world_completed', False) else '❌ Not completed'}", 
                "green"
            )
        elif input_text.lower() == "tutorial" and not self.story_engine.is_hello_world_completed():
            # Allow quick access to tutorial from adventure mode
            self.add_terminal_output("Returning to main menu to access tutorial...", "cyan")
            self.return_to_menu()
        else:
            if not self.story_engine.is_hello_world_completed():
                self.add_terminal_output(
                    "Unknown command. Type 'help' for commands or 'tutorial' to learn Prolog basics.", "yellow"
                )
            else:
                self.add_terminal_output(
                    "Unknown command. Type 'help' for available commands.", "yellow"
                )

    def add_terminal_output(self, text: str, color: str = "green"):
        """Add text to terminal output with color."""
        self.terminal_output.append(text)
        self.terminal_colors.append(color)

    def set_right_panel(self, content: str, color: str = "neon_green", title: str = "SYSTEM INFO"):
        """Set the content of the right panel."""
        self.right_panel_content = content
        self.right_panel_color = color
        self.right_panel_title = title

    def clear_terminal(self):
        """Clear terminal output."""
        self.terminal_output = []
        self.terminal_colors = []

    def set_user_input(self, value: str):
        """Set user input value."""
        self.user_input = value

    def handle_key_press(self, key: str):
        """Handle key press events."""
        if key == "Enter":
            self.handle_terminal_input(self.user_input)

    def _show_tutorial_hint(self):
        """Show hint for current tutorial step."""
        self.add_terminal_output("💡 Hint displayed in the right panel.", "cyan")
        
        # Get current tutorial step and provide appropriate hint
        current_step = self.tutorial_session.current_step
        hints = {
            0: "This is an introduction to Prolog. Read the explanation, then type 'begin', 'start', or 'ready' to show engagement.",
            1: "You need to identify components of a Prolog fact. Answer the specific questions about predicate, arguments, and punctuation.",
            2: "Write a complete Prolog fact that says 'Bob likes pizza'. Use the format: predicate(argument1, argument2).",
            3: "Write a query to ask if Alice likes chocolate. Remember to start with '?-' and end with a period.",
            4: "Write a query using a variable (uppercase letter) to find what Alice likes. Example format: ?- likes(alice, X).",
            5: "Tutorial complete! Type 'adventure' to start the main game or 'menu' to return."
        }
        
        hint_text = hints.get(current_step, "Follow the interactive exercise instructions.")
        self.set_right_panel(f"💡 INTERACTIVE HINT\n\n{hint_text}\n\n🚫 Note: This tutorial requires active participation. You cannot progress by typing 'next' - you must complete the hands-on exercises!", "neon_yellow", "HINT")

    def _complete_hello_world_tutorial(self):
        """Handle completion of the Hello World tutorial."""
        # Mark tutorial as completed in both systems
        self.story_engine.mark_hello_world_completed()
        self.puzzle_manager.player_stats["hello_world_completed"] = True
        
        # Add completion concepts to learned list
        new_concepts = ["prolog_basics", "facts", "queries", "variables"]
        for concept in new_concepts:
            if concept not in self.concepts_learned:
                self.concepts_learned.append(concept)
        
        # Display completion message
        self.add_terminal_output("🎉 TUTORIAL COMPLETE! 🎉", "yellow")
        self.add_terminal_output("", "green")
        
        # Get transition story
        transition_story = self.story_engine.get_hello_world_transition_story()
        self.add_terminal_output(transition_story.title, "yellow")
        self.add_terminal_output("", "green")
        
        # Display transition story content
        for line in transition_story.content:
            self.add_terminal_output(line, "cyan")
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("Type 'adventure' to begin the main quest or 'menu' to return.", "green")
        
        # Set completion message in right panel
        completion_text = """🎊 CONGRATULATIONS! 🎊

You've successfully completed the Hello World Prolog tutorial!

✅ Concepts Mastered:
• Facts and their syntax
• Queries and how to ask questions
• Variables and pattern matching
• Basic Prolog reasoning

🚀 READY FOR MORE?

The main Logic Quest adventure awaits! You'll learn advanced concepts like:
• Rules and logical implications
• Complex pattern matching
• Backtracking algorithms
• Recursive problem solving

Type 'adventure' to continue your journey!"""
        
        self.set_right_panel(completion_text, "neon_yellow", "TUTORIAL COMPLETE")

    def _transition_to_adventure(self):
        """Transition from tutorial completion to main adventure."""
        self.add_terminal_output("🚀 Transitioning to main adventure...", "cyan")
        self.add_terminal_output("", "green")
        
        # Start the main adventure
        self.start_adventure()

    def _show_adventure_hint(self):
        """Show hint for current adventure state."""
        self.add_terminal_output("💡 Hint displayed in the right panel.", "cyan")
        
        # Provide contextual hints based on game state and hello world completion
        if self.story_engine.is_hello_world_completed():
            hint_text = """💡 ADVANCED MISSION BRIEFING

Excellent work completing the tutorial! You now have the foundation needed for this mission.

You're at Cyberdyne Systems in 1985, tasked with repairing the LOGIC-1 AI system using your newly acquired Prolog skills.

Available commands:
• 'help' - Show all commands
• 'status' - Check your progress
• 'menu' - Return to main menu

The AI system corruption goes deeper than basic facts and queries. You'll need to master advanced concepts to fully restore the system."""
        else:
            hint_text = """💡 GETTING STARTED

You're at Cyberdyne Systems in 1985, tasked with repairing the LOGIC-1 AI system.

💡 RECOMMENDATION: If you're new to Prolog, consider starting with the Hello World tutorial from the main menu first. It will teach you the basics you need for this mission.

Available commands:
• 'help' - Show all commands
• 'status' - Check your progress
• 'menu' - Return to main menu

The AI system is waiting for you to begin the repair process."""
        
        self.set_right_panel(hint_text, "neon_yellow", "HINT")


def welcome_screen() -> rx.Component:
    """Welcome screen with game options."""
    return rx.center(
        retro_container(
            rx.vstack(
                # Title
                neon_text("LOGIC QUEST", color="neon_green", size="xl", glow=True),
                neon_text("A Prolog Learning Adventure", color="neon_cyan", size="md"),
                # ASCII Art
                ascii_art_display(
                    """
    ┌─────────────────────────────────────┐
    │  ╔══════════════════════════════╗   │
    │  ║    CYBERDYNE SYSTEMS 1985    ║   │
    │  ║      LOGIC-1 TERMINAL        ║   │
    │  ╚══════════════════════════════╝   │
    │                                     │
    │  [●] NEURAL INTERFACE: ONLINE       │
    │  [●] LOGIC CIRCUITS: CRITICAL       │
    │  [●] AI CORE: NEEDS REPAIR          │
    └─────────────────────────────────────┘
                    """,
                    color="neon_cyan",
                ),
                # Menu options - conditional based on hello world completion
                rx.cond(
                    GameState.story_engine.is_hello_world_completed(),
                    # Options when hello world is completed
                    rx.vstack(
                        cyberpunk_button(
                            "Continue Main Adventure",
                            on_click=GameState.start_adventure,
                            color="neon_green",
                        ),
                        cyberpunk_button(
                            "Review Hello World Tutorial",
                            on_click=GameState.start_tutorial,
                            color="neon_cyan",
                        ),
                        cyberpunk_button("Exit System", color="neon_red"),
                        spacing="3",
                        align="center",
                    ),
                    # Options when hello world is not completed
                    rx.vstack(
                        cyberpunk_button(
                            "Start Hello World Tutorial",
                            on_click=GameState.start_tutorial,
                            color="neon_green",
                        ),
                        cyberpunk_button(
                            "Begin Main Adventure",
                            on_click=GameState.start_adventure,
                            color="neon_cyan",
                        ),
                        cyberpunk_button("Exit System", color="neon_red"),
                        spacing="3",
                        align="center",
                    ),
                ),
                # Footer - conditional message
                rx.cond(
                    GameState.story_engine.is_hello_world_completed(),
                    neon_text(
                        "Welcome back, logic programmer!", color="neon_yellow", size="sm"
                    ),
                    neon_text(
                        "New to Prolog? Start with the tutorial!", color="neon_yellow", size="sm"
                    ),
                ),
                spacing="6",
                align="center",
            ),
            style={"max_width": "600px", "margin": "2rem auto"},
        ),
        height="100vh",
    )


def render_terminal_line(text, color) -> rx.Component:
    """Render a terminal line with proper color styling."""
    return rx.cond(
        color == "green",
        rx.text(text, font_family="monospace", font_size="14px", line_height="1.2", white_space="pre-wrap", color="#00ff00"),
        rx.cond(
            color == "cyan", 
            rx.text(text, font_family="monospace", font_size="14px", line_height="1.2", white_space="pre-wrap", color="#00ffff"),
            rx.cond(
                color == "yellow",
                rx.text(text, font_family="monospace", font_size="14px", line_height="1.2", white_space="pre-wrap", color="#ffff00"),
                rx.cond(
                    color == "red",
                    rx.text(text, font_family="monospace", font_size="14px", line_height="1.2", white_space="pre-wrap", color="#ff0000"),
                    rx.text(text, font_family="monospace", font_size="14px", line_height="1.2", white_space="pre-wrap", color="#ffffff")
                )
            )
        )
    )


def game_screen() -> rx.Component:
    """Main game screen with split terminal and explanation panel."""
    return rx.vstack(
        # Header
        rx.hstack(
            neon_text("LOGIC QUEST", color="neon_green", size="lg"),
            rx.spacer(),
            cyberpunk_button(
                "Main Menu", on_click=GameState.return_to_menu, color="neon_yellow"
            ),
            width="100%",
            padding="1rem",
            height="60px",  # Fixed header height
        ),
        # Split layout: Terminal on left (60%), Explanation panel on right (40%)
        rx.hstack(
            # Left side - Terminal (60% width)
            rx.box(
                terminal_window(
                    # Output area
                    rx.box(
                        rx.foreach(
                            rx.Var.range(GameState.terminal_output.length()),
                            lambda i: render_terminal_line(
                                GameState.terminal_output[i], 
                                GameState.terminal_colors[i]
                            ),
                        ),
                        height="calc(100vh - 200px)",  # Full height minus header and input
                        overflow_y="auto",
                        padding="1rem",
                    ),
                    # Input area
                    rx.hstack(
                        neon_text("LOGIC-1 > ", color="neon_yellow"),
                        rx.input(
                            value=GameState.user_input,
                            on_change=GameState.set_user_input,
                            on_key_down=GameState.handle_key_press,
                            placeholder="Enter command...",
                            style={
                                "background": "transparent",
                                "border": "1px solid #00ff00",
                                "color": "#00ff00",
                                "font_family": "monospace",
                            },
                            flex="1",
                        ),
                        width="100%",
                        padding="0.5rem 1rem",
                        height="50px",  # Fixed input height
                    ),
                    title="CYBERDYNE SYSTEMS TERMINAL",
                    style={"height": "calc(100vh - 80px)", "width": "100%"},
                ),
                width="60%",
                height="calc(100vh - 80px)",
            ),
            # Right side - Explanation panel (40% width)
            rx.box(
                explanation_panel(
                    GameState.right_panel_content,
                    GameState.right_panel_color,
                    GameState.right_panel_title,
                ),
                width="40%",
                height="calc(100vh - 80px)",
            ),
            width="100%",
            height="calc(100vh - 80px)",
            spacing="4",
        ),
        height="100vh",
        padding="1rem",
        spacing="0",
    )


def index() -> rx.Component:
    """Main application component."""
    return rx.box(
        rx.cond(GameState.current_screen == "welcome", welcome_screen(), game_screen()),
        style={
            "background": "#000000",
            "min_height": "100vh",
            "font_family": "monospace",
        },
    )


# Create the Reflex app
app = rx.App(
    style={
        "font_family": "monospace",
        "background_color": "#000000",
    }
)

app.add_page(index, route="/")

if __name__ == "__main__":
    app.run()
