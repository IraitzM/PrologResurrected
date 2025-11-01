"""
Playwright Configuration for Logic Quest E2E Tests

Configuration for end-to-end testing of the Logic Quest Reflex application.
"""

import pytest


def pytest_configure(config):
    """Configure pytest for Playwright tests."""
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test"
    )


def pytest_collection_modifyitems(config, items):
    """Add e2e marker to all tests in e2e directory."""
    for item in items:
        if "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


# Playwright configuration
PLAYWRIGHT_CONFIG = {
    "testDir": "tests/e2e",
    "timeout": 30000,  # 30 seconds per test
    "expect": {
        "timeout": 5000,  # 5 seconds for assertions
    },
    "fullyParallel": True,
    "forbidOnly": True,  # Fail if test.only is left in code
    "retries": 2,  # Retry failed tests
    "workers": 4,  # Number of parallel workers
    "reporter": [
        ["html", {"outputFolder": "test-results/html-report"}],
        ["junit", {"outputFile": "test-results/junit.xml"}],
        ["list"],
    ],
    "use": {
        "baseURL": "http://localhost:3001",
        "trace": "on-first-retry",  # Collect trace on first retry
        "screenshot": "only-on-failure",
        "video": "retain-on-failure",
    },
    "projects": [
        {
            "name": "chromium",
            "use": {
                "browserName": "chromium",
                "viewport": {"width": 1280, "height": 720},
                "ignoreHTTPSErrors": True,
            },
        },
        {
            "name": "firefox",
            "use": {
                "browserName": "firefox",
                "viewport": {"width": 1280, "height": 720},
                "ignoreHTTPSErrors": True,
            },
        },
        {
            "name": "webkit",
            "use": {
                "browserName": "webkit",
                "viewport": {"width": 1280, "height": 720},
                "ignoreHTTPSErrors": True,
            },
        },
        {
            "name": "mobile-chrome",
            "use": {
                "browserName": "chromium",
                "viewport": {"width": 375, "height": 667},
                "deviceScaleFactor": 2,
                "isMobile": True,
                "hasTouch": True,
            },
        },
    ],
    "webServer": {
        "command": "uv run reflex run --port 3001",
        "port": 3001,
        "timeout": 120000,  # 2 minutes to start server
        "reuseExistingServer": True,
    },
}