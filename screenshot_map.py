#!/usr/bin/env python3
"""
Simple script to take a screenshot of the generated map
"""

import os
import time
from playwright.sync_api import sync_playwright

def screenshot_map(html_file="improved_map.html", output_file="improved_map_screenshot.png"):
    """
    Take a screenshot of the generated map
    """
    if not os.path.exists(html_file):
        print(f"Error: {html_file} not found!")
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Load the map
        map_path = os.path.abspath(html_file)
        page.goto(f"file://{map_path}")
        
        # Wait for the map to load completely
        page.wait_for_load_state("networkidle")
        time.sleep(3)  # Extra time to ensure complete loading
        
        # Set viewport and take screenshot
        page.set_viewport_size({"width": 1200, "height": 800})
        page.screenshot(path=output_file)
        
        print(f"Screenshot saved: {output_file}")
        
        browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
        screenshot_map(html_file, output_file)
    else:
        screenshot_map()