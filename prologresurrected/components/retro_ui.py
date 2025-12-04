"""Retro UI components for Logic Quest cyberpunk interface."""

import reflex as rx


def retro_container(*children, **props) -> rx.Component:
    """Container with retro cyberpunk styling."""
    return rx.box(
        *children,
        style={
            "background": "linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)",
            "border": "2px solid #00ff00",
            "border_radius": "8px",
            "box_shadow": "0 0 20px rgba(0, 255, 0, 0.3), inset 0 0 20px rgba(0, 255, 0, 0.1)",
            "padding": "2rem",
            **props.get("style", {}),
        },
        **{k: v for k, v in props.items() if k != "style"},
    )


def neon_text(
    text, 
    color = "neon_green", 
    size: str = "md", 
    glow: bool = False
) -> rx.Component:
    """Text with neon cyberpunk styling.
    
    Args:
        text: Text content (can be string or reactive value)
        color: Color name or reactive value (neon_green, neon_cyan, neon_yellow, neon_red, neon_pink)
        size: Font size (sm, md, lg, xl)
        glow: Whether to add glow effect
    """
    # Map color names to hex codes using rx.cond for reactive values
    def get_color_code(color_name):
        return rx.cond(
            color_name == "neon_green", "#00ff00",
            rx.cond(
                color_name == "neon_cyan", "#00ffff",
                rx.cond(
                    color_name == "neon_yellow", "#ffff00",
                    rx.cond(
                        color_name == "neon_red", "#ff0040",
                        rx.cond(
                            color_name == "neon_pink", "#ff00ff",
                            "#00ff00"  # default
                        )
                    )
                )
            )
        )
    
    sizes = {
        "sm": "14px",
        "md": "18px", 
        "lg": "24px",
        "xl": "32px",
    }
    
    # Handle both static and reactive color values
    if isinstance(color, str):
        colors = {
            "neon_green": "#00ff00",
            "neon_cyan": "#00ffff", 
            "neon_yellow": "#ffff00",
            "neon_red": "#ff0040",
            "neon_pink": "#ff00ff",
        }
        color_code = colors.get(color, colors["neon_green"])
    else:
        # Reactive value - use conditional
        color_code = get_color_code(color)
    
    font_size = sizes.get(size, sizes["md"])
    
    base_style = {
        "color": color_code,
        "font_family": "monospace",
        "font_size": font_size,
        "font_weight": "bold",
        "text_transform": "uppercase",
    }
    
    # Handle glow - use rx.cond for reactive values
    if isinstance(glow, bool):
        # Static boolean
        if glow:
            base_style["text_shadow"] = f"0 0 10px {color_code}, 0 0 20px {color_code}, 0 0 30px {color_code}"
        return rx.text(text, style=base_style)
    else:
        # Reactive value - use rx.cond to conditionally apply text_shadow
        base_style["text_shadow"] = rx.cond(
            glow,
            f"0 0 10px {color_code}, 0 0 20px {color_code}, 0 0 30px {color_code}",
            "none"
        )
        return rx.text(text, style=base_style)


def cyberpunk_button(
    text: str, 
    on_click=None, 
    color: str = "neon_green",
    **props
) -> rx.Component:
    """Button with cyberpunk styling."""
    colors = {
        "neon_green": "#00ff00",
        "neon_cyan": "#00ffff",
        "neon_yellow": "#ffff00", 
        "neon_red": "#ff0040",
    }
    
    color_code = colors.get(color, colors["neon_green"])
    
    return rx.button(
        text,
        on_click=on_click,
        style={
            "background": "transparent",
            "border": f"2px solid {color_code}",
            "color": color_code,
            "font_family": "monospace",
            "font_weight": "bold",
            "text_transform": "uppercase",
            "padding": "12px 24px",
            "cursor": "pointer",
            "transition": "all 0.3s ease",
            "box_shadow": f"0 0 10px rgba({color_code[1:3]}, {color_code[3:5]}, {color_code[5:7]}, 0.3)",
            "_hover": {
                "background": color_code,
                "color": "#000000",
                "box_shadow": f"0 0 20px {color_code}",
            },
        },
        **props,
    )


def ascii_art_display(art: str, color: str = "neon_green") -> rx.Component:
    """Display ASCII art with cyberpunk styling."""
    colors = {
        "neon_green": "#00ff00",
        "neon_cyan": "#00ffff",
        "neon_yellow": "#ffff00",
        "neon_red": "#ff0040",
    }
    
    color_code = colors.get(color, colors["neon_green"])
    
    return rx.text(
        art,
        style={
            "font_family": "monospace",
            "color": color_code,
            "white_space": "pre",
            "font_size": "12px",
            "line_height": "1.2",
            "text_shadow": f"0 0 5px {color_code}",
        },
    )


