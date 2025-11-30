"""
Story Engine Module

Manages narrative flow, level progression, and story text
for the Logic Quest cyberpunk adventure.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from .complexity import ComplexityLevel, ExplanationDepth


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
    complexity_variants: Optional[Dict[ComplexityLevel, List[str]]] = None


class StoryEngine:
    """
    Manages narrative progression and story content delivery.

    Provides cyberpunk-themed story segments that introduce
    Prolog concepts within the game's narrative framework.
    """

    def __init__(self, complexity_level: ComplexityLevel = ComplexityLevel.BEGINNER):
        """Initialize the story engine with content."""
        self.current_level = GameLevel.TUTORIAL
        self.complexity_level = complexity_level
        self.story_segments = self._load_story_content()
        self.player_progress = {
            "name": "Junior Programmer",
            "level": 0,
            "score": 0,
            "concepts_learned": [],
            "story_flags": set(),
            "hello_world_completed": False,
        }

    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """Set the complexity level for story content adaptation."""
        self.complexity_level = level

    def get_complexity_level(self) -> ComplexityLevel:
        """Get the current complexity level."""
        return self.complexity_level

    def _get_complexity_appropriate_content(self, segment: StorySegment) -> List[str]:
        """Get content appropriate for the current complexity level."""
        if segment.complexity_variants and self.complexity_level in segment.complexity_variants:
            return segment.complexity_variants[self.complexity_level]
        return segment.content

    def _adapt_explanation_depth(self, base_content: List[str]) -> List[str]:
        """Adapt explanation depth based on complexity level."""
        depth = self._get_explanation_depth()
        
        if depth == ExplanationDepth.MINIMAL:
            # Keep only essential lines, remove detailed explanations
            return [line for line in base_content if line and not line.startswith("'")]
        elif depth == ExplanationDepth.BRIEF:
            # Keep main points, reduce verbosity
            return base_content[::2] if len(base_content) > 10 else base_content
        elif depth == ExplanationDepth.DETAILED:
            # Keep all content
            return base_content
        else:  # MODERATE
            return base_content

    def _get_explanation_depth(self) -> ExplanationDepth:
        """Get explanation depth based on complexity level."""
        depth_map = {
            ComplexityLevel.BEGINNER: ExplanationDepth.DETAILED,
            ComplexityLevel.INTERMEDIATE: ExplanationDepth.MODERATE,
            ComplexityLevel.ADVANCED: ExplanationDepth.BRIEF,
            ComplexityLevel.EXPERT: ExplanationDepth.MINIMAL,
        }
        return depth_map.get(self.complexity_level, ExplanationDepth.MODERATE)

    def _create_facts_intro(self) -> StorySegment:
        """Create Facts level intro with complexity variants."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                "You jack into the first memory bank. The screen flickers with",
                "fragments of data - basic facts about the world that the AI",
                "once knew with certainty.",
                "",
                "SYSTEM VOICE: 'Facts are the foundation of all logical reasoning.",
                "They are statements that are unconditionally true. Without facts,",
                "there can be no knowledge, no inference, no intelligence.'",
                "",
                "Think of facts like entries in a database - simple, direct statements.",
                "For example: 'The sky is blue' or 'Alice is a programmer.'",
                "",
                "The corrupted data streams past your eyes:",
                "- Employee records scattered",
                "- Relationship data fragmented",
                "- Basic truths lost in the digital void",
                "",
                "You must rebuild the fact database to restore the AI's",
                "fundamental understanding of reality.",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "You jack into the first memory bank. The screen flickers with",
                "fragments of data - basic facts about the world.",
                "",
                "SYSTEM VOICE: 'Facts are the foundation of logical reasoning.",
                "They are unconditionally true statements that form the knowledge base.'",
                "",
                "The corrupted data streams past:",
                "- Employee records scattered",
                "- Relationship data fragmented",
                "- Basic truths lost",
                "",
                "Rebuild the fact database to restore the AI's understanding.",
            ],
            ComplexityLevel.ADVANCED: [
                "Memory Bank Alpha. Facts database corrupted.",
                "",
                "SYSTEM: 'Facts form the knowledge base. Rebuild required.'",
                "",
                "Data corruption detected:",
                "- Records scattered",
                "- Relationships broken",
                "",
                "Restore the fact database.",
            ],
            ComplexityLevel.EXPERT: [
                "MEMORY BANK ALPHA",
                "Facts database: CORRUPTED",
                "",
                "Rebuild knowledge base.",
            ],
        }
        
        segment = StorySegment(
            title="MEMORY BANK ALPHA - FACTS DATABASE",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.FACTS,
            character="LOGIC-1 System",
            mood="mysterious",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def _create_rules_intro(self) -> StorySegment:
        """Create Rules level intro with complexity variants."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                "Deeper into the system, you encounter the inference engine.",
                "This is where the AI learned to make logical deductions,",
                "to derive new knowledge from existing facts.",
                "",
                "SYSTEM VOICE: 'Rules define relationships and implications.",
                "They allow reasoning beyond simple facts. If this, then that.",
                "The foundation of artificial intelligence itself.'",
                "",
                "Rules are like recipes - they tell the system how to combine",
                "facts to discover new information. For example:",
                "'If X is a parent of Y, and Y is a parent of Z, then X is a grandparent of Z.'",
                "",
                "The rule structures flicker unstably:",
                "- Conditional logic circuits sparking",
                "- Implication pathways severed",
                "- Deduction matrices corrupted",
                "",
                "You must repair the logical rules that allow the AI",
                "to think and reason about the world.",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "Deeper into the system, you encounter the inference engine.",
                "This is where the AI makes logical deductions.",
                "",
                "SYSTEM VOICE: 'Rules define relationships and implications.",
                "They enable reasoning beyond simple facts.'",
                "",
                "The rule structures flicker unstably:",
                "- Conditional logic circuits sparking",
                "- Implication pathways severed",
                "",
                "Repair the logical rules for AI reasoning.",
            ],
            ComplexityLevel.ADVANCED: [
                "Memory Bank Beta. Inference engine damaged.",
                "",
                "SYSTEM: 'Rules enable deduction. Repair required.'",
                "",
                "Logic circuits failing.",
                "",
                "Restore inference capabilities.",
            ],
            ComplexityLevel.EXPERT: [
                "MEMORY BANK BETA",
                "Inference engine: DAMAGED",
                "",
                "Restore deduction logic.",
            ],
        }
        
        segment = StorySegment(
            title="MEMORY BANK BETA - INFERENCE ENGINE",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.RULES,
            character="LOGIC-1 System",
            mood="mysterious",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def _create_unification_intro(self) -> StorySegment:
        """Create Unification level intro with complexity variants."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                "You've reached the pattern matching core - the heart of",
                "the AI's ability to find connections and similarities",
                "between different pieces of information.",
                "",
                "SYSTEM VOICE: 'Unification is the art of finding common",
                "patterns. It allows matching variables with values,",
                "connecting the abstract with the concrete.'",
                "",
                "Think of unification like solving a puzzle - finding which pieces",
                "fit together. Variables are like blank spaces that can be filled",
                "with specific values to make patterns match.",
                "",
                "The pattern matrices are in chaos:",
                "- Variable binding circuits overloaded",
                "- Matching algorithms fragmented",
                "- Pattern recognition failing",
                "",
                "Restore the unification engine to give the AI back",
                "its ability to recognize patterns and make connections.",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "You've reached the pattern matching core.",
                "",
                "SYSTEM VOICE: 'Unification finds common patterns.",
                "It matches variables with values, connecting abstract with concrete.'",
                "",
                "The pattern matrices are in chaos:",
                "- Variable binding circuits overloaded",
                "- Matching algorithms fragmented",
                "",
                "Restore pattern recognition capabilities.",
            ],
            ComplexityLevel.ADVANCED: [
                "Memory Bank Gamma. Pattern matching core unstable.",
                "",
                "SYSTEM: 'Unification enables pattern matching. Repair needed.'",
                "",
                "Variable binding failing.",
                "",
                "Restore unification engine.",
            ],
            ComplexityLevel.EXPERT: [
                "MEMORY BANK GAMMA",
                "Pattern matching: UNSTABLE",
                "",
                "Restore unification.",
            ],
        }
        
        segment = StorySegment(
            title="MEMORY BANK GAMMA - PATTERN MATCHING CORE",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.UNIFICATION,
            character="LOGIC-1 System",
            mood="mysterious",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def _create_backtracking_intro(self) -> StorySegment:
        """Create Backtracking level intro with complexity variants."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                "You've entered the search algorithm sector. This is where",
                "the AI learned to explore multiple possibilities,",
                "to backtrack when paths led nowhere.",
                "",
                "SYSTEM VOICE: 'Backtracking is the ability to explore",
                "alternative solutions. When one path fails, step back",
                "and try another. Persistence in the face of failure.'",
                "",
                "Imagine exploring a maze - when you hit a dead end, you go back",
                "to the last intersection and try a different path. That's backtracking!",
                "",
                "The search trees are collapsing:",
                "- Decision pathways tangled",
                "- Backtrack mechanisms jammed",
                "- Alternative solutions lost",
                "",
                "Repair the backtracking system to restore the AI's",
                "ability to systematically explore all possibilities.",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "You've entered the search algorithm sector.",
                "",
                "SYSTEM VOICE: 'Backtracking explores alternative solutions.",
                "When one path fails, try another.'",
                "",
                "The search trees are collapsing:",
                "- Decision pathways tangled",
                "- Backtrack mechanisms jammed",
                "",
                "Repair the backtracking system.",
            ],
            ComplexityLevel.ADVANCED: [
                "Memory Bank Delta. Search algorithms failing.",
                "",
                "SYSTEM: 'Backtracking enables solution exploration. Fix required.'",
                "",
                "Search trees collapsing.",
                "",
                "Restore backtracking.",
            ],
            ComplexityLevel.EXPERT: [
                "MEMORY BANK DELTA",
                "Search algorithms: FAILING",
                "",
                "Restore backtracking.",
            ],
        }
        
        segment = StorySegment(
            title="MEMORY BANK DELTA - SEARCH ALGORITHMS",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.BACKTRACKING,
            character="LOGIC-1 System",
            mood="mysterious",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def _create_recursion_intro(self) -> StorySegment:
        """Create Recursion level intro with complexity variants."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                "You've reached the deepest level - the recursive core.",
                "This is where the AI learned to solve complex problems",
                "by breaking them into smaller, similar pieces.",
                "",
                "SYSTEM VOICE: 'Recursion is the ultimate logical tool.",
                "To understand recursion, you must first understand recursion.",
                "Problems within problems, solutions within solutions.'",
                "",
                "Recursion is like Russian nesting dolls - each problem contains",
                "a smaller version of itself. You solve the smallest case first,",
                "then use that solution to solve bigger and bigger cases.",
                "",
                "The recursive structures are unstable:",
                "- Self-referential loops broken",
                "- Base cases corrupted",
                "- Infinite loops threatening system stability",
                "",
                "Master recursion to complete the AI's restoration",
                "and save Cyberdyne Systems from total collapse.",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "You've reached the deepest level - the recursive core.",
                "",
                "SYSTEM VOICE: 'Recursion solves complex problems",
                "by breaking them into smaller, similar pieces.'",
                "",
                "The recursive structures are unstable:",
                "- Self-referential loops broken",
                "- Base cases corrupted",
                "",
                "Master recursion to complete the restoration.",
            ],
            ComplexityLevel.ADVANCED: [
                "Memory Bank Epsilon. Recursive core unstable.",
                "",
                "SYSTEM: 'Recursion enables complex problem solving. Critical repair.'",
                "",
                "Self-referential loops broken.",
                "",
                "Restore recursive capabilities.",
            ],
            ComplexityLevel.EXPERT: [
                "MEMORY BANK EPSILON",
                "Recursive core: CRITICAL",
                "",
                "Restore recursion.",
            ],
        }
        
        segment = StorySegment(
            title="MEMORY BANK EPSILON - RECURSIVE CORE",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.RECURSION,
            character="LOGIC-1 System",
            mood="urgent",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def get_intro_story(self) -> StorySegment:
        """Get the opening story segment adapted to complexity level."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
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
                "Don't worry - I'll guide you through the basics step by step.",
                "Master its concepts, and you can save everything we've worked for.'",
                "",
                "The terminal flickers to life before you...",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "The year is 1985. Neon lights flicker outside your window as rain",
                "streaks down the glass of the Cyberdyne Systems building.",
                "",
                "You are a junior programmer working the night shift when alarms",
                "begin blaring throughout the facility.",
                "",
                "RED ALERT: LOGIC-1 AI SYSTEM MALFUNCTION",
                "CRITICAL ERROR: Logic circuits corrupted",
                "",
                "Your supervisor rushes over:",
                "",
                "'The LOGIC-1 computer has suffered a catastrophic logic failure.",
                "You need to dive into the system and restore the logical pathways",
                "using Prolog - the language of logic programming.'",
                "",
                "'You have some programming experience, so you should be able to",
                "handle this. Master the concepts and save our research.'",
                "",
                "The terminal flickers to life before you...",
            ],
            ComplexityLevel.ADVANCED: [
                "1985. Cyberdyne Systems. Night shift.",
                "",
                "RED ALERT: LOGIC-1 AI SYSTEM MALFUNCTION",
                "CRITICAL ERROR: Logic circuits corrupted",
                "",
                "Your supervisor: 'LOGIC-1 has failed. Restore the logical pathways",
                "using Prolog. You know what to do.'",
                "",
                "The terminal awaits your expertise...",
            ],
            ComplexityLevel.EXPERT: [
                "1985. Cyberdyne Systems.",
                "",
                "LOGIC-1 SYSTEM FAILURE",
                "Restore logic circuits. Prolog required.",
                "",
                "Terminal ready.",
            ],
        }
        
        segment = StorySegment(
            title="CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.TUTORIAL,
            character="Supervisor",
            mood="urgent",
            complexity_variants=complexity_variants,
        )
        
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def get_level_intro(self, level: GameLevel) -> StorySegment:
        """Get the introduction story for a specific level adapted to complexity."""
        intros = {
            GameLevel.FACTS: self._create_facts_intro(),
            GameLevel.RULES: self._create_rules_intro(),
            GameLevel.UNIFICATION: self._create_unification_intro(),
            GameLevel.BACKTRACKING: self._create_backtracking_intro(),
            GameLevel.RECURSION: self._create_recursion_intro(),
        }

        return intros.get(level, self._get_default_intro(level))

    def get_success_story(self, level: GameLevel) -> StorySegment:
        """Get the success story for completing a level adapted to complexity."""
        if level == GameLevel.RECURSION:
            complexity_variants = {
                ComplexityLevel.BEGINNER: [
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
                ComplexityLevel.INTERMEDIATE: [
                    "The final circuit clicks into place. Alarms fall silent.",
                    "",
                    "SYSTEM VOICE: 'Logic pathways restored. AI functions nominal.'",
                    "",
                    "Your supervisor: 'Excellent work! The LOGIC-1 system is operational.",
                    "You've mastered logic programming fundamentals.'",
                    "",
                    "Facts, rules, unification, backtracking, recursion - complete.",
                    "",
                    "CONGRATULATIONS - MISSION COMPLETE",
                ],
                ComplexityLevel.ADVANCED: [
                    "Final circuit restored. System online.",
                    "",
                    "SYSTEM: 'AI functions nominal.'",
                    "",
                    "Supervisor: 'Mission accomplished. Logic programming mastered.'",
                    "",
                    "MISSION COMPLETE",
                ],
                ComplexityLevel.EXPERT: [
                    "System restored.",
                    "AI operational.",
                    "",
                    "MISSION COMPLETE",
                ],
            }
            
            segment = StorySegment(
                title="SYSTEM RESTORATION COMPLETE",
                content=complexity_variants[ComplexityLevel.BEGINNER],
                level=GameLevel.RECURSION,
                character="Supervisor",
                mood="triumphant",
                complexity_variants=complexity_variants,
            )
            segment.content = self._get_complexity_appropriate_content(segment)
            return segment

        # Standard level completion
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                f"Memory bank restored! Logic circuits for {level.name.lower()} are online.",
                "Great work! The AI's reasoning grows stronger.",
                "You're making excellent progress. Continue to the next sector.",
            ],
            ComplexityLevel.INTERMEDIATE: [
                f"Memory bank restored. {level.name.lower()} circuits online.",
                "The AI's reasoning grows stronger. Continue to next sector.",
            ],
            ComplexityLevel.ADVANCED: [
                f"{level.name.lower()} circuits online.",
                "Continue.",
            ],
            ComplexityLevel.EXPERT: [
                f"{level.name}: ONLINE",
            ],
        }
        
        segment = StorySegment(
            title=f"LEVEL {level.value} COMPLETE",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=level,
            mood="neutral",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

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

    def mark_hello_world_completed(self) -> None:
        """Mark the Hello World tutorial as completed."""
        self.player_progress["hello_world_completed"] = True
        self.add_concept_learned("prolog_basics")
        self.add_concept_learned("facts")
        self.add_concept_learned("queries") 
        self.add_concept_learned("variables")

    def is_hello_world_completed(self) -> bool:
        """Check if Hello World tutorial has been completed."""
        return self.player_progress.get("hello_world_completed", False)

    def get_hello_world_transition_story(self) -> StorySegment:
        """Get story segment for transitioning from Hello World to main game."""
        complexity_variants = {
            ComplexityLevel.BEGINNER: [
                "🎉 Excellent work, programmer! You've mastered the basics of Prolog.",
                "",
                "The LOGIC-1 system has detected your newfound knowledge:",
                "",
                "SYSTEM ANALYSIS:",
                "✅ Facts comprehension: COMPLETE",
                "✅ Query formation: COMPLETE", 
                "✅ Variable usage: COMPLETE",
                "✅ Logic foundation: ESTABLISHED",
                "",
                "Your supervisor's voice crackles through the intercom:",
                "",
                "'Outstanding! You've proven you understand the fundamentals.",
                "Now it's time for the real challenge - the LOGIC-1 AI system",
                "is still malfunctioning, and we need you to dive deeper.'",
                "",
                "'The corruption goes beyond basic facts and queries. You'll need",
                "to master advanced concepts like rules, unification, backtracking,",
                "and recursion to fully restore the system.'",
                "",
                "'Are you ready to save Cyberdyne Systems and become a true",
                "logic programming expert?'",
                "",
                "The main terminal flickers to life, awaiting your command...",
            ],
            ComplexityLevel.INTERMEDIATE: [
                "Tutorial complete! You've grasped the Prolog basics.",
                "",
                "SYSTEM ANALYSIS:",
                "✅ Facts: COMPLETE",
                "✅ Queries: COMPLETE", 
                "✅ Variables: COMPLETE",
                "",
                "Supervisor: 'Good work! Now for the real challenge.",
                "Master rules, unification, backtracking, and recursion",
                "to restore the LOGIC-1 system.'",
                "",
                "Terminal ready...",
            ],
            ComplexityLevel.ADVANCED: [
                "Tutorial complete. Basics understood.",
                "",
                "Supervisor: 'Proceed to advanced concepts.",
                "Restore LOGIC-1 system.'",
                "",
                "Terminal ready.",
            ],
            ComplexityLevel.EXPERT: [
                "Tutorial: COMPLETE",
                "Proceed to system restoration.",
            ],
        }
        
        segment = StorySegment(
            title="TUTORIAL COMPLETE - READY FOR THE REAL CHALLENGE",
            content=complexity_variants[ComplexityLevel.BEGINNER],
            level=GameLevel.TUTORIAL,
            character="Supervisor",
            mood="triumphant",
            complexity_variants=complexity_variants,
        )
        segment.content = self._get_complexity_appropriate_content(segment)
        return segment

    def get_complexity_flavor_text(self, context: str) -> str:
        """Get complexity-specific cyberpunk flavor text for various contexts."""
        flavor_texts = {
            "puzzle_start": {
                ComplexityLevel.BEGINNER: "The terminal displays helpful guidance as you begin...",
                ComplexityLevel.INTERMEDIATE: "The terminal awaits your input...",
                ComplexityLevel.ADVANCED: "Terminal ready. Minimal assistance available.",
                ComplexityLevel.EXPERT: "Terminal ready.",
            },
            "hint_available": {
                ComplexityLevel.BEGINNER: "💡 HINT SYSTEM: Always available to guide you!",
                ComplexityLevel.INTERMEDIATE: "💡 HINT SYSTEM: Available on request.",
                ComplexityLevel.ADVANCED: "💡 HINT SYSTEM: Available after multiple attempts.",
                ComplexityLevel.EXPERT: "HINT SYSTEM: Disabled.",
            },
            "error_feedback": {
                ComplexityLevel.BEGINNER: "Don't worry! Let's analyze what went wrong and try again...",
                ComplexityLevel.INTERMEDIATE: "Error detected. Review your logic and retry.",
                ComplexityLevel.ADVANCED: "Error. Retry.",
                ComplexityLevel.EXPERT: "ERROR",
            },
            "success_feedback": {
                ComplexityLevel.BEGINNER: "🎉 Excellent work! You've solved it perfectly!",
                ComplexityLevel.INTERMEDIATE: "✅ Correct! Well done.",
                ComplexityLevel.ADVANCED: "✅ Correct.",
                ComplexityLevel.EXPERT: "✅",
            },
            "system_message": {
                ComplexityLevel.BEGINNER: "SYSTEM MESSAGE: I'm here to help you learn!",
                ComplexityLevel.INTERMEDIATE: "SYSTEM MESSAGE: Assistance available.",
                ComplexityLevel.ADVANCED: "SYSTEM: Limited assistance.",
                ComplexityLevel.EXPERT: "SYSTEM:",
            },
        }
        
        context_texts = flavor_texts.get(context, {})
        return context_texts.get(self.complexity_level, "")

    def get_tutorial_content_for_complexity(self, concept: str) -> List[str]:
        """Get tutorial content adapted to complexity level for a specific concept."""
        tutorials = {
            "facts": {
                ComplexityLevel.BEGINNER: [
                    "TUTORIAL: Understanding Facts",
                    "",
                    "Facts are the building blocks of Prolog. They're simple statements",
                    "that are always true. Think of them like entries in a database.",
                    "",
                    "Example: parent(tom, bob).",
                    "This means 'Tom is a parent of Bob'",
                    "",
                    "Facts always end with a period (.) and use lowercase names.",
                    "The format is: predicate(argument1, argument2, ...).",
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "TUTORIAL: Facts",
                    "",
                    "Facts are unconditionally true statements in Prolog.",
                    "Format: predicate(arguments).",
                    "",
                    "Example: parent(tom, bob).",
                ],
                ComplexityLevel.ADVANCED: [
                    "Facts: predicate(args).",
                    "Example: parent(tom, bob).",
                ],
                ComplexityLevel.EXPERT: [
                    "Facts: predicate(args).",
                ],
            },
            "queries": {
                ComplexityLevel.BEGINNER: [
                    "TUTORIAL: Making Queries",
                    "",
                    "Queries ask questions about your facts. They start with ?-",
                    "",
                    "Example: ?- parent(tom, bob).",
                    "This asks 'Is Tom a parent of Bob?'",
                    "",
                    "You can use variables (starting with uppercase) to find answers:",
                    "?- parent(tom, X).",
                    "This asks 'Who are Tom's children?'",
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "TUTORIAL: Queries",
                    "",
                    "Queries ask questions. Format: ?- predicate(args).",
                    "Use variables (uppercase) to find values.",
                    "",
                    "Example: ?- parent(tom, X).",
                ],
                ComplexityLevel.ADVANCED: [
                    "Queries: ?- predicate(args).",
                    "Variables: Uppercase.",
                ],
                ComplexityLevel.EXPERT: [
                    "Queries: ?- predicate(args).",
                ],
            },
            "rules": {
                ComplexityLevel.BEGINNER: [
                    "TUTORIAL: Understanding Rules",
                    "",
                    "Rules let you define relationships and make deductions.",
                    "They have a head (conclusion) and a body (conditions).",
                    "",
                    "Format: head :- body.",
                    "",
                    "Example: grandparent(X, Z) :- parent(X, Y), parent(Y, Z).",
                    "This means 'X is a grandparent of Z if X is a parent of Y",
                    "and Y is a parent of Z'",
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "TUTORIAL: Rules",
                    "",
                    "Rules define relationships. Format: head :- body.",
                    "",
                    "Example: grandparent(X, Z) :- parent(X, Y), parent(Y, Z).",
                ],
                ComplexityLevel.ADVANCED: [
                    "Rules: head :- body.",
                    "Example: grandparent(X, Z) :- parent(X, Y), parent(Y, Z).",
                ],
                ComplexityLevel.EXPERT: [
                    "Rules: head :- body.",
                ],
            },
        }
        
        concept_tutorials = tutorials.get(concept, {})
        return concept_tutorials.get(self.complexity_level, [])

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
