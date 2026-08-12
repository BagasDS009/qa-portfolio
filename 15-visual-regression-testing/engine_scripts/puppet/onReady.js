/**
 * Default onReady script for BackstopJS.
 * Runs after page load, before screenshot capture.
 */
module.exports = async (page, scenario) => {
    // Wait for page to be fully rendered
    await page.waitForTimeout(500);

    // Hide dynamic elements that change between runs
    await page.evaluate(() => {
        // Hide any date/time displays
        const dynamicElements = document.querySelectorAll('[data-dynamic]');
        dynamicElements.forEach((el) => {
            el.style.visibility = 'hidden';
        });
    });
};
