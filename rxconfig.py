"""Reflex configuration for Logic Quest."""

import reflex as rx

config = rx.Config(
    app_name="prologresurrected",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)