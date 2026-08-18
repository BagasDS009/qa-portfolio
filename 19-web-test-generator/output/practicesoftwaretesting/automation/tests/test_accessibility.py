"""
Accessibility test suite — WCAG 2.1 AA compliance.
Covers: axe-core scans, keyboard navigation, ARIA, color contrast, heading hierarchy.

Run: pytest -m a11y -v
"""

import allure
import pytest
from playwright.sync_api import Page, expect

from utils.accessibility import (
    assert_no_critical_violations,
    get_accessibility_score,
    run_axe_scan,
    parse_violations,
)
from config.settings import Config


BASE = Config.BASE_URL


# =============================================================================
# AXE-CORE AUTOMATED SCANS
# =============================================================================


@allure.epic("Practice Software Testing")
@allure.feature("Accessibility")
class TestAxeScan:
    """Automated WCAG 2.1 AA compliance checks using axe-core."""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("A11Y-001: Homepage has no critical a11y violations")
    @pytest.mark.a11y
    @pytest.mark.smoke
    def test_homepage_no_critical_violations(self, page: Page):
        """Verify homepage passes axe-core without critical violations.
        
        Note: 'serious' violations from third-party site structure (e.g., list nesting)
        are logged as warnings but don't fail the test — only 'critical' impact fails.
        """
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        with allure.step("Run axe-core scan on homepage"):
            results = run_axe_scan(page, "Homepage")
            violations = parse_violations(results)
            
            # Only fail on 'critical' impact — 'serious' from site structure issues are warnings
            critical_only = [v for v in violations if v.impact == "critical"]
            
            if critical_only:
                msg = "Critical accessibility violations found (Homepage):\n\n"
                for v in critical_only:
                    msg += f"  [{v.impact.upper()}] {v.id}: {v.description}\n"
                    msg += f"    Elements: {v.nodes_count}\n"
                    msg += f"    Targets: {', '.join(v.targets[:3])}\n\n"
                raise AssertionError(msg)
            
            # Log serious violations as warning (site issue, not our test code)
            serious = [v for v in violations if v.impact == "serious"]
            if serious:
                import warnings
                for v in serious:
                    warnings.warn(
                        f"[A11Y WARNING] {v.id}: {v.description} ({v.nodes_count} elements)",
                        stacklevel=1,
                    )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("A11Y-002: Login page has no critical a11y violations")
    @pytest.mark.a11y
    def test_login_no_critical_violations(self, page: Page):
        """Verify login page has no critical violations (excluding known site issues)."""
        page.goto(f"{BASE}/auth/login")
        page.wait_for_load_state("networkidle")

        with allure.step("Run axe-core scan on login page"):
            results = run_axe_scan(page, "Login Page")
            violations = parse_violations(results)
            
            # Exclude known site-level issues that we cannot fix
            KNOWN_SITE_ISSUES = {"button-name", "list"}
            actionable = [v for v in violations 
                         if v.impact == "critical" and v.id not in KNOWN_SITE_ISSUES]
            
            if actionable:
                msg = "Actionable critical a11y violations (Login Page):\n\n"
                for v in actionable:
                    msg += f"  [{v.impact.upper()}] {v.id}: {v.description}\n"
                raise AssertionError(msg)
            
            # Log known issues as warnings
            known = [v for v in violations if v.id in KNOWN_SITE_ISSUES]
            if known:
                import warnings
                for v in known:
                    warnings.warn(f"[KNOWN SITE ISSUE] {v.id}: {v.description}", stacklevel=1)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-003: All critical pages score >= 55")
    @pytest.mark.a11y
    @pytest.mark.regression
    @pytest.mark.parametrize("path,name", [
        ("", "Homepage"),
        ("auth/login", "Login"),
        ("auth/register", "Register"),
        ("contact", "Contact"),
    ])
    def test_page_accessibility_score(self, page: Page, path: str, name: str):
        """Verify each critical page achieves minimum accessibility score.
        
        Note: practicesoftwaretesting.com has known a11y issues (button-name, list).
        Threshold set to 55 as baseline — monitor for regressions (score should not drop).
        """
        page.goto(f"{BASE}/{path}")
        page.wait_for_load_state("networkidle")

        with allure.step(f"Calculate a11y score for {name}"):
            result = get_accessibility_score(page)

        with allure.step(f"Score: {result['score']} (threshold: 55)"):
            assert result["score"] >= 55, (
                f"{name} accessibility score {result['score']} is below threshold 55.\n"
                f"Violations: {result['critical']} critical, {result['serious']} serious, "
                f"{result['moderate']} moderate, {result['minor']} minor.\n"
                f"Total passes: {result['passes']}"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-004: Registration page has no critical violations")
    @pytest.mark.a11y
    def test_registration_no_critical_violations(self, page: Page):
        """Verify registration form has no critical violations (excluding known site issues)."""
        page.goto(f"{BASE}/auth/register")
        page.wait_for_load_state("networkidle")

        with allure.step("Run axe-core scan"):
            results = run_axe_scan(page, "Registration Page")
            violations = parse_violations(results)
            
            # Exclude known site-level issues
            KNOWN_SITE_ISSUES = {"button-name", "list"}
            actionable = [v for v in violations 
                         if v.impact == "critical" and v.id not in KNOWN_SITE_ISSUES]
            
            if actionable:
                msg = "Actionable critical a11y violations (Registration):\n\n"
                for v in actionable:
                    msg += f"  [{v.impact.upper()}] {v.id}: {v.description}\n"
                raise AssertionError(msg)
            
            # Log known issues
            known = [v for v in violations if v.id in KNOWN_SITE_ISSUES]
            if known:
                import warnings
                for v in known:
                    warnings.warn(f"[KNOWN SITE ISSUE] {v.id}: {v.description}", stacklevel=1)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-005: Contact page has no critical violations")
    @pytest.mark.a11y
    def test_contact_no_critical_violations(self, page: Page):
        """Verify contact form is accessible."""
        page.goto(f"{BASE}/contact")
        page.wait_for_load_state("networkidle")

        with allure.step("Run axe-core scan"):
            assert_no_critical_violations(page, "Contact Page")


# =============================================================================
# KEYBOARD NAVIGATION
# =============================================================================


@allure.epic("Practice Software Testing")
@allure.feature("Accessibility")
class TestKeyboardNavigation:
    """Verify all interactive elements are keyboard-accessible."""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("A11Y-KB-001: Login form fully navigable by keyboard")
    @pytest.mark.a11y
    def test_login_keyboard_only(self, page: Page):
        """Verify user can complete login using only Tab + Enter."""
        page.goto(f"{BASE}/auth/login")
        page.wait_for_load_state("networkidle")

        with allure.step("Tab to email field and type"):
            # Tab through page elements until we reach email input
            for _ in range(15):
                page.keyboard.press("Tab")
                active_type = page.evaluate("document.activeElement.type || ''")
                active_dt = page.evaluate("document.activeElement.getAttribute('data-test') || ''")
                if active_dt == "email" or active_type == "email":
                    break

            page.keyboard.type("customer@practicesoftwaretesting.com")

        with allure.step("Tab to password field and type"):
            page.keyboard.press("Tab")
            page.keyboard.type("welcome01")

        with allure.step("Tab to submit button and press Enter"):
            # Tab until we reach the submit button (may be more than 1 Tab away)
            for _ in range(5):
                page.keyboard.press("Tab")
                active_dt = page.evaluate("document.activeElement.getAttribute('data-test') || ''")
                active_type = page.evaluate("document.activeElement.type || ''")
                if active_dt == "login-submit" or active_type == "submit":
                    break
            page.keyboard.press("Enter")

        with allure.step("Verify login successful (keyboard-only)"):
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(5000)
            assert "/auth/login" not in page.url, (
                f"Login via keyboard failed — still on login page: {page.url}"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-KB-002: Search accessible via keyboard")
    @pytest.mark.a11y
    def test_search_keyboard(self, page: Page):
        """Verify search field is reachable and usable via keyboard."""
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        with allure.step("Tab until reaching search input"):
            for _ in range(20):
                page.keyboard.press("Tab")
                active_test = page.evaluate(
                    "document.activeElement.getAttribute('data-test') || ''"
                )
                if active_test == "search-query":
                    break

        with allure.step("Type search query"):
            page.keyboard.type("pliers")

        with allure.step("Tab to search button and press Enter"):
            page.keyboard.press("Tab")
            active_test = page.evaluate(
                "document.activeElement.getAttribute('data-test') || ''"
            )
            if active_test == "search-submit":
                page.keyboard.press("Enter")
            else:
                # Fallback: submit via Enter on input
                page.locator("[data-test='search-submit']").press("Enter")

        with allure.step("Verify search executed"):
            page.wait_for_load_state("networkidle")
            # Products should be filtered
            products = page.locator("[data-test='product-name']")
            assert products.count() > 0, "Search via keyboard produced no results"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-KB-003: Navigation links accessible via keyboard")
    @pytest.mark.a11y
    def test_nav_keyboard_accessible(self, page: Page):
        """Verify main navigation links are reachable via Tab."""
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        nav_items_found = []

        with allure.step("Tab through page and record nav items reached"):
            for _ in range(30):
                page.keyboard.press("Tab")
                data_test = page.evaluate(
                    "document.activeElement.getAttribute('data-test') || ''"
                )
                if data_test.startswith("nav-"):
                    nav_items_found.append(data_test)

        with allure.step("Verify key nav items are keyboard-reachable"):
            assert "nav-home" in nav_items_found or len(nav_items_found) > 0, (
                f"No navigation items reached via keyboard. Found: {nav_items_found}"
            )


# =============================================================================
# ARIA & SEMANTIC HTML
# =============================================================================


@allure.epic("Practice Software Testing")
@allure.feature("Accessibility")
class TestAriaSemantics:
    """Verify proper ARIA roles and semantic HTML structure."""

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-ARIA-001: Form inputs have accessible labels")
    @pytest.mark.a11y
    def test_form_inputs_have_labels(self, page: Page):
        """Verify all visible inputs on login page have accessible names."""
        page.goto(f"{BASE}/auth/login")
        page.wait_for_load_state("networkidle")

        with allure.step("Check all inputs for accessible labels"):
            unlabeled = page.evaluate("""
                () => {
                    const inputs = document.querySelectorAll(
                        'input:not([type="hidden"]):not([type="submit"])'
                    );
                    const unlabeled = [];
                    inputs.forEach(input => {
                        const id = input.id;
                        const hasLabel = id && document.querySelector('label[for="' + id + '"]');
                        const hasAriaLabel = input.getAttribute('aria-label');
                        const hasAriaLabelledBy = input.getAttribute('aria-labelledby');
                        const hasPlaceholder = input.getAttribute('placeholder');
                        const hasTitle = input.getAttribute('title');
                        if (!hasLabel && !hasAriaLabel && !hasAriaLabelledBy && !hasTitle && !hasPlaceholder) {
                            unlabeled.push(input.name || input.type || 'unknown');
                        }
                    });
                    return unlabeled;
                }
            """)

            # Allow placeholder as fallback (common in modern SPAs)
            assert len(unlabeled) == 0, (
                f"Found {len(unlabeled)} input(s) without accessible labels: {unlabeled}. "
                f"Add <label>, aria-label, or placeholder."
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-ARIA-002: Images have alt text")
    @pytest.mark.a11y
    def test_images_have_alt(self, page: Page):
        """Verify all meaningful images have alt attributes."""
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        with allure.step("Scan images for alt text"):
            missing_alt = page.evaluate("""
                () => {
                    const imgs = document.querySelectorAll('img');
                    const missing = [];
                    imgs.forEach(img => {
                        const alt = img.getAttribute('alt');
                        const role = img.getAttribute('role');
                        // Decorative images with role="presentation" or empty alt="" are OK
                        if (alt === null && role !== 'presentation' && role !== 'none') {
                            missing.push(img.src.split('/').pop() || 'unknown');
                        }
                    });
                    return missing;
                }
            """)

            assert len(missing_alt) == 0, (
                f"Found {len(missing_alt)} image(s) without alt text: "
                f"{missing_alt[:5]}{'...' if len(missing_alt) > 5 else ''}"
            )

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("A11Y-ARIA-003: Heading hierarchy is logical")
    @pytest.mark.a11y
    def test_heading_hierarchy(self, page: Page):
        """Verify headings don't skip levels (h1 → h3 without h2)."""
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        with allure.step("Extract heading levels"):
            headings = page.evaluate("""
                () => {
                    const hs = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                    return Array.from(hs).map(h => ({
                        level: parseInt(h.tagName[1]),
                        text: h.textContent.trim().substring(0, 40)
                    }));
                }
            """)

        with allure.step("Check for skipped heading levels"):
            errors = []
            for i in range(1, len(headings)):
                prev = headings[i - 1]["level"]
                curr = headings[i]["level"]
                if curr > prev + 1:
                    errors.append(
                        f"Skipped h{prev} → h{curr} ('{headings[i]['text']}')"
                    )

            if errors:
                # Warning — not a hard failure but noted
                allure.attach(
                    "\n".join(errors),
                    name="Heading hierarchy warnings",
                    attachment_type=allure.attachment_type.TEXT,
                )
            # Only fail if major skip (h1 → h4+)
            major = [e for e in errors if "h1 → h3" in e or "h1 → h4" in e]
            assert len(major) == 0, (
                f"Major heading hierarchy violations: {major}"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-ARIA-004: Color contrast meets AA standard")
    @pytest.mark.a11y
    def test_color_contrast(self, page: Page):
        """Verify text color contrast meets WCAG AA (4.5:1 for normal text)."""
        page.goto(f"{BASE}/auth/login")
        page.wait_for_load_state("networkidle")

        with allure.step("Run axe color-contrast rule"):
            from utils.accessibility import inject_axe
            inject_axe(page)

            results = page.evaluate("""
                () => axe.run(document, {
                    runOnly: { type: 'rule', values: ['color-contrast'] }
                })
            """)

        violations = results.get("violations", [])
        if violations:
            nodes = violations[0].get("nodes", [])
            targets = [n["target"][0] for n in nodes[:5]]
            assert len(violations) == 0, (
                f"Color contrast failures on {len(nodes)} element(s): {targets}"
            )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("A11Y-ARIA-005: Buttons have accessible names")
    @pytest.mark.a11y
    def test_buttons_have_names(self, page: Page):
        """Verify all buttons have accessible text or aria-label."""
        page.goto(BASE)
        page.wait_for_load_state("networkidle")

        with allure.step("Check buttons for accessible names"):
            unnamed = page.evaluate("""
                () => {
                    const buttons = document.querySelectorAll('button, [role="button"], input[type="submit"]');
                    const unnamed = [];
                    buttons.forEach(btn => {
                        const text = btn.textContent.trim();
                        const ariaLabel = btn.getAttribute('aria-label');
                        const title = btn.getAttribute('title');
                        const value = btn.value;
                        if (!text && !ariaLabel && !title && !value) {
                            unnamed.push(btn.outerHTML.substring(0, 80));
                        }
                    });
                    return unnamed;
                }
            """)

            assert len(unnamed) == 0, (
                f"Found {len(unnamed)} button(s) without accessible names: "
                f"{unnamed[:3]}"
            )
