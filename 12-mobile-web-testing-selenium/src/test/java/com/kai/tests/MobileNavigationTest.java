package com.kai.tests;

import com.kai.config.DeviceConfig;
import io.qameta.allure.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

import java.time.Duration;

@Epic("Mobile Web Testing")
@Feature("Mobile Navigation")
public class MobileNavigationTest extends BaseTest {

    @DataProvider(name = "mobileDevices")
    public Object[][] mobileDevices() {
        return new Object[][]{
                {DeviceConfig.IPHONE_13},
                {DeviceConfig.PIXEL_7},
                {DeviceConfig.GALAXY_S21}
        };
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Mobile Login")
    @Severity(SeverityLevel.CRITICAL)
    @Description("Verify login flow works on mobile device")
    public void testMobileLogin(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login on " + device.getName());
        login();

        Allure.step("Verify redirected to inventory page");
        Assert.assertTrue(driver.getCurrentUrl().contains("/inventory"),
                "Login failed on " + device.getName());
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Mobile Scroll")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify user can scroll through products on mobile")
    public void testMobileScroll(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login first");
        login();

        Allure.step("Scroll down on " + device.getName());
        js.executeScript("window.scrollTo(0, document.body.scrollHeight)");

        try { Thread.sleep(500); } catch (InterruptedException ignored) {}

        Number scrollY = (Number) js.executeScript("return window.scrollY || window.pageYOffset");
        Assert.assertTrue(scrollY.doubleValue() > 0, "Page did not scroll on " + device.getName());
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Mobile Add to Cart")
    @Severity(SeverityLevel.CRITICAL)
    @Description("Verify add to cart button responds to tap on mobile")
    public void testMobileAddToCart(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login");
        login();

        Allure.step("Tap 'Add to cart' on " + device.getName());
        driver.findElement(By.cssSelector("[data-test='add-to-cart-sauce-labs-backpack']")).click();

        try { Thread.sleep(500); } catch (InterruptedException ignored) {}

        Allure.step("Verify cart badge shows 1");
        WebElement badge = driver.findElement(By.cssSelector(".shopping_cart_badge"));
        Assert.assertTrue(badge.isDisplayed(), "Cart badge not visible on " + device.getName());
        Assert.assertEquals(badge.getText(), "1", "Cart badge not '1' on " + device.getName());
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Mobile Menu")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify hamburger/sidebar menu opens on mobile")
    public void testMobileHamburgerMenu(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login");
        login();

        Allure.step("Open hamburger menu on " + device.getName());
        driver.findElement(By.id("react-burger-menu-btn")).click();

        Allure.step("Verify menu items are visible");
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(5));
        WebElement menuItem = wait.until(
                ExpectedConditions.visibilityOfElementLocated(By.id("inventory_sidebar_link"))
        );
        Assert.assertTrue(menuItem.isDisplayed(), "Menu item not visible on " + device.getName());
    }
}
