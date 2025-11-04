"""
Unit tests for tutorial content data structures and navigation logic.
"""

import pytest
import time
from prologresurrected.game.tutorial_content import (
    TutorialProgress,
    TutorialStep,
    TutorialNavigator,
    TutorialSession,
    TUTORIAL_CONTENT,
)


class TestTutorialProgress:
    """Test the TutorialProgress dataclass functionality."""

    def test_initial_state(self):
        """Test that progress starts in correct initial state."""
        progress = TutorialProgress()

        assert progress.current_step == 0
        assert progress.completed_steps == []
        assert progress.user_facts == []
        assert progress.user_queries == []
        assert progress.mistakes_count == 0
        assert progress.hints_used == 0
        assert progress.start_time is None
        assert progress.step_completion_times == {}

    def test_mark_step_complete(self):
        """Test marking steps as complete."""
        progress = TutorialProgress()

        progress.mark_step_complete("introduction")
        assert "introduction" in progress.completed_steps
        assert progress.is_step_completed("introduction")

        # Test no duplicates
        progress.mark_step_complete("introduction")
        assert progress.completed_steps.count("introduction") == 1

    def test_add_user_content(self):
        """Test adding user-created facts and queries."""
        progress = TutorialProgress()

        progress.add_user_fact("likes(bob, pizza).")
        progress.add_user_query("?- likes(alice, chocolate).")

        assert "likes(bob, pizza)." in progress.user_facts
        assert "?- likes(alice, chocolate)." in progress.user_queries

    def test_increment_counters(self):
        """Test incrementing mistake and hint counters."""
        progress = TutorialProgress()

        progress.increment_mistakes()
        progress.increment_mistakes()
        progress.increment_hints()

        assert progress.mistakes_count == 2
        assert progress.hints_used == 1

    def test_completion_percentage(self):
        """Test completion percentage calculation."""
        progress = TutorialProgress()

        # No steps completed
        assert progress.get_completion_percentage() == 0.0

        # Complete some steps
        total_steps = len(TUTORIAL_CONTENT)
        progress.mark_step_complete("introduction")
        progress.mark_step_complete("facts_explanation")

        expected_percentage = (2 / total_steps) * 100
        assert progress.get_completion_percentage() == expected_percentage


class TestTutorialNavigator:
    """Test the TutorialNavigator functionality."""

    def test_initial_state(self):
        """Test navigator starts at first step."""
        navigator = TutorialNavigator()

        assert navigator.get_current_step() == TutorialStep.INTRODUCTION
        assert navigator.get_step_number() == 1
        assert navigator.get_total_steps() == 6
        assert navigator.can_go_next() is True
        assert navigator.can_go_previous() is False

    def test_step_navigation(self):
        """Test moving between steps."""
        navigator = TutorialNavigator()

        # Move forward
        assert navigator.next_step() is True
        assert navigator.get_current_step() == TutorialStep.FACTS_EXPLANATION
        assert navigator.get_step_number() == 2

        # Move backward
        assert navigator.previous_step() is True
        assert navigator.get_current_step() == TutorialStep.INTRODUCTION
        assert navigator.get_step_number() == 1

    def test_navigation_boundaries(self):
        """Test navigation at boundaries."""
        navigator = TutorialNavigator()

        # Can't go before first step
        assert navigator.previous_step() is False
        assert navigator.get_current_step() == TutorialStep.INTRODUCTION

        # Move to last step
        while navigator.can_go_next():
            navigator.next_step()

        assert navigator.get_current_step() == TutorialStep.COMPLETION
        assert navigator.can_go_next() is False
        assert navigator.next_step() is False

    def test_jump_to_step(self):
        """Test jumping directly to a specific step."""
        navigator = TutorialNavigator()

        # Jump to middle step
        assert navigator.jump_to_step(TutorialStep.QUERIES_EXPLANATION) is True
        assert navigator.get_current_step() == TutorialStep.QUERIES_EXPLANATION

        # Jump to completion
        assert navigator.jump_to_step(TutorialStep.COMPLETION) is True
        assert navigator.get_current_step() == TutorialStep.COMPLETION

    def test_reset(self):
        """Test resetting navigator to beginning."""
        navigator = TutorialNavigator()

        # Move to middle
        navigator.jump_to_step(TutorialStep.FACT_CREATION)
        assert navigator.get_current_step() == TutorialStep.FACT_CREATION

        # Reset
        navigator.reset()
        assert navigator.get_current_step() == TutorialStep.INTRODUCTION
        assert navigator.get_step_number() == 1

    def test_get_step_content(self):
        """Test loading step content."""
        navigator = TutorialNavigator()

        content = navigator.get_step_content(TutorialStep.INTRODUCTION)
        assert "title" in content
        assert "explanation" in content
        assert content["title"] == "🚀 Welcome to Prolog Programming"

    def test_progress_percentage(self):
        """Test progress percentage calculation."""
        navigator = TutorialNavigator()

        assert navigator.get_progress_percentage() == 0.0

        navigator.next_step()  # Move to step 2
        expected = (1 / 6) * 100  # 1 out of 6 steps completed
        assert navigator.get_progress_percentage() == expected


