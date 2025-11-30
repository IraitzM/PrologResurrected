"""
Memory Stack Failure Puzzle

First adventure mode puzzle teaching debugging concepts through Prolog-based
investigation of simulated system failures. Players examine stack traces,
write queries, and diagnose root causes.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
import random
import re

from prologresurrected.game.validation import PrologValidator, ValidationResult
from prologresurrected.game.hint_system import ComplexityAwareHintSystem, HintType
from prologresurrected.game.complexity import ComplexityLevel
from prologresurrected.game.puzzles import BasePuzzle, PuzzleDifficulty


class FailureScenario(Enum):
    """Types of system failures that can be investigated."""
    MEMORY_LEAK = "memory_leak"
    STACK_OVERFLOW = "stack_overflow"
    NULL_POINTER = "null_pointer"
    DEADLOCK = "deadlock"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


@dataclass
class StackFrame:
    """
    Represents a single stack frame in the memory trace.
    
    A stack frame captures the state of a function call including its
    identifier, name, caller relationship, timing, memory usage, and status.
    """
    frame_id: int
    function_name: str
    caller_id: Optional[int]
    timestamp: int
    memory_allocated: int
    status: str  # "active", "completed", "error"
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_prolog_facts(self) -> List[str]:
        """
        Convert stack frame to Prolog fact representation.
        
        Returns:
            List of Prolog fact strings representing this frame
        """
        facts = []
        
        # Basic frame information
        facts.append(
            f"frame({self.frame_id}, {self.function_name}, {self.timestamp}, {self.status})."
        )
        
        # Caller-callee relationship
        if self.caller_id is not None:
            facts.append(f"calls({self.caller_id}, {self.frame_id}).")
        
        # Memory allocation
        facts.append(f"allocated({self.frame_id}, {self.memory_allocated}).")
        
        # Function parameters
        for param_name, param_value in self.parameters.items():
            # Format parameter value appropriately
            if isinstance(param_value, str):
                formatted_value = param_value
            elif isinstance(param_value, (int, float)):
                formatted_value = str(param_value)
            elif param_value is None:
                formatted_value = "null"
            else:
                formatted_value = str(param_value)
            
            facts.append(f"param({self.frame_id}, {param_name}, {formatted_value}).")
        
        # Frame status
        facts.append(f"status({self.frame_id}, {self.status}).")
        
        return facts


class StackFrameGenerator:
    """
    Generates realistic stack frames with embedded anomalies for different
    failure scenarios.
    """
    
    # Common function names for realistic stack traces
    SYSTEM_FUNCTIONS = [
        "init_system", "load_config", "start_ai_core", "process_request",
        "allocate_buffer", "parse_input", "validate_data", "execute_query",
        "format_response", "cleanup_resources", "log_event", "check_permissions",
        "acquire_lock", "release_lock", "read_file", "write_file"
    ]
    
    def __init__(self, scenario: FailureScenario, seed: Optional[int] = None):
        """
        Initialize the stack frame generator.
        
        Args:
            scenario: The type of failure to simulate
            seed: Optional random seed for reproducible generation
        """
        self.scenario = scenario
        self.frames: List[StackFrame] = []
        self.next_frame_id = 1
        self.current_timestamp = 1000
        
        if seed is not None:
            random.seed(seed)
    
    def generate_stack_trace(self, num_frames: int = 10) -> List[StackFrame]:
        """
        Generate a complete stack trace with embedded anomaly.
        
        Args:
            num_frames: Number of stack frames to generate
            
        Returns:
            List of StackFrame objects representing the trace
        """
        self.frames = []
        self.next_frame_id = 1
        self.current_timestamp = 1000
        
        # Generate normal initialization frames
        self._generate_normal_frames(num_frames // 2)
        
        # Inject anomaly based on scenario
        if self.scenario == FailureScenario.MEMORY_LEAK:
            self._inject_memory_leak()
        elif self.scenario == FailureScenario.STACK_OVERFLOW:
            self._inject_stack_overflow()
        elif self.scenario == FailureScenario.NULL_POINTER:
            self._inject_null_pointer()
        elif self.scenario == FailureScenario.DEADLOCK:
            self._inject_deadlock()
        elif self.scenario == FailureScenario.RESOURCE_EXHAUSTION:
            self._inject_resource_exhaustion()
        
        # Generate remaining frames
        remaining = num_frames - len(self.frames)
        if remaining > 0:
            self._generate_normal_frames(remaining)
        
        return self.frames
    
    def _generate_normal_frames(self, count: int) -> None:
        """Generate normal, non-anomalous stack frames."""
        for _ in range(count):
            function_name = random.choice(self.SYSTEM_FUNCTIONS)
            caller_id = self.frames[-1].frame_id if self.frames else None
            
            frame = StackFrame(
                frame_id=self.next_frame_id,
                function_name=function_name,
                caller_id=caller_id,
                timestamp=self.current_timestamp,
                memory_allocated=random.randint(1024, 8192),  # 1KB to 8KB
                status=random.choice(["active", "completed"]),
                parameters=self._generate_normal_parameters()
            )
            
            self.frames.append(frame)
            self.next_frame_id += 1
            self.current_timestamp += random.randint(10, 100)
    
    def _generate_normal_parameters(self) -> Dict[str, Any]:
        """Generate normal function parameters."""
        param_count = random.randint(0, 3)
        params = {}
        
        for i in range(param_count):
            param_name = f"arg{i}"
            param_value = random.choice([
                random.randint(0, 1000),
                f"data_{random.randint(1, 100)}",
                None
            ])
            params[param_name] = param_value
        
        return params
    
    def _inject_memory_leak(self) -> None:
        """
        Inject memory leak anomaly.
        
        Creates multiple frames allocating memory without corresponding
        deallocation, with increasing memory usage.
        """
        # Create several allocate_buffer calls with no cleanup
        for i in range(3):
            frame = StackFrame(
                frame_id=self.next_frame_id,
                function_name="allocate_buffer",
                caller_id=self.frames[-1].frame_id if self.frames else None,
                timestamp=self.current_timestamp,
                memory_allocated=1048576,  # 1MB each
                status="active",
                parameters={"buffer_size": 1048576, "buffer_id": i}
            )
            
            self.frames.append(frame)
            self.next_frame_id += 1
            self.current_timestamp += 50
        
        # Note: No corresponding cleanup_resources or release frames
    
    def _inject_stack_overflow(self) -> None:
        """
        Inject stack overflow anomaly.
        
        Creates recursive calls that exceed reasonable depth.
        """
        # Create deep recursive call chain
        function_name = "recursive_process"
        
        for depth in range(15):  # Excessive recursion depth
            caller_id = self.frames[-1].frame_id if self.frames else None
            
            frame = StackFrame(
                frame_id=self.next_frame_id,
                function_name=function_name,
                caller_id=caller_id,
                timestamp=self.current_timestamp,
                memory_allocated=4096,
                status="active",
                parameters={"depth": depth, "max_depth": 10}  # Exceeds max!
            )
            
            self.frames.append(frame)
            self.next_frame_id += 1
            self.current_timestamp += 5
    
    def _inject_null_pointer(self) -> None:
        """
        Inject null pointer anomaly.
        
        Creates a frame with null/invalid parameters.
        """
        frame = StackFrame(
            frame_id=self.next_frame_id,
            function_name="process_request",
            caller_id=self.frames[-1].frame_id if self.frames else None,
            timestamp=self.current_timestamp,
            memory_allocated=2048,
            status="error",
            parameters={"request_data": None, "handler": None}  # Null parameters!
        )
        
        self.frames.append(frame)
        self.next_frame_id += 1
        self.current_timestamp += 20
    
    def _inject_deadlock(self) -> None:
        """
        Inject deadlock anomaly.
        
        Creates two frames waiting on each other's locks.
        """
        # Frame 1: Acquired lock A, waiting for lock B
        frame1 = StackFrame(
            frame_id=self.next_frame_id,
            function_name="acquire_lock",
            caller_id=self.frames[-1].frame_id if self.frames else None,
            timestamp=self.current_timestamp,
            memory_allocated=1024,
            status="active",
            parameters={"lock_id": "lock_a", "waiting_for": "lock_b"}
        )
        self.frames.append(frame1)
        self.next_frame_id += 1
        self.current_timestamp += 10
        
        # Frame 2: Acquired lock B, waiting for lock A
        frame2 = StackFrame(
            frame_id=self.next_frame_id,
            function_name="acquire_lock",
            caller_id=self.frames[-1].frame_id if self.frames else None,
            timestamp=self.current_timestamp,
            memory_allocated=1024,
            status="active",
            parameters={"lock_id": "lock_b", "waiting_for": "lock_a"}
        )
        self.frames.append(frame2)
        self.next_frame_id += 1
        self.current_timestamp += 10
    
    def _inject_resource_exhaustion(self) -> None:
        """
        Inject resource exhaustion anomaly.
        
        Creates frames showing excessive resource consumption.
        """
        # Create multiple frames with very high memory allocation
        for i in range(5):
            frame = StackFrame(
                frame_id=self.next_frame_id,
                function_name="load_dataset",
                caller_id=self.frames[-1].frame_id if self.frames else None,
                timestamp=self.current_timestamp,
                memory_allocated=10485760,  # 10MB each = 50MB total
                status="active",
                parameters={"dataset_id": i, "size": "large"}
            )
            
            self.frames.append(frame)
            self.next_frame_id += 1
            self.current_timestamp += 100


class QueryValidator(PrologValidator):
    """
    Extended validator for memory stack puzzle queries.
    
    Supports validation of:
    - Basic Prolog queries
    - Compound queries with multiple conditions (AND)
    - Negation queries (checking for absence of data)
    - Variable binding queries
    - Relationship queries
    """
    
    # Pattern for compound queries: ?- pred1(...), pred2(...).
    COMPOUND_QUERY_PATTERN = r"^\?\-\s+(.+)\.$"
    
    # Pattern for negation: \+ predicate(...)
    NEGATION_PATTERN = r"\\+\s*"
    
    # Valid predicates for memory stack puzzle
    VALID_PREDICATES = {
        "frame", "calls", "allocated", "param", "status"
    }
    
    @staticmethod
    def validate_query(user_input: str) -> ValidationResult:
        """
        Validate a Prolog query with support for compound and negation queries.
        
        Args:
            user_input: The user's query string to validate
            
        Returns:
            ValidationResult with validation status and feedback
        """
        if not user_input or not user_input.strip():
            return ValidationResult(
                is_valid=False,
                error_message="Empty input - please enter a Prolog query.",
                hint="A query should look like: ?- predicate(argument1, argument2).",
            )
        
        user_input = user_input.strip()
        
        # Check for missing query prefix
        if not user_input.startswith("?-"):
            return ValidationResult(
                is_valid=False,
                error_message="Missing query prefix '?-'.",
                hint="All Prolog queries must start with '?-'. Try: ?- predicate(arguments).",
            )
        
        # Check for missing period
        if not user_input.endswith("."):
            return ValidationResult(
                is_valid=False,
                error_message="Missing period at the end.",
                hint="All Prolog queries must end with a period (.).",
            )
        
        # Extract query body (remove ?- and .)
        query_body = user_input[2:-1].strip()
        
        if not query_body:
            return ValidationResult(
                is_valid=False,
                error_message="Empty query body.",
                hint="You need to specify what you want to query. Example: ?- frame(1, X, Y, Z).",
            )
        
        # Check if it's a negation query (check before compound)
        if query_body.startswith("\\+"):
            return QueryValidator._validate_negation_query(user_input, query_body)
        
        # Check if it's a compound query (split by commas outside parentheses)
        conditions = QueryValidator._split_conditions(query_body)
        if len(conditions) > 1:
            return QueryValidator._validate_compound_query(user_input, query_body)
        
        # Validate as simple query
        return QueryValidator._validate_simple_query(user_input, query_body)
    
    @staticmethod
    def _validate_simple_query(full_query: str, query_body: str) -> ValidationResult:
        """
        Validate a simple (single predicate) query.
        
        Args:
            full_query: The complete query string with ?- and .
            query_body: The query body without ?- and .
            
        Returns:
            ValidationResult with validation status and feedback
        """
        # Check basic structure with parentheses
        if "(" not in query_body or ")" not in query_body:
            return ValidationResult(
                is_valid=False,
                error_message="Missing parentheses around arguments.",
                hint="Queries need parentheses: ?- predicate(argument1, argument2).",
            )
        
        # Extract predicate name
        paren_pos = query_body.find("(")
        predicate = query_body[:paren_pos].strip()
        
        # Validate predicate name
        if not predicate:
            return ValidationResult(
                is_valid=False,
                error_message="Missing predicate name.",
                hint="Specify what you want to query. Example: ?- frame(1, X, Y, Z).",
            )
        
        if not re.match(r"^[a-z][a-zA-Z0-9_]*$", predicate):
            if predicate[0].isupper():
                return ValidationResult(
                    is_valid=False,
                    error_message="Predicate names must start with a lowercase letter.",
                    hint=f"Try changing '{predicate}' to start with lowercase.",
                )
            else:
                return ValidationResult(
                    is_valid=False,
                    error_message="Invalid predicate name.",
                    hint="Predicate names should contain only letters, numbers, and underscores.",
                )
        
        # Check for valid predicate in memory stack context
        if predicate not in QueryValidator.VALID_PREDICATES:
            return ValidationResult(
                is_valid=False,
                error_message=f"Unknown predicate '{predicate}'.",
                hint=f"Valid predicates are: {', '.join(sorted(QueryValidator.VALID_PREDICATES))}.",
            )
        
        # Check for mismatched parentheses
        open_count = query_body.count("(")
        close_count = query_body.count(")")
        if open_count != close_count:
            return ValidationResult(
                is_valid=False,
                error_message="Mismatched parentheses.",
                hint="Make sure each '(' has a matching ')'.",
            )
        
        # Extract and validate arguments
        try:
            args_start = query_body.find("(") + 1
            args_end = query_body.rfind(")")
            args_str = query_body[args_start:args_end].strip()
            
            if not args_str:
                return ValidationResult(
                    is_valid=False,
                    error_message="Empty argument list.",
                    hint=f"The {predicate} predicate requires arguments. Example: ?- {predicate}(arg1, arg2).",
                )
            
            arguments = [arg.strip() for arg in args_str.split(",")]
            
            # Validate each argument
            for arg in arguments:
                if not arg:
                    return ValidationResult(
                        is_valid=False,
                        error_message="Empty argument in query.",
                        hint="Check for extra commas or missing arguments.",
                    )
                
                # Check for valid argument format (atom, variable, or number)
                if not re.match(r"^([a-z][a-zA-Z0-9_]*|[A-Z_][a-zA-Z0-9_]*|\d+)$", arg):
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"Invalid argument '{arg}'.",
                        hint="Arguments should be atoms (lowercase), variables (uppercase), or numbers.",
                    )
            
            # Query is valid
            return ValidationResult(
                is_valid=True,
                parsed_components={
                    "type": "simple",
                    "predicate": predicate,
                    "arguments": arguments,
                    "full_query": full_query,
                },
            )
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message="Failed to parse query arguments.",
                hint="Check your query syntax. Example: ?- frame(1, X, Y, Z).",
            )
    
    @staticmethod
    def _validate_compound_query(full_query: str, query_body: str) -> ValidationResult:
        """
        Validate a compound query with multiple conditions.
        
        Args:
            full_query: The complete query string with ?- and .
            query_body: The query body without ?- and .
            
        Returns:
            ValidationResult with validation status and feedback
        """
        # Split by comma (but not commas inside parentheses)
        conditions = QueryValidator._split_conditions(query_body)
        
        if len(conditions) < 2:
            return ValidationResult(
                is_valid=False,
                error_message="Compound query should have multiple conditions.",
                hint="Use commas to separate conditions: ?- pred1(...), pred2(...).",
            )
        
        # Validate each condition
        validated_conditions = []
        for i, condition in enumerate(conditions):
            condition = condition.strip()
            
            # Check if it's a negation
            is_negation = condition.startswith("\\+")
            if is_negation:
                condition = condition[2:].strip()
            
            # Validate the condition as a simple query body
            temp_query = f"?- {condition}."
            result = QueryValidator._validate_simple_query(temp_query, condition)
            
            if not result.is_valid:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Error in condition {i+1}: {result.error_message}",
                    hint=result.hint,
                )
            
            validated_conditions.append({
                "condition": condition,
                "is_negation": is_negation,
                "predicate": result.parsed_components["predicate"],
                "arguments": result.parsed_components["arguments"],
            })
        
        return ValidationResult(
            is_valid=True,
            parsed_components={
                "type": "compound",
                "conditions": validated_conditions,
                "condition_count": len(validated_conditions),
                "full_query": full_query,
            },
        )
    
    @staticmethod
    def _validate_negation_query(full_query: str, query_body: str) -> ValidationResult:
        """
        Validate a negation query (checking for absence of data).
        
        Args:
            full_query: The complete query string with ?- and .
            query_body: The query body without ?- and .
            
        Returns:
            ValidationResult with validation status and feedback
        """
        # Remove negation operator
        if not query_body.startswith("\\+"):
            return ValidationResult(
                is_valid=False,
                error_message="Invalid negation syntax.",
                hint="Negation should start with \\+. Example: ?- \\+ frame(X, Y, Z, error).",
            )
        
        negated_part = query_body[2:].strip()
        
        if not negated_part:
            return ValidationResult(
                is_valid=False,
                error_message="Empty negation query.",
                hint="Specify what you want to check for absence. Example: ?- \\+ status(1, error).",
            )
        
        # Validate the negated part as a simple query
        temp_query = f"?- {negated_part}."
        result = QueryValidator._validate_simple_query(temp_query, negated_part)
        
        if not result.is_valid:
            return ValidationResult(
                is_valid=False,
                error_message=f"Error in negated query: {result.error_message}",
                hint=result.hint,
            )
        
        return ValidationResult(
            is_valid=True,
            parsed_components={
                "type": "negation",
                "negated_predicate": result.parsed_components["predicate"],
                "negated_arguments": result.parsed_components["arguments"],
                "full_query": full_query,
            },
        )
    
    @staticmethod
    def _split_conditions(query_body: str) -> List[str]:
        """
        Split compound query into individual conditions.
        
        Handles commas inside parentheses correctly.
        
        Args:
            query_body: The query body to split
            
        Returns:
            List of condition strings
        """
        conditions = []
        current_condition = []
        paren_depth = 0
        
        for char in query_body:
            if char == "(":
                paren_depth += 1
                current_condition.append(char)
            elif char == ")":
                paren_depth -= 1
                current_condition.append(char)
            elif char == "," and paren_depth == 0:
                # This comma separates conditions
                conditions.append("".join(current_condition))
                current_condition = []
            else:
                current_condition.append(char)
        
        # Add the last condition
        if current_condition:
            conditions.append("".join(current_condition))
        
        return conditions


@dataclass
class QueryResult:
    """Result of executing a query against the fact database."""
    success: bool
    results: List[Dict[str, Any]]
    formatted_output: str
    is_significant: bool = False  # True if query reveals important information
    discovery_type: Optional[str] = None  # Type of discovery made, if any


class ResultFormatter:
    """
    Formats query results for clear display to the user.
    
    Handles:
    - Clear result display with variable bindings
    - Empty result handling with explanations
    - Significance detection for important discoveries
    - Highlight formatting for significant results
    
    Requirements: 2.3, 2.4, 9.3, 9.5
    """
    
    # ANSI color codes for terminal highlighting
    COLOR_HIGHLIGHT = "\033[93m"  # Yellow for highlights
    COLOR_ERROR = "\033[91m"      # Red for errors
    COLOR_SUCCESS = "\033[92m"    # Green for success
    COLOR_RESET = "\033[0m"       # Reset to default
    
    def __init__(self, facts_db: Dict[str, List[Tuple]]):
        """
        Initialize the result formatter.
        
        Args:
            facts_db: The fact database for context in explanations
        """
        self.facts_db = facts_db
    
    def format_results(
        self,
        results: List[Dict[str, Any]],
        arguments: List[str],
        predicate: str = "",
        is_significant: bool = False,
        discovery_type: Optional[str] = None
    ) -> str:
        """
        Format query results for clear display.
        
        Args:
            results: List of variable binding dictionaries
            arguments: Original query arguments
            predicate: The predicate that was queried
            is_significant: Whether this result is significant
            discovery_type: Type of discovery if significant
            
        Returns:
            Formatted string representation of results
            
        Validates: Requirements 2.3, 9.3
        """
        if not results:
            return self.format_empty_result(predicate, arguments)
        
        # Collect all variables that appear in results
        all_vars = set()
        for result in results:
            all_vars.update(result.keys())
        
        # If no variables, just show count
        if not all_vars:
            output = f"Yes - found {len(results)} matching fact(s)."
            if is_significant:
                output = self._add_significance_highlight(output, discovery_type)
            return output
        
        # Format each result
        output_lines = [f"Found {len(results)} result(s):"]
        
        for i, result in enumerate(results, 1):
            bindings_str = ", ".join(
                f"{var} = {value}" for var, value in sorted(result.items())
            )
            output_lines.append(f"  {i}. {bindings_str}")
        
        output = "\n".join(output_lines)
        
        # Add significance highlighting if applicable
        if is_significant:
            output = self._add_significance_highlight(output, discovery_type)
        
        return output
    
    def format_empty_result(self, predicate: str, arguments: List[str]) -> str:
        """
        Format an empty result with helpful explanation.
        
        Provides context-aware suggestions to help users understand
        why their query returned no results and what to try next.
        
        Args:
            predicate: The predicate that was queried
            arguments: The query arguments
            
        Returns:
            Formatted explanation of why no results were found
            
        Validates: Requirements 2.4, 9.5
        """
        # Check if any facts exist for this predicate
        if predicate not in self.facts_db or not self.facts_db[predicate]:
            return (
                f"No facts found for predicate '{predicate}'.\n"
                f"Available predicates: {', '.join(sorted(self.facts_db.keys()))}"
            )
        
        # Facts exist but didn't match
        has_variables = any(self._is_variable(arg) for arg in arguments)
        
        if has_variables:
            # Query had variables but still no match
            explanation = (
                f"No results found matching the pattern.\n"
                f"\n"
                f"Suggestions:\n"
                f"  • Try using different constant values\n"
                f"  • Use more general variables (e.g., all uppercase)\n"
                f"  • Check if your constants match the data types in the facts"
            )
        else:
            # Query had all constants but no exact match
            explanation = (
                f"No exact match found for the specified values.\n"
                f"\n"
                f"Suggestions:\n"
                f"  • Try using variables (uppercase) to see what values exist\n"
                f"  • Example: ?- {predicate}(X, Y, Z, W).\n"
                f"  • Check your values for typos or incorrect data types"
            )
        
        return explanation
    
    def detect_significance(
        self,
        predicate: str,
        arguments: List[str],
        matches: List[Dict[str, Any]],
        scenario_type: Optional[FailureScenario] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Detect if a query reveals significant information.
        
        Identifies queries that discover important patterns or anomalies
        that are relevant to solving the puzzle.
        
        Args:
            predicate: The predicate that was queried
            arguments: The query arguments
            matches: The matching results
            scenario_type: The failure scenario type for context
            
        Returns:
            Tuple of (is_significant, discovery_type)
            
        Validates: Requirements 9.3
        """
        if not matches:
            return False, None
        
        # Check for error status discovery
        if predicate == "status" and "error" in arguments:
            return True, "error"
        
        # Check for recursive call patterns (check before general pattern)
        if predicate == "calls":
            # If we have many caller-callee relationships, might be recursion
            if len(matches) > 10:
                return True, "recursion"
        
        # Check for memory-related discoveries
        if predicate == "allocated":
            # Check for high memory allocation
            for match in matches:
                for key, value in match.items():
                    if isinstance(value, int) and value > 1000000:  # > 1MB
                        return True, "memory_anomaly"
        
        # Check for null/invalid parameters
        if predicate == "param":
            for match in matches:
                for key, value in match.items():
                    if value == "null" or value is None:
                        return True, "null_parameter"
        
        # Check for deadlock patterns (waiting_for parameters)
        if predicate == "param" and any("waiting_for" in str(m) for m in matches):
            return True, "deadlock"
        
        # Check for pattern discovery (many results) - check last as it's most general
        if len(matches) > 5:
            return True, "pattern"
        
        return False, None
    
    def _add_significance_highlight(
        self,
        output: str,
        discovery_type: Optional[str]
    ) -> str:
        """
        Add highlighting to significant results.
        
        Args:
            output: The formatted output string
            discovery_type: Type of discovery made
            
        Returns:
            Output with highlighting added
            
        Validates: Requirements 9.3
        """
        # Create significance message based on discovery type
        significance_messages = {
            "error": "⚠️  SIGNIFICANT: Error status detected!",
            "pattern": "🔍 SIGNIFICANT: Pattern detected in results!",
            "memory_anomaly": "⚠️  SIGNIFICANT: High memory allocation detected!",
            "recursion": "🔍 SIGNIFICANT: Recursive call pattern detected!",
            "null_parameter": "⚠️  SIGNIFICANT: Null parameter detected!",
            "deadlock": "⚠️  SIGNIFICANT: Potential deadlock detected!",
        }
        
        message = significance_messages.get(
            discovery_type,
            "🔍 SIGNIFICANT: Important discovery!"
        )
        
        # Add colored highlighting
        highlighted = (
            f"\n{self.COLOR_HIGHLIGHT}{'=' * 60}\n"
            f"{message}\n"
            f"{'=' * 60}{self.COLOR_RESET}\n\n"
            f"{output}\n\n"
            f"{self.COLOR_HIGHLIGHT}This discovery may be important for solving the puzzle.{self.COLOR_RESET}"
        )
        
        return highlighted
    
    @staticmethod
    def _is_variable(arg: str) -> bool:
        """Check if an argument is a variable (starts with uppercase or _)."""
        return arg and (arg[0].isupper() or arg[0] == "_")


