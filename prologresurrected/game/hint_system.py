"""
Complexity-aware hint and guidance system for Logic Quest.

This module provides adaptive hint generation and explanation systems that
adjust their behavior based on the selected complexity level, ensuring
appropriate guidance for learners at different skill levels.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from .complexity import ComplexityLevel, HintFrequency, ExplanationDepth


class HintType(Enum):
    """Types of hints that can be provided."""
    SYNTAX = "syntax"
    CONCEPT = "concept"
    STRATEGY = "strategy"
    EXAMPLE = "example"
    TEMPLATE = "template"
    ENCOURAGEMENT = "encouragement"


class HintTiming(Enum):
    """When hints should be made available."""
    IMMEDIATE = "immediate"
    AFTER_FIRST_ATTEMPT = "after_first_attempt"
    AFTER_MULTIPLE_ATTEMPTS = "after_multiple_attempts"
    ON_REQUEST_ONLY = "on_request_only"
    NEVER = "never"


@dataclass
class HintConfig:
    """Configuration for hint behavior at different complexity levels."""
    
    # Availability settings
    hint_frequency: HintFrequency
    max_hints_per_puzzle: int
    progressive_hints: bool  # Whether hints get more specific over time
    
    # Timing settings
    hint_timing: HintTiming
    attempts_before_hint: int
    
    # Content settings
    include_examples: bool
    include_templates: bool
    include_syntax_help: bool
    include_encouragement: bool
    
    # Hint types allowed at this complexity level
    allowed_hint_types: List[HintType]
    
    # Scoring impact
    hint_penalty_per_use: int
    
    def can_provide_hint(self, attempts: int, hints_used: int) -> bool:
        """Check if a hint can be provided based on current state."""
        # Check maximum hints limit
        if hints_used >= self.max_hints_per_puzzle:
            return False
        
        # Check frequency restrictions
        if self.hint_frequency == HintFrequency.NONE:
            return False
        
        # Check timing restrictions
        if self.hint_timing == HintTiming.NEVER:
            return False
        elif self.hint_timing == HintTiming.AFTER_FIRST_ATTEMPT and attempts < 1:
            return False
        elif self.hint_timing == HintTiming.AFTER_MULTIPLE_ATTEMPTS and attempts < self.attempts_before_hint:
            return False
        
        return True
    
    def should_show_hint_type(self, hint_type: HintType) -> bool:
        """Check if a specific hint type should be shown."""
        return hint_type in self.allowed_hint_types


@dataclass
class ExplanationConfig:
    """Configuration for explanation depth and style at different complexity levels."""
    
    # Depth settings
    explanation_depth: ExplanationDepth
    include_why_explanations: bool  # Explain why something works
    include_how_explanations: bool  # Explain how to do something
    include_what_explanations: bool  # Explain what something means
    
    # Content settings
    use_analogies: bool
    use_examples: bool
    use_step_by_step: bool
    use_visual_aids: bool  # ASCII diagrams, etc.
    
    # Language settings
    use_technical_terms: bool
    use_beginner_language: bool
    include_definitions: bool
    
    # Feedback settings
    provide_detailed_errors: bool
    suggest_corrections: bool
    explain_common_mistakes: bool
    
    def get_explanation_style(self) -> str:
        """Get a description of the explanation style."""
        if self.explanation_depth == ExplanationDepth.DETAILED:
            return "comprehensive with examples and step-by-step guidance"
        elif self.explanation_depth == ExplanationDepth.MODERATE:
            return "clear with some examples and guidance"
        elif self.explanation_depth == ExplanationDepth.BRIEF:
            return "concise with minimal examples"
        else:  # MINIMAL
            return "very brief and direct"


class HintGenerator:
    """Generates hints adapted to complexity levels."""
    
    def __init__(self):
        """Initialize the hint generator with complexity-specific configurations."""
        self.hint_configs = self._initialize_hint_configs()
        self.explanation_configs = self._initialize_explanation_configs()
        self.hint_templates = self._initialize_hint_templates()
    
    def _initialize_hint_configs(self) -> Dict[ComplexityLevel, HintConfig]:
        """Initialize hint configurations for each complexity level."""
        return {
            ComplexityLevel.BEGINNER: HintConfig(
                hint_frequency=HintFrequency.ALWAYS_AVAILABLE,
                max_hints_per_puzzle=5,
                progressive_hints=True,
                hint_timing=HintTiming.IMMEDIATE,
                attempts_before_hint=0,
                include_examples=True,
                include_templates=True,
                include_syntax_help=True,
                include_encouragement=True,
                allowed_hint_types=[
                    HintType.SYNTAX, HintType.CONCEPT, HintType.STRATEGY,
                    HintType.EXAMPLE, HintType.TEMPLATE, HintType.ENCOURAGEMENT
                ],
                hint_penalty_per_use=5
            ),
            ComplexityLevel.INTERMEDIATE: HintConfig(
                hint_frequency=HintFrequency.ON_REQUEST,
                max_hints_per_puzzle=3,
                progressive_hints=True,
                hint_timing=HintTiming.IMMEDIATE,
                attempts_before_hint=0,
                include_examples=True,
                include_templates=False,
                include_syntax_help=True,
                include_encouragement=True,
                allowed_hint_types=[
                    HintType.SYNTAX, HintType.CONCEPT, HintType.STRATEGY,
                    HintType.EXAMPLE, HintType.ENCOURAGEMENT
                ],
                hint_penalty_per_use=10
            ),
            ComplexityLevel.ADVANCED: HintConfig(
                hint_frequency=HintFrequency.AFTER_ATTEMPTS,
                max_hints_per_puzzle=2,
                progressive_hints=False,
                hint_timing=HintTiming.AFTER_MULTIPLE_ATTEMPTS,
                attempts_before_hint=2,
                include_examples=False,
                include_templates=False,
                include_syntax_help=False,
                include_encouragement=False,
                allowed_hint_types=[HintType.CONCEPT, HintType.STRATEGY],
                hint_penalty_per_use=20
            ),
            ComplexityLevel.EXPERT: HintConfig(
                hint_frequency=HintFrequency.NONE,
                max_hints_per_puzzle=0,
                progressive_hints=False,
                hint_timing=HintTiming.NEVER,
                attempts_before_hint=999,
                include_examples=False,
                include_templates=False,
                include_syntax_help=False,
                include_encouragement=False,
                allowed_hint_types=[],
                hint_penalty_per_use=0
            )
        }
    
    def _initialize_explanation_configs(self) -> Dict[ComplexityLevel, ExplanationConfig]:
        """Initialize explanation configurations for each complexity level."""
        return {
            ComplexityLevel.BEGINNER: ExplanationConfig(
                explanation_depth=ExplanationDepth.DETAILED,
                include_why_explanations=True,
                include_how_explanations=True,
                include_what_explanations=True,
                use_analogies=True,
                use_examples=True,
                use_step_by_step=True,
                use_visual_aids=True,
                use_technical_terms=False,
                use_beginner_language=True,
                include_definitions=True,
                provide_detailed_errors=True,
                suggest_corrections=True,
                explain_common_mistakes=True
            ),
            ComplexityLevel.INTERMEDIATE: ExplanationConfig(
                explanation_depth=ExplanationDepth.MODERATE,
                include_why_explanations=True,
                include_how_explanations=True,
                include_what_explanations=False,
                use_analogies=False,
                use_examples=True,
                use_step_by_step=True,
                use_visual_aids=False,
                use_technical_terms=True,
                use_beginner_language=False,
                include_definitions=False,
                provide_detailed_errors=True,
                suggest_corrections=True,
                explain_common_mistakes=False
            ),
            ComplexityLevel.ADVANCED: ExplanationConfig(
                explanation_depth=ExplanationDepth.BRIEF,
                include_why_explanations=False,
                include_how_explanations=True,
                include_what_explanations=False,
                use_analogies=False,
                use_examples=False,
                use_step_by_step=False,
                use_visual_aids=False,
                use_technical_terms=True,
                use_beginner_language=False,
                include_definitions=False,
                provide_detailed_errors=False,
                suggest_corrections=False,
                explain_common_mistakes=False
            ),
            ComplexityLevel.EXPERT: ExplanationConfig(
                explanation_depth=ExplanationDepth.MINIMAL,
                include_why_explanations=False,
                include_how_explanations=False,
                include_what_explanations=False,
                use_analogies=False,
                use_examples=False,
                use_step_by_step=False,
                use_visual_aids=False,
                use_technical_terms=True,
                use_beginner_language=False,
                include_definitions=False,
                provide_detailed_errors=False,
                suggest_corrections=False,
                explain_common_mistakes=False
            )
        }
    
    def _initialize_hint_templates(self) -> Dict[HintType, Dict[ComplexityLevel, List[str]]]:
        """Initialize hint templates for different types and complexity levels."""
        return {
            HintType.SYNTAX: {
                ComplexityLevel.BEGINNER: [
                    "Remember that Prolog facts end with a period (.)",
                    "Predicates are followed by parentheses containing arguments",
                    "Arguments are separated by commas",
                    "Atoms (like names) should be lowercase or in quotes"
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "Check your syntax - facts need periods",
                    "Verify predicate and argument structure",
                    "Ensure proper comma separation"
                ],
                ComplexityLevel.ADVANCED: [
                    "Syntax error detected",
                    "Check punctuation"
                ]
            },
            HintType.CONCEPT: {
                ComplexityLevel.BEGINNER: [
                    "A fact states something that is true in your world",
                    "Think about what relationship you're trying to express",
                    "Facts are like statements: 'X has property Y' or 'X relates to Y'"
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "Consider the logical relationship being expressed",
                    "Think about the predicate that best represents this concept"
                ],
                ComplexityLevel.ADVANCED: [
                    "Focus on the logical structure",
                    "Consider the semantic meaning"
                ]
            },
            HintType.STRATEGY: {
                ComplexityLevel.BEGINNER: [
                    "Start by identifying the main relationship",
                    "Then identify what things are involved in that relationship",
                    "Finally, put them together in the right order"
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "Break down the problem into its components",
                    "Consider what predicate best expresses the relationship"
                ],
                ComplexityLevel.ADVANCED: [
                    "Analyze the problem structure",
                    "Consider alternative approaches"
                ]
            },
            HintType.EXAMPLE: {
                ComplexityLevel.BEGINNER: [
                    "Example: likes(mary, pizza). means 'Mary likes pizza'",
                    "Example: owns(john, car). means 'John owns a car'",
                    "Example: parent(alice, bob). means 'Alice is parent of Bob'"
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "Similar structure: predicate(arg1, arg2).",
                    "Consider: relationship(subject, object)."
                ]
            },
            HintType.TEMPLATE: {
                ComplexityLevel.BEGINNER: [
                    "Template: predicate(argument1, argument2).",
                    "Fill in: _____(_____, _____).",
                    "Structure: relationship(who, what)."
                ]
            },
            HintType.ENCOURAGEMENT: {
                ComplexityLevel.BEGINNER: [
                    "You're doing great! Keep thinking through it step by step.",
                    "Don't worry, everyone finds Prolog tricky at first!",
                    "You're on the right track - just need a small adjustment.",
                    "Take your time - understanding is more important than speed."
                ],
                ComplexityLevel.INTERMEDIATE: [
                    "You've got this! Think it through.",
                    "Close! Just need to refine your approach.",
                    "Good progress - keep going!"
                ]
            }
        }
    
    def get_hint_config(self, complexity_level: ComplexityLevel) -> HintConfig:
        """Get hint configuration for a specific complexity level."""
        return self.hint_configs[complexity_level]
    
    def get_explanation_config(self, complexity_level: ComplexityLevel) -> ExplanationConfig:
        """Get explanation configuration for a specific complexity level."""
        return self.explanation_configs[complexity_level]
    
    def can_provide_hint(self, complexity_level: ComplexityLevel, attempts: int, hints_used: int) -> bool:
        """Check if a hint can be provided at the current state."""
        config = self.get_hint_config(complexity_level)
        return config.can_provide_hint(attempts, hints_used)
    
    def generate_hint(
        self, 
        complexity_level: ComplexityLevel, 
        hint_type: HintType, 
        hint_level: int,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a hint for the specified complexity level and type.
        
        Args:
            complexity_level: The current complexity level
            hint_type: The type of hint to generate
            hint_level: The progressive hint level (1 = first hint, higher = more specific)
            context: Optional context information for customizing the hint
            
        Returns:
            Generated hint text or empty string if hints not allowed
        """
        config = self.get_hint_config(complexity_level)
        
        # Check if this hint type is allowed
        if not config.should_show_hint_type(hint_type):
            return ""
        
        # Get templates for this hint type and complexity level
        templates = self.hint_templates.get(hint_type, {}).get(complexity_level, [])
        
        if not templates:
            return self._generate_fallback_hint(complexity_level, hint_type)
        
        # Select appropriate template based on hint level
        template_index = min(hint_level - 1, len(templates) - 1)
        base_hint = templates[template_index]
        
        # Customize hint based on context if provided
        if context:
            base_hint = self._customize_hint(base_hint, context, complexity_level)
        
        return base_hint
    
    def generate_progressive_hint(
        self,
        complexity_level: ComplexityLevel,
        hint_level: int,
        puzzle_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a progressive hint that gets more specific with each level.
        
        Args:
            complexity_level: The current complexity level
            hint_level: The progressive hint level
            puzzle_context: Context about the current puzzle
            
        Returns:
            Progressive hint text
        """
        config = self.get_hint_config(complexity_level)
        
        if not config.progressive_hints:
            # Non-progressive hints - check if any hints are allowed
            if complexity_level == ComplexityLevel.EXPERT:
                return "No hints available at Expert level. You've got this!"
            # For other levels, return a general hint
            return self.generate_hint(complexity_level, HintType.CONCEPT, 1, puzzle_context)
        
        # Progressive hint sequence based on complexity level
        if complexity_level == ComplexityLevel.BEGINNER:
            hint_sequence = [
                (HintType.ENCOURAGEMENT, "Take your time and think about what you're trying to express."),
                (HintType.CONCEPT, "Think about the relationship you want to represent."),
                (HintType.STRATEGY, "Identify the predicate and arguments you need."),
                (HintType.EXAMPLE, "Look at the pattern of similar facts."),
                (HintType.TEMPLATE, "Use the template structure to guide you.")
            ]
        elif complexity_level == ComplexityLevel.INTERMEDIATE:
            hint_sequence = [
                (HintType.CONCEPT, "Consider the logical relationship being expressed."),
                (HintType.STRATEGY, "Break down the problem into components."),
                (HintType.EXAMPLE, "Think about similar structures you've seen.")
            ]
        elif complexity_level == ComplexityLevel.ADVANCED:
            hint_sequence = [
                (HintType.STRATEGY, "Analyze the problem structure."),
                (HintType.CONCEPT, "Focus on the core logical relationship.")
            ]
        else:  # EXPERT
            return "No hints available at Expert level. You've got this!"
        
        # Select hint based on level
        if hint_level <= len(hint_sequence):
            hint_type, fallback_text = hint_sequence[hint_level - 1]
            generated_hint = self.generate_hint(complexity_level, hint_type, 1, puzzle_context)
            return generated_hint if generated_hint else fallback_text
        else:
            # Beyond available hints - provide encouragement
            encouragement = self.generate_hint(complexity_level, HintType.ENCOURAGEMENT, 1, puzzle_context)
            return encouragement if encouragement else "Keep trying!"
    
    def generate_explanation(
        self,
        complexity_level: ComplexityLevel,
        topic: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an explanation adapted to the complexity level.
        
        Args:
            complexity_level: The current complexity level
            topic: The topic to explain
            context: Optional context for customization
            
        Returns:
            Explanation text adapted to complexity level
        """
        config = self.get_explanation_config(complexity_level)
        
        # Base explanations for common topics
        base_explanations = {
            "facts": {
                ComplexityLevel.BEGINNER: "Facts in Prolog are statements that are always true. They're like saying 'This is how things are in our world.' For example, if we write 'likes(mary, pizza).', we're stating that Mary likes pizza. Facts always end with a period and follow the pattern: predicate(arguments).",
                ComplexityLevel.INTERMEDIATE: "Facts are basic statements in Prolog that declare relationships or properties. They follow the syntax predicate(arg1, arg2, ...). and are considered always true in the knowledge base.",
                ComplexityLevel.ADVANCED: "Facts are ground clauses that establish the knowledge base foundation.",
                ComplexityLevel.EXPERT: "Ground clauses in the knowledge base."
            },
            "syntax_error": {
                ComplexityLevel.BEGINNER: "It looks like there's a syntax error in your Prolog code. This means the computer can't understand what you wrote because it doesn't follow Prolog's rules. Common issues include: missing periods at the end, incorrect parentheses, or wrong comma placement. Take a moment to check these elements.",
                ComplexityLevel.INTERMEDIATE: "Syntax error detected. Check for proper punctuation, parentheses matching, and comma placement in your Prolog statement.",
                ComplexityLevel.ADVANCED: "Syntax error in Prolog statement.",
                ComplexityLevel.EXPERT: "Syntax error."
            }
        }
        
        # Get base explanation
        topic_explanations = base_explanations.get(topic, {})
        base_explanation = topic_explanations.get(
            complexity_level, 
            f"Information about {topic} at {complexity_level.name} level."
        )
        
        # Enhance explanation based on configuration
        enhanced_explanation = self._enhance_explanation(base_explanation, config, context)
        
        return enhanced_explanation
    
    def _customize_hint(self, hint: str, context: Dict[str, Any], complexity_level: ComplexityLevel) -> str:
        """Customize a hint based on context information."""
        # Replace placeholders in hints with context-specific information
        if "expected_predicate" in context and context["expected_predicate"] is not None:
            hint = hint.replace("predicate", context["expected_predicate"])
        
        if "expected_args" in context and context["expected_args"] is not None:
            args = context["expected_args"]
            if len(args) >= 2:
                hint = hint.replace("argument1", args[0])
                hint = hint.replace("argument2", args[1])
        
        return hint
    
    def _enhance_explanation(
        self, 
        base_explanation: str, 
        config: ExplanationConfig, 
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Enhance an explanation based on the configuration settings."""
        enhanced = base_explanation
        
        # Add step-by-step breakdown if configured
        if config.use_step_by_step and context and "steps" in context:
            enhanced += "\n\nStep by step:\n"
            for i, step in enumerate(context["steps"], 1):
                enhanced += f"{i}. {step}\n"
        
        # Add examples if configured
        if config.use_examples and context and "examples" in context:
            enhanced += "\n\nExamples:\n"
            for example in context["examples"]:
                enhanced += f"• {example}\n"
        
        # Add definitions if configured
        if config.include_definitions and context and "definitions" in context:
            enhanced += "\n\nDefinitions:\n"
            for term, definition in context["definitions"].items():
                enhanced += f"• {term}: {definition}\n"
        
        return enhanced
    
    def _generate_fallback_hint(self, complexity_level: ComplexityLevel, hint_type: HintType) -> str:
        """Generate a fallback hint when no templates are available."""
        if complexity_level == ComplexityLevel.BEGINNER:
            return "Take your time and think through the problem step by step."
        elif complexity_level == ComplexityLevel.INTERMEDIATE:
            return "Consider the structure of what you're trying to express."
        elif complexity_level == ComplexityLevel.ADVANCED:
            return "Think about the logical relationship."
        else:  # EXPERT
            return ""
    
    def get_hint_availability_message(self, complexity_level: ComplexityLevel, attempts: int, hints_used: int) -> str:
        """Get a message about hint availability at the current state."""
        config = self.get_hint_config(complexity_level)
        
        if config.hint_frequency == HintFrequency.NONE:
            return "Hints are not available at Expert level. You've got this!"
        
        if hints_used >= config.max_hints_per_puzzle:
            return f"You've used all {config.max_hints_per_puzzle} available hints for this puzzle."
        
        if config.hint_timing == HintTiming.AFTER_MULTIPLE_ATTEMPTS and attempts < config.attempts_before_hint:
            remaining = config.attempts_before_hint - attempts
            return f"Hints will be available after {remaining} more attempt{'s' if remaining != 1 else ''}."
        
        remaining_hints = config.max_hints_per_puzzle - hints_used
        return f"You have {remaining_hints} hint{'s' if remaining_hints != 1 else ''} remaining."
    
    def calculate_hint_penalty(self, complexity_level: ComplexityLevel, hints_used: int) -> int:
        """Calculate the score penalty for using hints."""
        config = self.get_hint_config(complexity_level)
        return hints_used * config.hint_penalty_per_use


# Convenience class for integrating with existing puzzle system
class ComplexityAwareHintSystem:
    """
    High-level interface for the hint system that integrates with the existing puzzle framework.
    """
    
    def __init__(self):
        """Initialize the hint system."""
        self.hint_generator = HintGenerator()
        self.current_complexity_level = ComplexityLevel.BEGINNER
    
    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """Set the current complexity level."""
        self.current_complexity_level = level
    
    def can_provide_hint(self, attempts: int, hints_used: int) -> bool:
        """Check if a hint can be provided at the current state."""
        return self.hint_generator.can_provide_hint(
            self.current_complexity_level, attempts, hints_used
        )
    
    def get_hint(self, hint_level: int, puzzle_context: Optional[Dict[str, Any]] = None) -> str:
        """Get a progressive hint for the current complexity level."""
        if not self.can_provide_hint(
            puzzle_context.get("attempts", 0) if puzzle_context else 0,
            puzzle_context.get("hints_used", 0) if puzzle_context else 0
        ):
            return self.hint_generator.get_hint_availability_message(
                self.current_complexity_level,
                puzzle_context.get("attempts", 0) if puzzle_context else 0,
                puzzle_context.get("hints_used", 0) if puzzle_context else 0
            )
        
        return self.hint_generator.generate_progressive_hint(
            self.current_complexity_level, hint_level, puzzle_context
        )
    
    def get_explanation(self, topic: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Get an explanation adapted to the current complexity level."""
        return self.hint_generator.generate_explanation(
            self.current_complexity_level, topic, context
        )
    
    def get_hint_config(self) -> HintConfig:
        """Get the current hint configuration."""
        return self.hint_generator.get_hint_config(self.current_complexity_level)
    
    def get_explanation_config(self) -> ExplanationConfig:
        """Get the current explanation configuration."""
        return self.hint_generator.get_explanation_config(self.current_complexity_level)
    
    def calculate_hint_penalty(self, hints_used: int) -> int:
        """Calculate the score penalty for using hints."""
        return self.hint_generator.calculate_hint_penalty(
            self.current_complexity_level, hints_used
        )