"""
Playwright E2E Test Configuration

Configuration and fixtures for end-to-end testing of Logic Quest.
"""

import pytest
import subprocess
import time
import requests
from playwright.sync_api import Playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def reflex_server():
    """Start the Reflex development server for testing."""
    # Start the Reflex server
    process = subprocess.Popen(
        ["uv", "run", "reflex", "run", "--port", "3001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait for server to start
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            response = requests.get("http://localhost:3001", timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
    else:
        process.terminate()
        raise RuntimeError("Reflex server failed to start")
    
    yield "http://localhost:3001"
    
    # Cleanup
    process.terminate()
    process.wait()


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    """Create a browser instance for testing."""
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> BrowserContext:
    """Create a browser context for each test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        # Enable console logging for debugging
        record_video_dir="test-results/videos" if False else None,
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Create a page for each test."""
    page = context.new_page()
    
    # Enable console logging for debugging
    page.on("console", lambda msg: print(f"Console: {msg.text}"))
    page.on("pageerror", lambda error: print(f"Page error: {error}"))
    
    yield page


@pytest.fixture
def logic_quest_page(page: Page, reflex_server: str) -> Page:
    """Navigate to Logic Quest and return the page."""
    page.goto(reflex_server)
    
    # Wait for the page to load
    page.wait_for_selector("text=LOGIC QUEST", timeout=10000)
    
    return page