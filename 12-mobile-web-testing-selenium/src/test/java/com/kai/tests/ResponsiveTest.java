package com.kai.tests;

import com.kai.config.DeviceConfig;
import io.qameta.allure.*;
import org.openqa.selenium.By;
import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

@Epic("Mobile Web Testing")
@Feature("Responsive Design")
public class ResponsiveTest extends BaseTest {

    @DataProvider(name = "mobileDevices")
    public Object[][] mobileDevices() {
        return new Object[][]{
                {DeviceConfig.IPHONE_13},
                {DeviceConfig.PIXEL_7},
                {DeviceConfig.GALAXY_S21}
        };
    }

    @DataProvider(name = "tabletDevices")
    public Object[][] tabletDevices() {
        return new Object[][]{
                {DeviceConfig.IPAD_PRO}
        };
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Mobile Rendering")
    @Severity(SeverityLevel.CRITICAL)
    @Description("Verify login page elements are visible on mobile viewport")
    public void testLoginPageRendersOnMobile(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Verify login form on " + device.getName());

        Assert.assertTrue(driver.findElement(By.id("user-name")).isDisplayed(),
                "Username field not visible on " + device.getName());
        Assert.assertTrue(driver.findElement(By.id("password")).isDisplayed(),
                "Password field not visible on " + device.getName());
        Assert.assertTrue(driver.findElement(By.id("login-button")).isDisplayed(),
                "Login button not visible on " + device.getName());
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Mobile Viewport")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify page viewport is within mobile range (<=500px)")
    public void testViewportWidth(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Check viewport on " + device.getName());

        Long viewportWidth = (Long) js.executeScript("return window.innerWidth");
        Assert.assertTrue(viewportWidth <= 500,
                "Viewport too wide for mobile on " + device.getName() + ": " + viewportWidth + "px");
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Touch Emulation")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify touch capabilities are emulated on mobile device")
    public void testTouchEnabled(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Check touch support on " + device.getName());

        // Firefox with dom.w3c_touch_events.enabled=1 exposes TouchEvent constructor
        Boolean hasTouch = (Boolean) js.executeScript(
                "return ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (typeof TouchEvent !== 'undefined')");
        Assert.assertTrue(hasTouch, "Touch events not enabled on " + device.getName());
    }

    @Test(dataProvider = "tabletDevices")
    @Story("Tablet Rendering")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify login page elements are visible on tablet viewport")
    public void testLoginPageRendersOnTablet(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Verify login form on " + device.getName());

        Assert.assertTrue(driver.findElement(By.id("user-name")).isDisplayed());
        Assert.assertTrue(driver.findElement(By.id("password")).isDisplayed());
        Assert.assertTrue(driver.findElement(By.id("login-button")).isDisplayed());
    }

    @Test(dataProvider = "tabletDevices")
    @Story("Tablet Viewport")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify tablet viewport is between mobile and desktop (700-1100px)")
    public void testTabletViewport(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Check viewport on " + device.getName());

        Long viewportWidth = (Long) js.executeScript("return window.innerWidth");
        Assert.assertTrue(viewportWidth >= 700 && viewportWidth <= 1100,
                "Unexpected tablet viewport: " + viewportWidth + "px");
    }
}
