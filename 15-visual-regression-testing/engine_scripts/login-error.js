/**
 * BackstopJS Engine Script: Trigger login error state.
 * Fills invalid credentials and submits form to capture error UI.
 */
module.exports = async (page) => {
    await page.waitForSelector('#user-name');
    await page.type('#user-name', 'invalid_user');
    await page.type('#password', 'wrong_password');
    await page.click('#login-button');
    await page.waitForSelector('[data-test="error"]');
    // Wait for error animation to complete
    await new Promise((resolve) => setTimeout(resolve, 500));
};
