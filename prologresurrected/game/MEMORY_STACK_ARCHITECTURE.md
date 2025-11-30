# Memory Stack Puzzle - Architecture Diagrams

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      MemoryStackPuzzle                          │
│                    (extends BasePuzzle)                         │
│                                                                 │
│  Properties:                                                    │
│  • scenario: FailureScenario                                   │
│  • stack_frames: List[StackFrame]                              │
│  • queries_made: List[str]                                     │
│  • discoveries: Set[str]                                       │
│  • completed: bool                                             │
│                                                                 │
│  Methods:                                                       │
│  • get_description() → str                                     │
│  • get_initial_context() → Dict                               │
│  • validate_solution(input) → ValidationResult                │
│  • get_hint(level) → str                                       │
│  • set_complexity_level(level)                                │
│  • get_completion_statistics() → Dict                         │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│StackFrameGenerator│  │  QueryProcessor  │  │DiagnosisValidator│
│                  │  │                  │  │                  │
│ • generate_stack │  │ • execute_query  │  │ • validate_      │
│   _trace()       │  │ • find_call_     │  │   diagnosis()    │
│ • _inject_       │  │   chain()        │  │ • get_hint_for_  │
│   anomaly()      │  │ • get_relation   │  │   diagnosis()    │
│                  │  │   ship_info()    │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
                              │
                              │
                              ▼
                      ┌──────────────────┐
                      │ QueryValidator   │
                      │                  │
                      │ • validate_query │
                      │ • _validate_     │
                      │   simple_query   │
                      │ • _validate_     │
                      │   compound_query │
                      └──────────────────┘
                              │
                              ▼
                      ┌──────────────────┐
                      │ ResultFormatter  │
                      │                  │
                      │ • format_results │
                      │ • detect_        │
                      │   significance   │
                      │ • format_empty_  │
                      │   result         │
                      └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              MemoryStackHintSystem                              │
│        (extends ComplexityAwareHintSystem)                      │
│                                                                 │
│  • update_progress(queries, discoveries)                       │
│  • get_adaptive_hint() → str                                   │
│  • generate_query_suggestion(phase) → str                      │
│  • _generate_exploration_hint()                                │
│  • _generate_investigation_hint()                              │
│  • _generate_diagnosis_hint()                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│   Player    │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  MemoryStackPuzzle.validate_solution()  │
└──────┬──────────────────────────────────┘
       │
       ├─── Is Query? ───────────────────────┐
       │                                     │
       │                                     ▼
       │                          ┌──────────────────┐
       │                          │ QueryValidator   │
       │                          │ .validate_query()│
       │                          └────────┬─────────┘
       │                                   │
       │                                   ▼
       │                          ┌──────────────────┐
       │                          │ QueryProcessor   │
       │                          │ .execute_query() │
       │                          └────────┬─────────┘
       │                                   │
       │                                   ▼
       │                          ┌──────────────────┐
       │                          │ ResultFormatter  │
       │                          │ .format_results()│
       │                          └────────┬─────────┘
       │                                   │
       │                                   ▼
       │                          ┌──────────────────┐
       │                          │ Track Progress   │
       │                          │ • queries_made++ │
       │                          │ • add discoveries│
       │                          └────────┬─────────┘
       │                                   │
       │                                   ▼
       │                          ┌──────────────────┐
       │                          │ Story Progression│
       │                          │ (if significant) │
       │                          └────────┬─────────┘
       │                                   │
       └───────────────────────────────────┤
                                           │
       ┌─── Is Diagnosis? ─────────────────┤
       │                                   │
       ▼                                   │
┌──────────────────┐                      │
│DiagnosisValidator│                      │
│.validate_        │                      │
│ diagnosis()      │                      │
└────────┬─────────┘                      │
         │                                │
         ▼                                │
┌──────────────────┐                      │
│ If Correct:      │                      │
│ • Mark complete  │                      │
│ • Calculate score│                      │
│ • Show narrative │                      │
└────────┬─────────┘                      │
         │                                │
         └────────────────────────────────┤
                                          │
                                          ▼
                                 ┌────────────────┐
                                 │ Return Result  │
                                 │ to Player      │
                                 └────────────────┘