class QueryProcessor:
    """
    Processes Prolog queries against stack frame data.
    
    Supports:
    - Exact matching queries
    - Variable binding in queries
    - Compound queries with multiple conditions (AND)
    - Negation queries (checking for missing facts)
    - Relationship queries with transitive closure (caller/callee chains)
    
    Requirements: 2.2, 3.1, 3.2, 3.3, 8.1, 8.3, 8.4
    """
    
    def __init__(self, stack_frames: List[StackFrame], scenario_type: Optional[FailureScenario] = None):
        """
        Initialize the query processor with stack frame data.
        
        Args:
            stack_frames: List of StackFrame objects to query against
            scenario_type: Optional failure scenario type for significance detection
        """
        self.stack_frames = stack_frames
        self.scenario_type = scenario_type
        self.facts = self._build_fact_database(stack_frames)
        self.formatter = ResultFormatter(self.facts)
        self._relationship_cache = {}  # Cache for transitive relationship queries
    
    def _build_fact_database(self, stack_frames: List[StackFrame]) -> Dict[str, List[Tuple]]:
        """
        Build a fact database from stack frames.
        
        Organizes facts by predicate name for efficient querying.
        
        Args:
            stack_frames: List of StackFrame objects
            
        Returns:
            Dictionary mapping predicate names to lists of fact tuples
        """
        facts = {
            "frame": [],
            "calls": [],
            "allocated": [],
            "param": [],
            "status": [],
        }
        
        for frame in stack_frames:
            # frame(frame_id, function_name, timestamp, status)
            facts["frame"].append((
                frame.frame_id,
                frame.function_name,
                frame.timestamp,
                frame.status
            ))
            
            # calls(caller_id, callee_id)
            if frame.caller_id is not None:
                facts["calls"].append((frame.caller_id, frame.frame_id))
            
            # allocated(frame_id, bytes)
            facts["allocated"].append((frame.frame_id, frame.memory_allocated))
            
            # param(frame_id, param_name, param_value)
            for param_name, param_value in frame.parameters.items():
                # Format parameter value
                if isinstance(param_value, str):
                    formatted_value = param_value
                elif isinstance(param_value, (int, float)):
                    formatted_value = param_value
                elif param_value is None:
                    formatted_value = "null"
                else:
                    formatted_value = str(param_value)
                
                facts["param"].append((frame.frame_id, param_name, formatted_value))
            
            # status(frame_id, status_value)
            facts["status"].append((frame.frame_id, frame.status))
        
        return facts
    
    def execute_query(self, query: str) -> QueryResult:
        """
        Execute a validated query against the fact database.
        
        Args:
            query: A validated Prolog query string
            
        Returns:
            QueryResult with execution results and formatted output
        """
        # First validate the query
        validation = QueryValidator.validate_query(query)
        
        if not validation.is_valid:
            return QueryResult(
                success=False,
                results=[],
                formatted_output=f"Error: {validation.error_message}\n{validation.hint}",
            )
        
        # Execute based on query type
        query_type = validation.parsed_components["type"]
        
        if query_type == "simple":
            return self._execute_simple_query(validation.parsed_components)
        elif query_type == "compound":
            return self._execute_compound_query(validation.parsed_components)
        elif query_type == "negation":
            return self._execute_negation_query(validation.parsed_components)
        else:
            return QueryResult(
                success=False,
                results=[],
                formatted_output=f"Unsupported query type: {query_type}",
            )
    
    def _execute_simple_query(self, components: Dict[str, Any]) -> QueryResult:
        """
        Execute a simple (single predicate) query.
        
        Args:
            components: Parsed query components from validation
            
        Returns:
            QueryResult with matching facts
        """
        predicate = components["predicate"]
        arguments = components["arguments"]
        
        # Get facts for this predicate
        if predicate not in self.facts:
            return QueryResult(
                success=True,
                results=[],
                formatted_output=f"No facts found for predicate '{predicate}'.",
            )
        
        predicate_facts = self.facts[predicate]
        
        # Match facts against query arguments
        matches = []
        for fact in predicate_facts:
            bindings = self._match_fact(arguments, fact)
            if bindings is not None:
                matches.append(bindings)
        
        # Detect significance
        is_significant, discovery_type = self.formatter.detect_significance(
            predicate, arguments, matches, self.scenario_type
        )
        
        # Format results
        formatted = self.formatter.format_results(
            matches, arguments, predicate, is_significant, discovery_type
        )
        
        return QueryResult(
            success=True,
            results=matches,
            formatted_output=formatted,
            is_significant=is_significant,
            discovery_type=discovery_type,
        )
    
    def _execute_compound_query(self, components: Dict[str, Any]) -> QueryResult:
        """
        Execute a compound query with multiple conditions (AND).
        
        Args:
            components: Parsed query components from validation
            
        Returns:
            QueryResult with facts matching all conditions
        """
        conditions = components["conditions"]
        
        # Start with all possible variable bindings from first condition
        first_condition = conditions[0]
        predicate = first_condition["predicate"]
        arguments = first_condition["arguments"]
        is_negation = first_condition["is_negation"]
        
        if predicate not in self.facts:
            return QueryResult(
                success=True,
                results=[],
                formatted_output=f"No facts found for predicate '{predicate}'.",
            )
        
        # Get initial matches
        if is_negation:
            # For negation in compound, we need to filter out matches
            current_matches = [{}]  # Start with empty binding
        else:
            current_matches = []
            for fact in self.facts[predicate]:
                bindings = self._match_fact(arguments, fact)
                if bindings is not None:
                    current_matches.append(bindings)
        
        # Apply each subsequent condition
        for condition in conditions[1:]:
            predicate = condition["predicate"]
            arguments = condition["arguments"]
            is_negation = condition["is_negation"]
            
            if predicate not in self.facts:
                return QueryResult(
                    success=True,
                    results=[],
                    formatted_output=f"No facts found for predicate '{predicate}'.",
                )
            
            new_matches = []
            
            for existing_binding in current_matches:
                # Apply existing bindings to arguments
                bound_arguments = self._apply_bindings(arguments, existing_binding)
                
                # Find facts that match with these bindings
                condition_matched = False
                for fact in self.facts[predicate]:
                    new_bindings = self._match_fact(bound_arguments, fact)
                    if new_bindings is not None:
                        condition_matched = True
                        # Merge bindings
                        merged = {**existing_binding, **new_bindings}
                        if not is_negation and merged not in new_matches:
                            new_matches.append(merged)
                
                # Handle negation: keep binding if condition did NOT match
                if is_negation and not condition_matched:
                    if existing_binding not in new_matches:
                        new_matches.append(existing_binding)
            
            current_matches = new_matches
            
            if not current_matches:
                break  # No matches, can stop early
        
        # Collect all variable names from all conditions
        all_vars = set()
        for condition in conditions:
            for arg in condition["arguments"]:
                if self._is_variable(arg):
                    all_vars.add(arg)
        
        # Format results using ResultFormatter
        formatted = self.formatter.format_results(
            current_matches, list(all_vars), predicate="compound"
        )
        
        return QueryResult(
            success=True,
            results=current_matches,
            formatted_output=formatted,
        )
    
    def _execute_negation_query(self, components: Dict[str, Any]) -> QueryResult:
        """
        Execute a negation query (checking for absence of data).
        
        Args:
            components: Parsed query components from validation
            
        Returns:
            QueryResult indicating whether the negated fact exists
        """
        predicate = components["negated_predicate"]
        arguments = components["negated_arguments"]
        
        # Get facts for this predicate
        if predicate not in self.facts:
            # No facts means negation succeeds
            return QueryResult(
                success=True,
                results=[{"result": "true"}],
                formatted_output=f"Yes - no facts found for '{predicate}'.",
            )
        
        predicate_facts = self.facts[predicate]
        
        # Check if any fact matches
        for fact in predicate_facts:
            bindings = self._match_fact(arguments, fact)
            if bindings is not None:
                # Found a match, negation fails
                return QueryResult(
                    success=True,
                    results=[],
                    formatted_output="No - the negated condition is true (fact exists).",
                )
        
        # No matches found, negation succeeds
        return QueryResult(
            success=True,
            results=[{"result": "true"}],
            formatted_output="Yes - the negated condition is false (fact does not exist).",
        )
    
    def _match_fact(self, arguments: List[str], fact: Tuple) -> Optional[Dict[str, Any]]:
        """
        Match query arguments against a fact tuple.
        
        Args:
            arguments: List of query arguments (atoms, variables, or numbers)
            fact: Tuple of fact values
            
        Returns:
            Dictionary of variable bindings if match succeeds, None otherwise
        """
        if len(arguments) != len(fact):
            return None
        
        bindings = {}
        
        for arg, value in zip(arguments, fact):
            if self._is_variable(arg):
                # Anonymous variable (_) matches anything but doesn't bind
                if arg == "_":
                    continue
                
                # Named variable - bind it
                if arg in bindings:
                    # Variable already bound, check consistency
                    if bindings[arg] != value:
                        return None  # Inconsistent binding
                else:
                    bindings[arg] = value
            else:
                # Constant - must match exactly
                arg_value = self._parse_constant(arg)
                if arg_value != value:
                    return None  # No match
        
        return bindings
    
    def _is_variable(self, arg: str) -> bool:
        """Check if an argument is a variable (starts with uppercase or _)."""
        return arg and (arg[0].isupper() or arg[0] == "_")
    
    def _parse_constant(self, arg: str) -> Any:
        """Parse a constant argument to its appropriate type."""
        # Try to parse as integer
        try:
            return int(arg)
        except ValueError:
            pass
        
        # Try to parse as float
        try:
            return float(arg)
        except ValueError:
            pass
        
        # Return as string (atom)
        return arg
    
    def _apply_bindings(self, arguments: List[str], bindings: Dict[str, Any]) -> List[str]:
        """
        Apply existing variable bindings to arguments.
        
        Args:
            arguments: List of query arguments
            bindings: Dictionary of variable bindings
            
        Returns:
            List of arguments with variables replaced by their bindings
        """
        result = []
        for arg in arguments:
            if self._is_variable(arg) and arg in bindings:
                # Replace variable with its binding
                result.append(str(bindings[arg]))
            else:
                result.append(arg)
        return result
    
    def find_call_chain(self, start_frame: int, direction: str = "callees") -> List[int]:
        """
        Find the complete call chain from a starting frame.
        
        Performs transitive closure over the calls/2 relationship to find
        all frames in the caller or callee chain.
        
        Args:
            start_frame: The frame ID to start from
            direction: Either "callees" (frames called by start) or 
                      "callers" (frames that called start)
        
        Returns:
            List of frame IDs in the call chain (excluding start_frame)
            
        Validates: Requirements 3.2
        """
        if direction not in ["callees", "callers"]:
            raise ValueError("direction must be 'callees' or 'callers'")
        
        # Check cache
        cache_key = (start_frame, direction)
        if cache_key in self._relationship_cache:
            return self._relationship_cache[cache_key]
        
        visited = set()
        to_visit = [start_frame]
        chain = []
        
        while to_visit:
            current = to_visit.pop(0)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Don't include the start frame in results
            if current != start_frame:
                chain.append(current)
            
            # Find related frames based on direction
            if direction == "callees":
                # Find frames called by current
                for caller, callee in self.facts.get("calls", []):
                    if caller == current and callee not in visited:
                        to_visit.append(callee)
            else:  # direction == "callers"
                # Find frames that called current
                for caller, callee in self.facts.get("calls", []):
                    if callee == current and caller not in visited:
                        to_visit.append(caller)
        
        # Cache the result
        self._relationship_cache[cache_key] = chain
        
        return chain
    
    def find_call_path(self, from_frame: int, to_frame: int) -> Optional[List[int]]:
        """
        Find a call path between two frames.
        
        Uses breadth-first search to find the shortest path through the
        calls/2 relationship from one frame to another.
        
        Args:
            from_frame: Starting frame ID
            to_frame: Target frame ID
        
        Returns:
            List of frame IDs representing the path (including both endpoints),
            or None if no path exists
            
        Validates: Requirements 3.2
        """
        if from_frame == to_frame:
            return [from_frame]
        
        # BFS to find shortest path
        queue = [(from_frame, [from_frame])]
        visited = {from_frame}
        
        while queue:
            current, path = queue.pop(0)
            
            # Check all frames called by current
            for caller, callee in self.facts.get("calls", []):
                if caller == current:
                    if callee == to_frame:
                        return path + [callee]
                    
                    if callee not in visited:
                        visited.add(callee)
                        queue.append((callee, path + [callee]))
        
        return None  # No path found
    
    def get_relationship_info(self, frame_id: int) -> Dict[str, Any]:
        """
        Get comprehensive relationship information for a frame.
        
        Returns information about direct callers, direct callees,
        and complete call chains in both directions.
        
        Args:
            frame_id: The frame ID to get relationship info for
        
        Returns:
            Dictionary with relationship information:
            - direct_caller: Frame ID of direct caller (or None)
            - direct_callees: List of frame IDs directly called
            - caller_chain: Complete chain of callers (transitive)
            - callee_chain: Complete chain of callees (transitive)
            
        Validates: Requirements 3.2
        """
        # Find direct relationships
        direct_caller = None
        direct_callees = []
        
        for caller, callee in self.facts.get("calls", []):
            if callee == frame_id:
                direct_caller = caller
            if caller == frame_id:
                direct_callees.append(callee)
        
        # Find transitive relationships
        caller_chain = self.find_call_chain(frame_id, "callers")
        callee_chain = self.find_call_chain(frame_id, "callees")
        
        return {
            "frame_id": frame_id,
            "direct_caller": direct_caller,
            "direct_callees": direct_callees,
            "caller_chain": caller_chain,
            "callee_chain": callee_chain,
        }
    
    def format_relationship_info(self, relationship_info: Dict[str, Any]) -> str:
        """
        Format relationship information for display.
        
        Creates a human-readable representation of a frame's relationships
        including call chains and direct relationships.
        
        Args:
            relationship_info: Dictionary from get_relationship_info()
        
        Returns:
            Formatted string representation
            
        Validates: Requirements 3.2
        """
        frame_id = relationship_info["frame_id"]
        lines = [f"Relationship information for frame {frame_id}:"]
        lines.append("")
        
        # Direct caller
        if relationship_info["direct_caller"] is not None:
            lines.append(f"  Direct caller: frame {relationship_info['direct_caller']}")
        else:
            lines.append("  Direct caller: none (root frame)")
        
        # Direct callees
        if relationship_info["direct_callees"]:
            callees_str = ", ".join(f"frame {c}" for c in relationship_info["direct_callees"])
            lines.append(f"  Direct callees: {callees_str}")
        else:
            lines.append("  Direct callees: none (leaf frame)")
        
        lines.append("")
        
        # Caller chain
        if relationship_info["caller_chain"]:
            chain_str = " -> ".join(str(f) for f in relationship_info["caller_chain"])
            lines.append(f"  Complete caller chain: {chain_str} -> {frame_id}")
        else:
            lines.append("  Complete caller chain: (this is a root frame)")
        
        # Callee chain
        if relationship_info["callee_chain"]:
            chain_str = " -> ".join(str(f) for f in relationship_info["callee_chain"])
            lines.append(f"  Complete callee chain: {frame_id} -> {chain_str}")
        else:
            lines.append("  Complete callee chain: (this is a leaf frame)")
        
        return "\n".join(lines)


