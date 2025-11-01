"""
Logic Quest - A Prolog Learning Game

Core game package containing terminal interface, story engine,
puzzle management, and concept implementations.
"""

from .terminal import Terminal, terminal_component
from .story import StoryEngine, GameLevel, StorySegment
from .puzzles import PuzzleManager, BasePuzzle, PuzzleResult
from .validation import PrologValidator, ValidationResult
from .tutorial_content import TutorialSession, TutorialStep

__all__ = [
    "Terminal",
    "terminal_component",
    "StoryEngine",
    "GameLevel",
    "StorySegment",
    "PuzzleManager",
    "BasePuzzle",
    "PuzzleResult",
    "PrologValidator",
    "ValidationResult",
    "TutorialSession",
    "TutorialStep",
]
