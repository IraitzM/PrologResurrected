"""
Prolog Concepts Module

Individual puzzle implementations for each Prolog concept taught in Logic Quest.
Contains specific puzzles for facts, rules, unification, backtracking, and recursion.
"""

from typing import Dict, Any
from .puzzles import BasePuzzle, PuzzleDifficulty
from .validation import ValidationResult, PrologValidator


class FactCreationPuzzle(BasePuzzle):
    """Puzzle for learning to create Prolog facts."""

    def __init__(self, puzzle_id: str, scenario: Dict[str, Any]):
        """
        Initialize a fact creation puzzle.

        Args:
            puzzle_id: Unique identifier for the puzzle
            scenario: Dictionary containing puzzle scenario details
        """
        super().__init__(puzzle_id, scenario["title"], PuzzleDifficulty.BEGINNER)
        self.scenario = scenario
        self.expected_predicate = scenario["predicate"]
        self.expected_args = scenario["arguments"]
        self.context_facts = scenario.get("context_facts", [])

    def get_description(self) -> str:
        return self.scenario["description"]

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": self.context_facts,
            "rules": [],
            "scenario": self.scenario.get("story_context", ""),
            "instructions": self.scenario.get("instructions", ""),
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # First validate basic syntax
        result = PrologValidator.validate_fact(user_input)

        if not result.is_valid:
            return result

        # Check if it matches the expected solution
        components = result.parsed_components
        if (
            components
            and components.get("predicate") == self.expected_predicate
            and components.get("arguments") == self.expected_args
        ):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The fact is syntactically correct but doesn't match the scenario.",
            hint=f"Make sure you're using the '{self.expected_predicate}' predicate with the correct arguments.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = self.scenario.get(
            "hints",
            [
                "Think about the relationship described in the scenario.",
                f"Use '{self.expected_predicate}' as the predicate name.",
                f"The arguments should be: {', '.join(self.expected_args)}",
                "Don't forget the period at the end!",
            ],
        )

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "You're very close! Check the exact format required."

    def get_expected_solution(self) -> str:
        args_str = ", ".join(self.expected_args)
        return f"{self.expected_predicate}({args_str})."


class QueryWritingPuzzle(BasePuzzle):
    """Puzzle for learning to write Prolog queries."""

    def __init__(self, puzzle_id: str, scenario: Dict[str, Any]):
        super().__init__(puzzle_id, scenario["title"], PuzzleDifficulty.BEGINNER)
        self.scenario = scenario
        self.knowledge_base = scenario["knowledge_base"]
        self.expected_query = scenario["expected_query"]

    def get_description(self) -> str:
        return self.scenario["description"]

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": self.knowledge_base,
            "rules": [],
            "question": self.scenario.get("question", ""),
            "instructions": "Write a query to answer the question.",
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # First validate basic query syntax
        result = PrologValidator.validate_query(user_input)

        if not result.is_valid:
            return result

        # Check if it matches the expected query pattern
        if self._queries_equivalent(user_input.strip(), self.expected_query):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The query is syntactically correct but doesn't answer the question.",
            hint="Make sure your query matches what the question is asking.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = self.scenario.get(
            "hints",
            [
                "Remember that queries start with '?-'",
                "Look at the facts to see what predicates are available",
                f"The query should look something like: {self.expected_query}",
                "Don't forget the period at the end!",
            ],
        )

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "Check the expected query format carefully."

    def get_expected_solution(self) -> str:
        return self.expected_query

    def _queries_equivalent(self, query1: str, query2: str) -> bool:
        """Check if two queries are logically equivalent."""
        # Simple string comparison for now - could be enhanced
        return query1.lower().replace(" ", "") == query2.lower().replace(" ", "")


