"""Reflex configuration for Logic Quest."""

import reflex as rx

config = rx.Config(
    app_name="prologresurrected",
    db_url="sqlite:///reflex.db",
    env=rx.Env.PROD,
    # Custom domain configuration
    # Replace with your actual domain (e.g., "logicquest.com" or "yourdomain.com")
    frontend_url="https://logicquest.pro",
    backend_url="https://logicquest.pro",
)