def explanation_panel(text: str, color: str = "neon_green", title: str = "SYSTEM INFO") -> rx.Component:
    """Display explanation text in a right-side panel with retro styling."""
    colors = {
        "neon_green": "#00ff00",
        "neon_cyan": "#00ffff",
        "neon_yellow": "#ffff00",
        "neon_red": "#ff0040",
        "neon_pink": "#ff00ff",
    }
    
    color_code = colors.get(color, colors["neon_green"])
    
    return rx.box(
        # Panel header
        rx.box(
            neon_text(title, color=color, size="sm"),
            style={
                "background": "#1a1a2e",
                "border_bottom": f"1px solid {color_code}",
                "padding": "8px 16px",
                "height": "40px",
            },
        ),
        # Panel content
        rx.box(
            rx.text(
                text,
                style={
                    "font_family": "monospace",
                    "color": color_code,
                    "font_size": "13px",
                    "line_height": "1.4",
                    "text_align": "left",
                    "white_space": "pre-wrap",
                },
            ),
            style={
                "padding": "1rem",
                "height": "calc(100% - 40px)",
                "overflow_y": "auto",
                "background": "rgba(0, 0, 0, 0.8)",
            },
        ),
        style={
            "border": f"2px solid {color_code}",
            "border_radius": "8px",
            "box_shadow": f"0 0 15px rgba({int(color_code[1:3], 16)}, {int(color_code[3:5], 16)}, {int(color_code[5:7], 16)}, 0.3)",
            "background": "#000000",
            "height": "100%",
            "width": "100%",
        },
    )


