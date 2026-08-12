# 15 - Visual Regression Testing with BackstopJS

![BackstopJS](https://img.shields.io/badge/BackstopJS-6.3-blue)
![Puppeteer](https://img.shields.io/badge/Puppeteer-Engine-green)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=githubactions)

## Overview

Visual regression testing using **BackstopJS** — an automated tool that compares screenshots pixel-by-pixel to detect unintended UI changes. Tests run across Desktop, Tablet, and Mobile viewports.

**Target Application:** [SauceDemo](https://www.saucedemo.com)

## Test Scenarios

| # | Scenario | Viewports | Threshold |
|---|----------|-----------|-----------|
| 1 | Login Page - Default State | Desktop, Tablet, Mobile | 0.1% |
| 2 | Login Page - Error State | Desktop, Tablet, Mobile | 0.1% |
| 3 | Inventory - Products List | Desktop, Tablet, Mobile | 0.2% |
| 4 | Inventory - Product Detail | Desktop, Tablet, Mobile | 0.2% |
| 5 | Cart Page - Empty | Desktop, Tablet, Mobile | 0.1% |
| 6 | Checkout Step One | Desktop, Tablet, Mobile | 0.1% |

> **Total screenshots:** 6 scenarios × 3 viewports = **18 visual comparisons**

## Viewports Tested

| Device | Width | Height |
|--------|-------|--------|
| Desktop | 1920px | 1080px |
| Tablet | 768px | 1024px |
| Mobile | 375px | 812px |

## How It Works

```
1. Reference  → Capture "golden" baseline screenshots
2. Test       → Capture current screenshots
3. Compare    → Pixel-by-pixel diff (threshold-based)
4. Report     → HTML report with side-by-side comparison
```

## Project Structure

```
15-visual-regression-testing/
├── backstop.json               # BackstopJS configuration
├── engine_scripts/
│   ├── login-error.js         # Trigger error state before capture
│   └── puppet/
│       └── onReady.js         # Default pre-capture script
├── cookies/
│   └── standard-user.json    # Auth cookies for logged-in pages
├── backstop_data/
│   └── bitmaps_reference/    # Golden baseline images (versioned)
├── package.json
├── .gitignore
└── README.md
```

## Setup & Run

### Prerequisites

```bash
npm install
```

### Workflow

```bash
# 1. Create baseline reference screenshots (first time or after intentional UI change)
npm run reference

# 2. Run visual comparison test
npm test

# 3. View HTML report with diffs
npm run report

# 4. Approve current screenshots as new baseline (after intentional changes)
npm run approve
```

## CI/CD Integration

```yaml
- name: Visual Regression Test
  run: |
    npm ci
    npx backstop test --docker
```

BackstopJS supports `--docker` flag for consistent rendering across CI environments.

## Mismatch Threshold

| Level | Threshold | Use Case |
|-------|-----------|----------|
| Strict | 0.0% | Pixel-perfect components (icons, logos) |
| Normal | 0.1% | Full page layouts |
| Relaxed | 0.5% | Pages with dynamic content |

## Sample Report Output

```
Scenario: "Login Page - Default State"
  ✓ Desktop (1920x1080) — diff: 0.00%
  ✓ Tablet (768x1024)   — diff: 0.02%
  ✓ Mobile (375x812)    — diff: 0.00%

Scenario: "Inventory - Products List"
  ✓ Desktop (1920x1080) — diff: 0.15%
  ✗ Tablet (768x1024)   — diff: 3.42% (FAIL: exceeds 0.2% threshold)
  ✓ Mobile (375x812)    — diff: 0.08%
```

## Key Concepts Demonstrated

- **Pixel-by-pixel comparison**: Detects even subtle CSS regressions
- **Multi-viewport testing**: Desktop, Tablet, Mobile in one run
- **Threshold-based pass/fail**: Configurable tolerance per scenario
- **Cookie injection**: Test authenticated pages without scripting login flow
- **Engine scripts**: Custom pre-capture actions (form fills, clicks, waits)
- **Reference management**: Golden images versioned in Git
- **CI integration**: Docker-based rendering for environment consistency

## When to Use Visual Regression

| Situation | Visual Regression | Unit/E2E Test |
|-----------|:-----------------:|:-------------:|
| CSS layout broke | ✅ | ❌ |
| Button moved 2px | ✅ | ❌ |
| Font changed | ✅ | ❌ |
| Color wrong | ✅ | ❌ |
| Feature broken | ❌ | ✅ |
| API response wrong | ❌ | ✅ |

## Author

**Bagas Dimas Saputra**

---

*Part of QA Portfolio - Demonstrating visual regression testing to catch UI regressions early*