class RuleDefinitionPuzzle(BasePuzzle):
    """Puzzle for learning to define Prolog rules."""

    def __init__(self, puzzle_id: str, scenario: Dict[str, Any]):
        super().__init__(puzzle_id, scenario["title"], PuzzleDifficulty.INTERMEDIATE)
        self.scenario = scenario
        self.base_facts = scenario["base_facts"]
        self.expected_rule = scenario["expected_rule"]
        self.rule_concept = scenario.get("concept", "logical implication")

    def get_description(self) -> str:
        return self.scenario["description"]

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": self.base_facts,
            "rules": [],
            "concept": self.rule_concept,
            "instructions": "Define a rule that captures the logical relationship.",
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # Basic rule syntax validation
        if not self._is_valid_rule_syntax(user_input):
            return ValidationResult(
                is_valid=False,
                error_message="Invalid rule syntax.",
                hint="Rules should follow the pattern: head :- body.",
            )

        # Check if it matches the expected rule concept
        if self._rule_matches_expected(user_input):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The rule syntax is correct but doesn't capture the intended logic.",
            hint="Think about what conditions need to be true for the conclusion to hold.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = self.scenario.get(
            "hints",
            [
                "Rules have a head (conclusion) and body (conditions)",
                "Use ':-' to separate the head from the body",
                "The body can have multiple conditions separated by commas",
                f"The rule should look something like: {self.expected_rule}",
            ],
        )

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "Consider what needs to be true for your conclusion to be valid."

    def get_expected_solution(self) -> str:
        return self.expected_rule

    def _is_valid_rule_syntax(self, rule: str) -> bool:
        """Check if the rule has valid Prolog syntax."""
        return ":-" in rule and rule.strip().endswith(".")

    def _rule_matches_expected(self, rule: str) -> bool:
        """Check if the rule matches the expected logical structure."""
        # Simplified matching - could be enhanced with proper parsing
        rule_clean = rule.lower().replace(" ", "")
        expected_clean = self.expected_rule.lower().replace(" ", "")
        return rule_clean == expected_clean


class UnificationPuzzle(BasePuzzle):
    """Puzzle for learning Prolog unification and pattern matching."""

    def __init__(self, puzzle_id: str, scenario: Dict[str, Any]):
        super().__init__(puzzle_id, scenario["title"], PuzzleDifficulty.INTERMEDIATE)
        self.scenario = scenario
        self.facts = scenario["facts"]
        self.pattern_query = scenario["pattern_query"]
        self.expected_bindings = scenario.get("expected_bindings", {})

    def get_description(self) -> str:
        return self.scenario["description"]

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": self.facts,
            "rules": [],
            "concept": "Pattern matching and variable binding",
            "instructions": "Write a query that demonstrates unification.",
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # Validate query syntax
        result = PrologValidator.validate_query(user_input)

        if not result.is_valid:
            return result

        # Check if it demonstrates the unification concept
        if self._demonstrates_unification(user_input):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The query is valid but doesn't demonstrate the unification concept.",
            hint="Use variables to show how Prolog matches patterns.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = self.scenario.get(
            "hints",
            [
                "Use variables (starting with uppercase) to find patterns",
                "Variables can match any value in the facts",
                "Think about what you want to find or match",
                f"Try a query like: {self.pattern_query}",
            ],
        )

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "Focus on using variables to demonstrate pattern matching."

    def get_expected_solution(self) -> str:
        return self.pattern_query

    def _demonstrates_unification(self, query: str) -> bool:
        """Check if the query demonstrates unification concepts."""
        # Check for variables (uppercase letters)
        import re

        has_variables = bool(re.search(r"\b[A-Z][a-zA-Z0-9_]*\b", query))
        return has_variables and "?-" in query


