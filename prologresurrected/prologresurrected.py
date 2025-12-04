"""
Logic Quest - Main Entry Point

Reflex-based web application entry point for the Prolog learning game.
Provides retro terminal interface with 80s cyberpunk styling.
"""

import reflex as rx
from .game.terminal import CYBERDYNE_LOGO
from .game.story import StoryEngine
from .game.puzzles import PuzzleManager
from .game.tutorial_content import TutorialSession
from .game.complexity import ComplexityLevel, ComplexityManager
from .game.complexity_help import ComplexityHelpSystem, format_help_for_terminal
from .components.retro_ui import (
    retro_container,
    neon_text,
    cyberpunk_button,
    ascii_art_display,
    terminal_window,
    explanation_panel,
    complexity_selection_screen,
    complexity_indicator_badge,
)


class GameState(rx.State):
    """Main application state for Logic Quest."""

    # Game state
    current_screen: str = "welcome"
    game_mode: str = "menu"  # menu, tutorial, adventure
    pending_action: str = ""  # Track what action to take after complexity selection
    
    # Complexity change state
    pending_complexity_change: str = ""  # Track pending complexity level change
    awaiting_complexity_confirmation: bool = False

    # Tutorial state
    tutorial_active: bool = False
    tutorial_step: int = 0

    # Story and puzzle state
    player_level: int = 1
    player_score: int = 0
    concepts_learned: list[str] = []

    # Complexity level state
    complexity_level: ComplexityLevel = ComplexityLevel.BEGINNER
    complexity_selection_shown: bool = False
    complexity_change_count: int = 0

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
    _hello_world_puzzle = None
    _complexity_manager = None
    _complexity_help_system = None
    _current_adventure_puzzle = None  # Current active adventure puzzle
    
    # Computed property for hello world completion status
    hello_world_completed: bool = False

    @property
    def tutorial_session(self):
        if self._tutorial_session is None:
            self._tutorial_session = TutorialSession()
        return self._tutorial_session

    @property
    def story_engine(self):
        if self._story_engine is None:
            self._story_engine = StoryEngine(complexity_level=self.complexity_level)
        return self._story_engine

    @property
    def puzzle_manager(self):
        if self._puzzle_manager is None:
            self._puzzle_manager = PuzzleManager()
        return self._puzzle_manager

    @property
    def complexity_manager(self):
        if self._complexity_manager is None:
            self._complexity_manager = ComplexityManager()
            # Sync the manager's current level with the state
            self._complexity_manager.set_complexity_level(self.complexity_level)
        return self._complexity_manager
    
    @property
    def complexity_help_system(self):
        if self._complexity_help_system is None:
            self._complexity_help_system = ComplexityHelpSystem(self.complexity_manager)
        return self._complexity_help_system
    
    def update_hello_world_status(self):
        """Update the hello world completion status from story engine."""
        if hasattr(self, '_story_engine') and self._story_engine:
            self.hello_world_completed = self.story_engine.is_hello_world_completed()

    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """
        Set the complexity level for the current game session with error handling.
        
        Args:
            level: The complexity level to set
            
        Raises:
            ValueError: If level is not a valid ComplexityLevel
        """
        if not isinstance(level, ComplexityLevel):
            # Log error and use fallback
            self.add_terminal_output("⚠️  Invalid complexity level selection.", "red")
            self.add_terminal_output("Using BEGINNER level as fallback.", "yellow")
            level = ComplexityLevel.BEGINNER
        
        try:
            old_level = self.complexity_level
            self.complexity_level = level
            
            # Update the complexity manager with error handling
            try:
                self.complexity_manager.set_complexity_level(level)
            except Exception as e:
                # Log but continue - state is already updated
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to update complexity manager: {e}")
            
            # Update the story engine if it exists
            if hasattr(self, '_story_engine') and self._story_engine:
                try:
                    self._story_engine.set_complexity_level(level)
                except Exception as e:
                    # Log but continue
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Failed to update story engine complexity: {e}")
            
            # Track complexity changes
            if old_level != level:
                self.complexity_change_count += 1
                
        except Exception as e:
            # Critical failure - notify user
            self.add_terminal_output("⚠️  Failed to change complexity level.", "red")
            self.add_terminal_output("Your current level has been preserved.", "yellow")
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Critical failure in set_complexity_level: {e}")

    def get_complexity_level(self) -> ComplexityLevel:
        """Get the current complexity level."""
        return self.complexity_level

    def show_complexity_selection(self) -> None:
        """Mark that the complexity selection screen has been shown."""
        self.complexity_selection_shown = True

    def handle_complexity_change(self, new_level: ComplexityLevel) -> None:
        """Handle a complexity level change with appropriate feedback."""
        self.set_complexity_level(new_level)
        
        # Get configuration for display
        config = self.complexity_manager.get_config(new_level)
        
        # Add confirmation message to terminal if in game
        if self.game_mode in ["tutorial", "adventure"]:
            self.add_terminal_output(f"🔧 Complexity level changed to {config.name}", "yellow")
            self.add_terminal_output(f"   {config.description}", "cyan")
            
            # Update right panel with new complexity info
            self._update_complexity_indicator()

    @rx.var
    def get_complexity_indicator(self) -> str:
        """Get a string representation of the current complexity level for UI display."""
        config = self.complexity_manager.get_current_config()
        return f"{config.ui_indicators.get('icon', '')} {config.name.upper()}"

    @rx.var
    def get_complexity_color(self) -> str:
        """Get the color associated with the current complexity level."""
        config = self.complexity_manager.get_current_config()
        return config.ui_indicators.get('color', 'neon_green')
    
    @rx.var
    def get_complexity_icon(self) -> str:
        """Get the icon associated with the current complexity level."""
        config = self.complexity_manager.get_current_config()
        return config.ui_indicators.get('icon', '🌱')
    
    @rx.var
    def get_complexity_name(self) -> str:
        """Get the name of the current complexity level."""
        config = self.complexity_manager.get_current_config()
        return config.name
    
    @rx.var
    def get_complexity_description(self) -> str:
        """Get the description of the current complexity level."""
        config = self.complexity_manager.get_current_config()
        return config.description

    def _update_complexity_indicator(self) -> None:
        """Update the right panel with current complexity level information."""
        config = self.complexity_manager.get_current_config()
        indicator_text = f"""🎯 COMPLEXITY LEVEL

{config.ui_indicators.get('icon', '')} {config.name.upper()}

{config.description}

Scoring Multiplier: {config.scoring_multiplier}x
Hint Availability: {config.hint_frequency.value}
Explanation Depth: {config.explanation_depth.value}

Changes Made: {self.complexity_change_count}"""
        
        self.set_right_panel(indicator_text, config.ui_indicators.get('color', 'neon_green'), "COMPLEXITY")

    def show_complexity_selection_screen(self):
        """Show the complexity level selection screen."""
        self.current_screen = "complexity_selection"
        self.complexity_selection_shown = True

    def select_complexity_level(self, level_name: str):
        """
        Handle complexity level selection from the UI with error handling.
        
        Args:
            level_name: Name of the complexity level (e.g., "BEGINNER")
        """
        level_mapping = {
            "BEGINNER": ComplexityLevel.BEGINNER,
            "INTERMEDIATE": ComplexityLevel.INTERMEDIATE,
            "ADVANCED": ComplexityLevel.ADVANCED,
            "EXPERT": ComplexityLevel.EXPERT,
        }
        
        try:
            if level_name in level_mapping:
                self.set_complexity_level(level_mapping[level_name])
            else:
                # Invalid level name - use fallback
                self.add_terminal_output(f"⚠️  Invalid complexity level: {level_name}", "red")
                self.add_terminal_output("Using BEGINNER level as fallback.", "yellow")
                self.set_complexity_level(ComplexityLevel.BEGINNER)
        except Exception as e:
            # Critical failure - notify user
            self.add_terminal_output("⚠️  Failed to select complexity level.", "red")
            self.add_terminal_output("Using BEGINNER level as fallback.", "yellow")
            self.set_complexity_level(ComplexityLevel.BEGINNER)
            
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Complexity selection failed: {e}")

    def continue_from_complexity_selection(self):
        """Continue from complexity selection to the intended game mode."""
        if self.pending_action == "tutorial":
            self.pending_action = ""
            self._start_tutorial_after_complexity()
        elif self.pending_action == "adventure":
            self.pending_action = ""
            self._start_adventure_after_complexity()
        else:
            # Return to welcome screen if no pending action
            self.current_screen = "welcome"

    def _start_tutorial_after_complexity(self):
        """Start tutorial after complexity selection is complete."""
        self.game_mode = "tutorial"
        self.tutorial_active = True
        self.tutorial_session.start_session()
        self.current_screen = "tutorial"

        # Initialize HelloWorldPuzzle for interactive exercises
        from .game.hello_world_puzzle import HelloWorldPuzzle
        self._hello_world_puzzle = HelloWorldPuzzle()
        self._hello_world_puzzle.initialize_for_interactive_mode(self)

        # Add welcome message to terminal
        self.terminal_output = []
        self.add_terminal_output("🚀 Starting Interactive Hello World Prolog Tutorial...", "cyan")
        self.add_terminal_output("", "green")
        self.add_terminal_output("⚠️  IMPORTANT: This is an INTERACTIVE tutorial!", "red")
        self.add_terminal_output("You must type correct Prolog commands to progress.", "red")
        self.add_terminal_output("Typing 'next' or 'continue' will NOT work!", "red")
        self.add_terminal_output("", "green")

        # Get first tutorial content
        content = self.tutorial_session.get_current_content()
        self.add_terminal_output(content.get("title", "Tutorial"), "yellow")
        self.add_terminal_output("", "green")
        
        # Display introduction content
        for line in content.get("explanation", []):
            self.add_terminal_output(line, "cyan")
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("🎯 READY TO BEGIN?", "yellow")
        self.add_terminal_output("This tutorial requires active participation and correct answers!", "yellow")
        self.add_terminal_output("Type 'begin', 'start', or 'ready' to show you're engaged.", "green")
        self.add_terminal_output("Type 'hint' for guidance or 'menu' to return.", "cyan")
        self.add_terminal_output("", "green")
        self.add_terminal_output("🚫 Remember: You CANNOT use 'next' to skip exercises!", "red")

        # Set explanation in right panel
        explanation_text = "\n".join(content.get("explanation", []))
        if explanation_text.strip():
            self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")

    def _start_adventure_after_complexity(self):
        """Start adventure after complexity selection is complete."""
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

    def start_tutorial(self):
        """Start the Hello World Prolog tutorial."""
        # Show complexity selection first if not shown yet
        if not self.complexity_selection_shown:
            self.pending_action = "tutorial"
            self.show_complexity_selection_screen()
            return
            
        self.game_mode = "tutorial"
        self.tutorial_active = True
        self.tutorial_session.start_session()
        self.current_screen = "tutorial"

        # Initialize HelloWorldPuzzle for interactive exercises
        from .game.hello_world_puzzle import HelloWorldPuzzle
        self._hello_world_puzzle = HelloWorldPuzzle()
        self._hello_world_puzzle.initialize_for_interactive_mode(self)

        # Add welcome message to terminal
        self.terminal_output = []
        self.add_terminal_output("🚀 Starting Interactive Hello World Prolog Tutorial...", "cyan")
        self.add_terminal_output("", "green")
        self.add_terminal_output("⚠️  IMPORTANT: This is an INTERACTIVE tutorial!", "red")
        self.add_terminal_output("You must type correct Prolog commands to progress.", "red")
        self.add_terminal_output("Typing 'next' or 'continue' will NOT work!", "red")
        self.add_terminal_output("", "green")

        # Get first tutorial content
        content = self.tutorial_session.get_current_content()
        self.add_terminal_output(content.get("title", "Tutorial"), "yellow")
        self.add_terminal_output("", "green")
        
        # Display introduction content
        for line in content.get("explanation", []):
            self.add_terminal_output(line, "cyan")
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("🎯 READY TO BEGIN?", "yellow")
        self.add_terminal_output("This tutorial requires active participation and correct answers!", "yellow")
        self.add_terminal_output("Type 'begin', 'start', or 'ready' to show you're engaged.", "green")
        self.add_terminal_output("Type 'hint' for guidance or 'menu' to return.", "cyan")
        self.add_terminal_output("", "green")
        self.add_terminal_output("🚫 Remember: You CANNOT use 'next' to skip exercises!", "red")

        # Set explanation in right panel
        explanation_text = "\n".join(content.get("explanation", []))
        if explanation_text.strip():
            self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")

    def start_adventure(self):
        """Start the main Logic Quest adventure."""
        # Show complexity selection first if not shown yet
        if not self.complexity_selection_shown:
            self.pending_action = "adventure"
            self.show_complexity_selection_screen()
            return
            
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

    def reset_game(self):
        """Reset all game statistics to initial values."""
        # Reset game state
        self.current_screen = "welcome"
        self.game_mode = "menu"
        self.pending_action = ""
        
        # Reset complexity change state
        self.pending_complexity_change = ""
        self.awaiting_complexity_confirmation = False
        
        # Reset tutorial state
        self.tutorial_active = False
        self.tutorial_step = 0
        
        # Reset story and puzzle state
        self.player_level = 1
        self.player_score = 0
        self.concepts_learned = []
        
        # Reset complexity level state
        self.complexity_level = ComplexityLevel.BEGINNER
        self.complexity_selection_shown = False
        self.complexity_change_count = 0
        
        # Reset terminal state
        self.terminal_output = []
        self.terminal_colors = []
        self.user_input = ""
        
        # Reset right panel state
        self.right_panel_content = "Welcome to Logic Quest!\n\nType 'hint' for guidance."
        self.right_panel_color = "neon_green"
        self.right_panel_title = "SYSTEM INFO"
        
        # Reset hello world completion status
        self.hello_world_completed = False
        
        # Reset non-serializable objects
        self._tutorial_session = None
        self._story_engine = None
        self._puzzle_manager = None
        self._hello_world_puzzle = None
        self._complexity_manager = None
        self._complexity_help_system = None
        self._current_adventure_puzzle = None
        
        # Display confirmation message
        self.add_terminal_output("🔄 Game statistics have been reset to initial values.", "yellow")
        self.add_terminal_output("", "green")
        self.add_terminal_output("All progress, scores, and achievements cleared.", "cyan")
        self.add_terminal_output("Welcome back to Logic Quest!", "green")

    def exit_to_prolog_site(self):
        """Redirect to the official Prolog website."""
        return rx.redirect("https://www.swi-prolog.org/")

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
        # Check if we're in complexity change flow
        if self.awaiting_complexity_confirmation:
            self._handle_complexity_confirmation(input_text)
            return
        
        # Check if we're in complexity selection
        if self.pending_complexity_change or input_text.lower() in ["beginner", "intermediate", "advanced", "expert"]:
            if input_text.lower() == "complexity":
                self._show_complexity_change_menu()
                return
            self._handle_complexity_change_input(input_text)
            return
        
        # Handle global commands first
        if input_text.lower() == "hint":
            self._show_tutorial_hint()
            return
        elif input_text.lower() == "menu":
            self.return_to_menu()
            return
        elif input_text.lower() == "reset":
            self.reset_game()
            return
        elif input_text.lower() == "status":
            self._show_player_status()
            return
        elif input_text.lower() == "achievements":
            self._show_complexity_achievements()
            return
        elif input_text.lower().startswith("complexity"):
            self._handle_complexity_command(input_text)
            return
        elif input_text.lower() == "adventure" and self.tutorial_session.is_complete():
            # Transition to main adventure after tutorial completion
            self._transition_to_adventure()
            return
        
        # Get current tutorial step to determine if we're in an interactive exercise
        current_step = self.tutorial_session.navigator.current_step_index
        
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
            # Clear input and terminal, then advance to next step
            self.user_input = ""
            self.clear_terminal()
            if self.tutorial_session.advance_step():
                content = self.tutorial_session.get_current_content()
                self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                self.add_terminal_output("", "green")
                
                # Set explanation in right panel
                explanation_text = "\n".join(content.get("explanation", []))
                if explanation_text.strip():
                    self.set_right_panel(explanation_text, "neon_green", "TUTORIAL")
                
                # Show first interactive exercise prompt
                self.add_terminal_output("Now let's test your understanding with an interactive exercise!", "cyan")
                self.add_terminal_output("", "green")
        elif input_text.lower() in ["next", "continue", ""]:
            self.add_terminal_output("❌ This tutorial requires active participation!", "red")
            self.add_terminal_output("You cannot progress by typing 'next' or 'continue'.", "red")
            self.add_terminal_output("Type 'begin', 'start', or 'ready' to show you're engaged.", "yellow")
        else:
            self.add_terminal_output("❌ Invalid command for this tutorial step.", "red")
            self.add_terminal_output("Type 'begin', 'start', or 'ready' to continue, or 'hint' for guidance.", "yellow")

    def _handle_facts_explanation_input(self, input_text: str):
        """Handle input during facts explanation with component identification."""
        # This step requires component identification - route to HelloWorldPuzzle
        if hasattr(self, '_hello_world_puzzle') and self._hello_world_puzzle:
            result = self._hello_world_puzzle.handle_component_identification_input(input_text)
            if result == "completed":
                # Exercise completed, clear input and terminal, then advance to next step
                self.user_input = ""
                self.clear_terminal()
                if self.tutorial_session.advance_step():
                    content = self.tutorial_session.get_current_content()
                    self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                    self.add_terminal_output("", "green")
                    
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
                # Exercise completed, clear input and terminal, then advance to next step
                self.user_input = ""
                self.clear_terminal()
                if self.tutorial_session.advance_step():
                    content = self.tutorial_session.get_current_content()
                    self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                    self.add_terminal_output("", "green")
                    
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
                # Exercise completed, clear input and terminal, then advance to next step
                self.user_input = ""
                self.clear_terminal()
                if self.tutorial_session.advance_step():
                    content = self.tutorial_session.get_current_content()
                    self.add_terminal_output("🎯 " + content.get("title", ""), "yellow")
                    self.add_terminal_output("", "green")
                    
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
                # Exercise completed, clear input and terminal, then advance to next step
                self.user_input = ""
                self.clear_terminal()
                if self.tutorial_session.advance_step():
                    # Tutorial completed - mark completion and offer transition
                    self._complete_hello_world_tutorial()
        else:
            self.add_terminal_output("Tutorial system error. Type 'menu' to return.", "red")

    def _handle_completion_input(self, input_text: str):
        """Handle input during completion step."""
        if input_text.lower() == "adventure":
            # Clear input before transitioning
            self.user_input = ""
            self._transition_to_adventure()
        elif input_text.lower() in ["next", "continue", ""]:
            self.add_terminal_output("❌ Tutorial complete! No more 'next' commands needed.", "red")
            self.add_terminal_output("Type 'adventure' to start the main game or 'menu' to return.", "yellow")
        else:
            self.add_terminal_output("❌ Invalid command.", "red")
            self.add_terminal_output("Type 'adventure' to start the main game or 'menu' to return.", "yellow")

    def _handle_adventure_input(self, input_text: str):
        """Handle input during adventure mode."""
        # Check if we're in complexity change flow
        if self.awaiting_complexity_confirmation:
            self._handle_complexity_confirmation(input_text)
            return
        
        # Check if we're in complexity selection (after typing 'complexity')
        if self.pending_complexity_change or input_text.lower() in ["beginner", "intermediate", "advanced", "expert"]:
            # If we just typed 'complexity', show the menu first
            if input_text.lower() == "complexity":
                self._show_complexity_change_menu()
                return
            # Otherwise handle as complexity change input
            self._handle_complexity_change_input(input_text)
            return
        
        # Check if we're in an active puzzle
        if hasattr(self, '_current_adventure_puzzle') and self._current_adventure_puzzle:
            self._handle_puzzle_input(input_text)
            return
        
        if input_text.lower() == "menu":
            self.return_to_menu()
        elif input_text.lower() == "reset":
            self.reset_game()
        elif input_text.lower() == "help":
            self.add_terminal_output("Available commands:", "yellow")
            self.add_terminal_output("  help - Show this help", "green")
            self.add_terminal_output("  hint - Get guidance on what to do next", "green")
            self.add_terminal_output("  status - Show game status and progress", "green")
            self.add_terminal_output("  achievements - View complexity-based achievements", "green")
            self.add_terminal_output("  complexity - Change complexity level", "green")
            self.add_terminal_output("  complexity help - Comprehensive complexity help system", "green")
            self.add_terminal_output("  start puzzle - Begin the Memory Stack Investigation", "green")
            self.add_terminal_output("  reset - Reset all game statistics", "green")
            self.add_terminal_output("  menu - Return to main menu", "green")
            if not self.hello_world_completed:
                self.add_terminal_output("", "green")
                self.add_terminal_output("💡 New to Prolog? Consider starting with the", "yellow")
                self.add_terminal_output("   Hello World tutorial from the main menu!", "yellow")
        elif input_text.lower() == "hint":
            self._show_adventure_hint()
        elif input_text.lower() == "status":
            self._show_player_status()
        elif input_text.lower() == "achievements":
            self._show_complexity_achievements()
        elif input_text.lower().startswith("complexity"):
            self._handle_complexity_command(input_text)
        elif input_text.lower() in ["start puzzle", "start", "begin puzzle", "begin"]:
            # Launch the Memory Stack Failure puzzle
            self._launch_memory_stack_puzzle()
        elif input_text.lower() == "tutorial" and not self.hello_world_completed:
            # Allow quick access to tutorial from adventure mode
            self.add_terminal_output("Returning to main menu to access tutorial...", "cyan")
            self.return_to_menu()
        else:
            if not self.hello_world_completed:
                self.add_terminal_output(
                    "Unknown command. Type 'help' for commands or 'tutorial' to learn Prolog basics.", "yellow"
                )
            else:
                self.add_terminal_output(
                    "Unknown command. Type 'help' for available commands.", "yellow"
                )

    def _show_player_status(self):
        """Display comprehensive player status including complexity achievements."""
        progress = self.story_engine.get_player_progress()
        puzzle_stats = self.puzzle_manager.get_player_stats()
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("═══════════════════════════════════════", "cyan")
        self.add_terminal_output("         PLAYER STATUS REPORT", "yellow")
        self.add_terminal_output("═══════════════════════════════════════", "cyan")
        self.add_terminal_output("", "green")
        
        # Basic progress
        self.add_terminal_output("📊 OVERALL PROGRESS", "yellow")
        self.add_terminal_output(f"  Current Level: {progress['level']}", "green")
        self.add_terminal_output(f"  Total Score: {puzzle_stats['total_score']}", "green")
        self.add_terminal_output(f"  Puzzles Completed: {puzzle_stats['puzzles_completed']}", "green")
        self.add_terminal_output(
            f"  Concepts Learned: {len(progress['concepts_learned'])}", "green"
        )
        self.add_terminal_output("", "green")
        
        # Hello World status
        hello_world_status = "✅ Completed" if progress.get('hello_world_completed', False) else "❌ Not completed"
        self.add_terminal_output(f"🎓 Hello World Tutorial: {hello_world_status}", "cyan")
        self.add_terminal_output("", "green")
        
        # Current complexity level
        self.add_terminal_output("🎯 CURRENT COMPLEXITY LEVEL", "yellow")
        config = self.complexity_manager.get_current_config()
        self.add_terminal_output(
            f"  {config.ui_indicators.get('icon', '')} {config.name.upper()}", 
            "green"
        )
        self.add_terminal_output(f"  {config.description}", "cyan")
        self.add_terminal_output(f"  Scoring Multiplier: {config.scoring_multiplier}x", "green")
        self.add_terminal_output("", "green")
        
        # Complexity achievements summary
        self.add_terminal_output("🏆 COMPLEXITY ACHIEVEMENTS", "yellow")
        all_achievements = self.puzzle_manager.get_all_complexity_achievements()
        
        for level_name, achievements in all_achievements.items():
            if achievements["puzzles_completed"] > 0:
                level_config = self.complexity_manager.get_config(
                    ComplexityLevel[level_name]
                )
                icon = level_config.ui_indicators.get('icon', '')
                self.add_terminal_output(
                    f"  {icon} {level_name}: {achievements['puzzles_completed']} puzzles, "
                    f"{achievements['total_score']} points (avg: {achievements['average_score']:.1f})",
                    "green"
                )
        
        if puzzle_stats['puzzles_completed'] == 0:
            self.add_terminal_output("  No puzzles completed yet", "cyan")
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("Type 'achievements' for detailed achievement breakdown", "cyan")
        self.add_terminal_output("Type 'help' for available commands", "cyan")
        self.add_terminal_output("═══════════════════════════════════════", "cyan")
        
        # Update right panel with status summary
        status_text = f"""📊 PLAYER STATUS

Overall Progress:
• Level: {progress['level']}
• Total Score: {puzzle_stats['total_score']}
• Puzzles: {puzzle_stats['puzzles_completed']}
• Concepts: {len(progress['concepts_learned'])}

Current Complexity:
{config.ui_indicators.get('icon', '')} {config.name.upper()}
Multiplier: {config.scoring_multiplier}x

Type 'achievements' for detailed stats"""
        
        self.set_right_panel(status_text, "neon_green", "STATUS")

    def _show_complexity_achievements(self):
        """Display detailed complexity-based achievements."""
        all_achievements = self.puzzle_manager.get_all_complexity_achievements()
        puzzle_stats = self.puzzle_manager.get_player_stats()
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("═══════════════════════════════════════", "cyan")
        self.add_terminal_output("      COMPLEXITY ACHIEVEMENTS", "yellow")
        self.add_terminal_output("═══════════════════════════════════════", "cyan")
        self.add_terminal_output("", "green")
        
        # Show achievements for each complexity level
        for level in ComplexityLevel:
            level_name = level.name
            achievements = all_achievements[level_name]
            config = self.complexity_manager.get_config(level)
            icon = config.ui_indicators.get('icon', '')
            
            # Highlight current level
            is_current = level == self.complexity_level
            marker = "→" if is_current else " "
            
            self.add_terminal_output(
                f"{marker} {icon} {level_name}", 
                "yellow" if is_current else "cyan"
            )
            self.add_terminal_output(f"   {config.description}", "cyan")
            
            if achievements["puzzles_completed"] > 0:
                self.add_terminal_output(
                    f"   ✅ Puzzles Completed: {achievements['puzzles_completed']}", 
                    "green"
                )
                self.add_terminal_output(
                    f"   🏆 Total Score: {achievements['total_score']}", 
                    "green"
                )
                self.add_terminal_output(
                    f"   📊 Average Score: {achievements['average_score']:.1f}", 
                    "green"
                )
            else:
                self.add_terminal_output("   ❌ No puzzles completed at this level", "cyan")
            
            self.add_terminal_output("", "green")
        
        # Show completion history if available
        if puzzle_stats["puzzle_completion_history"]:
            self.add_terminal_output("📜 RECENT COMPLETIONS", "yellow")
            self.add_terminal_output("", "green")
            
            # Show last 5 completions
            recent_completions = puzzle_stats["puzzle_completion_history"][-5:]
            for completion in recent_completions:
                level_config = self.complexity_manager.get_config(
                    ComplexityLevel[completion["complexity_level"]]
                )
                icon = level_config.ui_indicators.get('icon', '')
                
                self.add_terminal_output(
                    f"  {icon} {completion['puzzle_title']} ({completion['complexity_level']})",
                    "cyan"
                )
                self.add_terminal_output(
                    f"     Score: {completion['score']} | "
                    f"Attempts: {completion['attempts']} | "
                    f"Hints: {completion['hints_used']}",
                    "green"
                )
            
            if len(puzzle_stats["puzzle_completion_history"]) > 5:
                self.add_terminal_output(
                    f"  ... and {len(puzzle_stats['puzzle_completion_history']) - 5} more",
                    "cyan"
                )
            
            self.add_terminal_output("", "green")
        
        self.add_terminal_output("═══════════════════════════════════════", "cyan")
        
        # Update right panel with achievement details
        achievement_text = """🏆 ACHIEVEMENTS

Track your progress across all complexity levels!

Each level has its own:
• Puzzle completion count
• Total score earned
• Average performance

Complete puzzles at higher complexity levels for bonus scoring multipliers!

Type 'status' for overall progress"""
        
        self.set_right_panel(achievement_text, "neon_yellow", "ACHIEVEMENTS")

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
        current_step = self.tutorial_session.navigator.current_step_index
        hints = {
            0: "This is an introduction to Prolog. Read the explanation, then type 'begin', 'start', or 'ready' to show engagement. DO NOT type 'next'!",
            1: "You need to identify components of a Prolog fact. Answer the specific questions about predicate, arguments, and punctuation. Type your answers, not 'next'!",
            2: "Write a complete Prolog fact that says 'Bob likes pizza'. Use the format: predicate(argument1, argument2). Type the actual fact, not 'next'!",
            3: "Write a query to ask if Alice likes chocolate. Remember to start with '?-' and end with a period. Type the actual query, not 'next'!",
            4: "Write a query using a variable (uppercase letter) to find what Alice likes. Example format: ?- likes(alice, X). Type the actual query, not 'next'!",
            5: "Tutorial complete! Type 'adventure' to start the main game or 'menu' to return. No more 'next' commands!"
        }
        
        hint_text = hints.get(current_step, "Follow the interactive exercise instructions.")
        self.set_right_panel(f"💡 INTERACTIVE TUTORIAL HINT\n\n{hint_text}\n\n🚫 IMPORTANT: This tutorial requires active participation and correct Prolog syntax. You CANNOT progress by typing 'next', 'continue', or pressing Enter. You must complete each hands-on exercise with the correct answers!", "neon_yellow", "HINT")

    def _complete_hello_world_tutorial(self):
        """Handle completion of the Hello World tutorial."""
        # Mark tutorial as completed in both systems
        self.story_engine.mark_hello_world_completed()
        self.puzzle_manager.player_stats["hello_world_completed"] = True
        self.hello_world_completed = True
        
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
        
        # If in a puzzle, delegate to puzzle hint system
        if hasattr(self, '_current_adventure_puzzle') and self._current_adventure_puzzle:
            hint_text = self._current_adventure_puzzle.request_hint()
            self.add_terminal_output("", "green")
            for line in hint_text.split("\n"):
                self.add_terminal_output(line, "cyan")
            self.set_right_panel(hint_text, "neon_yellow", "PUZZLE HINT")
            return
        
        # Provide contextual hints based on game state and hello world completion
        if self.hello_world_completed:
            hint_text = """💡 ADVANCED MISSION BRIEFING

Excellent work completing the tutorial! You now have the foundation needed for this mission.

You're at Cyberdyne Systems in 1985, tasked with repairing the LOGIC-1 AI system using your newly acquired Prolog skills.

Available commands:
• 'help' - Show all commands
• 'start puzzle' - Begin the Memory Stack Investigation
• 'status' - Check your progress
• 'menu' - Return to main menu

The AI system corruption goes deeper than basic facts and queries. You'll need to master advanced concepts to fully restore the system."""
        else:
            hint_text = """💡 GETTING STARTED

You're at Cyberdyne Systems in 1985, tasked with repairing the LOGIC-1 AI system.

💡 RECOMMENDATION: If you're new to Prolog, consider starting with the Hello World tutorial from the main menu first. It will teach you the basics you need for this mission.

Available commands:
• 'help' - Show all commands
• 'start puzzle' - Begin the Memory Stack Investigation
• 'status' - Check your progress
• 'menu' - Return to main menu

The AI system is waiting for you to begin the repair process."""
        
        self.set_right_panel(hint_text, "neon_yellow", "HINT")
    
    def _launch_memory_stack_puzzle(self):
        """Launch the Memory Stack Failure puzzle."""
        # Get the puzzle from the puzzle manager
        puzzle = self.puzzle_manager.get_puzzle("memory_stack_failure")
        
        if not puzzle:
            self.add_terminal_output("", "green")
            self.add_terminal_output("❌ Puzzle not available.", "red")
            self.add_terminal_output("The Memory Stack Investigation puzzle could not be loaded.", "yellow")
            return
        
        # Set complexity level on the puzzle
        puzzle.set_complexity_level(self.complexity_level)
        
        # Store as current puzzle
        self._current_adventure_puzzle = puzzle
        
        # Clear terminal and show puzzle description
        self.clear_terminal()
        
        # Display puzzle description
        description = puzzle.get_description()
        for line in description.split("\n"):
            if line.startswith("="):
                self.add_terminal_output(line, "cyan")
            elif line.startswith(">>>"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("INCIDENT") or line.startswith("DIAGNOSTIC") or line.startswith("PROLOG") or line.startswith("TERMINAL") or line.startswith("MENTOR"):
                self.add_terminal_output(line, "yellow")
            elif line.strip().startswith("•"):
                self.add_terminal_output(line, "green")
            else:
                self.add_terminal_output(line, "cyan")
        
        # Get initial context and display stack frame facts
        context = puzzle.get_initial_context()
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("📊 STACK TRACE DATA LOADED", "yellow")
        self.add_terminal_output(f"   {context['frame_count']} stack frames", "green")
        self.add_terminal_output(f"   {context['fact_count']} Prolog facts", "green")
        self.add_terminal_output("", "green")
        self.add_terminal_output("Type your Prolog queries to investigate the stack trace.", "cyan")
        self.add_terminal_output("Type 'hint' for guidance or 'exit puzzle' to return.", "cyan")
        
        # Update right panel with puzzle objective
        objective_text = f"""🔍 INVESTIGATION OBJECTIVE

{context['objective']}

AVAILABLE PREDICATES:
• frame/4 - Stack frame info
• calls/2 - Call relationships
• allocated/2 - Memory allocation
• param/3 - Function parameters
• status/2 - Frame status

COMMANDS:
• hint - Get investigation guidance
• diagnose <text> - Submit diagnosis
• exit puzzle - Return to adventure mode

Type queries to investigate!"""
        
        self.set_right_panel(objective_text, "neon_green", "INVESTIGATION")
    
    def _handle_puzzle_input(self, input_text: str):
        """
        Handle input during active puzzle.
        
        Routes input to the puzzle for query execution or diagnosis submission.
        Handles puzzle-specific commands like hints and exit.
        
        Validates: Requirements 2.2, 2.3, 4.1, 5.1
        """
        # Check for puzzle exit command
        if input_text.lower() in ["exit puzzle", "exit", "quit puzzle", "quit"]:
            self._exit_puzzle()
            return
        
        # Check for hint command
        if input_text.lower() == "hint":
            self._show_adventure_hint()
            return
        
        # Check for diagnosis submission
        if input_text.lower().startswith("diagnose "):
            # Let the puzzle handle it through validate_solution
            result = self._current_adventure_puzzle.validate_solution(input_text)
            self._display_puzzle_result(result)
            
            # Check if puzzle is completed
            if self._current_adventure_puzzle.completed:
                self._handle_puzzle_completion()
            return
        
        # Check if it's a query (starts with ?-)
        if input_text.strip().startswith("?-"):
            result = self._current_adventure_puzzle.validate_solution(input_text)
            self._display_puzzle_result(result)
            return
        
        # Unknown command in puzzle context
        self.add_terminal_output("", "green")
        self.add_terminal_output("❓ Unknown command in puzzle context.", "yellow")
        self.add_terminal_output("", "green")
        self.add_terminal_output("Available actions:", "cyan")
        self.add_terminal_output("  • Write a Prolog query: ?- predicate(args).", "green")
        self.add_terminal_output("  • Submit diagnosis: diagnose <your diagnosis>", "green")
        self.add_terminal_output("  • Request hint: hint", "green")
        self.add_terminal_output("  • Exit puzzle: exit puzzle", "green")
    
    def _display_puzzle_result(self, result):
        """
        Display the result of a puzzle query or diagnosis.
        
        Formats and displays query results, error messages, and story
        progression messages in the terminal.
        
        Validates: Requirements 2.3, 9.3
        """
        self.add_terminal_output("", "green")
        
        if result.is_valid:
            # Successful query or diagnosis
            if result.parsed_components and result.parsed_components.get("type") == "query":
                # Query result
                formatted_output = result.parsed_components.get("formatted_output", "")
                
                # Check if it's a significant discovery
                is_significant = result.parsed_components.get("is_significant", False)
                
                if is_significant:
                    # Highlight significant discoveries
                    self.add_terminal_output("🔍 SIGNIFICANT DISCOVERY!", "yellow")
                    self.add_terminal_output("", "green")
                
                # Display the formatted output
                for line in formatted_output.split("\n"):
                    if line.startswith(">>>"):
                        self.add_terminal_output(line, "yellow")
                    elif "MENTOR" in line:
                        self.add_terminal_output(line, "cyan")
                    else:
                        self.add_terminal_output(line, "green")
            
            elif result.parsed_components and result.parsed_components.get("type") == "diagnosis":
                # Diagnosis result
                feedback = result.parsed_components.get("feedback", "")
                is_correct = result.parsed_components.get("is_correct", False)
                
                if is_correct:
                    self.add_terminal_output("🎉 CORRECT DIAGNOSIS!", "yellow")
                    self.add_terminal_output("", "green")
                
                for line in feedback.split("\n"):
                    if is_correct:
                        self.add_terminal_output(line, "green")
                    else:
                        self.add_terminal_output(line, "yellow")
        else:
            # Error or invalid input
            error_message = result.error_message or "Invalid input."
            for line in error_message.split("\n"):
                if line.startswith("❌") or "Error" in line:
                    self.add_terminal_output(line, "red")
                elif line.startswith("💡") or "Suggestion" in line:
                    self.add_terminal_output(line, "yellow")
                else:
                    self.add_terminal_output(line, "cyan")
            
            if result.hint:
                self.add_terminal_output("", "green")
                self.add_terminal_output(f"💡 Hint: {result.hint}", "yellow")
    
    def _exit_puzzle(self):
        """Exit the current puzzle and return to adventure mode."""
        if hasattr(self, '_current_adventure_puzzle') and self._current_adventure_puzzle:
            puzzle_title = self._current_adventure_puzzle.title
            self._current_adventure_puzzle = None
            
            self.add_terminal_output("", "green")
            self.add_terminal_output(f"Exiting {puzzle_title}...", "cyan")
            self.add_terminal_output("", "green")
            self.add_terminal_output("Returning to adventure mode.", "green")
            self.add_terminal_output("Type 'help' for available commands.", "cyan")
            
            # Reset right panel
            self.set_right_panel(
                "You've returned to adventure mode.\n\nType 'start puzzle' to resume the investigation.",
                "neon_green",
                "ADVENTURE MODE"
            )
    
    def _handle_puzzle_completion(self):
        """
        Handle puzzle completion.
        
        Updates player progress, awards points, and provides completion feedback.
        
        Validates: Requirements 5.2, 5.4, 5.5
        """
        puzzle = self._current_adventure_puzzle
        
        # Calculate score using the puzzle's internal calculation
        score = puzzle._calculate_score()
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("=" * 70, "cyan")
        self.add_terminal_output("🎉 PUZZLE COMPLETE! 🎉", "yellow")
        self.add_terminal_output("=" * 70, "cyan")
        self.add_terminal_output("", "green")
        self.add_terminal_output(f"Puzzle: {puzzle.title}", "cyan")
        self.add_terminal_output(f"Score: {score} points", "green")
        self.add_terminal_output(f"Queries Made: {puzzle.attempts}", "cyan")
        self.add_terminal_output(f"Hints Used: {puzzle.hints_used}", "cyan")
        self.add_terminal_output("", "green")
        
        # Update player stats
        self.player_score += score
        
        # Add concepts learned
        new_concepts = ["debugging", "stack_traces", "logical_deduction"]
        for concept in new_concepts:
            if concept not in self.concepts_learned:
                self.concepts_learned.append(concept)
        
        self.add_terminal_output("🎓 New Concepts Mastered:", "yellow")
        for concept in new_concepts:
            self.add_terminal_output(f"   • {concept.replace('_', ' ').title()}", "green")
        
        self.add_terminal_output("", "green")
        self.add_terminal_output("Type 'status' to view your progress.", "cyan")
        self.add_terminal_output("Type 'menu' to return to the main menu.", "cyan")
        
        # Update right panel with completion summary
        completion_text = f"""🎊 PUZZLE COMPLETED!

{puzzle.title}

Final Score: {score}
Queries: {puzzle.attempts}
Hints: {puzzle.hints_used}

Concepts Mastered:
• Debugging
• Stack Traces
• Logical Deduction

Great work, investigator!"""
        
        self.set_right_panel(completion_text, "neon_yellow", "COMPLETION")
        
        # Clear current puzzle
        self._current_adventure_puzzle = None

    def _show_complexity_change_menu(self):
        """Show the complexity level change menu."""
        self.add_terminal_output("", "green")
        self.add_terminal_output("🎯 COMPLEXITY LEVEL SELECTION", "yellow")
        self.add_terminal_output("", "green")
        self.add_terminal_output(f"Current Level: {self.get_complexity_indicator()}", "cyan")
        self.add_terminal_output("", "green")
        self.add_terminal_output("Available Complexity Levels:", "yellow")
        self.add_terminal_output("", "green")
        
        # Display all available complexity levels
        for level in ComplexityLevel:
            config = self.complexity_manager.get_config(level)
            icon = config.ui_indicators.get('icon', '')
            is_current = level == self.complexity_level
            marker = "→" if is_current else " "
            
            self.add_terminal_output(
                f"{marker} {icon} {config.name.upper()}", 
                "green" if is_current else "cyan"
            )
            self.add_terminal_output(f"   {config.description}", "cyan")
            self.add_terminal_output("", "green")
        
        self.add_terminal_output("To change complexity level, type:", "yellow")
        self.add_terminal_output("  'beginner', 'intermediate', 'advanced', or 'expert'", "green")
        self.add_terminal_output("  'cancel' to return to game", "green")
        self.add_terminal_output("", "green")
        
        # Update right panel with complexity info
        info_text = """🎯 COMPLEXITY LEVEL CHANGE

You can adjust the difficulty level at any time during gameplay.

⚠️ IMPORTANT:
• Your progress and score will be preserved
• Future puzzles will adapt to the new level
• Current puzzle state remains unchanged

Choose a level that matches your skill and learning goals."""
        
        self.set_right_panel(info_text, "neon_yellow", "COMPLEXITY CHANGE")

    def _handle_complexity_change_input(self, input_text: str):
        """Handle input during complexity level change."""
        level_mapping = {
            "beginner": ComplexityLevel.BEGINNER,
            "intermediate": ComplexityLevel.INTERMEDIATE,
            "advanced": ComplexityLevel.ADVANCED,
            "expert": ComplexityLevel.EXPERT,
        }
        
        if input_text.lower() == "cancel":
            self.awaiting_complexity_confirmation = False
            self.pending_complexity_change = ""
            self.add_terminal_output("", "green")
            self.add_terminal_output("Complexity change cancelled.", "yellow")
            self.add_terminal_output("Type 'help' for available commands.", "cyan")
            return
        
        if input_text.lower() in level_mapping:
            new_level = level_mapping[input_text.lower()]
            
            # Check if it's the same as current level
            if new_level == self.complexity_level:
                self.add_terminal_output("", "green")
                self.add_terminal_output(f"You are already at {input_text.upper()} level.", "yellow")
                self.add_terminal_output("Type another level or 'cancel' to return.", "cyan")
                return
            
            # Store pending change and request confirmation
            self.pending_complexity_change = input_text.lower()
            self.awaiting_complexity_confirmation = True
            
            config = self.complexity_manager.get_config(new_level)
            self.add_terminal_output("", "green")
            self.add_terminal_output("⚠️  CONFIRM COMPLEXITY CHANGE", "yellow")
            self.add_terminal_output("", "green")
            self.add_terminal_output(f"Change to: {config.ui_indicators.get('icon', '')} {config.name.upper()}", "cyan")
            self.add_terminal_output(f"{config.description}", "cyan")
            self.add_terminal_output("", "green")
            self.add_terminal_output("Your progress and score will be preserved.", "green")
            self.add_terminal_output("", "green")
            self.add_terminal_output("Type 'yes' to confirm or 'no' to cancel.", "yellow")
        else:
            self.add_terminal_output("", "green")
            self.add_terminal_output("Invalid complexity level.", "red")
            self.add_terminal_output("Type 'beginner', 'intermediate', 'advanced', 'expert', or 'cancel'.", "yellow")

    def _handle_complexity_confirmation(self, input_text: str):
        """Handle confirmation of complexity level change with error handling and recovery."""
        if input_text.lower() == "yes":
            # Apply the complexity change
            level_mapping = {
                "beginner": ComplexityLevel.BEGINNER,
                "intermediate": ComplexityLevel.INTERMEDIATE,
                "advanced": ComplexityLevel.ADVANCED,
                "expert": ComplexityLevel.EXPERT,
            }
            
            new_level = level_mapping[self.pending_complexity_change]
            
            # Store current progress for preservation
            current_score = self.player_score
            current_level = self.player_level
            current_concepts = self.concepts_learned.copy()
            
            try:
                # Apply the change
                self.handle_complexity_change(new_level)
                
                # Verify progress preservation
                progress_preserved = True
                error_messages = []
                
                if self.player_score != current_score:
                    error_messages.append("Score was not preserved")
                    progress_preserved = False
                    
                if self.player_level != current_level:
                    error_messages.append("Level was not preserved")
                    progress_preserved = False
                    
                if self.concepts_learned != current_concepts:
                    error_messages.append("Concepts were not preserved")
                    progress_preserved = False
                
                # Reset confirmation state
                self.awaiting_complexity_confirmation = False
                self.pending_complexity_change = ""
                
                if progress_preserved:
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("✅ Complexity level changed successfully!", "green")
                    self.add_terminal_output("All progress has been preserved.", "cyan")
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("Type 'help' for available commands.", "cyan")
                else:
                    # Progress preservation failed - restore and notify
                    self.player_score = current_score
                    self.player_level = current_level
                    self.concepts_learned = current_concepts
                    
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("⚠️  Complexity level changed with warnings:", "yellow")
                    for msg in error_messages:
                        self.add_terminal_output(f"   • {msg}", "yellow")
                    self.add_terminal_output("", "green")
                    self.add_terminal_output("✅ Progress has been restored to previous state.", "green")
                    self.add_terminal_output("Type 'help' for available commands.", "cyan")
                    
            except Exception as e:
                # Critical failure - restore state and notify user
                self.player_score = current_score
                self.player_level = current_level
                self.concepts_learned = current_concepts
                
                self.awaiting_complexity_confirmation = False
                self.pending_complexity_change = ""
                
                self.add_terminal_output("", "green")
                self.add_terminal_output("❌ Failed to change complexity level.", "red")
                self.add_terminal_output("Your progress and current level have been preserved.", "cyan")
                self.add_terminal_output("", "green")
                self.add_terminal_output("You can try again with 'complexity' command.", "yellow")
                
                # Log the error
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Complexity change failed: {e}")
            
        elif input_text.lower() == "no":
            # Cancel the change
            self.awaiting_complexity_confirmation = False
            self.pending_complexity_change = ""
            
            self.add_terminal_output("", "green")
            self.add_terminal_output("Complexity change cancelled.", "yellow")
            self.add_terminal_output("Type 'complexity' to try again or 'help' for commands.", "cyan")
        else:
            self.add_terminal_output("", "green")
            self.add_terminal_output("Please type 'yes' to confirm or 'no' to cancel.", "yellow")
    
    def _handle_complexity_command(self, input_text: str):
        """Handle complexity-related commands including help system."""
        parts = input_text.lower().split()
        
        if len(parts) == 1:
            # Just 'complexity' - show change menu
            self._show_complexity_change_menu()
        elif len(parts) == 2:
            if parts[1] == "help":
                # 'complexity help' - show overview
                self._show_complexity_help_overview()
            elif parts[1] == "compare":
                # 'complexity compare' - show comparison
                self._show_complexity_comparison()
            elif parts[1] == "tips":
                # 'complexity tips' - show tips
                self._show_complexity_tips()
            elif parts[1] == "faq":
                # 'complexity faq' - show FAQ
                self._show_complexity_faq()
            elif parts[1] in ["beginner", "intermediate", "advanced", "expert"]:
                # Level selection
                self._handle_complexity_change_input(parts[1])
            else:
                self.add_terminal_output("", "green")
                self.add_terminal_output("Unknown complexity command.", "red")
                self.add_terminal_output("Type 'complexity help' for available commands.", "yellow")
        elif len(parts) == 3 and parts[1] == "help":
            # 'complexity help <level>' - show level-specific help
            level_name = parts[2].upper()
            try:
                level = ComplexityLevel[level_name]
                self._show_level_specific_help(level)
            except KeyError:
                self.add_terminal_output("", "green")
                self.add_terminal_output(f"Unknown complexity level: {parts[2]}", "red")
                self.add_terminal_output("Valid levels: beginner, intermediate, advanced, expert", "yellow")
        else:
            self.add_terminal_output("", "green")
            self.add_terminal_output("Invalid complexity command.", "red")
            self.add_terminal_output("Type 'complexity help' for available commands.", "yellow")
    
    def _show_complexity_help_overview(self):
        """Show the complexity help system overview."""
        help_text = self.complexity_help_system.get_complexity_overview()
        lines = format_help_for_terminal(help_text)
        
        self.add_terminal_output("", "green")
        for line in lines:
            if line.startswith("🎯") or line.startswith("═"):
                self.add_terminal_output(line, "cyan")
            elif line.startswith("🌱") or line.startswith("⚡") or line.startswith("🔥") or line.startswith("💀"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("💡"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("•") or line.startswith("   •"):
                self.add_terminal_output(line, "green")
            else:
                self.add_terminal_output(line, "cyan")
        
        # Update right panel
        self.set_right_panel(
            "Complexity Help System\n\nUse these commands:\n• complexity help\n• complexity compare\n• complexity tips\n• complexity faq\n• complexity help <level>",
            "neon_cyan",
            "HELP SYSTEM"
        )
    
    def _show_complexity_comparison(self):
        """Show the complexity level comparison."""
        comparison_text = self.complexity_help_system.get_complexity_comparison()
        lines = format_help_for_terminal(comparison_text)
        
        self.add_terminal_output("", "green")
        for line in lines:
            if line.startswith("🎯") or line.startswith("═"):
                self.add_terminal_output(line, "cyan")
            elif line.startswith("┌") or line.startswith("├") or line.startswith("└") or line.startswith("│"):
                self.add_terminal_output(line, "green")
            elif "FEATURE" in line or "LEARNING" in line:
                self.add_terminal_output(line, "yellow")
            else:
                self.add_terminal_output(line, "cyan")
        
        # Update right panel
        quick_ref = self.complexity_help_system.get_quick_reference(self.complexity_level)
        self.set_right_panel(quick_ref, "neon_green", "QUICK REFERENCE")
    
    def _show_complexity_tips(self):
        """Show complexity level tips and recommendations."""
        tips_text = self.complexity_help_system.get_complexity_tips()
        lines = format_help_for_terminal(tips_text)
        
        self.add_terminal_output("", "green")
        for line in lines:
            if line.startswith("🎯") or line.startswith("═"):
                self.add_terminal_output(line, "cyan")
            elif line.startswith("🌱") or line.startswith("⚡") or line.startswith("🔥") or line.startswith("💀"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("💡"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("   ✓"):
                self.add_terminal_output(line, "green")
            elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
                self.add_terminal_output(line, "yellow")
            else:
                self.add_terminal_output(line, "cyan")
        
        # Update right panel with contextual help
        contextual_help = self.complexity_help_system.get_contextual_help(
            self.complexity_level, 
            "selection"
        )
        self.set_right_panel(contextual_help, "neon_yellow", "TIPS")
    
    def _show_complexity_faq(self):
        """Show complexity level FAQ."""
        faq_text = self.complexity_help_system.get_faq()
        lines = format_help_for_terminal(faq_text)
        
        self.add_terminal_output("", "green")
        for line in lines:
            if line.startswith("🎯") or line.startswith("═"):
                self.add_terminal_output(line, "cyan")
            elif line.startswith("Q:"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("A:"):
                self.add_terminal_output(line, "green")
            else:
                self.add_terminal_output(line, "cyan")
        
        # Update right panel
        self.set_right_panel(
            "Frequently Asked Questions\n\nAll your complexity level questions answered!\n\nType 'complexity help' for more information.",
            "neon_cyan",
            "FAQ"
        )
    
    def _show_level_specific_help(self, level: ComplexityLevel):
        """Show detailed help for a specific complexity level."""
        help_text = self.complexity_help_system.get_level_specific_help(level)
        lines = format_help_for_terminal(help_text)
        
        self.add_terminal_output("", "green")
        for line in lines:
            if line.startswith("🌱") or line.startswith("⚡") or line.startswith("🔥") or line.startswith("💀"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("═"):
                self.add_terminal_output(line, "cyan")
            elif line.startswith("•"):
                self.add_terminal_output(line, "green")
            elif line.startswith("WHAT TO EXPECT") or line.startswith("BEST PRACTICES") or line.startswith("WHEN TO"):
                self.add_terminal_output(line, "yellow")
            elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
                self.add_terminal_output(line, "yellow")
            else:
                self.add_terminal_output(line, "cyan")
        
        # Update right panel with quick reference
        quick_ref = self.complexity_help_system.get_quick_reference(level)
        self.set_right_panel(quick_ref, "neon_green", f"{level.name} GUIDE")


def welcome_screen() -> rx.Component:
    """Welcome screen with game options and complexity awareness."""
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
                
                # Current complexity level indicator with preview button
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            neon_text("Current Complexity:", color="neon_cyan", size="sm"),
                            rx.text(
                                GameState.get_complexity_indicator,
                                style={
                                    "color": rx.cond(
                                        GameState.get_complexity_color == "neon_green", "#00ff00",
                                        rx.cond(
                                            GameState.get_complexity_color == "neon_cyan", "#00ffff",
                                            rx.cond(
                                                GameState.get_complexity_color == "neon_yellow", "#ffff00",
                                                rx.cond(
                                                    GameState.get_complexity_color == "neon_red", "#ff0040",
                                                    "#00ff00"
                                                )
                                            )
                                        )
                                    ),
                                    "font_family": "monospace",
                                    "font_size": "14px",
                                    "font_weight": "bold",
                                    "text_transform": "uppercase",
                                }
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            GameState.get_complexity_description,
                            style={
                                "color": "#00ffff",
                                "font_family": "monospace",
                                "font_size": "12px",
                                "text_align": "center",
                                "margin_top": "8px",
                                "opacity": "0.8",
                            }
                        ),
                        spacing="1",
                        align="center",
                    ),
                    style={
                        "border": rx.cond(
                            GameState.get_complexity_color == "neon_green", "1px solid #00ff00",
                            rx.cond(
                                GameState.get_complexity_color == "neon_cyan", "1px solid #00ffff",
                                rx.cond(
                                    GameState.get_complexity_color == "neon_yellow", "1px solid #ffff00",
                                    rx.cond(
                                        GameState.get_complexity_color == "neon_red", "1px solid #ff0040",
                                        "1px solid #00ff00"
                                    )
                                )
                            )
                        ),
                        "border_radius": "6px",
                        "padding": "12px 16px",
                        "margin": "10px 0",
                        "background": "rgba(0, 0, 0, 0.3)",
                    },
                ),
                
                # Recommendation box for new players
                rx.cond(
                    ~GameState.hello_world_completed & (GameState.get_complexity_name != "BEGINNER"),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("💡", style={"font_size": "16px"}),
                                neon_text("Recommendation for New Players", color="neon_yellow", size="sm"),
                                spacing="2",
                                align="center",
                            ),
                            rx.text(
                                "We recommend starting with BEGINNER complexity for your first playthrough. "
                                "You can change this anytime from the Complexity Settings.",
                                style={
                                    "color": "#ffff00",
                                    "font_family": "monospace",
                                    "font_size": "12px",
                                    "text_align": "center",
                                    "margin_top": "8px",
                                    "opacity": "0.9",
                                }
                            ),
                            spacing="1",
                            align="center",
                        ),
                        style={
                            "border": "1px solid #ffff00",
                            "border_radius": "6px",
                            "padding": "12px 16px",
                            "margin": "10px 0",
                            "background": "rgba(255, 255, 0, 0.1)",
                        },
                    ),
                    rx.box(),  # Empty box when not showing recommendation
                ),
                
                # Menu options - conditional based on hello world completion
                rx.cond(
                    GameState.hello_world_completed,
                    # Options when hello world is completed
                    rx.vstack(
                        # Main action buttons with complexity info
                        rx.vstack(
                            cyberpunk_button(
                                "Continue Main Adventure",
                                on_click=GameState.start_adventure,
                                color="neon_green",
                            ),
                            rx.text(
                                "Continue your journey at " + GameState.get_complexity_name + " level",
                                style={
                                    "color": "#00ff00",
                                    "font_family": "monospace",
                                    "font_size": "11px",
                                    "text_align": "center",
                                    "margin_top": "-8px",
                                    "opacity": "0.7",
                                }
                            ),
                            spacing="1",
                            align="center",
                        ),
                        cyberpunk_button(
                            "Review Hello World Tutorial",
                            on_click=GameState.start_tutorial,
                            color="neon_cyan",
                        ),
                        cyberpunk_button(
                            "Complexity Settings",
                            on_click=GameState.show_complexity_selection_screen,
                            color="neon_yellow",
                        ),
                        cyberpunk_button(
                            "Learn More About Prolog", 
                            on_click=GameState.exit_to_prolog_site,
                            color="neon_red"
                        ),
                        spacing="3",
                        align="center",
                    ),
                    # Options when hello world is not completed
                    rx.vstack(
                        # Tutorial button with recommendation
                        rx.vstack(
                            cyberpunk_button(
                                "Start Hello World Tutorial",
                                on_click=GameState.start_tutorial,
                                color="neon_green",
                            ),
                            rx.text(
                                "⭐ Recommended for first-time players",
                                style={
                                    "color": "#00ff00",
                                    "font_family": "monospace",
                                    "font_size": "11px",
                                    "text_align": "center",
                                    "margin_top": "-8px",
                                    "opacity": "0.7",
                                }
                            ),
                            spacing="1",
                            align="center",
                        ),
                        # Adventure button with complexity info
                        rx.vstack(
                            cyberpunk_button(
                                "Begin Main Adventure",
                                on_click=GameState.start_adventure,
                                color="neon_cyan",
                            ),
                            rx.text(
                                "Start at " + GameState.get_complexity_name + " level",
                                style={
                                    "color": "#00ffff",
                                    "font_family": "monospace",
                                    "font_size": "11px",
                                    "text_align": "center",
                                    "margin_top": "-8px",
                                    "opacity": "0.7",
                                }
                            ),
                            spacing="1",
                            align="center",
                        ),
                        cyberpunk_button(
                            "Complexity Settings",
                            on_click=GameState.show_complexity_selection_screen,
                            color="neon_yellow",
                        ),
                        cyberpunk_button(
                            "Learn More About Prolog", 
                            on_click=GameState.exit_to_prolog_site,
                            color="neon_red"
                        ),
                        spacing="3",
                        align="center",
                    ),
                ),
                
                # Footer - conditional message with complexity tip
                rx.cond(
                    GameState.hello_world_completed,
                    rx.vstack(
                        neon_text(
                            "Welcome back, logic programmer!", color="neon_yellow", size="sm"
                        ),
                        rx.text(
                            "Tip: Try a higher complexity level for more challenge!",
                            style={
                                "color": "#ffff00",
                                "font_family": "monospace",
                                "font_size": "11px",
                                "text_align": "center",
                                "opacity": "0.6",
                            }
                        ),
                        spacing="1",
                        align="center",
                    ),
                    rx.vstack(
                        neon_text(
                            "New to Prolog? Start with the tutorial!", color="neon_yellow", size="sm"
                        ),
                        rx.text(
                            "The tutorial adapts to your selected complexity level",
                            style={
                                "color": "#ffff00",
                                "font_family": "monospace",
                                "font_size": "11px",
                                "text_align": "center",
                                "opacity": "0.6",
                            }
                        ),
                        spacing="1",
                        align="center",
                    ),
                ),
                spacing="5",
                align="center",
            ),
            style={"max_width": "650px", "margin": "2rem auto"},
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
        # Header with complexity indicator
        rx.hstack(
            neon_text("LOGIC QUEST", color="neon_green", size="lg"),
            rx.spacer(),
            # Complexity indicator badge in header
            complexity_indicator_badge(
                icon=GameState.get_complexity_icon,
                level_name=GameState.get_complexity_name,
                color=GameState.get_complexity_color,
            ),
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
                    # Output area with auto-scroll
                    rx.box(
                        rx.foreach(
                            rx.Var.range(GameState.terminal_output.length()),
                            lambda i: render_terminal_line(
                                GameState.terminal_output[i], 
                                GameState.terminal_colors[i]
                            ),
                        ),
                        id="terminal-output",
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
                    complexity_indicator=complexity_indicator_badge(
                        icon=GameState.get_complexity_icon,
                        level_name=GameState.get_complexity_name,
                        color=GameState.get_complexity_color,
                    ),
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
        # Script to auto-scroll terminal to bottom when content changes
        rx.script("""
            // Auto-scroll terminal output to bottom
            const observer = new MutationObserver(() => {
                const terminal = document.getElementById('terminal-output');
                if (terminal) {
                    terminal.scrollTop = terminal.scrollHeight;
                }
            });
            
            // Start observing when the terminal element is available
            const checkTerminal = setInterval(() => {
                const terminal = document.getElementById('terminal-output');
                if (terminal) {
                    observer.observe(terminal, { childList: true, subtree: true });
                    terminal.scrollTop = terminal.scrollHeight;
                    clearInterval(checkTerminal);
                }
            }, 100);
        """),
        height="100vh",
        padding="1rem",
        spacing="0",
    )


def complexity_selection_page() -> rx.Component:
    """Complexity level selection page."""
    return complexity_selection_screen(
        current_level=GameState.get_complexity_name,
        on_level_select=GameState.select_complexity_level,
        on_continue=GameState.continue_from_complexity_selection,
        show_continue=True,
    )


def index() -> rx.Component:
    """Main application component."""
    return rx.box(
        rx.cond(
            GameState.current_screen == "welcome",
            welcome_screen(),
            rx.cond(
                GameState.current_screen == "complexity_selection",
                complexity_selection_page(),
                game_screen(),
            ),
        ),
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
