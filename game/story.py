"""
Story Engine Module

Manages narrative flow, level progression, and story text
for the Logic Quest cyberpunk adventure.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class GameLevel(Enum):
    """Game progression levels."""

    TUTORIAL = 0
    FACTS = 1
    RULES = 2
    UNIFICATION = 3
    BACKTRACKING = 4
    RECURSION = 5


@dataclass
class StorySegment:
    """A segment of story content with metadata."""

    title: str
    content: List[str]
    level: GameLevel
    character: Optional[str] = None
    mood: str = "neutral"  # neutral, urgent, mysterious, triumphant


class StoryEngine:
    """
    Manages narrative progression and story content delivery.

    Provides cyberpunk-themed story segments that introduce
    Prolog concepts within the game's narrative framework.
    """

    def __init__(self):
        """Initialize the story engine with content."""
        self.current_level = GameLevel.TUTORIAL
        self.story_segments = self._load_story_content()
        self.player_progress = {
            "name": "Junior Programmer",
            "level": 0,
            "score": 0,
            "concepts_learned": [],
            "story_flags": set(),
        }

    def get_intro_story(self) -> StorySegment:
        """Get the opening story segment."""
        return StorySegment(
            title="CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL",
            content=[
                "The year is 1985. Neon lights flicker outside your window as rain",
                "streaks down the glass of the Cyberdyne Systems building.",
                "",
                "You are a junior programmer, fresh out of college, working the",
                "night shift when suddenly alarms begin blaring throughout the facility.",
                "",
                "RED ALERT: LOGIC-1 AI SYSTEM MALFUNCTION",
                "CRITICAL ERROR: Logic circuits corrupted",
                "ESTIMATED TIME TO TOTAL SYSTEM FAILURE: 4 hours",
                "",
                "Your supervisor rushes over, panic in their eyes:",
                "",
                "'Listen carefully - the LOGIC-1 computer that runs our AI research",
                "has suffered a catastrophic logic failure. The reasoning circuits",
                "are scrambled, and we're losing data fast.'",
                "",
                "'You're our only hope. You need to dive into the system's memory",
                "banks and restore the logical pathways. But be warned - you'll need",
                "to think like the machine itself, using pure logical reasoning.'",
                "",
                "'The system speaks in Prolog - the language of logic programming.",
                "Master its concepts, and you can save everything we've worked for.'",
                "",
                "The terminal flickers to life before you...",
            ],
            level=GameLevel.TUTORIAL,
            character="Supervisor",
            mood="urgent",
        )

    def get_level_intro(self, level: GameLevel) -> StorySegment:
        """Get the introduction story for a specific level."""
        intros = {
            GameLevel.FACTS: StorySegment(
                title="MEMORY BANK ALPHA - FACTS DATABASE",
                content=[
                    "You jack into the first memory bank. The screen flickers with",
                    "fragments of data - basic facts about the world that the AI",
                    "once knew with certainty.",
                    "",
                    "SYSTEM VOICE: 'Facts are the foundation of all logical reasoning.",
                    "They are statements that are unconditionally true. Without facts,",
                    "there can be no knowledge, no inference, no intelligence.'",
                    "",
                    "The corrupted data streams past your eyes:",
                    "- Employee records scattered",
                    "- Relationship data fragmented",
                    "- Basic truths lost in the digital void",
                    "",
                    "You must rebuild the fact database to restore the AI's",
                    "fundamental understanding of reality.",
                ],
                level=GameLevel.FACTS,
                character="LOGIC-1 System",
                mood="mysterious",
            ),
            GameLevel.RULES: StorySegment(
                title="MEMORY BANK BETA - INFERENCE ENGINE",
                content=[
                    "Deeper into the system, you encounter the inference engine.",
                    "This is where the AI learned to make logical deductions,",
                    "to derive new knowledge from existing facts.",
                    "",
                    "SYSTEM VOICE: 'Rules define relationships and implications.",
                    "They allow reasoning beyond simple facts. If this, then that.",
                    "The foundation of artificial intelligence itself.'",
                    "",
                    "The rule structures flicker unstably:",
                    "- Conditional logic circuits sparking",
                    "- Implication pathways severed",
                    "- Deduction matrices corrupted",
                    "",
                    "You must repair the logical rules that allow the AI",
                    "to think and reason about the world.",
                ],
                level=GameLevel.RULES,
                character="LOGIC-1 System",
                mood="mysterious",
            ),
            GameLevel.UNIFICATION: StorySegment(
                title="MEMORY BANK GAMMA - PATTERN MATCHING CORE",
                content=[
                    "You've reached the pattern matching core - the heart of",
                    "the AI's ability to find connections and similarities",
                    "between different pieces of information.",
                    "",
                    "SYSTEM VOICE: 'Unification is the art of finding common",
                    "patterns. It allows matching variables with values,",
                    "connecting the abstract with the concrete.'",
                    "",
                    "The pattern matrices are in chaos:",
                    "- Variable binding circuits overloaded",
                    "- Matching algorithms fragmented",
                    "- Pattern recognition failing",
                    "",
                    "Restore the unification engine to give the AI back",
                    "its ability to recognize patterns and make connections.",
                ],
                level=GameLevel.UNIFICATION,
                character="LOGIC-1 System",
                mood="mysterious",
            ),
            GameLevel.BACKTRACKING: StorySegment(
                title="MEMORY BANK DELTA - SEARCH ALGORITHMS",
                content=[
                    "You've entered the search algorithm sector. This is where",
                    "the AI learned to explore multiple possibilities,",
                    "to backtrack when paths led nowhere.",
                    "",
                    "SYSTEM VOICE: 'Backtracking is the ability to explore",
                    "alternative solutions. When one path fails, step back",
                    "and try another. Persistence in the face of failure.'",
                    "",
                    "The search trees are collapsing:",
                    "- Decision pathways tangled",
                    "- Backtrack mechanisms jammed",
                    "- Alternative solutions lost",
                    "",
                    "Repair the backtracking system to restore the AI's",
                    "ability to systematically explore all possibilities.",
                ],
                level=GameLevel.BACKTRACKING,
                character="LOGIC-1 System",
                mood="mysterious",
            ),
            GameLevel.RECURSION: StorySegment(
                title="MEMORY BANK EPSILON - RECURSIVE CORE",
                content=[
                    "You've reached the deepest level - the recursive core.",
                    "This is where the AI learned to solve complex problems",
                    "by breaking them into smaller, similar pieces.",
                    "",
                    "SYSTEM VOICE: 'Recursion is the ultimate logical tool.",
                    "To understand recursion, you must first understand recursion.",
                    "Problems within problems, solutions within solutions.'",
                    "",
                    "The recursive structures are unstable:",
                    "- Self-referential loops broken",
                    "- Base cases corrupted",
                    "- Infinite loops threatening system stability",
                    "",
                    "Master recursion to complete the AI's restoration",
                    "and save Cyberdyne Systems from total collapse.",
                ],
                level=GameLevel.RECURSION,
                character="LOGIC-1 System",
                mood="urgent",
            ),
        }

        return intros.get(level, self._get_default_intro(level))

    def get_success_story(self, level: GameLevel) -> StorySegment:
        """Get the success story for completing a level."""
        if level == GameLevel.RECURSION:
            return StorySegment(
                title="SYSTEM RESTORATION COMPLETE",
                content=[
                    "The final circuit clicks into place. Throughout the facility,",
                    "lights stop flickering and alarms fall silent.",
                    "",
                    "SYSTEM VOICE: 'Logic pathways restored. Reasoning circuits online.",
                    "Artificial intelligence functions nominal. Thank you, programmer.'",
                    "",
                    "Your supervisor appears on the screen, relief flooding their face:",
                    "",
                    "'You did it! The LOGIC-1 system is fully operational again.",
                    "You've not only saved our research, but you've mastered",
                    "the fundamental concepts of logic programming.'",
                    "",
                    "'Facts, rules, unification, backtracking, recursion - you",
                    "understand them all. You're no longer a junior programmer.",
                    "You're a logic programming expert.'",
                    "",
                    "Outside, the neon-soaked city of 1985 continues its digital",
                    "dreams, unaware that you've just prevented an AI catastrophe",
                    "and learned the secrets of logical reasoning.",
                    "",
                    "CONGRATULATIONS - MISSION COMPLETE",
                ],
                level=GameLevel.RECURSION,
                character="Supervisor",
                mood="triumphant",
            )

        return StorySegment(
            title=f"LEVEL {level.value} COMPLETE",
            content=[
                f"Memory bank restored. Logic circuits for {level.name.lower()} are online.",
                "The AI's reasoning grows stronger. Continue to the next sector.",
            ],
            level=level,
            mood="neutral",
        )

    def advance_level(self) -> bool:
        """
        Advance to the next game level.

        Returns:
            True if advanced successfully, False if at max level
        """
        current_value = self.current_level.value
        max_value = max(level.value for level in GameLevel)

        if current_value < max_value:
            self.current_level = GameLevel(current_value + 1)
            self.player_progress["level"] = current_value + 1
            return True
        return False

    def add_concept_learned(self, concept: str):
        """Add a concept to the player's learned concepts."""
        if concept not in self.player_progress["concepts_learned"]:
            self.player_progress["concepts_learned"].append(concept)

    def set_story_flag(self, flag: str):
        """Set a story flag for tracking narrative state."""
        self.player_progress["story_flags"].add(flag)

    def has_story_flag(self, flag: str) -> bool:
        """Check if a story flag is set."""
        return flag in self.player_progress["story_flags"]

    def get_player_progress(self) -> Dict[str, Any]:
        """Get current player progress."""
        return self.player_progress.copy()

    def _load_story_content(self) -> Dict[GameLevel, List[StorySegment]]:
        """Load all story content into memory."""
        # This would load from files in a full implementation
        return {}

    def _get_default_intro(self, level: GameLevel) -> StorySegment:
        """Get a default intro for levels without specific content."""
        return StorySegment(
            title=f"LEVEL {level.value} - {level.name}",
            content=[
                f"Entering {level.name.lower()} sector...",
                "System diagnostics in progress...",
            ],
            level=level,
            mood="neutral",
        )