@dataclass
class DiagnosisResult:
    """Result of validating a diagnosis submission."""
    is_correct: bool
    is_partial: bool  # True if diagnosis is partially correct
    feedback: str
    explanation: Optional[str] = None  # Detailed explanation for correct diagnosis


class DiagnosisValidator:
    """
    Validates player diagnosis of root cause.
    
    Supports:
    - Pattern matching for each scenario type
    - Multiple correct phrasings
    - Feedback generation for incorrect diagnoses
    - Partial credit detection for incomplete diagnoses
    
    Requirements: 5.1, 5.3
    """
    
    # Diagnosis patterns for each failure scenario
    # Each pattern is a list of keywords/phrases that should appear in the diagnosis
    DIAGNOSIS_PATTERNS = {
        FailureScenario.MEMORY_LEAK: {
            "required_keywords": [
                ["memory", "leak"],
                ["allocat", "not", "free"],
                ["allocat", "no", "release"],
                ["memory", "not", "released"],
                ["buffer", "not", "freed"],
            ],
            "partial_keywords": [
                ["memory", "problem"],
                ["allocat"],
                ["buffer"],
                ["leak"],
            ],
            "correct_explanation": (
                "Correct! The system experienced a memory leak.\n\n"
                "The allocate_buffer function was called multiple times, each allocating "
                "1MB of memory, but there were no corresponding cleanup_resources or "
                "deallocation calls. This caused memory to accumulate until the system "
                "ran out of available memory.\n\n"
                "In real debugging, you would look for:\n"
                "- Functions that allocate memory without freeing it\n"
                "- Missing cleanup code in error paths\n"
                "- Resource leaks in long-running processes"
            ),
            "incorrect_feedback": (
                "Not quite. Look more carefully at the memory allocation patterns.\n"
                "Hint: Check if allocated memory is being properly released."
            ),
            "partial_feedback": (
                "You're on the right track - there is a memory-related issue.\n"
                "But can you be more specific about what's happening to the allocated memory?"
            ),
        },
        FailureScenario.STACK_OVERFLOW: {
            "required_keywords": [
                ["stack", "overflow"],
                ["recursive", "too", "deep"],
                ["recursion", "depth"],
                ["excessive", "recursion"],
                ["infinite", "recursion"],
            ],
            "partial_keywords": [
                ["recursion"],
                ["stack"],
                ["depth"],
                ["too", "many", "call"],
            ],
            "correct_explanation": (
                "Correct! The system experienced a stack overflow.\n\n"
                "The recursive_process function called itself 15 times, exceeding the "
                "maximum depth of 10 specified in its parameters. Each recursive call "
                "added a new frame to the stack until the stack space was exhausted.\n\n"
                "In real debugging, you would look for:\n"
                "- Recursive functions without proper base cases\n"
                "- Recursion depth exceeding system limits\n"
                "- Missing termination conditions in recursive algorithms"
            ),
            "incorrect_feedback": (
                "Not quite. Look at the function call patterns and depths.\n"
                "Hint: Check if any function is calling itself too many times."
            ),
            "partial_feedback": (
                "You've identified recursion as part of the problem.\n"
                "But what specifically went wrong with the recursive calls?"
            ),
        },
        FailureScenario.NULL_POINTER: {
            "required_keywords": [
                ["null", "pointer"],
                ["null", "parameter"],
                ["invalid", "parameter"],
                ["null", "reference"],
                ["null", "value", "parameter"],
                ["null", "value", "passed"],
            ],
            "partial_keywords": [
                ["parameter", "problem"],
                ["invalid", "data"],
                ["parameter", "null"],
                ["null", "value"],
            ],
            "correct_explanation": (
                "Correct! The system experienced a null pointer error.\n\n"
                "The process_request function was called with null parameters "
                "(request_data and handler were both null). When the function tried "
                "to access these parameters, it caused an error because there was no "
                "valid data to process.\n\n"
                "In real debugging, you would look for:\n"
                "- Functions receiving null/None values unexpectedly\n"
                "- Missing null checks before dereferencing pointers\n"
                "- Uninitialized variables being passed as arguments"
            ),
            "incorrect_feedback": (
                "Not quite. Look at the parameter values in the stack frames.\n"
                "Hint: Check if any parameters have invalid or missing values."
            ),
            "partial_feedback": (
                "You've noticed something wrong with the parameters.\n"
                "But what specifically is wrong with them?"
            ),
        },
        FailureScenario.DEADLOCK: {
            "required_keywords": [
                ["deadlock"],
                ["circular", "wait"],
                ["lock", "wait", "each", "other"],
                ["mutual", "wait"],
                ["lock", "dependency"],
            ],
            "partial_keywords": [
                ["lock", "problem"],
                ["waiting"],
                ["blocked"],
            ],
            "correct_explanation": (
                "Correct! The system experienced a deadlock.\n\n"
                "Two frames were waiting on each other's locks: one acquired lock_a "
                "and was waiting for lock_b, while another acquired lock_b and was "
                "waiting for lock_a. This created a circular dependency where neither "
                "could proceed.\n\n"
                "In real debugging, you would look for:\n"
                "- Circular lock dependencies between threads\n"
                "- Inconsistent lock acquisition order\n"
                "- Missing timeout mechanisms for lock acquisition"
            ),
            "incorrect_feedback": (
                "Not quite. Look at the lock acquisition patterns.\n"
                "Hint: Check what locks are held and what locks are being waited for."
            ),
            "partial_feedback": (
                "You've identified that locks are involved in the problem.\n"
                "But what specifically is the relationship between the locks?"
            ),
        },
        FailureScenario.RESOURCE_EXHAUSTION: {
            "required_keywords": [
                ["resource", "exhaustion"],
                ["too", "much", "memory"],
                ["excessive", "memory"],
                ["memory", "exhausted"],
                ["out", "of", "memory"],
            ],
            "partial_keywords": [
                ["memory", "high"],
                ["too", "much"],
                ["resource"],
            ],
            "correct_explanation": (
                "Correct! The system experienced resource exhaustion.\n\n"
                "Multiple load_dataset calls each allocated 10MB of memory, totaling "
                "50MB or more. This excessive memory consumption exhausted the available "
                "system resources, causing the system to fail.\n\n"
                "In real debugging, you would look for:\n"
                "- Operations consuming excessive memory or CPU\n"
                "- Missing resource limits or quotas\n"
                "- Inefficient algorithms with high resource usage"
            ),
            "incorrect_feedback": (
                "Not quite. Look at the total resource consumption.\n"
                "Hint: Add up the memory allocated across multiple frames."
            ),
            "partial_feedback": (
                "You've noticed high resource usage.\n"
                "But what specifically caused the system to fail?"
            ),
        },
    }
    
    def __init__(self, scenario_type: FailureScenario):
        """
        Initialize the diagnosis validator.
        
        Args:
            scenario_type: The type of failure scenario to validate against
        """
        self.scenario_type = scenario_type
        self.patterns = self.DIAGNOSIS_PATTERNS[scenario_type]
    
    def validate_diagnosis(self, diagnosis: str) -> DiagnosisResult:
        """
        Validate a player's diagnosis submission.
        
        Checks if the diagnosis correctly identifies the root cause,
        supporting multiple phrasings and detecting partial correctness.
        
        Args:
            diagnosis: The player's diagnosis text
            
        Returns:
            DiagnosisResult with validation outcome and feedback
            
        Validates: Requirements 5.1, 5.3
        """
        if not diagnosis or not diagnosis.strip():
            return DiagnosisResult(
                is_correct=False,
                is_partial=False,
                feedback="Please provide a diagnosis of what caused the system failure.",
            )
        
        # Normalize diagnosis for matching
        normalized = diagnosis.lower().strip()
        
        # Check for required keywords (full match)
        is_correct = self._check_required_keywords(normalized)
        
        if is_correct:
            return DiagnosisResult(
                is_correct=True,
                is_partial=False,
                feedback="Excellent work! Your diagnosis is correct.",
                explanation=self.patterns["correct_explanation"],
            )
        
        # Check for partial match
        is_partial = self._check_partial_keywords(normalized)
        
        if is_partial:
            return DiagnosisResult(
                is_correct=False,
                is_partial=True,
                feedback=self.patterns["partial_feedback"],
            )
        
        # Incorrect diagnosis
        return DiagnosisResult(
            is_correct=False,
            is_partial=False,
            feedback=self.patterns["incorrect_feedback"],
        )
    
    def _check_required_keywords(self, diagnosis: str) -> bool:
        """
        Check if diagnosis contains required keywords for correct identification.
        
        Args:
            diagnosis: Normalized diagnosis text
            
        Returns:
            True if diagnosis matches any required keyword pattern
        """
        required_patterns = self.patterns["required_keywords"]
        
        for pattern in required_patterns:
            # Check if all keywords in this pattern appear in the diagnosis
            if all(keyword in diagnosis for keyword in pattern):
                return True
        
        return False
    
    def _check_partial_keywords(self, diagnosis: str) -> bool:
        """
        Check if diagnosis contains partial keywords indicating partial understanding.
        
        Args:
            diagnosis: Normalized diagnosis text
            
        Returns:
            True if diagnosis matches any partial keyword pattern
        """
        partial_patterns = self.patterns["partial_keywords"]
        
        for pattern in partial_patterns:
            # Check if all keywords in this pattern appear in the diagnosis
            if all(keyword in diagnosis for keyword in pattern):
                return True
        
        return False
    
    def get_hint_for_diagnosis(self, queries_made: int, discoveries: set) -> str:
        """
        Generate a hint to help the player formulate their diagnosis.
        
        Provides guidance based on what the player has discovered so far.
        
        Args:
            queries_made: Number of queries the player has made
            discoveries: Set of discovery types the player has found
            
        Returns:
            Hint text to guide diagnosis
        """
        # If player hasn't made many queries yet
        if queries_made < 3:
            return (
                "Before diagnosing, make sure you've thoroughly investigated the stack trace.\n"
                "Try querying different aspects: frame status, memory allocation, parameters, etc."
            )
        
        # If player has made discoveries, guide them toward synthesis
        if discoveries:
            return (
                "You've made some important discoveries. Now think about what they mean together.\n"
                "What pattern do these anomalies form? What would cause this kind of failure?"
            )
        
        # Generic hint
        return (
            "Look for patterns or anomalies in the data you've queried.\n"
            "What stands out as unusual? What could cause a system to fail?"
        )
    



