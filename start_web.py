#!/usr/bin/env python3
"""
Quick startup script for the Generative Map Art web application
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'flask_cors', 'playwright']
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing dependencies detected!")
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("\nTo install missing dependencies, run:")
        print("pip install -r requirements.txt")
        print("playwright install chromium")
        return False
    
    return True

def check_playwright():
    """Check if Playwright browser is installed"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to launch browser to check if it's installed
            browser = p.chromium.launch(headless=True)
            browser.close()
        return True
    except Exception:
        print("❌ Playwright browser not installed!")
        print("To install Playwright browser, run:")
        print("playwright install chromium")
        return False

def main():
    print("🎨 Generative Map Art - Web Application Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found!")
        print("Please run this script from the gen_maps directory")
        sys.exit(1)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ Dependencies OK")
    
    # Check Playwright
    print("🔍 Checking Playwright browser...")
    if not check_playwright():
        sys.exit(1)
    
    print("✅ Playwright browser OK")
    
    # Start the Flask app
    print("\n🚀 Starting web server...")
    print("📍 URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()