class BacktrackingPuzzle(BasePuzzle):
    """Puzzle for learning Prolog backtracking."""

    def __init__(self, puzzle_id: str, scenario: Dict[str, Any]):
        super().__init__(puzzle_id, scenario["title"], PuzzleDifficulty.ADVANCED)
        self.scenario = scenario
        self.knowledge_base = scenario["knowledge_base"]
        self.multi_solution_query = scenario["multi_solution_query"]

    def get_description(self) -> str:
        return self.scenario["description"]

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": self.knowledge_base.get("facts", []),
            "rules": self.knowledge_base.get("rules", []),
            "concept": "Backtracking and multiple solutions",
            "instructions": "Write a query that will find multiple solutions.",
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # Validate query syntax
        result = PrologValidator.validate_query(user_input)

        if not result.is_valid:
            return result

        # Check if it's designed to find multiple solutions
        if self._enables_backtracking(user_input):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The query is valid but won't demonstrate backtracking.",
            hint="Use variables in a way that can match multiple facts.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = self.scenario.get(
            "hints",
            [
                "Backtracking finds all possible solutions to a query",
                "Use variables that can match multiple facts",
                "Think about queries that have more than one answer",
                f"Try something like: {self.multi_solution_query}",
            ],
        )

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "Consider what query would return multiple different answers."

    def get_expected_solution(self) -> str:
        return self.multi_solution_query

    def _enables_backtracking(self, query: str) -> bool:
        """Check if the query is likely to produce multiple solutions."""
        # Simple heuristic: has variables and matches a general pattern
        import re

        has_variables = bool(re.search(r"\b[A-Z][a-zA-Z0-9_]*\b", query))
        return has_variables


class RecursionPuzzle(BasePuzzle):
    """Puzzle for learning Prolog recursion."""

    def __init__(self, puzzle_id: str, scenario: Dict[str, Any]):
        super().__init__(puzzle_id, scenario["title"], PuzzleDifficulty.EXPERT)
        self.scenario = scenario
        self.base_facts = scenario["base_facts"]
        self.recursive_rule = scenario["recursive_rule"]
        self.concept = scenario.get("concept", "recursive relationships")

    def get_description(self) -> str:
        return self.scenario["description"]

    def get_initial_context(self) -> Dict[str, Any]:
        return {
            "facts": self.base_facts,
            "rules": [],
            "concept": self.concept,
            "instructions": "Define a recursive rule that builds on simpler cases.",
        }

    def validate_solution(self, user_input: str) -> ValidationResult:
        # Check for basic rule syntax
        if not self._is_valid_rule_syntax(user_input):
            return ValidationResult(
                is_valid=False,
                error_message="Invalid rule syntax.",
                hint="Rules should follow the pattern: head :- body.",
            )

        # Check if it demonstrates recursion
        if self._is_recursive_rule(user_input):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            error_message="The rule is valid but doesn't demonstrate recursion.",
            hint="Recursive rules call themselves with simpler inputs.",
        )

    def get_hint(self, hint_level: int) -> str:
        hints = self.scenario.get(
            "hints",
            [
                "Recursive rules have two parts: base case and recursive case",
                "The base case stops the recursion",
                "The recursive case calls the same predicate with simpler input",
                f"The rule should look like: {self.recursive_rule}",
            ],
        )

        if hint_level <= len(hints):
            return hints[hint_level - 1]
        return "Think about how to break the problem into smaller pieces."

    def get_expected_solution(self) -> str:
        return self.recursive_rule

    def _is_valid_rule_syntax(self, rule: str) -> bool:
        """Check if the rule has valid Prolog syntax."""
        return ":-" in rule and rule.strip().endswith(".")

    def _is_recursive_rule(self, rule: str) -> bool:
        """Check if the rule demonstrates recursion."""
        # Extract the head predicate
        if ":-" not in rule:
            return False

        head = rule.split(":-")[0].strip()
        body = rule.split(":-")[1].strip()

        # Extract predicate name from head
        if "(" in head:
            predicate_name = head.split("(")[0].strip()
            # Check if the same predicate appears in the body
            return predicate_name in body

        return False