```

## Hint System Flow

```
┌──────────────┐
│ Player       │
│ Requests Hint│
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│ MemoryStackPuzzle.get_hint()        │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ MemoryStackHintSystem               │
│ .update_progress(queries,           │
│                  discoveries)        │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Determine Phase:                    │
│ • 0-2 queries: Exploration          │
│ • 3-5 queries: Investigation        │
│ • 6+ queries: Diagnosis             │
└──────┬──────────────────────────────┘
       │
       ├─── Exploration ────────────────┐
       │                                │
       ├─── Investigation ──────────────┤
       │                                │
       └─── Diagnosis ─────────────────┤
                                        │
                                        ▼
                              ┌──────────────────┐
                              │ Check Complexity │
                              │ Level            │
                              └────────┬─────────┘
                                       │
       ┌───────────────────────────────┼───────────────────────────┐
       │                               │                           │
       ▼                               ▼                           ▼
┌──────────────┐              ┌──────────────┐           ┌──────────────┐
│  BEGINNER    │              │ INTERMEDIATE │           │   ADVANCED   │
│              │              │              │           │   / EXPERT   │
│ • Detailed   │              │ • Moderate   │           │ • Minimal    │
│   hints      │              │   guidance   │           │   hints      │
│ • Examples   │              │ • No examples│           │ • Conceptual │
│ • Templates  │              │              │           │   only       │
└──────┬───────┘              └──────┬───────┘           └──────┬───────┘
       │                             │                          │
       └─────────────────────────────┼──────────────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ Check Discoveries│
                            │ for Context      │
                            └────────┬─────────┘
                                     │
       ┌─────────────────────────────┼─────────────────────────┐
       │                             │                         │
       ▼                             ▼                         ▼
┌──────────────┐           ┌──────────────┐         ┌──────────────┐
│ Error Found  │           │Memory Anomaly│         │ Null Params  │
│              │           │              │         │              │
│ • Guide to   │           │ • Check      │         │ • Identify   │
│   parameters │           │   allocations│         │   frame      │
└──────┬───────┘           └──────┬───────┘         └──────┬───────┘
       │                          │                        │
       └──────────────────────────┼────────────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Generate Hint    │
                         │ with Mentor Voice│
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Add Query        │
                         │ Suggestion       │
                         │ (BEGINNER only)  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Return Hint      │
                         │ to Player        │
                         └──────────────────┘
