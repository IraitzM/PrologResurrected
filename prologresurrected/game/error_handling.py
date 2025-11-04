"""
Comprehensive Error Handling System for Hello World Prolog Tutorial

This module provides a progressive hint system with escalating help levels,
specific error messages for common Prolog syntax mistakes, encouraging tone
in all error and help messages, options to show correct answers after multiple
failed attempts, and recovery mechanisms for stuck users.
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

from .validation import ValidationResult


class HintLevel(Enum):
    """Escalating hint levels for progressive assistance."""
    GENTLE = "gentle"
    SPECIFIC = "specific"
    DETAILED = "detailed"
    EXPLICIT = "explicit"
    SHOW_ANSWER = "show_answer"


class ErrorCategory(Enum):
    """Categories of common Prolog syntax errors."""
    MISSING_PERIOD = "missing_period"
    UPPERCASE_PREDICATE = "uppercase_predicate"
    MISSING_PARENTHESES = "missing_parentheses"
    MISSING_QUERY_PREFIX = "missing_query_prefix"
    SPACES_IN_PREDICATE = "spaces_in_predicate"
    MISMATCHED_PARENTHESES = "mismatched_parens"
    LOWERCASE_VARIABLE = "lowercase_variable"
    INVALID_CHARACTERS = "invalid_characters"
    EMPTY_INPUT = "empty_input"
    CONTENT_MISMATCH = "content_mismatch"
    GENERIC_SYNTAX = "generic_syntax"


@dataclass
class ErrorContext:
    """Context information for error handling."""
    user_input: str
    expected_answer: str
    attempt_count: int
    error_category: ErrorCategory
    validation_result: Optional[ValidationResult] = None
    exercise_type: str = "fact"  # "fact", "query", "variable_query"


@dataclass
class HelpResponse:
    """Response from the error handling system."""
    message_lines: List[str]
    box_title: str
    color: str
    hint_level: HintLevel
    show_answer: bool = False
    offer_options: bool = False


class ProgressiveHintSystem:
    """
    Progressive hint system with escalating help levels.
    
    Provides increasingly specific guidance as users make more attempts,
    maintaining an encouraging tone throughout the learning process.
    """
    
    # Encouraging messages for different situations
    ENCOURAGING_MESSAGES = {
        "first_attempt": [
            "No worries! Even experienced programmers make syntax errors.",
            "That's okay! Prolog syntax takes some getting used to.",
            "Good attempt! Let's fix this together.",
            "You're learning! Each mistake brings you closer to mastery.",
            "Almost there! Just a small syntax adjustment needed.",
        ],
        "multiple_attempts": [
            "You're showing great persistence!",
            "Don't give up! You're doing great so far.",
            "Learning is a process - you're on the right track!",
            "Every attempt teaches you something new.",
            "Your dedication to learning is admirable!",
        ],
        "stuck_user": [
            "Sometimes the best way to learn is to see the answer.",
            "It's perfectly normal to need help when learning something new.",
            "Let's work through this together step by step.",
            "You've made a great effort - let me help you understand.",
            "Learning Prolog is challenging, but you're doing well!",
        ],
        "success_after_struggle": [
            "Persistence pays off! Well done!",
            "You didn't give up, and that's what matters most!",
            "This experience will make you a better programmer!",
            "You've built resilience as a programmer!",
            "Every programmer goes through this learning process!",
        ]
    }
    
    # Specific error patterns and their targeted messages
    ERROR_PATTERNS = {
        ErrorCategory.MISSING_PERIOD: {
            "detection": lambda text: not text.strip().endswith('.'),
            "messages": {
                HintLevel.GENTLE: "Don't forget the period (.) at the end!",
                HintLevel.SPECIFIC: "All Prolog statements must end with a period (.) - it's like punctuation in English.",
                HintLevel.DETAILED: "The period tells Prolog that your statement is complete. Add a '.' at the very end.",
                HintLevel.EXPLICIT: "Type exactly what you have, but add a period (.) at the end."
            }
        },
        ErrorCategory.UPPERCASE_PREDICATE: {
            "detection": lambda text: len(text) > 0 and text[0].isupper(),
            "messages": {
                HintLevel.GENTLE: "Predicate names start with lowercase letters.",
                HintLevel.SPECIFIC: "In Prolog, predicates (like 'likes') always start with lowercase letters.",
                HintLevel.DETAILED: "Change the first letter to lowercase. For example: 'Likes' should be 'likes'.",
                HintLevel.EXPLICIT: "Make the first letter lowercase and keep everything else the same."
            }
        },
        ErrorCategory.MISSING_PARENTHESES: {
            "detection": lambda text: '(' not in text or ')' not in text,
            "messages": {
                HintLevel.GENTLE: "Arguments go inside parentheses: predicate(arg1, arg2).",
                HintLevel.SPECIFIC: "You need parentheses around the arguments. The format is: predicate(argument1, argument2).",
                HintLevel.DETAILED: "Put opening parenthesis '(' after the predicate name, then your arguments, then closing parenthesis ')'.",
                HintLevel.EXPLICIT: "Add parentheses around your arguments like this: predicate(argument1, argument2)."
            }
        },
        ErrorCategory.MISSING_QUERY_PREFIX: {
            "detection": lambda text: not text.strip().startswith('?-'),
            "messages": {
                HintLevel.GENTLE: "Queries start with '?-': ?- predicate(arguments).",
                HintLevel.SPECIFIC: "All Prolog queries must start with '?-' followed by a space.",
                HintLevel.DETAILED: "Add '?- ' at the beginning of your query. The '?-' tells Prolog this is a question.",
                HintLevel.EXPLICIT: "Type '?- ' at the very beginning, then add your predicate and arguments."
            }
        },
        ErrorCategory.LOWERCASE_VARIABLE: {
            "detection": lambda text: any(c.islower() for c in text if c.isalpha() and text.find(c) > text.find('(')),
            "messages": {
                HintLevel.GENTLE: "Variables must start with UPPERCASE letters!",
                HintLevel.SPECIFIC: "In Prolog, variables always start with uppercase letters like X, Y, Name, etc.",
                HintLevel.DETAILED: "Change your variable to start with a capital letter. For example: 'x' should be 'X'.",
                HintLevel.EXPLICIT: "Make your variable uppercase. If you wrote 'x', change it to 'X'."
            }
        }
    }

    @staticmethod
    def get_encouraging_message(situation: str = "first_attempt") -> str:
        """
        Get a random encouraging message for the given situation.
        
        Args:
            situation: The situation context for the message
            
        Returns:
            An encouraging message string
        """
        messages = ProgressiveHintSystem.ENCOURAGING_MESSAGES.get(situation, 
                    ProgressiveHintSystem.ENCOURAGING_MESSAGES["first_attempt"])
        return random.choice(messages)

    @staticmethod
    def determine_hint_level(attempt_count: int) -> HintLevel:
        """
        Determine the appropriate hint level based on attempt count.
        
        Args:
            attempt_count: Number of attempts made
            
        Returns:
            Appropriate HintLevel for the attempt count
        """
        if attempt_count == 1:
            return HintLevel.GENTLE
        elif attempt_count == 2:
            return HintLevel.SPECIFIC
        elif attempt_count == 3:
            return HintLevel.DETAILED
        elif attempt_count == 4:
            return HintLevel.EXPLICIT
        else:
            return HintLevel.SHOW_ANSWER

    @staticmethod
    def categorize_error(error_context: ErrorContext) -> ErrorCategory:
        """
        Categorize the error based on user input and validation result.
        
        Args:
            error_context: Context information about the error
            
        Returns:
            ErrorCategory enum value
        """
        user_input = error_context.user_input.strip()
        validation_result = error_context.validation_result
        
        # Check for empty input
        if not user_input:
            return ErrorCategory.EMPTY_INPUT
        
        # Check for specific patterns
        if not user_input.endswith('.'):
            return ErrorCategory.MISSING_PERIOD
        
        if user_input and user_input[0].isupper():
            return ErrorCategory.UPPERCASE_PREDICATE
        
        if '(' not in user_input or ')' not in user_input:
            return ErrorCategory.MISSING_PARENTHESES
        
        if error_context.exercise_type in ["query", "variable_query"] and not user_input.startswith('?-'):
            return ErrorCategory.MISSING_QUERY_PREFIX
        
        # Check for lowercase variables in queries (check this before spaces in predicate)
        if error_context.exercise_type == "variable_query":
            paren_start = user_input.find('(')
            paren_end = user_input.rfind(')')
            if paren_start != -1 and paren_end != -1:
                args_section = user_input[paren_start+1:paren_end]
                # Look for single letters that should be variables
                for arg in args_section.split(','):
                    arg = arg.strip()
                    if len(arg) == 1 and arg.islower():
                        return ErrorCategory.LOWERCASE_VARIABLE
        
        if ' ' in user_input.split('(')[0] if '(' in user_input else False:
            return ErrorCategory.SPACES_IN_PREDICATE
        
        if user_input.count('(') != user_input.count(')'):
            return ErrorCategory.MISMATCHED_PARENTHESES
        
        # Use validation result if available
        if validation_result and validation_result.error_message:
            if "period" in validation_result.error_message.lower():
                return ErrorCategory.MISSING_PERIOD
            elif "uppercase" in validation_result.error_message.lower() or "lowercase" in validation_result.error_message.lower():
                if error_context.exercise_type == "variable_query":
                    return ErrorCategory.LOWERCASE_VARIABLE
                else:
                    return ErrorCategory.UPPERCASE_PREDICATE
            elif "parenthes" in validation_result.error_message.lower():
                return ErrorCategory.MISSING_PARENTHESES
            elif "query prefix" in validation_result.error_message.lower() or "?-" in validation_result.error_message:
                return ErrorCategory.MISSING_QUERY_PREFIX
        
        return ErrorCategory.GENERIC_SYNTAX

    @staticmethod
    def generate_error_response(error_context: ErrorContext) -> HelpResponse:
        """
        Generate a comprehensive error response with progressive hints.
        
        Args:
            error_context: Context information about the error
            
        Returns:
            HelpResponse with appropriate message and formatting
        """
        hint_level = ProgressiveHintSystem.determine_hint_level(error_context.attempt_count)
        error_category = ProgressiveHintSystem.categorize_error(error_context)
        
        # Get encouraging message based on attempt count
        if error_context.attempt_count == 1:
            encouragement = ProgressiveHintSystem.get_encouraging_message("first_attempt")
        elif error_context.attempt_count <= 3:
            encouragement = ProgressiveHintSystem.get_encouraging_message("multiple_attempts")
        else:
            encouragement = ProgressiveHintSystem.get_encouraging_message("stuck_user")
        
        # Build the response message
        message_lines = [encouragement, ""]
        
        # Add error-specific guidance
        if hint_level == HintLevel.SHOW_ANSWER:
            return ProgressiveHintSystem._generate_show_answer_response(error_context)
        
        # Get specific error message
        error_patterns = ProgressiveHintSystem.ERROR_PATTERNS.get(error_category)
        if error_patterns and hint_level in error_patterns["messages"]:
            specific_hint = error_patterns["messages"][hint_level]
        else:
            # Fallback to validation result hint or generic message
            if error_context.validation_result and error_context.validation_result.hint:
                specific_hint = error_context.validation_result.hint
            else:
                specific_hint = "Check your syntax and try again."
        
        # Add the error message and hint
        if error_context.validation_result and error_context.validation_result.error_message:
            message_lines.append(f"❌ Error: {error_context.validation_result.error_message}")
        else:
            message_lines.append("❌ There's a syntax error in your input.")
        
        message_lines.extend(["", f"💡 {specific_hint}"])
        
        # Add progressive guidance based on hint level
        if hint_level == HintLevel.SPECIFIC:
            message_lines.extend([
                "",
                "🔍 Remember the pattern:",
                f"   {ProgressiveHintSystem._get_pattern_example(error_context.exercise_type)}"
            ])
        elif hint_level == HintLevel.DETAILED:
            message_lines.extend([
                "",
                "📝 Let's check your syntax step by step:",
                *ProgressiveHintSystem._get_detailed_checklist(error_context.exercise_type)
            ])
        elif hint_level == HintLevel.EXPLICIT:
            message_lines.extend([
                "",
                "🎯 Here's exactly what you need:",
                "",
                f"   {error_context.expected_answer}",
                "",
                "Try typing this pattern with your specific content."
            ])
        
        # Determine box styling
        if hint_level in [HintLevel.GENTLE, HintLevel.SPECIFIC]:
            box_title = "SYNTAX ERROR - TRY AGAIN"
            color = "yellow"
        elif hint_level == HintLevel.DETAILED:
            box_title = "LET'S DEBUG THIS TOGETHER"
            color = "yellow"
        else:  # EXPLICIT
            box_title = "DETAILED GUIDANCE"
            color = "cyan"
        
        return HelpResponse(
            message_lines=message_lines,
            box_title=box_title,
            color=color,
            hint_level=hint_level,
            offer_options=(error_context.attempt_count >= 3)
        )

    @staticmethod
    def _generate_show_answer_response(error_context: ErrorContext) -> HelpResponse:
        """Generate response for showing the correct answer."""
        encouragement = ProgressiveHintSystem.get_encouraging_message("stuck_user")
        
        message_lines = [
            encouragement,
            "",
            "After several attempts, let me show you the correct answer:",
            "",
            f"✅ {error_context.expected_answer}",
            "",
            "Let's break this down completely:",
            *ProgressiveHintSystem._get_complete_breakdown(error_context.expected_answer, error_context.exercise_type)
        ]
        
        return HelpResponse(
            message_lines=message_lines,
            box_title="HERE'S THE COMPLETE ANSWER",
            color="green",
            hint_level=HintLevel.SHOW_ANSWER,
            show_answer=True
        )

    @staticmethod
    def _get_pattern_example(exercise_type: str) -> str:
        """Get pattern example for the exercise type."""
        if exercise_type == "fact":
            return "predicate(argument1, argument2)."
        elif exercise_type == "query":
            return "?- predicate(argument1, argument2)."
        elif exercise_type == "variable_query":
            return "?- predicate(Variable, argument)."
        else:
            return "predicate(argument1, argument2)."

    @staticmethod
    def _get_detailed_checklist(exercise_type: str) -> List[str]:
        """Get detailed syntax checklist for the exercise type."""
        if exercise_type == "fact":
            return [
                "   1. Does it start with a lowercase predicate?",
                "   2. Are the arguments in parentheses?",
                "   3. Are arguments separated by commas?",
                "   4. Does it end with a period (.)?",
            ]
        elif exercise_type == "query":
            return [
                "   1. Does it start with '?-' followed by a space?",
                "   2. Is the predicate lowercase?",
                "   3. Are the arguments in parentheses?",
                "   4. Does it end with a period (.)?",
            ]
        elif exercise_type == "variable_query":
            return [
                "   1. Does it start with '?-' followed by a space?",
                "   2. Is the predicate lowercase?",
                "   3. Are variables UPPERCASE?",
                "   4. Are arguments in parentheses?",
                "   5. Does it end with a period (.)?",
            ]
        else:
            return ["   Check the basic Prolog syntax rules."]

    @staticmethod
    def _get_complete_breakdown(answer: str, exercise_type: str) -> List[str]:
        """Get complete breakdown of the correct answer."""
        breakdown = []
        
        if exercise_type == "fact":
            breakdown.extend([
                "",
                "🔍 Predicate: The relationship name (lowercase)",
                "🔍 Arguments: The things involved (in parentheses)",
                "🔍 Period: Marks the end of the statement (required!)",
                "",
                "This fact tells Prolog something that is always true.",
            ])
        elif exercise_type in ["query", "variable_query"]:
            breakdown.extend([
                "",
                "🔍 '?-': Query prefix (asks 'Is it true that...')",
                "🔍 Predicate: The relationship to check (lowercase)",
                "🔍 Arguments: What to check (atoms or Variables)",
                "🔍 Period: Marks the end of the query (required!)",
                "",
                "This query asks Prolog to find matching facts.",
            ])
            
            if exercise_type == "variable_query":
                breakdown.extend([
                    "",
                    "💡 Variables (UPPERCASE) can match any value!",
                ])
        
        return breakdown


class RecoveryMechanisms:
    """
    Recovery mechanisms for users who are stuck or frustrated.
    
    Provides various options to help users continue learning without
    giving up when they encounter difficulties.
    """
    
    @staticmethod
    def offer_help_options(attempt_count: int, exercise_type: str) -> Dict[str, str]:
        """
        Offer appropriate help options based on user's situation.
        
        Args:
            attempt_count: Number of attempts made
            exercise_type: Type of exercise (fact, query, variable_query)
            
        Returns:
            Dictionary of option codes to descriptions
        """
        base_options = {
            "continue": "Keep trying (I can do this!)",
            "hint": "Give me a more specific hint",
            "example": "Show me a similar example",
            "answer": "Show me the correct answer",
        }
        
        if attempt_count >= 3:
            base_options["skip"] = "Skip this exercise for now"
        
        if attempt_count >= 5:
            base_options["review"] = "Review the concept explanation again"
        
        return base_options

    @staticmethod
    def generate_help_menu(attempt_count: int, exercise_type: str) -> List[str]:
        """
        Generate a help menu with available options.
        
        Args:
            attempt_count: Number of attempts made
            exercise_type: Type of exercise
            
        Returns:
            List of menu lines to display
        """
        options = RecoveryMechanisms.offer_help_options(attempt_count, exercise_type)
        
        menu_lines = [
            "🤔 You've made several attempts. What would you like to do?",
            "",
        ]
        
        for i, (code, description) in enumerate(options.items(), 1):
            menu_lines.append(f"{i}. {description}")
        
        menu_lines.extend([
            "",
            "Choose a number, or type 'continue' to keep trying:",
        ])
        
        return menu_lines

    @staticmethod
    def provide_alternative_explanation(exercise_type: str, concept: str) -> List[str]:
        """
        Provide alternative explanation for a concept.
        
        Args:
            exercise_type: Type of exercise
            concept: Specific concept to explain
            
        Returns:
            List of explanation lines
        """
        explanations = {
            "fact": [
                "🎯 Think of facts like entries in a database:",
                "",
                "• Each fact is a piece of information",
                "• It states something that is always true",
                "• Format: relationship(thing1, thing2).",
                "",
                "Example: likes(alice, chocolate).",
                "This means 'Alice likes chocolate' is true.",
            ],
            "query": [
                "🎯 Think of queries like questions you ask:",
                "",
                "• You're asking 'Is this true?'",
                "• Start with '?-' to signal it's a question",
                "• Use the same format as facts",
                "",
                "Example: ?- likes(alice, chocolate).",
                "This asks 'Does Alice like chocolate?'",
            ],
            "variable_query": [
                "🎯 Variables are like blanks to fill in:",
                "",
                "• Variables start with UPPERCASE letters",
                "• They can match any value",
                "• Prolog finds all possible matches",
                "",
                "Example: ?- likes(alice, X).",
                "This asks 'What does Alice like?'",
            ]
        }
        
        return explanations.get(exercise_type, ["No alternative explanation available."])


def create_comprehensive_error_handler():
    """
    Factory function to create a comprehensive error handler.
    
    Returns:
        Configured error handling system
    """
    return {
        "hint_system": ProgressiveHintSystem(),
        "recovery": RecoveryMechanisms(),
        "max_attempts": 6,
        "show_answer_threshold": 4,
        "offer_help_threshold": 3,
    }