class TestTutorialSession:
    """Test the TutorialSession functionality."""

    def test_session_initialization(self):
        """Test session starts correctly."""
        session = TutorialSession()

        assert session.navigator is not None
        assert session.progress is not None
        assert session.session_active is True
        assert session.progress.start_time is None

    def test_start_and_end_session(self):
        """Test session lifecycle management."""
        session = TutorialSession()

        # Start session
        start_time = time.time()
        session.start_session()

        assert session.session_active is True
        assert session.progress.start_time is not None
        assert session.progress.start_time >= start_time

        # End session
        session.end_session()
        assert session.session_active is False

    def test_get_current_content(self):
        """Test getting current step content."""
        session = TutorialSession()

        content = session.get_current_content()
        assert "title" in content
        assert content["title"] == "🚀 Welcome to Prolog Programming"

    def test_advance_step(self):
        """Test advancing through steps."""
        session = TutorialSession()

        # Should start at introduction
        current_step = session.navigator.get_current_step()
        assert current_step == TutorialStep.INTRODUCTION

        # Advance step
        assert session.advance_step() is True

        # Should mark previous step complete and move to next
        assert session.progress.is_step_completed("introduction")
        assert session.navigator.get_current_step() == TutorialStep.FACTS_EXPLANATION

    def test_record_user_input(self):
        """Test recording user input."""
        session = TutorialSession()

        session.record_user_input("fact", "likes(bob, pizza).")
        session.record_user_input("query", "?- likes(alice, chocolate).")

        assert "likes(bob, pizza)." in session.progress.user_facts
        assert "?- likes(alice, chocolate)." in session.progress.user_queries

    def test_record_mistakes_and_hints(self):
        """Test recording mistakes and hints."""
        session = TutorialSession()

        session.record_mistake()
        session.record_mistake()
        session.record_hint_used()

        assert session.progress.mistakes_count == 2
        assert session.progress.hints_used == 1

    def test_session_summary(self):
        """Test getting session summary."""
        session = TutorialSession()

        # Add some progress
        session.record_user_input("fact", "likes(bob, pizza).")
        session.record_mistake()
        session.advance_step()

        summary = session.get_session_summary()

        assert "completion_percentage" in summary
        assert "steps_completed" in summary
        assert "total_steps" in summary
        assert "facts_created" in summary
        assert "queries_written" in summary
        assert "mistakes_made" in summary
        assert "hints_used" in summary
        assert "user_facts" in summary
        assert "user_queries" in summary

        assert summary["facts_created"] == 1
        assert summary["mistakes_made"] == 1
        assert summary["steps_completed"] == 1
        assert summary["total_steps"] == 6

    def test_is_complete(self):
        """Test completion detection."""
        session = TutorialSession()

        # Not complete initially
        assert session.is_complete() is False

        # Move to completion step but don't mark complete
        session.navigator.jump_to_step(TutorialStep.COMPLETION)
        assert session.is_complete() is False

        # Mark completion step as complete
        session.progress.mark_step_complete(TutorialStep.COMPLETION.value)
        assert session.is_complete() is True


class TestTutorialContent:
    """Test the tutorial content structure."""

    def test_content_structure(self):
        """Test that all required content exists."""
        required_steps = [
            "introduction",
            "facts_explanation",
            "fact_creation",
            "queries_explanation",
            "variables_introduction",
            "completion",
        ]

        for step in required_steps:
            assert step in TUTORIAL_CONTENT
            content = TUTORIAL_CONTENT[step]
            assert "title" in content
            assert isinstance(content["title"], str)

    def test_introduction_content(self):
        """Test introduction step has required content."""
        intro = TUTORIAL_CONTENT["introduction"]

        assert "title" in intro
        assert "explanation" in intro
        assert "cyberpunk_flavor" in intro
        assert "continue_prompt" in intro
        assert isinstance(intro["explanation"], list)
        assert isinstance(intro["cyberpunk_flavor"], list)

    def test_facts_explanation_content(self):
        """Test facts explanation has required content."""
        facts = TUTORIAL_CONTENT["facts_explanation"]

        assert "title" in facts
        assert "explanation" in facts
        assert "examples" in facts
        assert "practice_exercise" in facts
        assert isinstance(facts["examples"], list)
        assert isinstance(facts["practice_exercise"], dict)

    def test_fact_creation_content(self):
        """Test fact creation has required content."""
        creation = TUTORIAL_CONTENT["fact_creation"]

        assert "title" in creation
        assert "explanation" in creation
        assert "exercise_prompt" in creation
        assert "expected_pattern" in creation
        assert "validation_hints" in creation
        assert "success_message" in creation

    def test_queries_explanation_content(self):
        """Test queries explanation has required content."""
        queries = TUTORIAL_CONTENT["queries_explanation"]

        assert "title" in queries
        assert "explanation" in queries
        assert "examples" in queries
        assert "practice_exercise" in queries

    def test_variables_introduction_content(self):
        """Test variables introduction has required content."""
        variables = TUTORIAL_CONTENT["variables_introduction"]

        assert "title" in variables
        assert "explanation" in variables
        assert "examples" in variables
        assert "practice_exercise" in variables

    def test_completion_content(self):
        """Test completion step has required content."""
        completion = TUTORIAL_CONTENT["completion"]

        assert "title" in completion
        assert "celebration" in completion
        assert "summary" in completion
        assert "next_steps" in completion
        assert "options" in completion
        assert isinstance(completion["options"], dict)


if __name__ == "__main__":
    pytest.main([__file__])
