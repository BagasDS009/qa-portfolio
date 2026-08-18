"""Accessibility testing utilities using axe-core via Playwright."""

from dataclasses import dataclass
from playwright.sync_api import Page


AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"


@dataclass
class A11yViolation:
    """Represents a single accessibility violation."""

    id: str
    impact: str  # critical, serious, moderate, minor
    description: str
    help_url: str
    nodes_count: int
    targets: list[str]


def inject_axe(page: Page) -> None:
    """Inject axe-core script into the page if not already loaded."""
    page.evaluate(f"""
        () => {{
            return new Promise((resolve, reject) => {{
                if (window.axe) {{ resolve(); return; }}
                const script = document.createElement('script');
                script.src = '{AXE_CDN}';
                script.onload = resolve;
                script.onerror = () => reject(new Error('Failed to load axe-core'));
                document.head.appendChild(script);
            }});
        }}
    """)


def run_axe_scan(page: Page, context: str = "full page") -> dict:
    """Run axe-core accessibility scan on current page.

    Returns raw axe results dict with violations, passes, incomplete, inapplicable.
    """
    inject_axe(page)

    results = page.evaluate("""
        () => axe.run(document, {
            runOnly: {
                type: 'tag',
                values: ['wcag2a', 'wcag2aa', 'best-practice']
            }
        })
    """)
    return results


def parse_violations(results: dict) -> list[A11yViolation]:
    """Parse raw axe results into structured violation list."""
    violations = []
    for v in results.get("violations", []):
        nodes = v.get("nodes", [])
        targets = []
        for node in nodes[:5]:  # Limit to first 5 for readability
            target = node.get("target", ["unknown"])
            targets.append(target[0] if target else "unknown")

        violations.append(A11yViolation(
            id=v["id"],
            impact=v.get("impact", "unknown"),
            description=v["description"],
            help_url=v["helpUrl"],
            nodes_count=len(nodes),
            targets=targets,
        ))
    return violations


def get_violations_by_impact(results: dict) -> dict[str, list[A11yViolation]]:
    """Group violations by impact level."""
    violations = parse_violations(results)
    grouped = {"critical": [], "serious": [], "moderate": [], "minor": []}
    for v in violations:
        if v.impact in grouped:
            grouped[v.impact].append(v)
    return grouped


def assert_no_critical_violations(page: Page, context: str = "") -> None:
    """Assert no critical or serious accessibility violations exist.

    Raises AssertionError with detailed violation info if found.
    """
    results = run_axe_scan(page, context)
    violations = parse_violations(results)

    critical = [v for v in violations if v.impact in ("critical", "serious")]

    if critical:
        msg = f"Accessibility violations found"
        if context:
            msg += f" ({context})"
        msg += ":\n\n"
        for v in critical:
            msg += f"  [{v.impact.upper()}] {v.id}: {v.description}\n"
            msg += f"    Elements affected: {v.nodes_count}\n"
            msg += f"    Targets: {', '.join(v.targets[:3])}\n"
            msg += f"    Help: {v.help_url}\n\n"
        raise AssertionError(msg)


def get_accessibility_score(page: Page) -> dict:
    """Calculate accessibility score based on violations.

    Returns dict with score (0-100), violation counts by impact.
    """
    results = run_axe_scan(page)
    violations = parse_violations(results)

    counts = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
    for v in violations:
        if v.impact in counts:
            counts[v.impact] += 1

    total_violations = sum(counts.values())
    # Scoring: deduct points per violation severity
    score = max(0, 100 - (
        counts["critical"] * 25 +
        counts["serious"] * 10 +
        counts["moderate"] * 3 +
        counts["minor"] * 1
    ))

    return {
        "score": score,
        "total_violations": total_violations,
        **counts,
        "passes": len(results.get("passes", [])),
    }


def check_focus_visible(page: Page, selector: str) -> bool:
    """Check if an element has visible focus indicator when focused."""
    page.locator(selector).focus()
    # Check if element or its parent has outline/box-shadow on :focus
    has_focus_style = page.evaluate(f"""
        (selector) => {{
            const el = document.querySelector(selector);
            if (!el) return false;
            el.focus();
            const style = window.getComputedStyle(el);
            const outline = style.outline;
            const boxShadow = style.boxShadow;
            return (outline && outline !== 'none' && !outline.includes('0px')) ||
                   (boxShadow && boxShadow !== 'none');
        }}
    """, selector)
    return has_focus_style