class MemoryStackHintSystem(ComplexityAwareHintSystem):
    """
    Adaptive hint system for the Memory Stack Failure Puzzle.
    
    Provides progress-aware hints that adapt based on:
    - Number of queries made
    - Discoveries found
    - Current complexity level
    
    Hint progression follows: exploration → investigation → diagnosis
    
    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
    """
    
    def __init__(self, scenario_type: FailureScenario):
        """
        Initialize the memory stack hint system.
        
        Args:
            scenario_type: The failure scenario type for context-specific hints
        """
        super().__init__()
        self.scenario_type = scenario_type
        self.queries_made = 0
        self.discoveries: Set[str] = set()
        self.hint_count = 0
    
    def update_progress(self, queries_made: int, discoveries: Set[str]) -> None:
        """
        Update the progress tracking for adaptive hints.
        
        Args:
            queries_made: Total number of queries the player has made
            discoveries: Set of discovery types found (e.g., "error", "memory_anomaly")
        """
        self.queries_made = queries_made
        self.discoveries = discoveries
    
    def get_adaptive_hint(self) -> str:
        """
        Get a hint adapted to current progress and complexity level.
        
        Implements progressive hint logic:
        - Phase 1 (0-2 queries): Exploration hints
        - Phase 2 (3-5 queries): Investigation hints
        - Phase 3 (6+ queries): Diagnosis hints
        
        Returns:
            Hint text adapted to progress and complexity level
            
        Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5
        """
        # Check if hints are available at current complexity level
        puzzle_context = {
            "attempts": self.queries_made,
            "hints_used": self.hint_count,
        }
        
        if not self.can_provide_hint(self.queries_made, self.hint_count):
            return self.hint_generator.get_hint_availability_message(
                self.current_complexity_level,
                self.queries_made,
                self.hint_count
            )
        
        # Increment hint count
        self.hint_count += 1
        
        # Determine hint phase based on progress
        if self.queries_made < 3:
            phase = "exploration"
        elif self.queries_made < 6:
            phase = "investigation"
        else:
            phase = "diagnosis"
        
        # Generate hint based on phase and complexity level
        hint = self._generate_phase_hint(phase)
        
        return hint
    
    def _generate_phase_hint(self, phase: str) -> str:
        """
        Generate a hint for the specified phase.
        
        Args:
            phase: One of "exploration", "investigation", or "diagnosis"
            
        Returns:
            Phase-appropriate hint text
        """
        if phase == "exploration":
            return self._generate_exploration_hint()
        elif phase == "investigation":
            return self._generate_investigation_hint()
        else:  # diagnosis
            return self._generate_diagnosis_hint()
    
    def _generate_exploration_hint(self) -> str:
        """
        Generate hints for the exploration phase (0-2 queries).
        
        Encourages players to start querying the data and understanding
        the available predicates. Uses mentor character voice.
        
        Returns:
            Exploration phase hint adapted to complexity level
            
        Validates: Requirements 4.4, 4.5, 10.4
        """
        config = self.hint_generator.get_hint_config(self.current_complexity_level)
        
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            hints = [
                ">>> MENTOR: \"Alright, first things first - you need to see what you're "
                "working with. Start by querying for all the stack frames:\n"
                "  ?- frame(X, Y, Z, W).\n\n"
                "This dumps everything. X will be the frame ID, Y the function name, "
                "Z the timestamp, W the status. Get the lay of the land first.\"",
                
                ">>> MENTOR: \"Now let's look at memory usage. That's often where problems hide:\n"
                "  ?- allocated(FrameId, Bytes).\n\n"
                "Watch for numbers that seem way too high. In 1985, memory's precious - "
                "anything over a megabyte should raise eyebrows.\"",
                
                ">>> MENTOR: \"Time to check for errors. Systems usually leave breadcrumbs:\n"
                "  ?- status(FrameId, Status).\n\n"
                "Look for 'error' status. That's your smoking gun right there. "
                "Find the error, find your culprit.\"",
            ]
            
            if config.include_templates:
                return hints[min(self.hint_count - 1, len(hints) - 1)]
            else:
                return hints[0]
        
        elif self.current_complexity_level == ComplexityLevel.INTERMEDIATE:
            hints = [
                ">>> MENTOR: \"Start with broad queries - get a feel for the data. "
                "Check frames, statuses, memory allocations. Look for anything that "
                "jumps out as wrong.\"",
                
                ">>> MENTOR: \"You've got five predicates to work with: frame, status, "
                "allocated, param, and calls. Each one tells part of the story. "
                "Start connecting the dots.\"",
                
                ">>> MENTOR: \"Think like a detective. What's unusual? What doesn't fit? "
                "Systems don't crash for no reason - there's always a pattern.\"",
            ]
            return hints[min(self.hint_count - 1, len(hints) - 1)]
        
        elif self.current_complexity_level == ComplexityLevel.ADVANCED:
            return (
                ">>> MENTOR: \"You know the drill. Query the stack trace, "
                "find the anomalies, trace the cause. The data's all there.\""
            )
        
        else:  # EXPERT
            return ">>> MENTOR: \"You've got this. Start investigating.\""
    
    def _generate_investigation_hint(self) -> str:
        """
        Generate hints for the investigation phase (3-5 queries).
        
        Guides players to dig deeper into patterns they've discovered
        and make connections between different pieces of data.
        Uses mentor character voice.
        
        Returns:
            Investigation phase hint adapted to complexity level
            
        Validates: Requirements 4.4, 4.5, 10.4
        """
        config = self.hint_generator.get_hint_config(self.current_complexity_level)
        
        # Provide context-specific hints based on discoveries
        if "error" in self.discoveries:
            return self._generate_error_investigation_hint()
        elif "memory_anomaly" in self.discoveries:
            return self._generate_memory_investigation_hint()
        elif "recursion" in self.discoveries:
            return self._generate_recursion_investigation_hint()
        elif "null_parameter" in self.discoveries:
            return self._generate_null_investigation_hint()
        elif "deadlock" in self.discoveries:
            return self._generate_deadlock_investigation_hint()
        
        # Generic investigation hints if no specific discoveries yet
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            hints = [
                ">>> MENTOR: \"Good start. Now let's dig deeper. You can combine conditions "
                "to narrow things down. Try this:\n"
                "  ?- frame(Id, Name, Time, Status), status(Id, error).\n\n"
                "That comma means AND - both conditions have to be true. "
                "It'll show you frames that have errors. That's where the action is.\"",
                
                ">>> MENTOR: \"Time to trace the execution flow. Use the calls predicate:\n"
                "  ?- calls(CallerId, CalleeId).\n\n"
                "This shows you which function called which. Follow the chain - "
                "sometimes the problem isn't where the crash happened, but what led to it.\"",
                
                ">>> MENTOR: \"Don't forget to check the parameters. Bad data in, bad results out:\n"
                "  ?- param(FrameId, ParamName, ParamValue).\n\n"
                "Look for null values, weird numbers, anything that doesn't smell right. "
                "Parameters tell you what the function was trying to do when it failed.\"",
            ]
            return hints[min(self.hint_count - 1, len(hints) - 1)]
        
        elif self.current_complexity_level == ComplexityLevel.INTERMEDIATE:
            return (
                ">>> MENTOR: \"You're making progress. Now connect the dots - "
                "use compound queries to see how frames, memory, and status relate. "
                "The pattern's in there, you just need to tease it out.\""
            )
        
        elif self.current_complexity_level == ComplexityLevel.ADVANCED:
            return (
                ">>> MENTOR: \"Dig into the relationships. Compound queries will "
                "show you how the pieces fit together.\""
            )
        
        else:  # EXPERT
            return ">>> MENTOR: \"Connect the data points. Find the pattern.\""
    
    def _generate_diagnosis_hint(self) -> str:
        """
        Generate hints for the diagnosis phase (6+ queries).
        
        Helps players synthesize their findings into a diagnosis
        of the root cause. Uses mentor character voice.
        
        Returns:
            Diagnosis phase hint adapted to complexity level
            
        Validates: Requirements 4.4, 4.5, 10.4
        """
        # Provide scenario-specific guidance based on what they've discovered
        if len(self.discoveries) == 0:
            return (
                ">>> MENTOR: \"You're spinning your wheels. You've made a lot of queries "
                "but haven't found the key anomalies yet. Try different angles - check status, "
                "memory, parameters, call chains. The smoking gun's in there somewhere.\""
            )
        
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return (
                ">>> MENTOR: \"Alright, you've done the legwork. Time to put it together.\n\n"
                "Here's what you've found:\n"
                f"- {', '.join(self.discoveries)}\n\n"
                "Now think: what kind of failure causes these symptoms? "
                "Memory leak? Stack overflow? Null pointer? Deadlock? Resource exhaustion?\n\n"
                "When you've got it figured out, submit your diagnosis:\n"
                "  diagnose <your diagnosis>\n\n"
                "Don't overthink it - trust your analysis. You've got the evidence.\""
            )
        
        elif self.current_complexity_level == ComplexityLevel.INTERMEDIATE:
            return (
                f">>> MENTOR: \"You've found {', '.join(self.discoveries)}. "
                "Now connect those dots. What failure pattern matches these symptoms? "
                "Time to make the call.\""
            )
        
        elif self.current_complexity_level == ComplexityLevel.ADVANCED:
            return (
                ">>> MENTOR: \"You have the evidence. Synthesize it into a diagnosis. "
                "What's the root cause?\""
            )
        
        else:  # EXPERT
            return ">>> MENTOR: \"Make your diagnosis.\""
    
    def _generate_error_investigation_hint(self) -> str:
        """Generate hint when player has discovered error status."""
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return (
                ">>> MENTOR: \"Bingo! You found the error frame. Now dig into what caused it. "
                "Check the parameters:\n"
                "  ?- param(ErrorFrameId, ParamName, ParamValue).\n\n"
                "Replace ErrorFrameId with the actual frame number that errored out. "
                "The parameters will tell you what data it was working with when it died.\""
            )
        else:
            return (
                ">>> MENTOR: \"Error frame located. Now investigate the parameters "
                "and context. What was it trying to do when it failed?\""
            )
    
    def _generate_memory_investigation_hint(self) -> str:
        """Generate hint when player has discovered memory anomaly."""
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return (
                ">>> MENTOR: \"Hot damn! Those memory numbers are through the roof. "
                "Now look for the pattern:\n"
                "- Multiple frames allocating big chunks?\n"
                "- Same function name showing up repeatedly?\n"
                "- Any cleanup or deallocation happening?\n\n"
                "Try this: ?- frame(Id, allocate_buffer, Time, Status).\n"
                "See if there's a pattern in the allocations.\""
            )
        else:
            return (
                ">>> MENTOR: \"High memory usage confirmed. Check if allocations "
                "are balanced by deallocations. What functions are involved?\""
            )
    
    def _generate_recursion_investigation_hint(self) -> str:
        """Generate hint when player has discovered recursion pattern."""
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return (
                ">>> MENTOR: \"There's your recursion! Now figure out if it's out of control:\n"
                "- Count how deep it goes\n"
                "- Look for depth parameters\n"
                "- Check if it exceeds any limits\n\n"
                "Try: ?- param(FrameId, depth, Depth).\n"
                "See if the depth values tell you anything.\""
            )
        else:
            return (
                ">>> MENTOR: \"Recursion detected. Check the depth - "
                "does it exceed the limits?\""
            )
    
    def _generate_null_investigation_hint(self) -> str:
        """Generate hint when player has discovered null parameters."""
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return (
                ">>> MENTOR: \"Jackpot! Null parameters - that's your culprit right there. "
                "Now nail down the details:\n"
                "- Which frame has the nulls?\n"
                "- What function is it?\n"
                "- What's the frame status?\n\n"
                "You're looking at the root cause. Just need to confirm it.\""
            )
        else:
            return (
                ">>> MENTOR: \"Null parameters found. Identify the frame and "
                "connect it to the failure.\""
            )
    
    def _generate_deadlock_investigation_hint(self) -> str:
        """Generate hint when player has discovered deadlock pattern."""
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return (
                ">>> MENTOR: \"Lock contention! Now trace the deadlock:\n"
                "- Which frames are holding locks?\n"
                "- What locks are they waiting for?\n"
                "- Is there a circular wait?\n\n"
                "Try: ?- param(Id, waiting_for, Lock).\n"
                "Map out who's waiting for what. The circle is your answer.\""
            )
        else:
            return (
                ">>> MENTOR: \"Lock operations detected. Map the acquisition "
                "and waiting patterns. Find the circular dependency.\""
            )
    
    def generate_query_suggestion(self, phase: str) -> Optional[str]:
        """
        Generate a suggested query for the current phase.
        
        Only provides suggestions at BEGINNER level where templates are enabled.
        
        Args:
            phase: Current hint phase ("exploration", "investigation", "diagnosis")
            
        Returns:
            Suggested query string or None if not applicable
            
        Validates: Requirements 4.4, 4.5
        """
        config = self.hint_generator.get_hint_config(self.current_complexity_level)
        
        # Only provide query suggestions at BEGINNER level
        if not config.include_templates:
            return None
        
        if phase == "exploration":
            suggestions = [
                "?- frame(X, Y, Z, W).",
                "?- status(FrameId, Status).",
                "?- allocated(FrameId, Bytes).",
            ]
            return suggestions[min(self.queries_made, len(suggestions) - 1)]
        
        elif phase == "investigation":
            if "error" in self.discoveries:
                return "?- frame(Id, Name, Time, error)."
            elif "memory_anomaly" in self.discoveries:
                return "?- frame(Id, allocate_buffer, Time, Status)."
            else:
                return "?- param(FrameId, ParamName, ParamValue)."
        
        else:  # diagnosis phase
            return None  # No query suggestions for diagnosis phase
    
    def reset_progress(self) -> None:
        """
        Reset progress tracking for a new puzzle attempt.
        
        Clears queries made, discoveries, and hint count.
        """
        self.queries_made = 0
        self.discoveries = set()
        self.hint_count = 0
    
    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """
        Set the complexity level and reset hint count.
        
        Overrides parent method to also reset hint count when
        complexity changes.
        
        Args:
            level: The new complexity level
            
        Validates: Requirements 6.5
        """
        super().set_complexity_level(level)
        # Reset hint count when complexity changes
        self.hint_count = 0



