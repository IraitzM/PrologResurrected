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
    text: str, 
    color: str = "neon_green", 
    size: str = "md", 
    glow: bool = False
) -> rx.Component:
    """Text with neon cyberpunk styling."""
    colors = {
        "neon_green": "#00ff00",
        "neon_cyan": "#00ffff", 
        "neon_yellow": "#ffff00",
        "neon_red": "#ff0040",
        "neon_pink": "#ff00ff",
    }
    
    sizes = {
        "sm": "14px",
        "md": "18px", 
        "lg": "24px",
        "xl": "32px",
    }
    
    color_code = colors.get(color, colors["neon_green"])
    font_size = sizes.get(size, sizes["md"])
    
    style = {
        "color": color_code,
        "font_family": "monospace",
        "font_size": font_size,
        "font_weight": "bold",
        "text_transform": "uppercase",
    }
    
    if glow:
        style["text_shadow"] = f"0 0 10px {color_code}, 0 0 20px {color_code}, 0 0 30px {color_code}"
    
    return rx.text(text, style=style)


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


def terminal_window(*children, title: str = "TERMINAL", **props) -> rx.Component:
    """Terminal window with retro styling."""
    return rx.box(
        # Title bar
        rx.box(
            rx.hstack(
                neon_text(title, color="neon_cyan", size="sm"),
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