def complexity_level_card(
    level_name: str,
    description: str,
    icon: str,
    color: str,
    multiplier: float,
    hint_frequency: str,
    explanation_depth: str,
    on_click=None,
    selected: bool = False
) -> rx.Component:
    """Cyberpunk-styled complexity level selection card."""
    colors = {
        "neon_green": "#00ff00",
        "cyan": "#00ffff",
        "yellow": "#ffff00",
        "red": "#ff0040",
        "neon_cyan": "#00ffff",
        "neon_yellow": "#ffff00",
        "neon_red": "#ff0040",
    }
    
    color_code = colors.get(color, colors["neon_green"])
    
    # Enhanced styling for selected state - use rx.cond for reactive values
    border_style = rx.cond(
        selected,
        f"3px solid {color_code}",
        f"2px solid {color_code}"
    )
    box_shadow = rx.cond(
        selected,
        f"0 0 25px {color_code}, inset 0 0 15px rgba({int(color_code[1:3], 16)}, {int(color_code[3:5], 16)}, {int(color_code[5:7], 16)}, 0.2)",
        f"0 0 15px rgba({int(color_code[1:3], 16)}, {int(color_code[3:5], 16)}, {int(color_code[5:7], 16)}, 0.3)"
    )
    
    return rx.box(
        rx.vstack(
            # Header with icon and level name
            rx.hstack(
                rx.text(
                    icon,
                    style={
                        "font_size": "24px",
                        "margin_right": "8px",
                    }
                ),
                neon_text(level_name, color=color, size="lg", glow=selected),
                spacing="2",
                align="center",
            ),
            
            # Description
            rx.text(
                description,
                style={
                    "color": color_code,
                    "font_family": "monospace",
                    "font_size": "14px",
                    "line_height": "1.4",
                    "text_align": "center",
                    "margin": "12px 0",
                    "opacity": "0.9",
                }
            ),
            
            # Stats grid
            rx.vstack(
                rx.hstack(
                    rx.text("SCORING:", style={"color": "#888", "font_family": "monospace", "font_size": "12px", "font_weight": "bold"}),
                    rx.text(f"{multiplier}x", style={"color": color_code, "font_family": "monospace", "font_size": "12px", "font_weight": "bold"}),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("HINTS:", style={"color": "#888", "font_family": "monospace", "font_size": "12px", "font_weight": "bold"}),
                    rx.text(hint_frequency.upper(), style={"color": color_code, "font_family": "monospace", "font_size": "12px", "font_weight": "bold"}),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("GUIDANCE:", style={"color": "#888", "font_family": "monospace", "font_size": "12px", "font_weight": "bold"}),
                    rx.text(explanation_depth.upper(), style={"color": color_code, "font_family": "monospace", "font_size": "12px", "font_weight": "bold"}),
                    justify="between",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            
            spacing="3",
            align="center",
            width="100%",
        ),
        on_click=on_click,
        style={
            "background": "linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%)",
            "border": border_style,
            "border_radius": "12px",
            "box_shadow": box_shadow,
            "padding": "20px",
            "cursor": "pointer",
            "transition": "all 0.3s ease",
            "min_height": "200px",
            "width": "280px",
            "display": "flex",
            "flex_direction": "column",
            "justify_content": "center",
            "_hover": {
                "transform": "translateY(-5px)",
                "box_shadow": f"0 0 30px {color_code}",
            },
        },
    )


def complexity_selection_screen(
    current_level,
    on_level_select,
    on_continue,
    show_continue: bool = True
) -> rx.Component:
    """Complete complexity level selection screen with cyberpunk styling and recommendations."""
    return rx.center(
        retro_container(
            rx.vstack(
                # Title
                neon_text("SELECT COMPLEXITY LEVEL", color="neon_cyan", size="xl", glow=True),
                rx.text(
                    "Choose your preferred difficulty level for the Logic Quest adventure",
                    style={
                        "color": "#00ffff",
                        "font_family": "monospace",
                        "font_size": "16px",
                        "text_align": "center",
                        "margin": "10px 0 20px 0",
                        "opacity": "0.8",
                    }
                ),
                
                # Recommendation box for new players
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("💡", style={"font_size": "18px"}),
                            neon_text("Recommendation for New Players", color="neon_yellow", size="md"),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "If you're new to Prolog or logic programming, we recommend starting with BEGINNER level. "
                            "It provides maximum guidance and step-by-step explanations to help you build a strong foundation.",
                            style={
                                "color": "#ffff00",
                                "font_family": "monospace",
                                "font_size": "13px",
                                "text_align": "center",
                                "margin_top": "8px",
                                "line_height": "1.5",
                                "opacity": "0.9",
                            }
                        ),
                        rx.text(
                            "You can change the complexity level at any time during gameplay!",
                            style={
                                "color": "#00ff00",
                                "font_family": "monospace",
                                "font_size": "12px",
                                "text_align": "center",
                                "margin_top": "8px",
                                "font_style": "italic",
                                "opacity": "0.8",
                            }
                        ),
                        spacing="2",
                        align="center",
                    ),
                    style={
                        "border": "2px solid #ffff00",
                        "border_radius": "8px",
                        "padding": "16px 20px",
                        "margin": "10px 0 20px 0",
                        "background": "rgba(255, 255, 0, 0.1)",
                        "box_shadow": "0 0 15px rgba(255, 255, 0, 0.3)",
                    },
                ),
                
                # Complexity level cards grid
                rx.grid(
                    complexity_level_card(
                        level_name="BEGINNER",
                        description="Perfect for newcomers to Prolog. Maximum guidance with step-by-step explanations and simple problems.",
                        icon="🌱",
                        color="neon_green",
                        multiplier=1.0,
                        hint_frequency="always",
                        explanation_depth="detailed",
                        on_click=lambda: on_level_select("BEGINNER"),
                        selected=(current_level == "BEGINNER"),
                    ),
                    complexity_level_card(
                        level_name="INTERMEDIATE",
                        description="For those with some programming experience. Moderate guidance with standard complexity problems.",
                        icon="⚡",
                        color="cyan",
                        multiplier=1.2,
                        hint_frequency="on request",
                        explanation_depth="moderate",
                        on_click=lambda: on_level_select("INTERMEDIATE"),
                        selected=(current_level == "INTERMEDIATE"),
                    ),
                    complexity_level_card(
                        level_name="ADVANCED",
                        description="For experienced programmers. Minimal guidance with complex problems and multiple solution paths.",
                        icon="🔥",
                        color="yellow",
                        multiplier=1.5,
                        hint_frequency="after attempts",
                        explanation_depth="brief",
                        on_click=lambda: on_level_select("ADVANCED"),
                        selected=(current_level == "ADVANCED"),
                    ),
                    complexity_level_card(
                        level_name="EXPERT",
                        description="For Prolog masters. No guidance with optimization challenges and edge cases.",
                        icon="💀",
                        color="red",
                        multiplier=2.0,
                        hint_frequency="none",
                        explanation_depth="minimal",
                        on_click=lambda: on_level_select("EXPERT"),
                        selected=(current_level == "EXPERT"),
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                    justify="center",
                ),
                
                # Preview information box
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("ℹ️", style={"font_size": "16px"}),
                            neon_text("What Each Level Means", color="neon_cyan", size="sm"),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "• BEGINNER: Detailed explanations, templates provided, unlimited hints\n"
                            "• INTERMEDIATE: Moderate explanations, hints on request, standard puzzles\n"
                            "• ADVANCED: Brief explanations, hints after attempts, complex puzzles\n"
                            "• EXPERT: Minimal explanations, no hints, optimization challenges",
                            style={
                                "color": "#00ffff",
                                "font_family": "monospace",
                                "font_size": "12px",
                                "text_align": "left",
                                "margin_top": "8px",
                                "line_height": "1.6",
                                "opacity": "0.8",
                                "white_space": "pre-line",
                            }
                        ),
                        spacing="2",
                        align="start",
                    ),
                    style={
                        "border": "1px solid #00ffff",
                        "border_radius": "6px",
                        "padding": "12px 16px",
                        "margin": "20px 0 10px 0",
                        "background": "rgba(0, 255, 255, 0.05)",
                    },
                ),
                
                # Continue button (conditional)
                rx.cond(
                    show_continue,
                    rx.vstack(
                        rx.text(
                            f"Current Selection: {current_level}",
                            style={
                                "color": "#00ff00",
                                "font_family": "monospace",
                                "font_size": "16px",
                                "font_weight": "bold",
                                "text_align": "center",
                                "margin": "10px 0 10px 0",
                            }
                        ),
                        cyberpunk_button(
                            "Continue with Selected Level",
                            on_click=on_continue,
                            color="neon_green",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.box(),  # Empty box when continue button is hidden
                ),
                
                spacing="4",
                align="center",
                width="100%",
            ),
            style={"max_width": "950px", "width": "100%", "padding": "20px"},
        ),
        width="100%",
        height="100vh",
        style={"overflow_y": "auto"},
    )