class MemoryStackPuzzle(BasePuzzle):
    """
    Memory Stack Failure Puzzle - First adventure mode puzzle.
    
    Teaches debugging concepts through Prolog-based investigation of
    simulated system failures. Players examine stack traces, write queries,
    and diagnose root causes.
    
    Integrates with the existing puzzle system and provides:
    - Narrative context for the investigation
    - Stack frame facts as initial context
    - Query execution and validation
    - Diagnosis submission and validation
    - Progress-aware adaptive hints
    
    Requirements: 1.1, 1.2, 1.3, 1.4, 2.2, 5.1
    """
    
    def __init__(self, scenario: Optional[FailureScenario] = None, seed: Optional[int] = None):
        """
        Initialize the Memory Stack Failure Puzzle.
        
        Args:
            scenario: Optional specific failure scenario to use. If None, randomly selected.
            seed: Optional random seed for reproducible generation
        """
        super().__init__(
            puzzle_id="memory_stack_failure",
            title="Memory Stack Investigation",
            difficulty=PuzzleDifficulty.BEGINNER
        )
        
        # Select scenario
        if scenario is None:
            scenario = random.choice(list(FailureScenario))
        self.scenario = scenario
        
        # Generate stack trace with anomaly
        generator = StackFrameGenerator(self.scenario, seed=seed)
        self.stack_frames = generator.generate_stack_trace(num_frames=12)
        
        # Initialize query processor
        self.query_processor = QueryProcessor(self.stack_frames, self.scenario)
        
        # Initialize diagnosis validator
        self.diagnosis_validator = DiagnosisValidator(self.scenario)
        
        # Initialize hint system
        self.memory_hint_system = MemoryStackHintSystem(self.scenario)
        
        # Track progress
        self.queries_made: List[str] = []
        self.discoveries: Set[str] = set()
        self.diagnosis_submitted = False
        
        # Narrative state
        self.investigation_started = False
    
    def get_description(self) -> str:
        """
        Get the puzzle description with narrative context.
        
        Provides an engaging introduction to the puzzle within the
        LOGIC-1 malfunction storyline, explaining the scenario and
        the player's objective. Includes additional guidance for BEGINNER level.
        
        Returns:
            Puzzle description with narrative context
            
        Validates: Requirements 1.1, 1.5, 6.1, 6.2, 10.1
        """
        # Scenario-specific narrative with cyberpunk 1985 flavor
        scenario_narratives = {
            FailureScenario.MEMORY_LEAK: (
                "At 03:47 hours, LOGIC-1's memory banks started hemorrhaging. "
                "The core's RAM consumption climbed like a runaway freight train until "
                "the whole system flatlined. The diagnostic dump shows a memory stack "
                "frozen at the moment of crash.\n\n"
                "Dr. Chen from the AI Research Division is breathing down your neck. "
                "The brass wants answers, and they want them yesterday. Your mission: "
                "jack into the stack trace and figure out what's bleeding the system dry."
            ),
            FailureScenario.STACK_OVERFLOW: (
                "LOGIC-1 went down hard at 04:23 hours with a stack overflow fault. "
                "The call stack spiraled out of control, deeper and deeper, until it "
                "smashed through the system's limits like a wrecking ball.\n\n"
                "The night shift supervisor is panicking - this is the third crash this week. "
                "Your job: dive into the stack trace and trace back what sent the system "
                "into this recursive death spiral."
            ),
            FailureScenario.NULL_POINTER: (
                "At 02:15 hours, LOGIC-1 choked on bad data and crashed hard. "
                "The system tried to process a request but hit a null reference - "
                "like reaching for a file that ain't there. Total system halt.\n\n"
                "The security logs show someone - or something - fed garbage into the core. "
                "Your assignment: examine the stack trace and pinpoint exactly what "
                "invalid data caused the crash."
            ),
            FailureScenario.DEADLOCK: (
                "LOGIC-1 locked up solid at 05:30 hours. Every process frozen, "
                "every thread stuck waiting. The whole system's in a Mexican standoff - "
                "nothing can move, nothing can proceed.\n\n"
                "The operations team tried a soft reset but the core won't respond. "
                "Your task: analyze the stack trace and identify the deadlock - "
                "figure out what's got the system tied in knots."
            ),
            FailureScenario.RESOURCE_EXHAUSTION: (
                "At 01:55 hours, LOGIC-1 ran itself into the ground. "
                "The system tried to load too much, process too much, hold too much - "
                "until it simply ran out of juice and collapsed under its own weight.\n\n"
                "The resource monitors went red across the board before the crash. "
                "Your mission: dig through the stack trace and determine what operations "
                "pushed the system past its breaking point."
            ),
        }
        
        description = [
            "=" * 70,
            "MEMORY STACK INVESTIGATION - LOGIC-1 DIAGNOSTIC TERMINAL",
            "=" * 70,
            "",
            ">>> CYBERDYNE SYSTEMS MAINFRAME ACCESS",
            ">>> CLEARANCE LEVEL: TECHNICIAN",
            ">>> DATE: NOVEMBER 15, 1985 - 06:00 HOURS",
            ">>> STATUS: ⚠️  CRITICAL SYSTEM FAILURE DETECTED",
            "",
            "INCIDENT REPORT:",
            scenario_narratives[self.scenario],
            "",
            "DIAGNOSTIC TOOLS AVAILABLE:",
            "  The stack trace has been dumped to the Prolog inference engine.",
            "  You can query the data using logical predicates to piece together",
            "  what went wrong. Think of it like detective work - follow the clues,",
            "  find the patterns, identify the culprit.",
            "",
            "PROLOG PREDICATES (Your Investigation Tools):",
            "  • frame(FrameId, FunctionName, Timestamp, Status)",
            "      - Each frame is a snapshot of a function call",
            "  • calls(CallerFrameId, CalleeFrameId)",
            "      - Shows which functions called which others",
            "  • allocated(FrameId, Bytes)",
            "      - Memory allocation for each frame",
            "  • param(FrameId, ParamName, ParamValue)",
            "      - Function parameters and their values",
            "  • status(FrameId, StatusValue)",
            "      - Current status: active, completed, or error",
            "",
        ]
        
        # Add BEGINNER-specific guidance with mentor voice
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            description.extend([
                "MENTOR NOTE - Dr. Sarah Martinez, Senior Systems Analyst:",
                "  \"Listen up, rookie. I know this looks intimidating, but debugging",
                "   is just asking the right questions. Start broad, then narrow down.",
                "   Here are some queries to get you started:\"",
                "",
                "  • List all frames: ?- frame(X, Y, Z, W).",
                "      (Shows everything - good for getting the lay of the land)",
                "  • Find errors: ?- status(FrameId, error).",
                "      (Errors are usually a smoking gun)",
                "  • Check memory: ?- allocated(FrameId, Bytes).",
                "      (Look for unusually high numbers)",
                "  • View parameters: ?- param(FrameId, ParamName, ParamValue).",
                "      (Bad data often shows up in parameters)",
                "  • See call relationships: ?- calls(Caller, Callee).",
                "      (Helps you trace the execution flow)",
                "",
                "  \"Remember: Variables (uppercase) match anything. Constants (lowercase",
                "   or numbers) match exactly. Use variables first to explore, then add",
                "   constants to zero in on the problem. You got this.\"",
                "",
            ])
        
        description.extend([
            "TERMINAL COMMANDS:",
            "  • hint          - Request guidance from your mentor",
            "  • diagnose <diagnosis> - Submit your root cause analysis",
            "",
            "The clock's ticking, investigator. LOGIC-1 needs to be back online",
            "before the morning shift. Find that bug and nail it down.",
            "",
            ">>> DIAGNOSTIC SESSION ACTIVE - AWAITING YOUR QUERIES...",
            "=" * 70,
        ])
        
        return "\n".join(description)
    
    def get_initial_context(self) -> Dict[str, Any]:
        """
        Get initial context including stack frame facts.
        
        Returns the stack trace data as Prolog facts that the player
        can query against. Also includes the investigation objective.
        Provides templates and examples for BEGINNER level.
        
        Returns:
            Dictionary with stack frame facts and context
            
        Validates: Requirements 1.2, 1.5, 6.1, 7.1, 7.2
        """
        # Convert stack frames to Prolog facts
        all_facts = []
        for frame in self.stack_frames:
            all_facts.extend(frame.to_prolog_facts())
        
        context = {
            "facts": all_facts,
            "fact_count": len(all_facts),
            "frame_count": len(self.stack_frames),
            "scenario_type": self.scenario.value,
            "objective": (
                "Investigate the stack trace by writing Prolog queries. "
                "Identify the root cause of the system failure and submit your diagnosis."
            ),
            "example_queries": [
                "?- frame(X, Y, Z, W).",  # List all frames
                "?- status(FrameId, error).",  # Find frames with errors
                "?- allocated(FrameId, Bytes).",  # Check memory allocations
            ],
        }
        
        # Add templates and detailed examples for BEGINNER level
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            context["query_templates"] = self._get_beginner_query_templates()
            context["template_explanations"] = self._get_template_explanations()
        
        return context
    
    def _get_beginner_query_templates(self) -> List[Dict[str, str]]:
        """
        Get query templates for BEGINNER level.
        
        Provides ready-to-use query patterns that players can adapt
        for their investigation.
        
        Returns:
            List of template dictionaries with pattern and description
            
        Validates: Requirements 1.5, 6.1
        """
        return [
            {
                "pattern": "?- frame(X, Y, Z, W).",
                "description": "List all frames with their properties",
                "usage": "Shows all stack frames. X=frame_id, Y=function_name, Z=timestamp, W=status"
            },
            {
                "pattern": "?- status(FrameId, Status).",
                "description": "Check the status of frames",
                "usage": "Find frames with specific status. Try: ?- status(X, error)."
            },
            {
                "pattern": "?- allocated(FrameId, Bytes).",
                "description": "Check memory allocation for frames",
                "usage": "See how much memory each frame allocated. Look for high values."
            },
            {
                "pattern": "?- param(FrameId, ParamName, ParamValue).",
                "description": "Examine function parameters",
                "usage": "Check what parameters were passed to functions. Look for null or unusual values."
            },
            {
                "pattern": "?- calls(CallerFrameId, CalleeFrameId).",
                "description": "See which frames called which other frames",
                "usage": "Understand the call relationships. Useful for finding recursion."
            },
            {
                "pattern": "?- frame(Id, FunctionName, Time, Status), status(Id, error).",
                "description": "Compound query: Find frames with errors",
                "usage": "Combines multiple conditions. This finds frames that have error status."
            },
            {
                "pattern": "?- allocated(Id, Bytes), Bytes > 1000000.",
                "description": "Find frames with high memory allocation",
                "usage": "Note: Comparison operators may not work in simple Prolog. Use variables to see all values."
            },
        ]
    
    def _get_template_explanations(self) -> Dict[str, str]:
        """
        Get explanations for query template usage.
        
        Returns:
            Dictionary with explanation topics and text
            
        Validates: Requirements 1.5, 6.1
        """
        return {
            "variables": (
                "Variables start with uppercase (X, Y, FrameId) and match any value. "
                "Use them to find all possible values."
            ),
            "constants": (
                "Constants are specific values like 'error', 1, or 'allocate_buffer'. "
                "Use them to filter for exact matches."
            ),
            "compound_queries": (
                "Combine multiple conditions with commas: ?- pred1(...), pred2(...).\n"
                "All conditions must be true for a result to match."
            ),
            "tips": (
                "Start broad (use all variables) then narrow down (add specific values). "
                "Look for patterns, anomalies, and relationships between frames."
            ),
        }
    
    def validate_solution(self, user_input: str) -> ValidationResult:
        """
        Validate user input - routes to query execution or diagnosis validation.
        
        Determines whether the input is a query or a diagnosis submission
        and routes it to the appropriate handler.
        
        Args:
            user_input: The user's input string
            
        Returns:
            ValidationResult with outcome and feedback
            
        Validates: Requirements 2.1, 2.2, 5.1
        """
        if not user_input or not user_input.strip():
            return ValidationResult(
                is_valid=False,
                error_message="Empty input. Please enter a query or diagnosis.",
                hint="Write a query like: ?- frame(X, Y, Z, W).\nOr submit a diagnosis: diagnose <your diagnosis>",
            )
        
        user_input = user_input.strip()
        
        # Check if it's a diagnosis submission
        if user_input.lower().startswith("diagnose "):
            diagnosis_text = user_input[9:].strip()  # Remove "diagnose " prefix
            return self._handle_diagnosis(diagnosis_text)
        
        # Otherwise, treat as a query
        return self._handle_query(user_input)
    
    def _handle_query(self, query: str) -> ValidationResult:
        """
        Handle query execution.
        
        Validates and executes a Prolog query against the stack frame facts.
        Tracks queries made and discoveries for progress-aware hints.
        Adds story progression messages for significant discoveries.
        
        Args:
            query: The Prolog query string
            
        Returns:
            ValidationResult with query results and story progression
            
        Validates: Requirements 2.1, 2.2, 2.3, 3.1, 10.2
        """
        # Execute the query
        result = self.query_processor.execute_query(query)
        
        # Track query for progress
        if result.success:
            self.queries_made.append(query)
            
            # Track discoveries and add story progression
            story_message = None
            if result.is_significant and result.discovery_type:
                # Check if this is a new discovery
                is_new_discovery = result.discovery_type not in self.discoveries
                self.discoveries.add(result.discovery_type)
                
                # Add story progression for new discoveries
                if is_new_discovery:
                    story_message = self._get_discovery_story_message(result.discovery_type)
            
            # Update hint system progress
            self.memory_hint_system.update_progress(
                len(self.queries_made),
                self.discoveries
            )
            
            # Add story message to formatted output if present
            formatted_output = result.formatted_output
            if story_message:
                formatted_output = f"{result.formatted_output}\n\n{story_message}"
        else:
            formatted_output = result.formatted_output
        
        # Convert QueryResult to ValidationResult
        return ValidationResult(
            is_valid=result.success,
            error_message=None if result.success else formatted_output,
            hint=None,
            parsed_components={
                "type": "query",
                "results": result.results,
                "formatted_output": formatted_output,
                "is_significant": result.is_significant,
                "discovery_type": result.discovery_type,
            },
        )
    
    def _get_discovery_story_message(self, discovery_type: str) -> str:
        """
        Get story progression message for a discovery.
        
        Provides narrative feedback when players make significant discoveries,
        advancing the story and maintaining immersion.
        
        Args:
            discovery_type: Type of discovery made
            
        Returns:
            Story progression message with cyberpunk 1985 flavor
            
        Validates: Requirements 10.2, 10.4, 10.5
        """
        story_messages = {
            "error": (
                ">>> MENTOR COMM: \"Nice catch! You found a frame with error status. "
                "That's your first solid lead. Now dig deeper - what caused that error? "
                "Check the parameters, the memory allocation, the call chain. "
                "The answer's in there somewhere.\""
            ),
            "memory_anomaly": (
                ">>> MENTOR COMM: \"Whoa, those memory numbers are way out of line! "
                "You're onto something big here. In my 15 years debugging systems, "
                "I've seen this pattern before. Keep following the memory trail - "
                "see if there's a pattern to these allocations.\""
            ),
            "recursion": (
                ">>> MENTOR COMM: \"Bingo! That's a recursive call pattern if I ever saw one. "
                "The system's calling itself over and over. Now the question is: "
                "is it supposed to stop? Check those parameters - look for depth counters "
                "or termination conditions. Something's not adding up.\""
            ),
            "null_parameter": (
                ">>> MENTOR COMM: \"Jackpot! Null parameters - that's your smoking gun right there. "
                "The system tried to process data that wasn't there. Classic mistake, "
                "but deadly for a system like LOGIC-1. You're close now - "
                "figure out which function choked on that null and you've got your culprit.\""
            ),
            "deadlock": (
                ">>> MENTOR COMM: \"There it is - lock contention! You've found the deadlock. "
                "Two processes waiting on each other, neither can proceed. "
                "It's like a standoff in an old Western. Check which locks are held "
                "and which are being waited for. The circular dependency is your answer.\""
            ),
            "pattern": (
                ">>> MENTOR COMM: \"Good eye! You're spotting patterns in the data. "
                "That's what separates the rookies from the pros. Keep analyzing - "
                "patterns tell stories, and this one's trying to tell you what went wrong.\""
            ),
        }
        
        return story_messages.get(
            discovery_type,
            ">>> MENTOR COMM: \"Interesting find. Keep digging - you're on the right track.\""
        )
    
    def _handle_diagnosis(self, diagnosis: str) -> ValidationResult:
        """
        Handle diagnosis submission.
        
        Validates the player's diagnosis of the root cause and provides
        feedback. Marks puzzle as complete if diagnosis is correct.
        Adds completion narrative with story consequences and scoring information.
        
        Args:
            diagnosis: The player's diagnosis text
            
        Returns:
            ValidationResult with diagnosis outcome, story conclusion, and score
            
        Validates: Requirements 5.1, 5.2, 5.3, 5.4, 10.3
        """
        self.diagnosis_submitted = True
        
        # Validate the diagnosis
        result = self.diagnosis_validator.validate_diagnosis(diagnosis)
        
        # If correct, mark puzzle as complete and add story conclusion
        if result.is_correct:
            self.completed = True
            
            # Calculate score
            final_score = self._calculate_score()
            
            # Get completion statistics
            stats = self.get_completion_statistics()
            
            # Add completion narrative with story consequences
            completion_story = self._get_completion_narrative()
            
            # Format scoring information
            score_info = self._format_score_information(stats)
            
            # Combine feedback, explanation, story, and score
            feedback_parts = [
                result.feedback,
                "\n" + "=" * 70,
                result.explanation if result.explanation else "",
                "\n" + "=" * 70,
                completion_story,
                "\n" + "=" * 70,
                score_info,
            ]
        else:
            # For incorrect or partial diagnoses, just show feedback
            feedback_parts = [result.feedback]
            if result.explanation:
                feedback_parts.append("\n\n" + result.explanation)
        
        return ValidationResult(
            is_valid=result.is_correct,
            error_message=None if result.is_correct else "\n".join(feedback_parts),
            hint=None,
            parsed_components={
                "type": "diagnosis",
                "is_correct": result.is_correct,
                "is_partial": result.is_partial,
                "feedback": result.feedback,
                "explanation": result.explanation,
                "score": final_score if result.is_correct else 0,
                "statistics": stats if result.is_correct else None,
            },
        )
    
    def _format_score_information(self, stats: Dict[str, Any]) -> str:
        """
        Format scoring information for display.
        
        Creates a clear, readable summary of the player's performance
        including score breakdown and efficiency ratings.
        
        Args:
            stats: Completion statistics dictionary
            
        Returns:
            Formatted score information string
            
        Validates: Requirements 5.2, 5.4
        """
        score_breakdown = stats["score_breakdown"]
        efficiency = stats["efficiency_rating"]
        
        lines = [
            "PERFORMANCE ANALYSIS",
            "=" * 70,
            "",
            f"Complexity Level: {stats['complexity_level'].upper()}",
            f"Queries Made: {stats['queries_made']} ({efficiency['query_efficiency']} efficiency)",
            f"Discoveries Found: {stats['discoveries_found']}",
            f"Hints Used: {stats['hints_used']} ({efficiency['hint_efficiency']} efficiency)",
            "",
            "SCORE BREAKDOWN:",
            f"  Base Score:              {score_breakdown['base_score']} points",
            f"  Query Penalty:          -{score_breakdown['query_penalty']} points",
            f"  Hint Penalty:           -{score_breakdown['hint_penalty']} points",
            f"  Score Before Multiplier: {score_breakdown['score_before_multiplier']} points",
            f"  Complexity Multiplier:   x{score_breakdown['complexity_multiplier']}",
            "",
            f"FINAL SCORE: {score_breakdown['final_score']} points",
            "",
        ]
        
        # Add performance feedback
        if stats['queries_made'] <= 8 and stats['hints_used'] == 0:
            lines.append("🌟 OUTSTANDING! You solved this efficiently without hints!")
        elif stats['queries_made'] <= 12 and stats['hints_used'] <= 2:
            lines.append("✨ EXCELLENT! You demonstrated strong debugging skills!")
        elif stats['hints_used'] == 0:
            lines.append("💪 GREAT! You solved it without hints!")
        else:
            lines.append("✅ GOOD WORK! You persevered and found the solution!")
        
        return "\n".join(lines)
    
    def _get_completion_narrative(self) -> str:
        """
        Get completion narrative with story consequences.
        
        Provides an immersive conclusion to the puzzle that ties back
        to the LOGIC-1 storyline and shows the impact of the player's work.
        
        Returns:
            Completion narrative with cyberpunk 1985 flavor
            
        Validates: Requirements 10.3, 10.4, 10.5
        """
        # Scenario-specific completion narratives
        completion_narratives = {
            FailureScenario.MEMORY_LEAK: (
                "SYSTEM STATUS UPDATE:\n"
                ">>> LOGIC-1 DIAGNOSTIC COMPLETE\n"
                ">>> ROOT CAUSE IDENTIFIED: MEMORY LEAK\n"
                ">>> REPAIR PROTOCOL INITIATED\n\n"
                "You patch the code, adding proper cleanup routines to the allocate_buffer "
                "function. The fix is elegant - just a few lines, but they make all the difference. "
                "You recompile, reload, and watch the memory monitors. Steady. Stable. Clean.\n\n"
                "Dr. Chen walks into the terminal room at 07:15, coffee in hand. "
                "\"Status report?\" she asks. You gesture to the green lights on the console. "
                "\"LOGIC-1 is back online, Doc. Memory leak in the buffer allocation. "
                "Patched and tested.\"\n\n"
                "She nods, impressed. \"Good work. The AI Research Division can resume testing. "
                "You just saved us three days of downtime.\" She pauses at the door. "
                "\"Keep this up and you won't be a junior programmer for long.\"\n\n"
                ">>> PUZZLE COMPLETE - LOGIC-1 OPERATIONAL\n"
                ">>> NEXT CHALLENGE UNLOCKED"
            ),
            FailureScenario.STACK_OVERFLOW: (
                "SYSTEM STATUS UPDATE:\n"
                ">>> LOGIC-1 DIAGNOSTIC COMPLETE\n"
                ">>> ROOT CAUSE IDENTIFIED: STACK OVERFLOW\n"
                ">>> REPAIR PROTOCOL INITIATED\n\n"
                "You add a depth check to the recursive function - a simple guard condition "
                "that should have been there from the start. The fix goes in clean. "
                "You restart LOGIC-1 and run the test suite. No crashes. No overflow. "
                "The recursion stays within bounds.\n\n"
                "The night shift supervisor practically runs into the terminal room. "
                "\"Tell me you fixed it,\" he says, looking haggard. You point to the "
                "status display showing all green. \"Stack overflow in recursive_process. "
                "Added depth limiting. System's stable now.\"\n\n"
                "He slumps into a chair, relieved. \"Thank God. The brass was ready to "
                "pull the plug on the whole project. You just saved LOGIC-1.\" "
                "He grins. \"And probably my job too.\"\n\n"
                ">>> PUZZLE COMPLETE - LOGIC-1 OPERATIONAL\n"
                ">>> NEXT CHALLENGE UNLOCKED"
            ),
            FailureScenario.NULL_POINTER: (
                "SYSTEM STATUS UPDATE:\n"
                ">>> LOGIC-1 DIAGNOSTIC COMPLETE\n"
                ">>> ROOT CAUSE IDENTIFIED: NULL POINTER ERROR\n"
                ">>> REPAIR PROTOCOL INITIATED\n\n"
                "You add null checks to the process_request function - defensive programming "
                "101, but someone missed it. The fix is straightforward: validate inputs "
                "before processing. You recompile and test with various inputs, including "
                "null values. The system handles them gracefully now, no more crashes.\n\n"
                "Security Chief Morrison reviews your findings at 08:00. \"So someone fed "
                "bad data into the core,\" he says, studying the logs. \"Accidental or "
                "deliberate?\" You shrug. \"Can't say for sure, but the system should have "
                "handled it either way. It does now.\"\n\n"
                "He nods slowly. \"Good catch. I'll tighten up input validation across the board. "
                "And I'll be keeping an eye on who has access to LOGIC-1's input channels.\" "
                "He heads for the door. \"Nice work, investigator.\"\n\n"
                ">>> PUZZLE COMPLETE - LOGIC-1 OPERATIONAL\n"
                ">>> NEXT CHALLENGE UNLOCKED"
            ),
            FailureScenario.DEADLOCK: (
                "SYSTEM STATUS UPDATE:\n"
                ">>> LOGIC-1 DIAGNOSTIC COMPLETE\n"
                ">>> ROOT CAUSE IDENTIFIED: DEADLOCK\n"
                ">>> REPAIR PROTOCOL INITIATED\n\n"
                "You reorder the lock acquisition sequence - a classic fix for a classic problem. "
                "All threads now acquire locks in the same order, eliminating the circular "
                "dependency. You restart LOGIC-1 and run the concurrent processing tests. "
                "No freezes. No deadlocks. The system flows smoothly.\n\n"
                "The operations team crowds around your terminal at 07:30. \"Did you break "
                "the deadlock?\" asks the lead operator. You bring up the process monitor "
                "showing all threads running clean. \"Lock ordering issue. Fixed and tested. "
                "LOGIC-1 won't freeze up anymore.\"\n\n"
                "The team erupts in cheers. \"You're a lifesaver!\" someone shouts. "
                "The lead operator shakes your hand. \"We've been fighting this deadlock "
                "for weeks. Management was about to scrap the whole concurrent processing "
                "module. You just saved the project.\"\n\n"
                ">>> PUZZLE COMPLETE - LOGIC-1 OPERATIONAL\n"
                ">>> NEXT CHALLENGE UNLOCKED"
            ),
            FailureScenario.RESOURCE_EXHAUSTION: (
                "SYSTEM STATUS UPDATE:\n"
                ">>> LOGIC-1 DIAGNOSTIC COMPLETE\n"
                ">>> ROOT CAUSE IDENTIFIED: RESOURCE EXHAUSTION\n"
                ">>> REPAIR PROTOCOL INITIATED\n\n"
                "You implement resource limits and lazy loading for the dataset operations. "
                "Instead of loading everything at once, the system now loads data on demand "
                "and releases it when done. You restart LOGIC-1 and run the full dataset "
                "processing suite. Memory usage stays reasonable. No crashes.\n\n"
                "Dr. Chen reviews your solution at the morning briefing. \"Elegant,\" she says, "
                "studying the code. \"You didn't just fix the crash - you made the system "
                "more efficient.\" She looks up. \"The AI models can now process larger "
                "datasets without overwhelming the hardware.\"\n\n"
                "The research team applauds. \"This opens up new possibilities,\" says one "
                "of the AI researchers. \"We can finally test the neural network on the "
                "full training set.\" Dr. Chen smiles. \"Outstanding work, investigator. "
                "You've earned your place on this team.\"\n\n"
                ">>> PUZZLE COMPLETE - LOGIC-1 OPERATIONAL\n"
                ">>> NEXT CHALLENGE UNLOCKED"
            ),
        }
        
        return completion_narratives.get(
            self.scenario,
            ">>> PUZZLE COMPLETE - LOGIC-1 OPERATIONAL\n>>> NEXT CHALLENGE UNLOCKED"
        )
    
    def get_hint(self, hint_level: int) -> str:
        """
        Get a progress-aware hint adapted to complexity level.
        
        Provides hints that adapt based on:
        - Number of queries made
        - Discoveries found
        - Current complexity level
        - Hint progression (exploration → investigation → diagnosis)
        
        Args:
            hint_level: Level of hint requested (not used, kept for interface compatibility)
            
        Returns:
            Adaptive hint text
            
        Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5
        """
        # Update hint system with current progress
        self.memory_hint_system.update_progress(
            len(self.queries_made),
            self.discoveries
        )
        
        # Get adaptive hint from the hint system
        hint = self.memory_hint_system.get_adaptive_hint()
        
        # Add query suggestion if available (BEGINNER level only)
        phase = self._get_current_phase()
        suggestion = self.memory_hint_system.generate_query_suggestion(phase)
        
        if suggestion:
            hint += f"\n\nSuggested query: {suggestion}"
        
        return hint
    
    def _get_current_phase(self) -> str:
        """
        Determine the current investigation phase based on progress.
        
        Returns:
            One of "exploration", "investigation", or "diagnosis"
        """
        if len(self.queries_made) < 3:
            return "exploration"
        elif len(self.queries_made) < 6:
            return "investigation"
        else:
            return "diagnosis"
    
    def get_expected_solution(self) -> str:
        """
        Get the expected solution (diagnosis) for this puzzle.
        
        Returns:
            Description of the correct diagnosis
        """
        scenario_solutions = {
            FailureScenario.MEMORY_LEAK: "Memory leak - allocated memory not being freed",
            FailureScenario.STACK_OVERFLOW: "Stack overflow - excessive recursion depth",
            FailureScenario.NULL_POINTER: "Null pointer error - invalid parameters passed",
            FailureScenario.DEADLOCK: "Deadlock - circular lock dependency",
            FailureScenario.RESOURCE_EXHAUSTION: "Resource exhaustion - excessive memory consumption",
        }
        
        return scenario_solutions[self.scenario]
    
    def set_complexity_level(self, level: ComplexityLevel) -> None:
        """
        Set complexity level for the puzzle and its hint system.
        
        Overrides parent method to also update the memory-specific hint system.
        Handles dynamic complexity changes by updating all relevant components
        and resetting hint availability.
        
        Args:
            level: The complexity level to set
            
        Validates: Requirements 1.5, 6.1, 6.2, 6.3, 6.4, 6.5
        """
        # Store previous level for comparison
        previous_level = self.current_complexity_level
        
        # Update parent class complexity level
        super().set_complexity_level(level)
        
        # Update memory-specific hint system
        self.memory_hint_system.set_complexity_level(level)
        
        # If complexity changed during active puzzle, provide feedback
        if previous_level != level and self.queries_made:
            self._handle_complexity_change(previous_level, level)
    
    def _handle_complexity_change(self, previous_level: ComplexityLevel, new_level: ComplexityLevel) -> None:
        """
        Handle dynamic complexity level changes during active puzzle.
        
        Adjusts hint availability and provides feedback about the change.
        
        Args:
            previous_level: The previous complexity level
            new_level: The new complexity level
            
        Validates: Requirements 6.4, 6.5
        """
        # Log the change (in a real implementation, this might update UI or provide feedback)
        # For now, we just ensure the hint system is properly updated
        
        # The hint system's set_complexity_level already resets hint count,
        # which is appropriate for dynamic changes
        
        # Note: In a full implementation, you might want to:
        # - Notify the player about the change
        # - Adjust available hints based on new level
        # - Update any UI elements showing complexity-specific information
        pass
    
    def reset(self):
        """
        Reset puzzle state for a new attempt.
        
        Clears queries, discoveries, and resets hint system while
        keeping the same scenario and stack frames.
        """
        super().reset()
        self.queries_made = []
        self.discoveries = set()
        self.diagnosis_submitted = False
        self.investigation_started = False
        self.memory_hint_system.reset_progress()
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """
        Get a summary of investigation progress.
        
        Returns:
            Dictionary with progress information including queries made,
            discoveries found, and current phase
        """
        return {
            "queries_made": len(self.queries_made),
            "discoveries": list(self.discoveries),
            "diagnosis_submitted": self.diagnosis_submitted,
            "completed": self.completed,
            "current_phase": self._get_current_phase(),
            "hints_used": self.hints_used,
            "attempts": self.attempts,
        }
    
    def get_stack_trace_summary(self) -> str:
        """
        Get a formatted summary of the stack trace.
        
        Provides a high-level overview of the stack frames without
        revealing the anomaly directly.
        
        Returns:
            Formatted stack trace summary
        """
        lines = [
            "STACK TRACE SUMMARY",
            "=" * 50,
            f"Total frames: {len(self.stack_frames)}",
            f"Scenario type: {self.scenario.value}",
            "",
            "Frame overview:",
        ]
        
        for frame in self.stack_frames[:5]:  # Show first 5 frames
            lines.append(
                f"  Frame {frame.frame_id}: {frame.function_name} "
                f"[{frame.status}] - {frame.memory_allocated} bytes"
            )
        
        if len(self.stack_frames) > 5:
            lines.append(f"  ... and {len(self.stack_frames) - 5} more frames")
        
        lines.append("")
        lines.append("Use queries to investigate the details.")
        
        return "\n".join(lines)
    
    def get_complexity_adapted_examples(self) -> List[str]:
        """
        Get example queries adapted to the current complexity level.
        
        Provides different levels of example detail based on complexity:
        - BEGINNER: Detailed examples with explanations
        - INTERMEDIATE: Basic examples without explanations
        - ADVANCED: Minimal examples
        - EXPERT: No examples
        
        Returns:
            List of example query strings
            
        Validates: Requirements 1.5, 6.1, 6.2, 6.3, 6.4
        """
        if self.current_complexity_level == ComplexityLevel.BEGINNER:
            return [
                "?- frame(X, Y, Z, W).  # List all frames",
                "?- status(FrameId, error).  # Find frames with errors",
                "?- allocated(FrameId, Bytes).  # Check memory allocations",
                "?- param(FrameId, ParamName, ParamValue).  # View parameters",
                "?- calls(Caller, Callee).  # See call relationships",
            ]
        elif self.current_complexity_level == ComplexityLevel.INTERMEDIATE:
            return [
                "?- frame(X, Y, Z, W).",
                "?- status(FrameId, error).",
                "?- allocated(FrameId, Bytes).",
            ]
        elif self.current_complexity_level == ComplexityLevel.ADVANCED:
            return [
                "?- frame(X, Y, Z, W).",
                "?- status(FrameId, Status).",
            ]
        else:  # EXPERT
            return []  # No examples for expert level
    
    def _calculate_score(self) -> int:
        """
        Calculate score based on queries made, hints used, and complexity level.
        
        Scoring factors:
        - Base score: 100 points
        - Query efficiency: Deduct points for excessive queries
        - Hint penalty: Deduct points for hints used (complexity-aware)
        - Complexity multiplier: Bonus for higher difficulty levels
        
        Returns:
            Final calculated score
            
        Validates: Requirements 5.2, 5.4
        """
        base_score = self.max_score
        
        # Calculate query efficiency penalty
        # Optimal query count is around 5-8 queries
        # Penalize for too many queries (inefficient investigation)
        query_count = len(self.queries_made)
        if query_count <= 8:
            # Efficient investigation - no penalty
            query_penalty = 0
        elif query_count <= 12:
            # Moderate investigation - small penalty
            query_penalty = (query_count - 8) * 3
        else:
            # Excessive queries - larger penalty
            query_penalty = 12 + (query_count - 12) * 5
        
        # Use hint system to calculate hint penalty based on complexity level
        hint_penalty = self.hint_system.calculate_hint_penalty(self.hints_used)
        
        # Calculate score before complexity multiplier
        score_before_multiplier = max(10, base_score - query_penalty - hint_penalty)
        
        # Apply complexity multiplier
        complexity_multiplier = self.complexity_manager.get_scoring_multiplier()
        final_score = int(score_before_multiplier * complexity_multiplier)
        
        return final_score
    
    def get_completion_statistics(self) -> Dict[str, Any]:
        """
        Get detailed statistics about puzzle completion.
        
        Provides comprehensive information about the player's performance
        including efficiency metrics and scoring breakdown.
        
        Returns:
            Dictionary with completion statistics
            
        Validates: Requirements 5.2, 5.4, 5.5
        """
        if not self.completed:
            return {
                "completed": False,
                "message": "Puzzle not yet completed",
            }
        
        # Calculate score components
        base_score = self.max_score
        query_count = len(self.queries_made)
        
        # Query efficiency analysis
        if query_count <= 8:
            query_efficiency = "Excellent"
            query_penalty = 0
        elif query_count <= 12:
            query_efficiency = "Good"
            query_penalty = (query_count - 8) * 3
        else:
            query_efficiency = "Could be improved"
            query_penalty = 12 + (query_count - 12) * 5
        
        # Hint penalty
        hint_penalty = self.hint_system.calculate_hint_penalty(self.hints_used)
        
        # Complexity multiplier
        complexity_multiplier = self.complexity_manager.get_scoring_multiplier()
        
        # Final score
        score_before_multiplier = max(10, base_score - query_penalty - hint_penalty)
        final_score = int(score_before_multiplier * complexity_multiplier)
        
        return {
            "completed": True,
            "scenario_type": self.scenario.value,
            "complexity_level": self.current_complexity_level.name.lower(),  # Use .name for string representation
            "queries_made": query_count,
            "discoveries_found": len(self.discoveries),
            "discoveries": list(self.discoveries),
            "hints_used": self.hints_used,
            "score_breakdown": {
                "base_score": base_score,
                "query_penalty": query_penalty,
                "hint_penalty": hint_penalty,
                "score_before_multiplier": score_before_multiplier,
                "complexity_multiplier": complexity_multiplier,
                "final_score": final_score,
            },
            "efficiency_rating": {
                "query_efficiency": query_efficiency,
                "hint_efficiency": "Perfect" if self.hints_used == 0 else "Good" if self.hints_used <= 2 else "Moderate",
            },
            "educational_summary": self._get_educational_summary(),
        }
    
    def _get_educational_summary(self) -> Dict[str, Any]:
        """
        Get educational summary connecting puzzle to real-world debugging.
        
        Provides context about how the puzzle concepts apply to actual
        software development and debugging practices.
        
        Returns:
            Dictionary with educational content
            
        Validates: Requirements 7.5
        """
        # Scenario-specific educational content
        educational_content = {
            FailureScenario.MEMORY_LEAK: {
                "concept": "Memory Leak Detection",
                "real_world_application": (
                    "Memory leaks are one of the most common causes of application crashes "
                    "in production systems. They occur when allocated memory is not properly "
                    "freed, causing memory usage to grow over time until the system runs out."
                ),
                "debugging_techniques": [
                    "Use memory profilers to track allocation patterns",
                    "Look for functions that allocate without corresponding deallocation",
                    "Check for missing cleanup in error handling paths",
                    "Monitor memory usage trends over time",
                ],
                "prolog_connection": (
                    "In this puzzle, you used Prolog queries to identify allocation patterns "
                    "without corresponding cleanup - the same logical reasoning you'd apply "
                    "when analyzing memory dumps or profiler output in real debugging."
                ),
            },
            FailureScenario.STACK_OVERFLOW: {
                "concept": "Stack Overflow and Recursion Limits",
                "real_world_application": (
                    "Stack overflows occur when recursive functions exceed the call stack limit, "
                    "or when deeply nested function calls consume too much stack space. This is "
                    "common in recursive algorithms without proper base cases or depth limits."
                ),
                "debugging_techniques": [
                    "Check for missing or incorrect base cases in recursive functions",
                    "Verify recursion depth against system limits",
                    "Consider iterative alternatives for deep recursion",
                    "Use tail recursion optimization where available",
                ],
                "prolog_connection": (
                    "You used Prolog's pattern matching to identify excessive recursion depth - "
                    "the same logical analysis you'd perform when examining stack traces in "
                    "debuggers or crash dumps."
                ),
            },
            FailureScenario.NULL_POINTER: {
                "concept": "Null Pointer Dereference",
                "real_world_application": (
                    "Null pointer errors (or None/null reference errors) are among the most "
                    "common runtime errors. They occur when code attempts to use a reference "
                    "that doesn't point to valid data, often due to missing validation or "
                    "initialization."
                ),
                "debugging_techniques": [
                    "Add null checks before dereferencing pointers/references",
                    "Validate function inputs at entry points",
                    "Use static analysis tools to detect potential null dereferences",
                    "Initialize variables properly before use",
                ],
                "prolog_connection": (
                    "Your Prolog queries identified null parameters in the stack trace - "
                    "demonstrating how logical queries can pinpoint invalid data that causes "
                    "runtime errors, similar to analyzing variable states in a debugger."
                ),
            },
            FailureScenario.DEADLOCK: {
                "concept": "Deadlock Detection and Prevention",
                "real_world_application": (
                    "Deadlocks occur in concurrent systems when two or more processes wait "
                    "for each other to release resources, creating a circular dependency. "
                    "This is a critical issue in multi-threaded applications and distributed systems."
                ),
                "debugging_techniques": [
                    "Establish consistent lock acquisition ordering",
                    "Use timeout mechanisms for lock acquisition",
                    "Implement deadlock detection algorithms",
                    "Analyze thread dumps to identify circular wait conditions",
                ],
                "prolog_connection": (
                    "You used Prolog's relational queries to map lock dependencies and identify "
                    "circular waits - the same logical reasoning used in deadlock detection "
                    "algorithms and thread analysis tools."
                ),
            },
            FailureScenario.RESOURCE_EXHAUSTION: {
                "concept": "Resource Exhaustion and Capacity Planning",
                "real_world_application": (
                    "Resource exhaustion occurs when applications consume more resources "
                    "(memory, CPU, file handles, etc.) than available, causing system failure. "
                    "This is common in systems without proper resource limits or capacity planning."
                ),
                "debugging_techniques": [
                    "Implement resource limits and quotas",
                    "Monitor resource usage trends",
                    "Use lazy loading and resource pooling",
                    "Profile resource consumption patterns",
                ],
                "prolog_connection": (
                    "Your Prolog queries aggregated resource usage across multiple operations - "
                    "demonstrating how logical queries can analyze cumulative effects, similar "
                    "to how monitoring tools aggregate metrics to detect resource issues."
                ),
            },
        }
        
        content = educational_content[self.scenario]
        
        return {
            "concept": content["concept"],
            "real_world_application": content["real_world_application"],
            "debugging_techniques": content["debugging_techniques"],
            "prolog_connection": content["prolog_connection"],
            "skills_practiced": [
                "Logical reasoning and pattern recognition",
                "Systematic investigation methodology",
                "Data analysis and anomaly detection",
                "Root cause analysis",
                "Hypothesis formation and testing",
            ],
        }