# Predefined puzzle scenarios for each concept
FACT_SCENARIOS = [
    {
        "title": "Employee Database",
        "description": "Create a fact stating that Alice works in the Engineering department.",
        "predicate": "works_in",
        "arguments": ["alice", "engineering"],
        "story_context": "You're building an employee database for Cyberdyne Systems.",
        "instructions": "Use the 'works_in' predicate to state Alice's department.",
        "hints": [
            "Think about the relationship between Alice and her department.",
            "Use 'works_in' as the predicate name.",
            "The format should be: works_in(alice, engineering).",
            "Don't forget the period at the end!",
        ],
    },
    {
        "title": "Family Relationships",
        "description": "Create a fact stating that Tom is the parent of Bob.",
        "predicate": "parent",
        "arguments": ["tom", "bob"],
        "story_context": "You're modeling family relationships in the AI's memory.",
        "instructions": "Use the 'parent' predicate to show the relationship.",
        "hints": [
            "Think about the parent-child relationship.",
            "Use 'parent' as the predicate name.",
            "Tom should be the first argument, Bob the second.",
            "Remember the period at the end!",
        ],
    },
]

QUERY_SCENARIOS = [
    {
        "title": "Finding Employees",
        "description": "Write a query to find who works in the engineering department.",
        "knowledge_base": [
            "works_in(alice, engineering).",
            "works_in(bob, marketing).",
            "works_in(charlie, engineering).",
        ],
        "expected_query": "?- works_in(X, engineering).",
        "question": "Who works in engineering?",
        "hints": [
            "Use a variable (starting with uppercase) for the unknown person.",
            "The department 'engineering' is known.",
            "Format: ?- works_in(Variable, engineering).",
            "Don't forget the period!",
        ],
    }
]

RULE_SCENARIOS = [
    {
        "title": "Sibling Relationship",
        "description": "Define a rule that determines when two people are siblings.",
        "base_facts": [
            "parent(tom, alice).",
            "parent(tom, bob).",
            "parent(mary, alice).",
            "parent(mary, bob).",
        ],
        "expected_rule": "sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \\= Y.",
        "concept": "Two people are siblings if they have the same parent and are different people.",
        "hints": [
            "Siblings share at least one parent.",
            "Use variables to represent the people and parent.",
            "Make sure X and Y are different people (X \\= Y).",
            "Format: sibling(X, Y) :- conditions.",
        ],
    }
]

UNIFICATION_SCENARIOS = [
    {
        "title": "Pattern Matching",
        "description": "Write a query to find all people and what they like.",
        "facts": [
            "likes(alice, chocolate).",
            "likes(bob, pizza).",
            "likes(charlie, ice_cream).",
        ],
        "pattern_query": "?- likes(Person, Food).",
        "expected_bindings": {
            "Person": ["alice", "bob", "charlie"],
            "Food": ["chocolate", "pizza", "ice_cream"],
        },
        "hints": [
            "Use variables for both the person and what they like.",
            "Variables start with uppercase letters.",
            "This will find all person-food combinations.",
            "Format: ?- likes(Person, Food).",
        ],
    }
]

BACKTRACKING_SCENARIOS = [
    {
        "title": "Multiple Solutions",
        "description": "Write a query that finds all of Alice's interests using backtracking.",
        "knowledge_base": {
            "facts": [
                "likes(alice, chocolate).",
                "likes(alice, reading).",
                "likes(alice, programming).",
                "likes(bob, pizza).",
            ]
        },
        "multi_solution_query": "?- likes(alice, X).",
        "hints": [
            "Use a variable for what Alice likes.",
            "This will find multiple answers through backtracking.",
            "Prolog will find all things Alice likes.",
            "Format: ?- likes(alice, X).",
        ],
    }
]

RECURSION_SCENARIOS = [
    {
        "title": "Ancestor Relationship",
        "description": "Define a recursive rule for the ancestor relationship.",
        "base_facts": [
            "parent(tom, bob).",
            "parent(bob, alice).",
            "parent(mary, charlie).",
        ],
        "recursive_rule": "ancestor(X, Y) :- parent(X, Y). ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).",
        "concept": "An ancestor is either a parent (base case) or a parent of an ancestor (recursive case).",
        "hints": [
            "You need both a base case and a recursive case.",
            "Base case: a parent is an ancestor.",
            "Recursive case: ancestor of ancestor is ancestor.",
            "Use the same predicate name in the rule body.",
        ],
    }
]
