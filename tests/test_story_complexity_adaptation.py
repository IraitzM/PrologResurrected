"""
Unit tests for complexity-aware story content in StoryEngine.

Tests verify that story content adapts appropriately to different
complexity levels while maintaining educational objectives.
"""

from prologresurrected.game.story import StoryEngine, GameLevel, StorySegment
from prologresurrected.game.complexity import ComplexityLevel


class TestStoryEngineComplexityAdaptation:
    """Test suite for StoryEngine complexity adaptation."""

    def test_story_engine_initialization_with_complexity(self):
        """Test StoryEngine can be initialized with different complexity levels."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            assert engine.get_complexity_level() == level

    def test_story_engine_default_complexity(self):
        """Test StoryEngine defaults to BEGINNER complexity."""
        engine = StoryEngine()
        assert engine.get_complexity_level() == ComplexityLevel.BEGINNER

    def test_set_complexity_level(self):
        """Test setting complexity level after initialization."""
        engine = StoryEngine()
        engine.set_complexity_level(ComplexityLevel.EXPERT)
        assert engine.get_complexity_level() == ComplexityLevel.EXPERT

    def test_intro_story_has_complexity_variants(self):
        """Test intro story adapts to different complexity levels."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_intro_story()
            
            assert intro.title == "CYBERDYNE SYSTEMS - EMERGENCY PROTOCOL"
            assert intro.level == GameLevel.TUTORIAL
            assert len(intro.content) > 0
            
            # Beginner should have longest content
            if level == ComplexityLevel.BEGINNER:
                assert len(intro.content) > 15
            # Expert should have shortest content
            elif level == ComplexityLevel.EXPERT:
                assert len(intro.content) < 10

    def test_intro_story_content_length_decreases_with_complexity(self):
        """Test that intro story gets shorter as complexity increases."""
        lengths = {}
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_intro_story()
            lengths[level] = len(intro.content)
        
        # Beginner should have more content than Expert
        assert lengths[ComplexityLevel.BEGINNER] > lengths[ComplexityLevel.EXPERT]
        assert lengths[ComplexityLevel.INTERMEDIATE] > lengths[ComplexityLevel.ADVANCED]

    def test_level_intro_facts_adapts_to_complexity(self):
        """Test Facts level intro adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_level_intro(GameLevel.FACTS)
            
            assert intro.title == "MEMORY BANK ALPHA - FACTS DATABASE"
            assert intro.level == GameLevel.FACTS
            assert len(intro.content) > 0
            
            # Beginner should include detailed explanations
            if level == ComplexityLevel.BEGINNER:
                content_text = " ".join(intro.content)
                assert "foundation" in content_text.lower()
                assert len(intro.content) > 10
            # Expert should be minimal
            elif level == ComplexityLevel.EXPERT:
                assert len(intro.content) < 8

    def test_level_intro_rules_adapts_to_complexity(self):
        """Test Rules level intro adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_level_intro(GameLevel.RULES)
            
            assert intro.title == "MEMORY BANK BETA - INFERENCE ENGINE"
            assert intro.level == GameLevel.RULES
            assert len(intro.content) > 0

    def test_level_intro_unification_adapts_to_complexity(self):
        """Test Unification level intro adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_level_intro(GameLevel.UNIFICATION)
            
            assert intro.title == "MEMORY BANK GAMMA - PATTERN MATCHING CORE"
            assert intro.level == GameLevel.UNIFICATION
            assert len(intro.content) > 0

    def test_level_intro_backtracking_adapts_to_complexity(self):
        """Test Backtracking level intro adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_level_intro(GameLevel.BACKTRACKING)
            
            assert intro.title == "MEMORY BANK DELTA - SEARCH ALGORITHMS"
            assert intro.level == GameLevel.BACKTRACKING
            assert len(intro.content) > 0

    def test_level_intro_recursion_adapts_to_complexity(self):
        """Test Recursion level intro adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_level_intro(GameLevel.RECURSION)
            
            assert intro.title == "MEMORY BANK EPSILON - RECURSIVE CORE"
            assert intro.level == GameLevel.RECURSION
            assert len(intro.content) > 0

    def test_success_story_adapts_to_complexity(self):
        """Test success story adapts to complexity level."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            success = engine.get_success_story(GameLevel.RECURSION)
            
            assert success.title == "SYSTEM RESTORATION COMPLETE"
            assert success.level == GameLevel.RECURSION
            assert len(success.content) > 0
            
            # Beginner should have detailed celebration
            if level == ComplexityLevel.BEGINNER:
                assert len(success.content) > 10
            # Expert should be minimal
            elif level == ComplexityLevel.EXPERT:
                assert len(success.content) < 8

    def test_standard_level_success_adapts_to_complexity(self):
        """Test standard level completion adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            success = engine.get_success_story(GameLevel.FACTS)
            
            assert "COMPLETE" in success.title
            assert success.level == GameLevel.FACTS
            assert len(success.content) > 0

    def test_hello_world_transition_adapts_to_complexity(self):
        """Test Hello World transition story adapts to complexity."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            transition = engine.get_hello_world_transition_story()
            
            assert "TUTORIAL COMPLETE" in transition.title
            assert transition.level == GameLevel.TUTORIAL
            assert len(transition.content) > 0
            
            # Beginner should have detailed transition
            if level == ComplexityLevel.BEGINNER:
                assert len(transition.content) > 15
            # Expert should be minimal
            elif level == ComplexityLevel.EXPERT:
                assert len(transition.content) < 5

    def test_complexity_flavor_text_puzzle_start(self):
        """Test complexity-specific flavor text for puzzle start."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_text = engine_beginner.get_complexity_flavor_text("puzzle_start")
        expert_text = engine_expert.get_complexity_flavor_text("puzzle_start")
        
        assert len(beginner_text) > len(expert_text)
        assert "guidance" in beginner_text.lower() or "helpful" in beginner_text.lower()

    def test_complexity_flavor_text_hint_available(self):
        """Test complexity-specific flavor text for hint availability."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_text = engine_beginner.get_complexity_flavor_text("hint_available")
        expert_text = engine_expert.get_complexity_flavor_text("hint_available")
        
        assert "available" in beginner_text.lower() or "guide" in beginner_text.lower()
        assert "disabled" in expert_text.lower() or expert_text == "HINT SYSTEM: Disabled."

    def test_complexity_flavor_text_error_feedback(self):
        """Test complexity-specific flavor text for error feedback."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_text = engine_beginner.get_complexity_flavor_text("error_feedback")
        expert_text = engine_expert.get_complexity_flavor_text("error_feedback")
        
        assert len(beginner_text) > len(expert_text)
        assert "ERROR" in expert_text

    def test_complexity_flavor_text_success_feedback(self):
        """Test complexity-specific flavor text for success feedback."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_text = engine_beginner.get_complexity_flavor_text("success_feedback")
        expert_text = engine_expert.get_complexity_flavor_text("success_feedback")
        
        assert len(beginner_text) > len(expert_text)

    def test_tutorial_content_facts_adapts_to_complexity(self):
        """Test tutorial content for facts adapts to complexity."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_tutorial = engine_beginner.get_tutorial_content_for_complexity("facts")
        expert_tutorial = engine_expert.get_tutorial_content_for_complexity("facts")
        
        assert len(beginner_tutorial) > len(expert_tutorial)
        assert any("building blocks" in line.lower() or "database" in line.lower() 
                   for line in beginner_tutorial)

    def test_tutorial_content_queries_adapts_to_complexity(self):
        """Test tutorial content for queries adapts to complexity."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_tutorial = engine_beginner.get_tutorial_content_for_complexity("queries")
        expert_tutorial = engine_expert.get_tutorial_content_for_complexity("queries")
        
        assert len(beginner_tutorial) > len(expert_tutorial)

    def test_tutorial_content_rules_adapts_to_complexity(self):
        """Test tutorial content for rules adapts to complexity."""
        engine_beginner = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        engine_expert = StoryEngine(complexity_level=ComplexityLevel.EXPERT)
        
        beginner_tutorial = engine_beginner.get_tutorial_content_for_complexity("rules")
        expert_tutorial = engine_expert.get_tutorial_content_for_complexity("rules")
        
        assert len(beginner_tutorial) > len(expert_tutorial)

    def test_all_complexity_levels_produce_valid_content(self):
        """Test that all complexity levels produce valid, non-empty content."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            
            # Test all major story segments
            intro = engine.get_intro_story()
            assert len(intro.content) > 0
            
            facts_intro = engine.get_level_intro(GameLevel.FACTS)
            assert len(facts_intro.content) > 0
            
            success = engine.get_success_story(GameLevel.RECURSION)
            assert len(success.content) > 0
            
            transition = engine.get_hello_world_transition_story()
            assert len(transition.content) > 0

    def test_complexity_change_affects_subsequent_content(self):
        """Test that changing complexity level affects subsequent story content."""
        engine = StoryEngine(complexity_level=ComplexityLevel.BEGINNER)
        
        beginner_intro = engine.get_intro_story()
        beginner_length = len(beginner_intro.content)
        
        engine.set_complexity_level(ComplexityLevel.EXPERT)
        
        expert_intro = engine.get_intro_story()
        expert_length = len(expert_intro.content)
        
        assert beginner_length > expert_length

    def test_story_segment_has_complexity_variants_field(self):
        """Test that StorySegment dataclass includes complexity_variants field."""
        segment = StorySegment(
            title="Test",
            content=["Test content"],
            level=GameLevel.TUTORIAL,
            complexity_variants={
                ComplexityLevel.BEGINNER: ["Beginner content"],
                ComplexityLevel.EXPERT: ["Expert content"],
            }
        )
        
        assert segment.complexity_variants is not None
        assert ComplexityLevel.BEGINNER in segment.complexity_variants
        assert ComplexityLevel.EXPERT in segment.complexity_variants

    def test_educational_objectives_maintained_across_complexity(self):
        """Test that core educational content is present at all complexity levels."""
        # All levels should mention key concepts even if briefly
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            
            facts_intro = engine.get_level_intro(GameLevel.FACTS)
            content_text = " ".join(facts_intro.content).lower()
            assert "fact" in content_text or "database" in content_text
            
            rules_intro = engine.get_level_intro(GameLevel.RULES)
            content_text = " ".join(rules_intro.content).lower()
            assert "rule" in content_text or "inference" in content_text

    def test_cyberpunk_theme_maintained_across_complexity(self):
        """Test that cyberpunk theme is maintained at all complexity levels."""
        for level in ComplexityLevel:
            engine = StoryEngine(complexity_level=level)
            intro = engine.get_intro_story()
            
            content_text = " ".join(intro.content).lower()
            # Should mention key cyberpunk elements
            assert any(keyword in content_text for keyword in 
                      ["1985", "cyberdyne", "logic-1", "system", "terminal"])
