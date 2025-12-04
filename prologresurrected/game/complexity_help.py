"""
Complexity level documentation and help system.

This module provides comprehensive in-game help for complexity levels,
including comparison guides, contextual help, tips, and recommendations.
"""

from typing import Dict, List, Optional
from .complexity import ComplexityLevel, ComplexityManager


class ComplexityHelpSystem:
    """Provides comprehensive help and documentation for complexity levels."""
    
    def __init__(self, complexity_manager: ComplexityManager):
        """
        Initialize the help system.
        
        Args:
            complexity_manager: The complexity manager instance
        """
        self.complexity_manager = complexity_manager
    
    def get_complexity_overview(self) -> str:
        """Get a comprehensive overview of the complexity level system."""
        return """🎯 COMPLEXITY LEVEL SYSTEM OVERVIEW

Logic Quest features four adaptive complexity levels that adjust puzzle difficulty,
hint availability, and explanation depth to match your skill level.

═══════════════════════════════════════════════════════════════════

🌱 BEGINNER - Perfect for Newcomers
   • Maximum guidance with step-by-step explanations
   • Hints always available when you need them
   • Simple problems with templates provided
   • Detailed explanations of every concept
   • Scoring multiplier: 1.0x

⚡ INTERMEDIATE - For Developing Skills
   • Moderate guidance with standard problems
   • Hints available on request
   • More complex syntax and concepts
   • Balanced explanations
   • Scoring multiplier: 1.2x

🔥 ADVANCED - For Experienced Programmers
   • Minimal guidance with complex problems
   • Hints only after multiple attempts
   • Multiple solution paths and optimization
   • Brief, focused explanations
   • Scoring multiplier: 1.5x

💀 EXPERT - For Prolog Masters
   • No guidance - you're on your own!
   • No hints available
   • Optimization challenges and edge cases
   • Minimal explanations
   • Scoring multiplier: 2.0x

═══════════════════════════════════════════════════════════════════

💡 KEY FEATURES:
• Change complexity level anytime during gameplay
• Your progress and score are always preserved
• Each level tracks achievements separately
• Higher levels earn bonus scoring multipliers

Type 'complexity compare' for a detailed comparison
Type 'complexity tips' for level-specific recommendations"""
    
    def get_complexity_comparison(self) -> str:
        """Get a detailed comparison of all complexity levels."""
        return """🎯 COMPLEXITY LEVEL COMPARISON

═══════════════════════════════════════════════════════════════════

FEATURE COMPARISON:

┌─────────────────┬──────────┬──────────────┬──────────┬────────┐
│ FEATURE         │ BEGINNER │ INTERMEDIATE │ ADVANCED │ EXPERT │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Hint Frequency  │ Always   │ On Request   │ After    │ None   │
│                 │          │              │ Attempts │        │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Explanations    │ Detailed │ Moderate     │ Brief    │ Minimal│
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Templates       │ Yes      │ No           │ No       │ No     │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Examples        │ Yes      │ Yes          │ No       │ No     │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Max Variables   │ 2        │ 4            │ 6        │ 8      │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Max Predicates  │ 3        │ 5            │ 8        │ 12     │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Complex Syntax  │ No       │ Yes          │ Yes      │ Yes    │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Optimization    │ No       │ No           │ Yes      │ Yes    │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Edge Cases      │ No       │ No           │ No       │ Yes    │
├─────────────────┼──────────┼──────────────┼──────────┼────────┤
│ Score Multiplier│ 1.0x     │ 1.2x         │ 1.5x     │ 2.0x   │
└─────────────────┴──────────┴──────────────┴──────────┴────────┘

═══════════════════════════════════════════════════════════════════

LEARNING OBJECTIVES:

All complexity levels cover the same core Prolog concepts:
• Facts and their syntax
• Queries and pattern matching
• Variables and unification
• Rules and logical implications
• Backtracking and search
• Recursion and problem solving

The difference is in HOW these concepts are presented and practiced.

═══════════════════════════════════════════════════════════════════

Type 'complexity tips' for recommendations on choosing a level"""
    
    def get_complexity_tips(self) -> str:
        """Get tips and recommendations for choosing complexity levels."""
        return """🎯 COMPLEXITY LEVEL TIPS & RECOMMENDATIONS

═══════════════════════════════════════════════════════════════════

🌱 CHOOSE BEGINNER IF:
   ✓ You're completely new to Prolog
   ✓ You're new to logic programming concepts
   ✓ You prefer detailed step-by-step guidance
   ✓ You want to build a strong foundation
   ✓ You learn best with examples and templates

⚡ CHOOSE INTERMEDIATE IF:
   ✓ You have some programming experience
   ✓ You understand basic logic concepts
   ✓ You want a balanced challenge
   ✓ You prefer to figure things out with occasional help
   ✓ You've completed the beginner level

🔥 CHOOSE ADVANCED IF:
   ✓ You're an experienced programmer
   ✓ You understand logic programming basics
   ✓ You enjoy complex problem-solving
   ✓ You want to optimize your solutions
   ✓ You prefer minimal guidance

💀 CHOOSE EXPERT IF:
   ✓ You're already familiar with Prolog
   ✓ You want maximum challenge
   ✓ You enjoy optimization puzzles
   ✓ You don't need any guidance
   ✓ You want the highest scoring multiplier

═══════════════════════════════════════════════════════════════════

💡 GENERAL TIPS:

1. START LOWER, PROGRESS HIGHER
   It's better to start at a lower level and move up than to get
   frustrated at a level that's too difficult.

2. CHANGE ANYTIME
   You can change complexity levels at any time during gameplay.
   Your progress is always preserved!

3. TRY DIFFERENT LEVELS
   Each level offers a different learning experience. Try them all
   to find what works best for you.

4. TRACK YOUR ACHIEVEMENTS
   The game tracks your achievements at each complexity level
   separately. Challenge yourself to complete puzzles at all levels!

5. SCORING MULTIPLIERS
   Higher complexity levels earn bonus points, but only if you
   complete the puzzles. A completed beginner puzzle is better
   than a failed expert puzzle!

═══════════════════════════════════════════════════════════════════

Type 'complexity help <level>' for level-specific guidance
Example: 'complexity help beginner'"""
    
    def get_level_specific_help(self, level: ComplexityLevel) -> str:
        """
        Get detailed help for a specific complexity level.
        
        Args:
            level: The complexity level to get help for
            
        Returns:
            Detailed help text for the specified level
        """
        config = self.complexity_manager.get_config(level)
        
        help_texts = {
            ComplexityLevel.BEGINNER: """🌱 BEGINNER LEVEL - DETAILED GUIDE

═══════════════════════════════════════════════════════════════════

WHAT TO EXPECT:

• MAXIMUM GUIDANCE
  Every puzzle comes with detailed explanations and step-by-step
  instructions. You'll never feel lost or confused.

• ALWAYS-AVAILABLE HINTS
  Stuck? Just type 'hint' anytime to get helpful guidance. Hints
  are unlimited and always available.

• TEMPLATES PROVIDED
  Many puzzles provide templates or starting code to help you
  understand the structure of solutions.

• SIMPLE PROBLEMS
  Puzzles use simple syntax with limited variables (max 2) and
  predicates (max 3). Focus on learning concepts, not complexity.

• DETAILED EXPLANATIONS
  Every concept is explained thoroughly with examples and context.
  You'll understand not just WHAT to do, but WHY.

═══════════════════════════════════════════════════════════════════

BEST PRACTICES:

1. READ EVERYTHING
   Take time to read all explanations and examples. They're designed
   to build your understanding progressively.

2. USE HINTS FREELY
   Don't struggle unnecessarily. Hints are there to help you learn,
   not to penalize you.

3. EXPERIMENT
   Try different approaches. The beginner level is forgiving and
   encourages exploration.

4. ASK QUESTIONS
   Use the 'hint' command whenever you're unsure. Learning is about
   understanding, not just completing puzzles.

5. TAKE YOUR TIME
   There's no rush. Focus on understanding each concept before
   moving to the next puzzle.

═══════════════════════════════════════════════════════════════════

WHEN TO MOVE UP:

Consider moving to INTERMEDIATE when:
• You consistently complete puzzles without hints
• You understand the basic syntax and concepts
• You want more challenging problems
• You feel confident in your Prolog basics

Remember: You can always come back to BEGINNER level!""",
            
            ComplexityLevel.INTERMEDIATE: """⚡ INTERMEDIATE LEVEL - DETAILED GUIDE

═══════════════════════════════════════════════════════════════════

WHAT TO EXPECT:

• MODERATE GUIDANCE
  Puzzles include explanations, but you'll need to figure out more
  on your own. Good balance of support and challenge.

• HINTS ON REQUEST
  Hints are available when you ask for them with the 'hint' command.
  Use them strategically when you're stuck.

• NO TEMPLATES
  You'll write solutions from scratch, applying what you've learned.
  This builds real problem-solving skills.

• STANDARD COMPLEXITY
  Puzzles use more variables (up to 4) and predicates (up to 5).
  Complex syntax is introduced gradually.

• BALANCED EXPLANATIONS
  Explanations cover key concepts without excessive detail. You'll
  need to connect the dots yourself sometimes.

═══════════════════════════════════════════════════════════════════

BEST PRACTICES:

1. TRY BEFORE ASKING
   Attempt puzzles on your own before using hints. This builds
   problem-solving skills and confidence.

2. LEARN FROM MISTAKES
   Errors are learning opportunities. Read error messages carefully
   and understand what went wrong.

3. REVIEW CONCEPTS
   If you're struggling, review the explanations from previous
   puzzles or drop to BEGINNER temporarily.

4. PLAN YOUR APPROACH
   Think through your solution before coding. What predicates do
   you need? What variables? What's the logic?

5. USE HINTS STRATEGICALLY
   When stuck, use hints to get unstuck, then try to complete the
   puzzle on your own.

═══════════════════════════════════════════════════════════════════

WHEN TO MOVE UP/DOWN:

Move to ADVANCED when:
• You rarely need hints
• You understand complex syntax
• You want optimization challenges
• You're comfortable with Prolog concepts

Move to BEGINNER if:
• You're using hints on every puzzle
• You're feeling frustrated or lost
• You need more detailed explanations
• You want to review fundamentals""",
            
            ComplexityLevel.ADVANCED: """🔥 ADVANCED LEVEL - DETAILED GUIDE

═══════════════════════════════════════════════════════════════════

WHAT TO EXPECT:

• MINIMAL GUIDANCE
  Brief explanations focus on key points. You're expected to
  understand concepts and apply them independently.

• HINTS AFTER ATTEMPTS
  Hints only become available after you've made several attempts.
  This encourages persistence and problem-solving.

• COMPLEX PROBLEMS
  Puzzles feature multiple solution paths, optimization challenges,
  and complex syntax with up to 6 variables and 8 predicates.

• BRIEF EXPLANATIONS
  Explanations are concise and focused. You should already understand
  the fundamentals and be ready for advanced concepts.

• OPTIMIZATION REQUIRED
  Some puzzles require efficient solutions. Brute force approaches
  may not be sufficient.

═══════════════════════════════════════════════════════════════════

BEST PRACTICES:

1. THINK DEEPLY
   Advanced puzzles require careful analysis. Consider multiple
   approaches and choose the most elegant solution.

2. OPTIMIZE YOUR CODE
   Look for ways to make your solutions more efficient. Can you
   reduce the number of predicates? Simplify the logic?

3. EMBRACE COMPLEXITY
   Don't shy away from complex syntax or multiple variables. These
   are tools for solving sophisticated problems.

4. PERSIST THROUGH CHALLENGES
   Hints are limited. Develop your problem-solving skills by working
   through difficulties on your own.

5. LEARN FROM PATTERNS
   Recognize common patterns in Prolog programming and apply them
   to new situations.

═══════════════════════════════════════════════════════════════════

WHEN TO MOVE UP/DOWN:

Move to EXPERT when:
• You complete puzzles without hints
• You optimize solutions naturally
• You want maximum challenge
• You're ready for edge cases

Move to INTERMEDIATE if:
• You're consistently stuck
• You need more explanation
• The complexity is overwhelming
• You want to review concepts""",
            
            ComplexityLevel.EXPERT: """💀 EXPERT LEVEL - DETAILED GUIDE

═══════════════════════════════════════════════════════════════════

WHAT TO EXPECT:

• NO GUIDANCE
  You're on your own. Minimal explanations assume you already know
  Prolog well. This is the ultimate challenge.

• NO HINTS
  Hints are not available at this level. You must solve puzzles
  using your knowledge and problem-solving skills alone.

• OPTIMIZATION CHALLENGES
  Puzzles require efficient, elegant solutions. Edge cases and
  performance matter. Up to 8 variables and 12 predicates.

• MINIMAL EXPLANATIONS
  Brief problem statements with no hand-holding. You should
  understand what's needed from minimal description.

• EDGE CASES INCLUDED
  Puzzles test boundary conditions and unusual scenarios. Your
  solutions must be robust and handle all cases.

═══════════════════════════════════════════════════════════════════

BEST PRACTICES:

1. MASTER THE FUNDAMENTALS
   Expert level assumes complete mastery of Prolog basics. If you're
   struggling, review fundamentals at a lower level.

2. THINK LIKE A COMPUTER SCIENTIST
   Consider algorithmic complexity, edge cases, and optimization.
   Write code that's both correct and efficient.

3. TEST THOROUGHLY
   Without hints, you must verify your solutions carefully. Think
   through edge cases and test your logic.

4. EMBRACE THE CHALLENGE
   Expert level is meant to be difficult. Persistence and deep
   thinking are required. Don't give up!

5. LEARN FROM FAILURE
   Failed attempts teach valuable lessons. Analyze what went wrong
   and refine your approach.

═══════════════════════════════════════════════════════════════════

SCORING BONUS:

Expert level offers a 2.0x scoring multiplier - the highest in the
game. But remember: you only get points for completed puzzles!

═══════════════════════════════════════════════════════════════════

WHEN TO MOVE DOWN:

Move to ADVANCED if:
• You're consistently unable to complete puzzles
• You need occasional hints
• The difficulty is too frustrating
• You want to review advanced concepts

There's no shame in adjusting difficulty. The goal is to learn and
enjoy the game, not to struggle endlessly!"""
        }
        
        return help_texts.get(level, "Help not available for this level.")
    
    def get_contextual_help(self, current_level: ComplexityLevel, context: str = "general") -> str:
        """
        Get contextual help based on current level and game context.
        
        Args:
            current_level: The player's current complexity level
            context: The current game context (e.g., "puzzle", "menu", "general")
            
        Returns:
            Contextual help text
        """
        config = self.complexity_manager.get_config(current_level)
        
        if context == "puzzle":
            return self._get_puzzle_context_help(current_level, config)
        elif context == "selection":
            return self._get_selection_context_help(current_level, config)
        elif context == "change":
            return self._get_change_context_help(current_level, config)
        else:
            return self._get_general_context_help(current_level, config)
    
    def _get_puzzle_context_help(self, level: ComplexityLevel, config) -> str:
        """Get help specific to puzzle-solving context."""
        help_by_level = {
            ComplexityLevel.BEGINNER: f"""💡 PUZZLE HELP ({config.name.upper()})

You're at {config.name.upper()} level. Here's what's available:

• HINTS: Type 'hint' anytime for guidance (unlimited)
• EXAMPLES: Look for example solutions in explanations
• TEMPLATES: Many puzzles provide starting code
• EXPLANATIONS: Read the detailed explanations carefully

Don't hesitate to use hints - they're here to help you learn!""",
            
            ComplexityLevel.INTERMEDIATE: f"""💡 PUZZLE HELP ({config.name.upper()})

You're at {config.name.upper()} level. Here's what's available:

• HINTS: Type 'hint' when you need guidance
• EXPLANATIONS: Moderate detail - read carefully
• NO TEMPLATES: Write solutions from scratch

Try to solve puzzles on your own first, but use hints when stuck.""",
            
            ComplexityLevel.ADVANCED: f"""💡 PUZZLE HELP ({config.name.upper()})

You're at {config.name.upper()} level. Here's what's available:

• HINTS: Available after multiple attempts
• EXPLANATIONS: Brief - focus on key concepts
• OPTIMIZATION: Look for efficient solutions

Persist through challenges. Hints are limited at this level.""",
            
            ComplexityLevel.EXPERT: f"""💡 PUZZLE HELP ({config.name.upper()})

You're at {config.name.upper()} level. You're on your own!

• NO HINTS: Solve puzzles using your knowledge
• MINIMAL EXPLANATIONS: Brief problem statements
• EDGE CASES: Test your solutions thoroughly

This is the ultimate challenge. Good luck!"""
        }
        
        return help_by_level.get(level, "")
    
    def _get_selection_context_help(self, level: ComplexityLevel, config) -> str:
        """Get help for complexity level selection."""
        return f"""💡 COMPLEXITY SELECTION HELP

You're currently at {config.name.upper()} level.

CHOOSING A LEVEL:
• Consider your Prolog experience
• Think about your learning goals
• Remember you can change anytime

RECOMMENDATIONS:
• New to Prolog? → Start with BEGINNER
• Some experience? → Try INTERMEDIATE
• Experienced programmer? → ADVANCED or EXPERT

Your progress is always preserved when changing levels!

Type 'complexity tips' for detailed recommendations"""
    
    def _get_change_context_help(self, level: ComplexityLevel, config) -> str:
        """Get help for changing complexity levels."""
        return f"""💡 COMPLEXITY CHANGE HELP

Current Level: {config.name.upper()}

CHANGING LEVELS:
1. Type 'complexity' to see all levels
2. Type the level name (e.g., 'beginner')
3. Confirm the change

WHAT HAPPENS:
✓ Your progress is preserved
✓ Your score is preserved
✓ Future puzzles adapt to new level
✓ Current puzzle state unchanged

WHEN TO CHANGE:
• Too easy? → Move up for more challenge
• Too hard? → Move down for more guidance
• Want variety? → Try different levels

There's no penalty for changing levels!"""
    
    def _get_general_context_help(self, level: ComplexityLevel, config) -> str:
        """Get general contextual help."""
        return f"""💡 COMPLEXITY SYSTEM HELP

Current Level: {config.ui_indicators.get('icon', '')} {config.name.upper()}

{config.description}

QUICK REFERENCE:
• Scoring Multiplier: {config.scoring_multiplier}x
• Hint Availability: {config.hint_frequency.value}
• Explanation Depth: {config.explanation_depth.value}

COMMANDS:
• 'complexity' - Change level
• 'complexity help' - Full help system
• 'complexity compare' - Compare all levels
• 'complexity tips' - Get recommendations

Type 'help' for all game commands"""
    
    def get_quick_reference(self, level: ComplexityLevel) -> str:
        """
        Get a quick reference card for a specific complexity level.
        
        Args:
            level: The complexity level
            
        Returns:
            Quick reference text
        """
        config = self.complexity_manager.get_config(level)
        
        return f"""╔═══════════════════════════════════════════════════════════╗
║  {config.ui_indicators.get('icon', '')} {config.name.upper()} LEVEL - QUICK REFERENCE
╚═══════════════════════════════════════════════════════════╝

DESCRIPTION:
{config.description}

FEATURES:
• Hints: {config.hint_frequency.value}
• Explanations: {config.explanation_depth.value}
• Scoring: {config.scoring_multiplier}x multiplier
• Max Variables: {config.puzzle_parameters.get('max_variables', 'N/A')}
• Max Predicates: {config.puzzle_parameters.get('max_predicates', 'N/A')}
• Templates: {'Yes' if config.puzzle_parameters.get('provide_templates') else 'No'}
• Examples: {'Yes' if config.puzzle_parameters.get('show_examples') else 'No'}

BEST FOR:
{self._get_best_for_text(level)}

═══════════════════════════════════════════════════════════════

Type 'complexity help {level.name.lower()}' for detailed guide"""
    
    def _get_best_for_text(self, level: ComplexityLevel) -> str:
        """Get 'best for' text for a level."""
        best_for = {
            ComplexityLevel.BEGINNER: "Complete beginners, those new to Prolog, learners who\nprefer detailed guidance and step-by-step instructions",
            ComplexityLevel.INTERMEDIATE: "Programmers with some experience, those who understand\nbasics and want balanced challenge with moderate support",
            ComplexityLevel.ADVANCED: "Experienced programmers, those comfortable with logic\nprogramming, learners who enjoy complex problem-solving",
            ComplexityLevel.EXPERT: "Prolog masters, those seeking maximum challenge,\nexperienced developers who don't need guidance"
        }
        return best_for.get(level, "")
    
    def get_faq(self) -> str:
        """Get frequently asked questions about complexity levels."""
        return """🎯 COMPLEXITY LEVELS - FREQUENTLY ASKED QUESTIONS

═══════════════════════════════════════════════════════════════════

Q: Can I change complexity levels during gameplay?
A: Yes! You can change levels anytime by typing 'complexity'. Your
   progress and score are always preserved.

Q: Will changing levels affect my score?
A: No. Your existing score is preserved. Only future puzzles will
   use the new scoring multiplier.

Q: Do all levels teach the same concepts?
A: Yes. All levels cover the same core Prolog concepts. The
   difference is in how they're presented and practiced.

Q: Which level should I start with?
A: If you're new to Prolog, start with BEGINNER. You can always
   move up later. It's better to start easier and progress.

Q: Can I complete puzzles at different levels?
A: Yes! The game tracks achievements separately for each level.
   You can challenge yourself to complete puzzles at all levels.

Q: Do higher levels give more points?
A: Yes. Higher levels have scoring multipliers (up to 2.0x for
   EXPERT), but only if you complete the puzzles!

Q: What if a level is too hard?
A: Change to an easier level anytime. There's no penalty. The goal
   is to learn and enjoy the game.

Q: What if a level is too easy?
A: Move up to a higher level for more challenge and better scoring
   multipliers. Test your skills!

Q: Are hints penalized?
A: No. Hints are a learning tool. Use them freely, especially at
   lower complexity levels.

Q: Can I see my achievements at each level?
A: Yes! Type 'achievements' to see your progress and scores at
   each complexity level.

═══════════════════════════════════════════════════════════════════

Type 'complexity help' for more information"""


def format_help_for_terminal(help_text: str) -> List[str]:
    """
    Format help text for terminal display.
    
    Args:
        help_text: The help text to format
        
    Returns:
        List of lines ready for terminal display
    """
    return help_text.split('\n')
