"""
Mobile Orientation & Device Comparison Tests.
Verify layout adapts to portrait vs landscape and across different screen sizes.
"""

import allure
import pytest
from playwright.sync_api import sync_playwright


BASE_URL = "https://www.saucedemo.com"


@allure.epic("Mobile Web Testing")
@allure.feature("Orientation & Layout")
class TestMobileOrientation:
    """Test orientation changes and layout comparison."""

    @allure.title("Portrait vs Landscape - login page layout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.responsive
    def test_portrait_vs_landscape(self):
        """Verify login page works in both portrait and landscape."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # Portrait (iPhone)
            with allure.step("Test in PORTRAIT mode (390x844)"):
                portrait_ctx = browser.new_context(
                    viewport={"width": 390, "height": 844},
                    is_mobile=True,
                    has_touch=True,
                )
                portrait_page = portrait_ctx.new_page()
                portrait_page.goto(BASE_URL)
                portrait_page.wait_for_load_state("domcontentloaded")
                assert portrait_page.locator("#login-button").is_visible()
                portrait_width = portrait_page.evaluate("window.innerWidth")
                portrait_ctx.close()

            # Landscape (same device rotated)
            with allure.step("Test in LANDSCAPE mode (844x390)"):
                landscape_ctx = browser.new_context(
                    viewport={"width": 844, "height": 390},
                    is_mobile=True,
                    has_touch=True,
                )
                landscape_page = landscape_ctx.new_page()
                landscape_page.goto(BASE_URL)
                landscape_page.wait_for_load_state("domcontentloaded")
                assert landscape_page.locator("#login-button").is_visible()
                landscape_width = landscape_page.evaluate("window.innerWidth")
                landscape_ctx.close()

            with allure.step("Compare viewports"):
                assert landscape_width > portrait_width

            browser.close()

    @allure.title("Small phone vs Large phone comparison")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.responsive
    def test_small_vs_large_phone(self):
        """Verify layout works on both small (320px) and large (428px) phones."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            devices = {
                "Small Phone (320px)": {"width": 320, "height": 568},
                "Large Phone (428px)": {"width": 428, "height": 926},
            }

            for device_name, viewport in devices.items():
                with allure.step(f"Test on {device_name}"):
                    ctx = browser.new_context(
                        viewport=viewport,
                        is_mobile=True,
                        has_touch=True,
                    )
                    page = ctx.new_page()
                    page.goto(BASE_URL)
                    page.wait_for_load_state("domcontentloaded")

                    # Login form should be visible regardless of size
                    assert page.locator("#user-name").is_visible(), f"Username not visible on {device_name}"
                    assert page.locator("#login-button").is_visible(), f"Button not visible on {device_name}"

                    # No horizontal scroll (content fits viewport)
                    has_h_scroll = page.evaluate(
                        "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                    )
                    assert not has_h_scroll, f"Horizontal scroll detected on {device_name}"

                    ctx.close()

            browser.close()

    @allure.title("Mobile user agent is set correctly")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.mobile
    def test_mobile_user_agent(self, mobile_page):
        """Verify the mobile user agent is being sent."""
        page, device_name = mobile_page

        with allure.step(f"Check user agent on {device_name}"):
            ua = page.evaluate("navigator.userAgent")
            assert "Mobile" in ua or "Android" in ua or "iPhone" in ua, (
                f"User agent doesn't indicate mobile on {device_name}: {ua}"
            )

    @allure.title("Device pixel ratio is set for high-DPI screens")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.mobile
    def test_device_pixel_ratio(self, mobile_page):
        """Verify device pixel ratio is > 1 (retina/high-DPI emulation)."""
        page, device_name = mobile_page

        with allure.step(f"Check DPR on {device_name}"):
            dpr = page.evaluate("window.devicePixelRatio")
            assert dpr > 1, f"DPR should be > 1 for mobile on {device_name}, got {dpr}"
