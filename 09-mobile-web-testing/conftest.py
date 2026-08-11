"""
Mobile Web Testing - Playwright Device Emulation
No physical devices needed - uses Playwright's built-in device profiles.
"""

import pytest
from playwright.sync_api import sync_playwright


# Device configurations
DEVICES = {
    "iphone_13": {
        "name": "iPhone 13",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 390, "height": 844},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
    "iphone_14_pro": {
        "name": "iPhone 14 Pro",
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 393, "height": 852},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
    "pixel_7": {
        "name": "Pixel 7",
        "user_agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 915},
        "device_scale_factor": 2.625,
        "is_mobile": True,
        "has_touch": True,
    },
    "ipad_pro": {
        "name": "iPad Pro 11",
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 834, "height": 1194},
        "device_scale_factor": 2,
        "is_mobile": True,
        "has_touch": True,
    },
    "galaxy_s21": {
        "name": "Samsung Galaxy S21",
        "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 360, "height": 800},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
}

BASE_URL = "https://www.saucedemo.com"


@pytest.fixture(params=["iphone_13", "pixel_7", "galaxy_s21"], ids=["iPhone13", "Pixel7", "GalaxyS21"])
def mobile_page(request):
    """Create a mobile-emulated page for each device."""
    device_config = DEVICES[request.param]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=device_config["viewport"],
            user_agent=device_config["user_agent"],
            device_scale_factor=device_config["device_scale_factor"],
            is_mobile=device_config["is_mobile"],
            has_touch=device_config["has_touch"],
        )
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        
        yield page, device_config["name"]
        
        context.close()
        browser.close()


@pytest.fixture(params=["ipad_pro"], ids=["iPadPro"])
def tablet_page(request):
    """Create a tablet-emulated page."""
    device_config = DEVICES[request.param]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=device_config["viewport"],
            user_agent=device_config["user_agent"],
            device_scale_factor=device_config["device_scale_factor"],
            is_mobile=device_config["is_mobile"],
            has_touch=device_config["has_touch"],
        )
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded")
        
        yield page, device_config["name"]
        
        context.close()
        browser.close()
