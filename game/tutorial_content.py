"""
Tutorial Content Data Structures

This module contains the tutorial content definitions, progress tracking,
and navigation logic for the Hello World Prolog Challenge.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class TutorialStep(Enum):
    """Enumeration of tutorial steps for type safety and navigation."""

    INTRODUCTION = "introduction"
    FACTS_EXPLANATION = "facts_explanation"
    FACT_CREATION = "fact_creation"
    QUERIES_EXPLANATION = "queries_explanation"
    VARIABLES_INTRODUCTION = "variables_introduction"
    COMPLETION = "completion"


@dataclass
class TutorialProgress:
    """
    Tracks user advancement through the Hello World Prolog tutorial.

    Attributes:
        current_step: Current tutorial step index
        completed_steps: List of completed step names
        user_facts: Facts created by the user during exercises
        user_queries: Queries written by the user during exercises
        mistakes_count: Total number of syntax errors made
        hints_used: Number of hints requested or automatically shown
        start_time: When the tutorial was started (for analytics)
        step_completion_times: Time spent on each step
    """

    current_step: int = 0
    completed_steps: List[str] = field(default_factory=list)
    user_facts: List[str] = field(default_factory=list)
    user_queries: List[str] = field(default_factory=list)
    mistakes_count: int = 0
    hints_used: int = 0
    start_time: Optional[float] = None
    step_completion_times: Dict[str, float] = field(default_factory=dict)

    def mark_step_complete(self, step_name: str) -> None:
        """Mark a tutorial step as completed."""
        if step_name not in self.completed_steps:
            self.completed_steps.append(step_name)

    def is_step_completed(self, step_name: str) -> bool:
        """Check if a specific step has been completed."""
        return step_name in self.completed_steps

    def add_user_fact(self, fact: str) -> None:
        """Record a fact created by the user."""
        self.user_facts.append(fact)

    def add_user_query(self, query: str) -> None:
        """Record a query written by the user."""
        self.user_queries.append(query)

    def increment_mistakes(self) -> None:
        """Increment the mistake counter."""
        self.mistakes_count += 1

    def increment_hints(self) -> None:
        """Increment the hints used counter."""
        self.hints_used += 1

    def get_completion_percentage(self) -> float:
        """Calculate tutorial completion percentage."""
        total_steps = len(TUTORIAL_CONTENT)
        return (len(self.completed_steps) / total_steps) * 100 if total_steps > 0 else 0


# Tutorial content dictionary with all step definitions
TUTORIAL_CONTENT: Dict[str, Dict[str, Any]] = {
    "introduction": {
        "title": "🚀 Welcome to Prolog Programming",
        "subtitle": "Your Journey into Logic Programming Begins",
        "explanation": [
            "Welcome to the world of Prolog - a unique programming language that thinks differently!",
            "",
            "Unlike traditional programming languages that tell the computer HOW to solve problems,",
            "Prolog lets you describe WHAT the problem is, and it figures out the solution.",
            "",
            "🔮 In Prolog, you work with three main concepts:",
            "   • FACTS - Things that are unconditionally true",
            "   • RULES - Logical relationships and conditions",
            "   • QUERIES - Questions you ask the system",
            "",
            "Think of it like being a detective 🕵️ - you gather facts, establish rules,",
            "and then ask questions to solve mysteries!",
            "",
            "This tutorial will teach you the absolute basics step by step.",
            "Don't worry if it seems strange at first - that's completely normal!",
        ],
        "cyberpunk_flavor": [
            "🌆 CYBERDYNE SYSTEMS - LOGIC TRAINING MODULE",
            "📡 Initializing Prolog neural interface...",
            "🔋 Logic circuits: ONLINE",
            "🧠 Preparing to upload knowledge directly to your brain...",
            "",
            "In the neon-lit world of 1985, logic programming is the key",
            "to unlocking the secrets of artificial intelligence.",
            "Are you ready to jack into the matrix of pure logic?",
        ],
        "continue_prompt": "Press ENTER to begin your Prolog journey...",
    },
    "facts_explanation": {
        "title": "📋 Your First Prolog Fact",
        "subtitle": "The Building Blocks of Logic",
        "explanation": [
            "Let's start with the simplest building block in Prolog: FACTS.",
            "",
            "A fact is something that is unconditionally true. It's like saying:",
            "'The sky is blue' or 'Alice likes chocolate'",
            "",
            "🔍 Here's how we write facts in Prolog:",
            "",
            "   likes(alice, chocolate).",
            "",
            "Let's break this down:",
            "   • 'likes' is the PREDICATE (the relationship)",
            "   • 'alice' and 'chocolate' are ARGUMENTS (the things involved)",
            "   • The period (.) at the end is REQUIRED - it's like a full stop",
            "",
            "📝 The pattern is always: predicate(argument1, argument2, ...).",
            "",
            "More examples:",
            "   parent(tom, bob).     ← Tom is Bob's parent",
            "   employee(sarah, tech_corp).  ← Sarah works at Tech Corp",
            "   color(grass, green).  ← Grass is green",
        ],
        "examples": [
            "likes(alice, chocolate).",
            "parent(tom, bob).",
            "employee(sarah, tech_corp).",
            "color(grass, green).",
            "owns(john, car).",
        ],
        "practice_exercise": {
            "prompt": "Now it's your turn! Can you identify the parts of this fact?",
            "example_fact": "loves(romeo, juliet).",
            "questions": [
                "What is the predicate (relationship) in this fact?",
                "What are the two arguments?",
                "What punctuation mark ends the fact?",
            ],
            "answers": ["loves", "romeo and juliet", "period (.)"],
        },
        "continue_prompt": "Press ENTER when you're ready to create your own fact...",
    },
    "fact_creation": {
        "title": "✍️ Create Your First Fact",
        "subtitle": "Time to Write Some Prolog!",
        "explanation": [
            "Now comes the fun part - creating your very own Prolog fact!",
            "",
            "Remember the pattern: predicate(argument1, argument2).",
            "",
            "🎯 Let's practice with a specific scenario:",
            "Write a fact that says 'Bob likes pizza'",
            "",
            "💡 Hints to remember:",
            "   • Predicate names start with lowercase letters",
            "   • Arguments go inside parentheses",
            "   • Separate multiple arguments with commas",
            "   • Always end with a period (.)",
            "",
            "Don't worry if you make mistakes - that's how we learn!",
            "I'll help you fix any syntax errors.",
        ],
        "exercise_prompt": "Write a fact that says 'Bob likes pizza':",
        "expected_pattern": "likes(bob, pizza).",
        "alternative_answers": [
            "likes(bob, pizza).",
            "enjoys(bob, pizza).",
            "loves(bob, pizza).",
        ],
        "validation_hints": [
            "Remember: predicate(argument1, argument2).",
            "The predicate should describe the relationship (like 'likes')",
            "Don't forget the period at the end!",
            "Make sure 'bob' and 'pizza' are the arguments",
        ],
        "success_message": [
            "🎉 Excellent! You've created your first Prolog fact!",
            "",
            "Your fact tells the Prolog system that it's true that Bob likes pizza.",
            "This fact is now part of the 'knowledge base' - the collection of",
            "things that Prolog knows to be true.",
            "",
            "Next, we'll learn how to ask questions about these facts!",
        ],
    },
    "queries_explanation": {
        "title": "❓ Asking Questions with Queries",
        "subtitle": "How to Talk to Prolog",
        "explanation": [
            "Now that we have facts, let's learn how to ask questions about them!",
            "",
            "In Prolog, questions are called QUERIES. They start with '?-'",
            "",
            "🔍 If we have the fact: likes(alice, chocolate).",
            "We can ask: ?- likes(alice, chocolate).",
            "",
            "Prolog will answer 'yes' (or 'true') because this matches our fact exactly.",
            "",
            "📝 Query pattern: ?- predicate(argument1, argument2).",
            "",
            "Let's see some examples:",
            "   Facts we know:",
            "   likes(alice, chocolate).",
            "   likes(bob, pizza).",
            "   parent(tom, bob).",
            "",
            "   Queries we can ask:",
            "   ?- likes(alice, chocolate).  ← Answer: yes",
            "   ?- likes(bob, pizza).        ← Answer: yes",
            "   ?- likes(alice, pizza).      ← Answer: no",
            "   ?- parent(tom, bob).         ← Answer: yes",
        ],
        "examples": [
            "?- likes(alice, chocolate).",
            "?- parent(tom, bob).",
            "?- employee(sarah, tech_corp).",
            "?- owns(john, car).",
        ],
        "practice_exercise": {
            "prompt": "Given the fact: likes(bob, pizza).",
            "instruction": "Write a query to ask if Bob likes pizza:",
            "expected_answer": "?- likes(bob, pizza).",
            "explanation": "Perfect! The '?-' tells Prolog this is a question, not a new fact.",
        },
    },
    "variables_introduction": {
        "title": "🔤 Variables: The Power of 'What If?'",
        "subtitle": "Finding Multiple Answers",
        "explanation": [
            "Here's where Prolog gets really powerful - VARIABLES!",
            "",
            "Variables let you ask 'What if?' questions like:",
            "'What does Alice like?' or 'Who likes chocolate?'",
            "",
            "🔍 Variables in Prolog start with UPPERCASE letters:",
            "   X, Y, Person, Thing, Something, etc.",
            "",
            "Let's say we have these facts:",
            "   likes(alice, chocolate).",
            "   likes(alice, ice_cream).",
            "   likes(bob, pizza).",
            "",
            "Now we can ask: ?- likes(alice, X).",
            "",
            "Prolog will find ALL the things Alice likes:",
            "   X = chocolate",
            "   X = ice_cream",
            "",
            "🎯 More examples:",
            "   ?- likes(Person, chocolate).  ← Who likes chocolate?",
            "   ?- parent(tom, Child).        ← Who are Tom's children?",
            "   ?- employee(X, tech_corp).    ← Who works at Tech Corp?",
        ],
        "examples": [
            "?- likes(alice, X).",
            "?- likes(Person, chocolate).",
            "?- parent(tom, Child).",
            "?- employee(X, tech_corp).",
        ],
        "practice_exercise": {
            "prompt": "Given these facts:\n   likes(alice, chocolate).\n   likes(bob, pizza).\n   likes(charlie, chocolate).",
            "instruction": "Write a query to find everyone who likes chocolate:",
            "expected_pattern": "likes(X, chocolate)",
            "expected_answer": "?- likes(X, chocolate).",
            "explanation": "Great! X will match both 'alice' and 'charlie' - anyone who likes chocolate.",
        },
    },
    "completion": {
        "title": "🎊 Congratulations, Logic Programmer!",
        "subtitle": "You've Mastered the Basics!",
        "celebration": [
            "🌟 MISSION ACCOMPLISHED! 🌟",
            "",
            "You've successfully learned the fundamental building blocks of Prolog:",
            "",
            "✅ FACTS - You can create statements of truth",
            "✅ QUERIES - You can ask yes/no questions",
            "✅ VARIABLES - You can find multiple solutions",
            "",
            "These three concepts are the foundation of ALL Prolog programming!",
            "",
            "🚀 What you can do now:",
            "   • Create knowledge bases with facts",
            "   • Query information from those facts",
            "   • Use variables to find patterns and relationships",
            "",
            "This is just the beginning of your logic programming journey!",
        ],
        "summary": [
            "📚 QUICK REFERENCE:",
            "",
            "Facts:     predicate(arg1, arg2).",
            "Queries:   ?- predicate(arg1, arg2).",
            "Variables: ?- predicate(X, arg2).",
            "",
            "Remember: Facts end with periods, queries start with '?-',",
            "and variables begin with uppercase letters!",
        ],
        "next_steps": [
            "🎮 Ready for more adventure?",
            "",
            "The main Logic Quest game will teach you advanced concepts like:",
            "   • Rules and logical implications",
            "   • Complex pattern matching",
            "   • Backtracking and multiple solutions",
            "   • Recursive problem solving",
            "",
            "You now have the foundation to tackle these challenges!",
        ],
        "options": {
            "continue_to_game": "Start the main Logic Quest adventure",
            "review_concepts": "Review the concepts you just learned",
            "exit_tutorial": "Exit and practice on your own",
        },
    },
}


class TutorialNavigator:
    """
    Handles tutorial step navigation and content loading.

    Provides methods to move between steps, load content,
    and manage tutorial progression.
    """

    def __init__(self):
        """Initialize the navigator with step order."""
        self.step_order = [
            TutorialStep.INTRODUCTION,
            TutorialStep.FACTS_EXPLANATION,
            TutorialStep.FACT_CREATION,
            TutorialStep.QUERIES_EXPLANATION,
            TutorialStep.VARIABLES_INTRODUCTION,
            TutorialStep.COMPLETION,
        ]
        self.current_step_index = 0

    def get_current_step(self) -> TutorialStep:
        """Get the current tutorial step."""
        if 0 <= self.current_step_index < len(self.step_order):
            return self.step_order[self.current_step_index]
        return TutorialStep.COMPLETION

    def get_step_content(self, step: TutorialStep) -> Dict[str, Any]:
        """
        Load content for a specific tutorial step.

        Args:
            step: The tutorial step to load content for

        Returns:
            Dictionary containing all content for the step
        """
        step_key = step.value if isinstance(step, TutorialStep) else step
        return TUTORIAL_CONTENT.get(step_key, {})

    def next_step(self) -> bool:
        """
        Move to the next tutorial step.

        Returns:
            True if successfully moved to next step, False if at end
        """
        if self.current_step_index < len(self.step_order) - 1:
            self.current_step_index += 1
            return True
        return False

    def previous_step(self) -> bool:
        """
        Move to the previous tutorial step.

        Returns:
            True if successfully moved to previous step, False if at beginning
        """
        if self.current_step_index > 0:
            self.current_step_index -= 1
            return True
        return False

    def can_go_next(self) -> bool:
        """Check if there is a next step available."""
        return self.current_step_index < len(self.step_order) - 1

    def can_go_previous(self) -> bool:
        """Check if there is a previous step available."""
        return self.current_step_index > 0

    def get_step_number(self) -> int:
        """Get the current step number (1-indexed for display)."""
        return self.current_step_index + 1

    def get_total_steps(self) -> int:
        """Get the total number of tutorial steps."""
        return len(self.step_order)

    def get_progress_percentage(self) -> float:
        """Calculate tutorial progress as a percentage."""
        return (self.current_step_index / len(self.step_order)) * 100

    def jump_to_step(self, step: TutorialStep) -> bool:
        """
        Jump directly to a specific step.

        Args:
            step: The step to jump to

        Returns:
            True if step exists and jump was successful
        """
        try:
            self.current_step_index = self.step_order.index(step)
            return True
        except ValueError:
            return False

    def reset(self) -> None:
        """Reset navigator to the beginning."""
        self.current_step_index = 0


class TutorialSession:
    """
    Manages a complete tutorial session with progress persistence.

    Combines navigation, progress tracking, and content management
    for a cohesive tutorial experience.
    """

    def __init__(self):
        """Initialize a new tutorial session."""
        self.navigator = TutorialNavigator()
        self.progress = TutorialProgress()
        self.session_active = True

    def start_session(self) -> None:
        """Start the tutorial session and initialize timing."""
        import time

        self.progress.start_time = time.time()
        self.session_active = True

    def end_session(self) -> None:
        """End the tutorial session."""
        self.session_active = False

    def get_current_content(self) -> Dict[str, Any]:
        """Get content for the current step."""
        current_step = self.navigator.get_current_step()
        return self.navigator.get_step_content(current_step)

    def advance_step(self) -> bool:
        """
        Advance to the next step and update progress.

        Returns:
            True if advanced successfully, False if at end
        """
        current_step = self.navigator.get_current_step()
        self.progress.mark_step_complete(current_step.value)

        return self.navigator.next_step()

    def go_back_step(self) -> bool:
        """
        Go back to the previous step.

        Returns:
            True if went back successfully, False if at beginning
        """
        return self.navigator.previous_step()

    def record_user_input(self, input_type: str, user_input: str) -> None:
        """
        Record user input for progress tracking.

        Args:
            input_type: Type of input ('fact' or 'query')
            user_input: The actual user input string
        """
        if input_type == "fact":
            self.progress.add_user_fact(user_input)
        elif input_type == "query":
            self.progress.add_user_query(user_input)

    def record_mistake(self) -> None:
        """Record that the user made a mistake."""
        self.progress.increment_mistakes()

    def record_hint_used(self) -> None:
        """Record that a hint was used or shown."""
        self.progress.increment_hints()

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the tutorial session.

        Returns:
            Dictionary with session statistics and progress
        """
        return {
            "completion_percentage": self.progress.get_completion_percentage(),
            "steps_completed": len(self.progress.completed_steps),
            "total_steps": self.navigator.get_total_steps(),
            "facts_created": len(self.progress.user_facts),
            "queries_written": len(self.progress.user_queries),
            "mistakes_made": self.progress.mistakes_count,
            "hints_used": self.progress.hints_used,
            "user_facts": self.progress.user_facts.copy(),
            "user_queries": self.progress.user_queries.copy(),
        }

    def is_complete(self) -> bool:
        """Check if the tutorial has been completed."""
        return (
            self.navigator.get_current_step() == TutorialStep.COMPLETION
            and TutorialStep.COMPLETION.value in self.progress.completed_steps
        )