def complexity_indicator_badge(
    icon: str,
    level_name: str,
    color: str = "neon_green"
) -> rx.Component:
    """Display a compact complexity level indicator badge."""
    colors = {
        "neon_green": "#00ff00",
        "cyan": "#00ffff",
        "yellow": "#ffff00",
        "red": "#ff0040",
        "neon_cyan": "#00ffff",
        "neon_yellow": "#ffff00",
        "neon_red": "#ff0040",
    }
    
    color_code = colors.get(color, colors["neon_green"])
    
    return rx.box(
        rx.hstack(
            rx.text(
                icon,
                style={
                    "font_size": "14px",
                    "margin_right": "4px",
                }
            ),
            rx.text(
                level_name,
                style={
                    "color": color_code,
                    "font_family": "monospace",
                    "font_size": "12px",
                    "font_weight": "bold",
                    "text_transform": "uppercase",
                    "text_shadow": f"0 0 5px {color_code}",
                }
            ),
            spacing="1",
            align="center",
        ),
        style={
            "background": "rgba(0, 0, 0, 0.6)",
            "border": f"1px solid {color_code}",
            "border_radius": "4px",
            "padding": "4px 8px",
            "box_shadow": f"0 0 8px rgba({int(color_code[1:3], 16)}, {int(color_code[3:5], 16)}, {int(color_code[5:7], 16)}, 0.4)",
        }
    )


def terminal_window(*children, title: str = "TERMINAL", complexity_indicator=None, **props) -> rx.Component:
    """Terminal window with retro styling and optional complexity indicator."""
    return rx.box(
        # Title bar
        rx.box(
            rx.hstack(
                neon_text(title, color="neon_cyan", size="sm"),
                rx.spacer(),
                # Complexity indicator (if provided)
                rx.cond(
                    complexity_indicator is not None,
                    complexity_indicator,
                    rx.box(),  # Empty box when no indicator
                ),
                rx.spacer(),
                rx.hstack(
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px", 
                            "border_radius": "50%",
                            "background": "#ff0040",
                        }
                    ),
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px",
                            "border_radius": "50%", 
                            "background": "#ffff00",
                        }
                    ),
                    rx.box(
                        style={
                            "width": "12px",
                            "height": "12px",
                            "border_radius": "50%",
                            "background": "#00ff00",
                        }
                    ),
                    spacing="2",
                ),
                width="100%",
                align="center",
            ),
            style={
                "background": "#1a1a2e",
                "border_bottom": "1px solid #00ff00",
                "padding": "8px 16px",
                "height": "40px",  # Fixed title bar height
            },
        ),
        # Content
        rx.vstack(
            *children,
            style={
                "background": "#000000",
                "height": "100%",  # Take full available height
                "flex": "1",
            },
            spacing="0",
        ),
        style={
            "border": "2px solid #00ff00",
            "border_radius": "8px",
            "box_shadow": "0 0 20px rgba(0, 255, 0, 0.3)",
            "overflow": "hidden",
            "display": "flex",
            "flex_direction": "column",
            "height": "100%",  # Take full available height
            "width": "100%",   # Take full available width
            **props.get("style", {}),
        },
        **{k: v for k, v in props.items() if k != "style"},
    )