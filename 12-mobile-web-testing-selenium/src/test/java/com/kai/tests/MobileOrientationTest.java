package com.kai.tests;

import com.kai.config.DeviceConfig;
import io.qameta.allure.*;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.Test;

@Epic("Mobile Web Testing")
@Feature("Orientation & Layout")
public class MobileOrientationTest extends BaseTest {

    @Test
    @Story("Orientation")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify login page works in both portrait (390x844) and landscape (844x390)")
    public void testPortraitVsLandscape() {
        // Portrait mode
        Allure.step("Test in PORTRAIT mode (390x844)");
        initCustomViewport(390, 844, true, true);
        navigateToBase();
        Assert.assertTrue(driver.findElement(By.id("login-button")).isDisplayed());
        Long portraitWidth = (Long) js.executeScript("return window.innerWidth");
        driver.quit();

        // Landscape mode
        Allure.step("Test in LANDSCAPE mode (844x390)");
        initCustomViewport(844, 390, true, true);
        navigateToBase();
        Assert.assertTrue(driver.findElement(By.id("login-button")).isDisplayed());
        Long landscapeWidth = (Long) js.executeScript("return window.innerWidth");

        Allure.step("Compare viewports");
        Assert.assertTrue(landscapeWidth > portraitWidth,
                "Landscape width (" + landscapeWidth + ") should be > portrait width (" + portraitWidth + ")");
    }

    @Test
    @Story("Screen Size Comparison")
    @Severity(SeverityLevel.MINOR)
    @Description("Verify layout works on both small (320px) and large (428px) phones without horizontal scroll")
    public void testSmallVsLargePhone() {
        int[][] devices = {
                {320, 568},  // Small Phone
                {428, 926}   // Large Phone
        };
        String[] names = {"Small Phone (320px)", "Large Phone (428px)"};

        for (int i = 0; i < devices.length; i++) {
            Allure.step("Test on " + names[i]);
            initCustomViewport(devices[i][0], devices[i][1], true, true);
            navigateToBase();

            // Login form should be visible
            Assert.assertTrue(driver.findElement(By.id("user-name")).isDisplayed(),
                    "Username not visible on " + names[i]);
            Assert.assertTrue(driver.findElement(By.id("login-button")).isDisplayed(),
                    "Button not visible on " + names[i]);

            // No horizontal scroll
            Boolean hasHScroll = (Boolean) js.executeScript(
                    "return document.documentElement.scrollWidth > document.documentElement.clientWidth"
            );
            Assert.assertFalse(hasHScroll, "Horizontal scroll detected on " + names[i]);

            driver.quit();
        }
    }

    @Test
    @Story("User Agent")
    @Severity(SeverityLevel.MINOR)
    @Description("Verify the mobile user agent is correctly set")
    public void testMobileUserAgent() {
        // Use a device config that sets user agent
        initMobileDriver(DeviceConfig.IPHONE_13);
        navigateToBase();

        Allure.step("Check user agent contains Mobile indicator");
        String ua = (String) js.executeScript("return navigator.userAgent");
        Assert.assertTrue(ua.contains("Mobile") || ua.contains("Android") || ua.contains("iPhone"),
                "User agent doesn't indicate mobile: " + ua);
    }

    @Test
    @Story("Device Pixel Ratio")
    @Severity(SeverityLevel.MINOR)
    @Description("Verify device pixel ratio is > 1 for high-DPI emulation")
    public void testDevicePixelRatio() {
        initMobileDriver(DeviceConfig.IPHONE_13);
        navigateToBase();

        Allure.step("Check DPR > 1");
        Number dpr = (Number) js.executeScript("return window.devicePixelRatio");
        Assert.assertTrue(dpr.doubleValue() > 1,
                "DPR should be > 1 for mobile, got " + dpr);
    }
}
