"""
Story Engine Tests

Tests for the story engine module, including narrative progression,
level management, and story content delivery for Logic Quest.
"""

from prologresurrected.game.story import StoryEngine, GameLevel, StorySegment


class TestGameLevel:
    """Test cases for the GameLevel enum."""

    def test_game_level_values(self):
        """Test that game levels have correct values."""
        assert GameLevel.TUTORIAL.value == 0
        assert GameLevel.FACTS.value == 1
        assert GameLevel.RULES.value == 2
        assert GameLevel.UNIFICATION.value == 3
        assert GameLevel.BACKTRACKING.value == 4
        assert GameLevel.RECURSION.value == 5

    def test_game_level_ordering(self):
        """Test that game levels are properly ordered."""
        levels = list(GameLevel)
        values = [level.value for level in levels]

        # Values should be sequential from 0 to 5
        assert values == list(range(6))

    def test_game_level_names(self):
        """Test that game levels have appropriate names."""
        expected_names = [
            "TUTORIAL",
            "FACTS",
            "RULES",
            "UNIFICATION",
            "BACKTRACKING",
            "RECURSION",
        ]

        actual_names = [level.name for level in GameLevel]
        assert actual_names == expected_names


class TestStorySegment:
    """Test cases for the StorySegment dataclass."""

    def test_story_segment_creation(self):
        """Test creating a story segment with required fields."""
        segment = StorySegment(
            title="Test Title", content=["Line 1", "Line 2"], level=GameLevel.FACTS
        )

        assert segment.title == "Test Title"
        assert segment.content == ["Line 1", "Line 2"]
        assert segment.level == GameLevel.FACTS
        assert segment.character is None  # Default value
        assert segment.mood == "neutral"  # Default value

    def test_story_segment_with_optional_fields(self):
        """Test creating a story segment with all fields."""
        segment = StorySegment(
            title="Emergency Alert",
            content=["System failure detected!"],
            level=GameLevel.TUTORIAL,
            character="LOGIC-1 System",
            mood="urgent",
        )

        assert segment.title == "Emergency Alert"
        assert segment.content == ["System failure detected!"]
        assert segment.level == GameLevel.TUTORIAL
        assert segment.character == "LOGIC-1 System"
        assert segment.mood == "urgent"


