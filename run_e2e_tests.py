#!/usr/bin/env python3
"""
E2E Test Runner for Logic Quest

Simple script to run end-to-end tests with proper setup and teardown.
"""

import subprocess
import sys
import time
import requests
import signal
import os


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import playwright
        import pytest
        print("✅ Dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: uv sync")
        return False


def install_playwright_browsers():
    """Install Playwright browsers."""
    print("🎭 Installing Playwright browsers...")
    try:
        result = subprocess.run(
            ["uv", "run", "playwright", "install", "--with-deps"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Playwright browsers installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        return False


def start_reflex_server():
    """Start the Reflex development server."""
    print("🚀 Starting Reflex server...")
    
    # Start server in background
    process = subprocess.Popen(
        ["uv", "run", "reflex", "run", "--port", "3001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid if os.name != 'nt' else None
    )
    
    # Wait for server to be ready
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:3001", timeout=1)
            if response.status_code == 200:
                print("✅ Reflex server is ready")
                return process
        except requests.exceptions.RequestException:
            if attempt < max_attempts - 1:
                time.sleep(1)
            else:
                print("❌ Reflex server failed to start")
                process.terminate()
                return None
    
    return process


def run_e2e_tests(headed=False):
    """Run the E2E tests."""
    print("🧪 Running E2E tests...")
    
    cmd = ["uv", "run", "pytest", "tests/e2e/", "-v"]
    if headed:
        cmd.append("--headed")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ E2E tests passed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ E2E tests failed!")
        return False


def cleanup_server(process):
    """Clean up the Reflex server process."""
    if process:
        print("🧹 Cleaning up server...")
        if os.name == 'nt':
            process.terminate()
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait()
        print("✅ Server cleaned up")


def main():
    """Main function to run E2E tests."""
    print("🎮 Logic Quest E2E Test Runner")
    print("=" * 40)
    
    # Check if --headed flag is provided
    headed = "--headed" in sys.argv or "--ui" in sys.argv
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        sys.exit(1)
    
    # Start Reflex server
    server_process = start_reflex_server()
    if not server_process:
        sys.exit(1)
    
    try:
        # Run E2E tests
        success = run_e2e_tests(headed=headed)
        
        if success:
            print("\n🎉 All E2E tests completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 E2E tests failed!")
            sys.exit(1)
            
    finally:
        # Always cleanup
        cleanup_server(server_process)


if __name__ == "__main__":
    main()