"""
Demonstration of the Complexity Help System

This script demonstrates the various help features available in the
complexity level system. Run this to see examples of all help commands.
"""

from prologresurrected.game.complexity import ComplexityLevel, ComplexityManager
from prologresurrected.game.complexity_help import ComplexityHelpSystem, format_help_for_terminal


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_overview(help_system: ComplexityHelpSystem):
    """Demonstrate the complexity overview."""
    print_section("COMPLEXITY OVERVIEW")
    overview = help_system.get_complexity_overview()
    print(overview)


def demo_comparison(help_system: ComplexityHelpSystem):
    """Demonstrate the complexity comparison."""
    print_section("COMPLEXITY COMPARISON")
    comparison = help_system.get_complexity_comparison()
    print(comparison)


def demo_tips(help_system: ComplexityHelpSystem):
    """Demonstrate the complexity tips."""
    print_section("COMPLEXITY TIPS")
    tips = help_system.get_complexity_tips()
    print(tips)


def demo_level_specific_help(help_system: ComplexityHelpSystem):
    """Demonstrate level-specific help."""
    print_section("LEVEL-SPECIFIC HELP: BEGINNER")
    beginner_help = help_system.get_level_specific_help(ComplexityLevel.BEGINNER)
    print(beginner_help)


def demo_contextual_help(help_system: ComplexityHelpSystem):
    """Demonstrate contextual help."""
    print_section("CONTEXTUAL HELP: PUZZLE CONTEXT")
    contextual = help_system.get_contextual_help(ComplexityLevel.INTERMEDIATE, "puzzle")
    print(contextual)


def demo_quick_reference(help_system: ComplexityHelpSystem):
    """Demonstrate quick reference cards."""
    print_section("QUICK REFERENCE: ADVANCED LEVEL")
    quick_ref = help_system.get_quick_reference(ComplexityLevel.ADVANCED)
    print(quick_ref)


def demo_faq(help_system: ComplexityHelpSystem):
    """Demonstrate FAQ."""
    print_section("FREQUENTLY ASKED QUESTIONS")
    faq = help_system.get_faq()
    print(faq)


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("  COMPLEXITY HELP SYSTEM DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo shows all the help features available in Logic Quest.")
    print("In the game, players can access these with commands like:")
    print("  - 'complexity help'")
    print("  - 'complexity compare'")
    print("  - 'complexity tips'")
    print("  - 'complexity help <level>'")
    print("  - 'complexity faq'")
    
    # Initialize the help system
    manager = ComplexityManager()
    help_system = ComplexityHelpSystem(manager)
    
    # Run demonstrations
    demo_overview(help_system)
    input("\nPress Enter to continue...")
    
    demo_comparison(help_system)
    input("\nPress Enter to continue...")
    
    demo_tips(help_system)
    input("\nPress Enter to continue...")
    
    demo_level_specific_help(help_system)
    input("\nPress Enter to continue...")
    
    demo_contextual_help(help_system)
    input("\nPress Enter to continue...")
    
    demo_quick_reference(help_system)
    input("\nPress Enter to continue...")
    
    demo_faq(help_system)
    
    print("\n" + "=" * 70)
    print("  END OF DEMONSTRATION")
    print("=" * 70)
    print("\nAll help features are fully integrated into Logic Quest!")
    print("Players can access them anytime during gameplay.\n")


if __name__ == "__main__":
    main()
