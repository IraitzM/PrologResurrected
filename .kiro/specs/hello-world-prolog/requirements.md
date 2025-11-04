# Requirements Document

## Introduction

The Hello World Prolog Challenge is an entry-level tutorial that introduces players to the absolute fundamentals of Prolog programming through an engaging, story-driven experience. This challenge serves as a gentle introduction before the main Logic Quest adventure, teaching players the basic syntax and concepts they'll need to succeed in the full game.

## Requirements

### Requirement 1

**User Story:** As a new player with no Prolog experience, I want to learn what Prolog is and how it differs from other programming languages, so that I understand the context for what I'm about to learn.

#### Acceptance Criteria

1. WHEN the player starts the hello world challenge THEN the system SHALL display an engaging introduction explaining Prolog as a logic programming language
2. WHEN the introduction is shown THEN the system SHALL explain that Prolog works with facts, rules, and queries in simple terms
3. WHEN the explanation is complete THEN the system SHALL use the 80s cyberpunk theme to make the learning context immersive
4. WHEN the introduction concludes THEN the system SHALL require the user to type a specific command (not just "next") to demonstrate engagement and proceed to the next section

### Requirement 2

**User Story:** As a beginner, I want to see and understand my first Prolog fact, so that I can grasp the basic building block of Prolog programming.

#### Acceptance Criteria

1. WHEN the player is introduced to facts THEN the system SHALL show a simple, relatable example like "likes(alice, chocolate)."
2. WHEN a fact is displayed THEN the system SHALL explain the syntax: predicate(argument1, argument2)
3. WHEN the syntax is explained THEN the system SHALL clarify that facts end with a period and represent unconditional truths
4. WHEN the explanation is complete THEN the system SHALL require the player to actively identify components of a given fact by typing their specific answers (e.g., "What is the predicate in this fact?")
5. WHEN the player provides their identification THEN the system SHALL validate the response and block progression until correct understanding is demonstrated
6. WHEN the player provides incorrect answers THEN the system SHALL provide specific hints and allow retry until correct

### Requirement 3

**User Story:** As a learner, I want to create my first Prolog fact, so that I can practice the syntax and feel accomplished.

#### Acceptance Criteria

1. WHEN the player understands fact syntax THEN the system SHALL prompt them to write their own fact with a specific scenario (e.g., "Write a fact that says Bob likes pizza")
2. WHEN the player is prompted THEN the system SHALL require them to type the complete fact, not just press "next"
3. WHEN the player enters their answer THEN the system SHALL validate both syntax (proper format, period, parentheses) and semantic content (correct predicate and arguments)
4. WHEN the answer is correct THEN the system SHALL provide positive feedback and explain why it's correct
5. WHEN the answer is incorrect THEN the system SHALL provide specific syntax hints and block progression until a valid fact is entered
6. WHEN the player struggles THEN the system SHALL offer increasingly specific hints but still require them to type the correct answer

### Requirement 4

**User Story:** As a new Prolog programmer, I want to understand how to ask questions (queries) about facts, so that I can see how Prolog finds answers.

#### Acceptance Criteria

1. WHEN the player has mastered facts THEN the system SHALL introduce the concept of queries with the "?-" prefix syntax
2. WHEN queries are introduced THEN the system SHALL demonstrate with a simple example like "?- likes(alice, chocolate)."
3. WHEN the example is shown THEN the system SHALL explain that Prolog responds with "yes" or "no"
4. WHEN the concept is explained THEN the system SHALL require the player to write a specific query (e.g., "Write a query to ask if Alice likes chocolate")
5. WHEN the player submits their query THEN the system SHALL validate both the "?-" prefix and proper syntax
6. WHEN the query is incorrect THEN the system SHALL provide specific feedback about missing prefix, syntax errors, or format issues and block progression until correct
7. WHEN the query is correct THEN the system SHALL show what Prolog's response would be and explain the reasoning

### Requirement 5

**User Story:** As a beginner, I want to understand variables in Prolog queries, so that I can ask more interesting questions.

#### Acceptance Criteria

1. WHEN the player understands basic queries THEN the system SHALL introduce variables using uppercase letters with examples like "?- likes(alice, X)."
2. WHEN variables are introduced THEN the system SHALL explain that X can match any value and demonstrate how Prolog finds all possible solutions
3. WHEN variables are explained THEN the system SHALL require the player to write a specific variable query (e.g., "Write a query to find what Alice likes using a variable")
4. WHEN the player submits their variable query THEN the system SHALL validate that variables use uppercase letters and proper query syntax
5. WHEN the variable query is incorrect THEN the system SHALL provide specific feedback about variable naming (uppercase), syntax, or format and block progression
6. WHEN the variable query is correct THEN the system SHALL demonstrate what solutions Prolog would find and explain the matching process
7. WHEN the player uses lowercase for variables THEN the system SHALL specifically explain that variables must start with uppercase letters

### Requirement 6

**User Story:** As a player completing the hello world challenge, I want to feel accomplished and ready for the main game, so that I'm motivated to continue learning.

#### Acceptance Criteria

1. WHEN all concepts are mastered THEN the system SHALL provide a congratulatory message
2. WHEN congratulations are shown THEN the system SHALL summarize what the player has learned
3. WHEN the summary is complete THEN the system SHALL connect the concepts to the main Logic Quest adventure
4. WHEN the connection is made THEN the system SHALL offer to start the main game or review concepts again
5. WHEN the challenge ends THEN the system SHALL track completion for progress purposes

### Requirement 7

**User Story:** As a player who makes mistakes, I want helpful feedback and encouragement, so that I don't get frustrated and quit.

#### Acceptance Criteria

1. WHEN the player makes a syntax error THEN the system SHALL provide specific, helpful error messages
2. WHEN an error is shown THEN the system SHALL highlight what went wrong and how to fix it
3. WHEN multiple attempts are made THEN the system SHALL provide increasingly specific hints
4. WHEN the player seems stuck THEN the system SHALL offer to show the correct answer with explanation
5. WHEN help is provided THEN the system SHALL maintain an encouraging, supportive tone

### Requirement 8

**User Story:** As a visual learner, I want the hello world challenge to use the same engaging retro terminal interface as the main game, so that the experience is consistent and immersive.

#### Acceptance Criteria

1. WHEN the challenge runs THEN the system SHALL use the same 80s cyberpunk styling as the main game
2. WHEN text is displayed THEN the system SHALL use appropriate colors (green for success, red for errors, cyan for information)
3. WHEN concepts are explained THEN the system SHALL use bordered boxes for important information
4. WHEN the player progresses THEN the system SHALL use visual feedback like progress indicators
5. WHEN examples are shown THEN the system SHALL clearly distinguish between user input and system output

### Requirement 9

**User Story:** As a learner who wants to truly understand Prolog, I want the tutorial to require active participation rather than passive reading, so that I actually learn the concepts instead of just clicking through.

#### Acceptance Criteria

1. WHEN the tutorial is running THEN the system SHALL NOT allow progression by simply typing "next" or "continue"
2. WHEN each concept is taught THEN the system SHALL require specific user input that demonstrates understanding of that concept
3. WHEN the user tries to skip exercises THEN the system SHALL block progression and explain that active participation is required
4. WHEN the user provides incorrect input THEN the system SHALL provide hints but still require correct input before proceeding
5. WHEN the user completes an exercise correctly THEN the system SHALL provide positive feedback and then move to the next concept
6. WHEN the tutorial is complete THEN the system SHALL ensure the user has actively practiced facts, queries, and variables through hands-on exercises