class TestStoryEngine:
    """Test cases for the StoryEngine class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.story_engine = StoryEngine()

    def test_story_engine_initialization(self):
        """Test that story engine initializes correctly."""
        assert self.story_engine.current_level == GameLevel.TUTORIAL
        assert isinstance(self.story_engine.story_segments, dict)
        assert isinstance(self.story_engine.player_progress, dict)

        # Check player progress structure
        progress = self.story_engine.player_progress
        assert progress["name"] == "Junior Programmer"
        assert progress["level"] == 0
        assert progress["score"] == 0
        assert progress["concepts_learned"] == []
        assert isinstance(progress["story_flags"], set)

    def test_get_intro_story(self):
        """Test getting the introduction story segment."""
        intro = self.story_engine.get_intro_story()

        assert isinstance(intro, StorySegment)
        assert intro.title == "CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL"
        assert intro.level == GameLevel.TUTORIAL
        assert intro.character == "Supervisor"
        assert intro.mood == "urgent"
        assert len(intro.content) > 10  # Should have substantial content

        # Check for key story elements
        content_text = " ".join(intro.content)
        assert "1985" in content_text
        assert "Cyberdyne Systems" in content_text
        assert "LOGIC-1" in content_text
        assert "junior programmer" in content_text
        assert "Prolog" in content_text

    def test_get_level_intro_facts(self):
        """Test getting the introduction for Facts level."""
        intro = self.story_engine.get_level_intro(GameLevel.FACTS)

        assert isinstance(intro, StorySegment)
        assert intro.title == "MEMORY BANK ALPHA - FACTS DATABASE"
        assert intro.level == GameLevel.FACTS
        assert intro.character == "LOGIC-1 System"
        assert intro.mood == "mysterious"

        content_text = " ".join(intro.content)
        assert "facts" in content_text.lower()
        assert "unconditionally true" in content_text
        assert "foundation" in content_text.lower()

    def test_get_level_intro_rules(self):
        """Test getting the introduction for Rules level."""
        intro = self.story_engine.get_level_intro(GameLevel.RULES)

        assert isinstance(intro, StorySegment)
        assert intro.title == "MEMORY BANK BETA - INFERENCE ENGINE"
        assert intro.level == GameLevel.RULES
        assert intro.character == "LOGIC-1 System"

        content_text = " ".join(intro.content)
        assert "rules" in content_text.lower()
        assert "inference" in content_text.lower()
        assert "if this, then that" in content_text.lower()

    def test_get_level_intro_unification(self):
        """Test getting the introduction for Unification level."""
        intro = self.story_engine.get_level_intro(GameLevel.UNIFICATION)

        assert isinstance(intro, StorySegment)
        assert intro.title == "MEMORY BANK GAMMA - PATTERN MATCHING CORE"
        assert intro.level == GameLevel.UNIFICATION

        content_text = " ".join(intro.content)
        assert "unification" in content_text.lower()
        assert "pattern" in content_text.lower()
        assert "matching" in content_text.lower()

    def test_get_level_intro_backtracking(self):
        """Test getting the introduction for Backtracking level."""
        intro = self.story_engine.get_level_intro(GameLevel.BACKTRACKING)

        assert isinstance(intro, StorySegment)
        assert intro.title == "MEMORY BANK DELTA - SEARCH ALGORITHMS"
        assert intro.level == GameLevel.BACKTRACKING

        content_text = " ".join(intro.content)
        assert "backtracking" in content_text.lower()
        assert "alternative" in content_text.lower()
        assert "explore" in content_text.lower()

    def test_get_level_intro_recursion(self):
        """Test getting the introduction for Recursion level."""
        intro = self.story_engine.get_level_intro(GameLevel.RECURSION)

        assert isinstance(intro, StorySegment)
        assert intro.title == "MEMORY BANK EPSILON - RECURSIVE CORE"
        assert intro.level == GameLevel.RECURSION
        assert intro.mood == "urgent"

        content_text = " ".join(intro.content)
        assert "recursion" in content_text.lower()
        assert "recursive" in content_text.lower()
        assert "problems within problems" in content_text.lower()

    def test_get_level_intro_default(self):
        """Test getting default intro for undefined levels."""
        # This tests the fallback mechanism
        intro = self.story_engine._get_default_intro(GameLevel.TUTORIAL)

        assert isinstance(intro, StorySegment)
        assert (
            intro.title
            == f"LEVEL {GameLevel.TUTORIAL.value} - {GameLevel.TUTORIAL.name}"
        )
        assert intro.level == GameLevel.TUTORIAL
        assert intro.mood == "neutral"
        assert len(intro.content) >= 2

    def test_get_success_story_final_level(self):
        """Test getting success story for final level (Recursion)."""
        success = self.story_engine.get_success_story(GameLevel.RECURSION)

        assert isinstance(success, StorySegment)
        assert success.title == "SYSTEM RESTORATION COMPLETE"
        assert success.level == GameLevel.RECURSION
        assert success.character == "Supervisor"
        assert success.mood == "triumphant"

        content_text = " ".join(success.content)
        assert "MISSION COMPLETE" in content_text
        assert "logic programming expert" in content_text
        assert "saved" in content_text.lower()

    def test_get_success_story_intermediate_level(self):
        """Test getting success story for intermediate levels."""
        success = self.story_engine.get_success_story(GameLevel.FACTS)

        assert isinstance(success, StorySegment)
        assert success.title == f"LEVEL {GameLevel.FACTS.value} COMPLETE"
        assert success.level == GameLevel.FACTS
        assert success.mood == "neutral"

        content_text = " ".join(success.content)
        assert "restored" in content_text.lower()
        assert "online" in content_text.lower()

    def test_advance_level(self):
        """Test advancing through game levels."""
        # Start at tutorial level
        assert self.story_engine.current_level == GameLevel.TUTORIAL
        assert self.story_engine.player_progress["level"] == 0

        # Advance through all levels
        for expected_level in [
            GameLevel.FACTS,
            GameLevel.RULES,
            GameLevel.UNIFICATION,
            GameLevel.BACKTRACKING,
            GameLevel.RECURSION,
        ]:
            result = self.story_engine.advance_level()
            assert result is True
            assert self.story_engine.current_level == expected_level
            assert self.story_engine.player_progress["level"] == expected_level.value

        # Try to advance beyond max level
        result = self.story_engine.advance_level()
        assert result is False
        assert self.story_engine.current_level == GameLevel.RECURSION

    def test_add_concept_learned(self):
        """Test adding learned concepts to player progress."""
        concepts = ["facts", "queries", "variables", "rules"]

        for concept in concepts:
            self.story_engine.add_concept_learned(concept)

        learned = self.story_engine.player_progress["concepts_learned"]
        assert len(learned) == len(concepts)
        for concept in concepts:
            assert concept in learned

    def test_add_concept_learned_no_duplicates(self):
        """Test that adding the same concept twice doesn't create duplicates."""
        concept = "facts"

        self.story_engine.add_concept_learned(concept)
        self.story_engine.add_concept_learned(concept)

        learned = self.story_engine.player_progress["concepts_learned"]
        assert learned.count(concept) == 1

    def test_story_flags(self):
        """Test setting and checking story flags."""
        flags = ["intro_seen", "first_puzzle_complete", "ai_restored"]

        # Initially no flags should be set
        for flag in flags:
            assert not self.story_engine.has_story_flag(flag)

        # Set flags and verify
        for flag in flags:
            self.story_engine.set_story_flag(flag)
            assert self.story_engine.has_story_flag(flag)

        # Check that all flags are in the set
        story_flags = self.story_engine.player_progress["story_flags"]
        for flag in flags:
            assert flag in story_flags

    def test_get_player_progress(self):
        """Test getting player progress returns a copy."""
        # Modify the story engine state
        self.story_engine.advance_level()
        self.story_engine.add_concept_learned("facts")
        self.story_engine.set_story_flag("test_flag")

        # Get progress
        progress = self.story_engine.get_player_progress()

        # Should be a copy, not the original
        assert progress is not self.story_engine.player_progress

        # But should contain the same data
        assert progress["level"] == 1  # Advanced from 0
        assert "facts" in progress["concepts_learned"]
        assert "test_flag" in progress["story_flags"]

        # Modifying the returned copy shouldn't affect the original
        progress["level"] = 999
        assert self.story_engine.player_progress["level"] == 1