```

## Stack Frame Generation

```
┌──────────────────────────────────────┐
│ StackFrameGenerator.__init__()      │
│ • scenario: FailureScenario          │
│ • seed: Optional[int]                │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ generate_stack_trace(num_frames)    │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Generate Normal Frames               │
│ (num_frames // 2)                    │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ Inject Anomaly Based on Scenario:   │
└──────┬───────────────────────────────┘
       │
       ├─── MEMORY_LEAK ────────────────┐
       │                                │
       ├─── STACK_OVERFLOW ─────────────┤
       │                                │
       ├─── NULL_POINTER ───────────────┤
       │                                │
       ├─── DEADLOCK ───────────────────┤
       │                                │
       └─── RESOURCE_EXHAUSTION ────────┤
                                        │
                                        ▼
                              ┌──────────────────┐
                              │ _inject_anomaly()│
                              │ • Create frames  │
                              │   with specific  │
                              │   anomaly        │
                              │   properties     │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Generate         │
                              │ Remaining Frames │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Return           │
                              │ List[StackFrame] │
                              └──────────────────┘
```

## Query Processing Pipeline

```
┌──────────────────┐
│ User Query       │
│ "?- frame(X,Y,Z)"│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ QueryValidator.validate_query()      │
│ • Check syntax                       │
│ • Identify type (simple/compound/neg)│
│ • Parse components                   │
└────────┬─────────────────────────────┘
         │
         ├─── Invalid ──────────────────┐
         │                              │
         │                              ▼
         │                     ┌──────────────────┐
         │                     │ Return Error     │
         │                     │ with Hint        │
         │                     └──────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ QueryProcessor.execute_query()       │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Route by Query Type:                 │
└────────┬─────────────────────────────┘
         │
         ├─── Simple ───────────────────┐
         │                              │
         ├─── Compound ─────────────────┤
         │                              │
         └─── Negation ────────────────┤
                                        │
                                        ▼
                              ┌──────────────────┐
                              │ Match Against    │
                              │ Fact Database    │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Bind Variables   │
                              │ to Values        │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ ResultFormatter  │
                              │ .format_results()│
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Detect           │
                              │ Significance     │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Return           │
                              │ QueryResult      │
                              └──────────────────┘
```

## Complexity Level Adaptation

```
┌──────────────────────────────────────┐
│ Complexity Level Set                 │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ MemoryStackPuzzle                    │
│ .set_complexity_level(level)         │
└────────┬─────────────────────────────┘
         │
         ├─── Update Parent ────────────┐
         │                              │
         └─── Update Hint System ───────┤
                                        │
                                        ▼
                              ┌──────────────────┐
                              │ Adjust:          │
                              │ • Hint detail    │
                              │ • Examples       │
                              │ • Templates      │
                              │ • Guidance level │
                              └────────┬─────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────┐
         │                             │                         │
         ▼                             ▼                         ▼
┌──────────────┐           ┌──────────────┐          ┌──────────────┐
│  BEGINNER    │           │ INTERMEDIATE │          │   ADVANCED   │
│              │           │              │          │   / EXPERT   │
│ Templates: ✓ │           │ Templates: ✗ │          │ Templates: ✗ │
│ Examples: ✓  │           │ Examples: ~  │          │ Examples: ✗  │
│ Hints: Full  │           │ Hints: Mod   │          │ Hints: Min   │
│ Guidance: ✓  │           │ Guidance: ~  │          │ Guidance: ✗  │
└──────────────┘           └──────────────┘          └──────────────┘
```

## Scoring System

```
┌──────────────────────────────────────┐
│ Puzzle Completed                     │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Calculate Base Score                 │
│ base_score = 100                     │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Calculate Query Penalty              │
│ • 0-8 queries: 0 penalty             │
│ • 9-12 queries: (count-8) × 3        │
│ • 13+ queries: 12 + (count-12) × 5   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Calculate Hint Penalty               │
│ (complexity-aware)                   │
│ • BEGINNER: hints × 5                │
│ • INTERMEDIATE: hints × 10           │
│ • ADVANCED: hints × 15               │
│ • EXPERT: hints × 20                 │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ score_before_multiplier =            │
│ max(10, base - query_pen - hint_pen) │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Apply Complexity Multiplier          │
│ • BEGINNER: × 1.0                    │
│ • INTERMEDIATE: × 1.5                │
│ • ADVANCED: × 2.0                    │
│ • EXPERT: × 2.5                      │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ final_score =                        │
│ int(score_before_multiplier ×        │
│     complexity_multiplier)           │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Return Score with Breakdown          │
└──────────────────────────────────────┘
```

## Integration with Game Systems

```
┌─────────────────────────────────────────────────────────────┐
│                        Game State                           │
└────────┬────────────────────────────────────────────────────┘
         │
         ├─── Manages ──────────────────────────────────────┐
         │                                                   │
         ▼                                                   ▼
┌──────────────────┐                            ┌──────────────────┐
│ PuzzleManager    │                            │ ComplexityManager│
│                  │                            │                  │
│ • register()     │                            │ • set_level()    │
│ • get_current()  │                            │ • get_config()   │
└────────┬─────────┘                            └────────┬─────────┘
         │                                                │
         │                                                │
         ▼                                                ▼
┌─────────────────────────────────────────────────────────────┐
│                   MemoryStackPuzzle                         │
└────────┬────────────────────────────────────────────────────┘
         │
         ├─── Uses ─────────────────────────────────────────┐
         │                                                   │
         ▼                                                   ▼
┌──────────────────┐                            ┌──────────────────┐
│ HintSystem       │                            │ StoryEngine      │
│                  │                            │                  │
│ • get_hint()     │                            │ • progress()     │
│ • track_usage()  │                            │ • narrate()      │
└──────────────────┘                            └──────────────────┘
```

---

**Legend:**
- `┌─┐` Boxes represent components or processes
- `│` Vertical lines show flow or relationships
- `▼` Arrows indicate direction of flow
- `├─┤` Branches show decision points or parallel paths