class TestStoryProgression:
    """Integration tests for story progression."""

    def setup_method(self):
        """Set up test fixtures."""
        self.story_engine = StoryEngine()

    def test_complete_story_progression(self):
        """Test a complete playthrough progression."""
        # Start with intro
        intro = self.story_engine.get_intro_story()
        assert intro.level == GameLevel.TUTORIAL

        # Progress through each level
        levels = [
            GameLevel.FACTS,
            GameLevel.RULES,
            GameLevel.UNIFICATION,
            GameLevel.BACKTRACKING,
            GameLevel.RECURSION,
        ]

        for level in levels:
            # Advance to the level
            self.story_engine.advance_level()
            assert self.story_engine.current_level == level

            # Get level intro
            level_intro = self.story_engine.get_level_intro(level)
            assert level_intro.level == level

            # Mark concept as learned
            concept_name = level.name.lower()
            self.story_engine.add_concept_learned(concept_name)

            # Get success story
            success = self.story_engine.get_success_story(level)
            assert success.level == level

        # Verify final state
        progress = self.story_engine.get_player_progress()
        assert progress["level"] == GameLevel.RECURSION.value
        assert len(progress["concepts_learned"]) == len(levels)

    def test_story_consistency(self):
        """Test that story content is consistent and thematic."""
        # Get all level intros
        intros = []
        for level in GameLevel:
            if level != GameLevel.TUTORIAL:  # Skip tutorial, test others
                intro = self.story_engine.get_level_intro(level)
                intros.append(intro)

        # All should have cyberpunk/AI themes
        cyberpunk_terms = ["memory bank", "system", "logic", "ai", "circuits", "neural"]

        for intro in intros:
            content_text = " ".join(intro.content).lower()
            title_text = intro.title.lower()

            # Each intro should contain cyberpunk terminology
            has_cyberpunk_theme = any(
                term in content_text or term in title_text for term in cyberpunk_terms
            )
            assert has_cyberpunk_theme, (
                f"Level {intro.level.name} should have cyberpunk theme"
            )

            # Should mention the specific Prolog concept
            concept_name = intro.level.name.lower()
            if concept_name == "unification":
                # Unification might be referred to as "pattern matching"
                assert "unification" in content_text or "pattern" in content_text, (
                    f"Level intro should mention {concept_name}"
                )
            else:
                assert concept_name in content_text, (
                    f"Level intro should mention {concept_name}"
                )

    def test_narrative_mood_progression(self):
        """Test that narrative mood progresses appropriately."""
        # Intro should be urgent (crisis setup)
        intro = self.story_engine.get_intro_story()
        assert intro.mood == "urgent"

        # Most level intros should be mysterious (exploring the system)
        mysterious_count = 0
        for level in [
            GameLevel.FACTS,
            GameLevel.RULES,
            GameLevel.UNIFICATION,
            GameLevel.BACKTRACKING,
        ]:
            level_intro = self.story_engine.get_level_intro(level)
            if level_intro.mood == "mysterious":
                mysterious_count += 1

        assert mysterious_count >= 3, "Most level intros should have mysterious mood"

        # Final level should be urgent (climax)
        final_intro = self.story_engine.get_level_intro(GameLevel.RECURSION)
        assert final_intro.mood == "urgent"

        # Final success should be triumphant
        final_success = self.story_engine.get_success_story(GameLevel.RECURSION)
        assert final_success.mood == "triumphant"
