package com.kai.tests;

import com.kai.config.DeviceConfig;
import io.qameta.allure.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.testng.Assert;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

@Epic("Mobile Web Testing")
@Feature("Mobile Checkout")
public class MobileCheckoutTest extends BaseTest {

    @DataProvider(name = "mobileDevices")
    public Object[][] mobileDevices() {
        return new Object[][]{
                {DeviceConfig.IPHONE_13},
                {DeviceConfig.PIXEL_7},
                {DeviceConfig.GALAXY_S21}
        };
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Full Checkout")
    @Severity(SeverityLevel.CRITICAL)
    @Description("Verify user can complete full purchase flow on mobile device")
    public void testFullCheckoutFlow(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login on " + device.getName());
        login();

        Allure.step("Add product to cart");
        driver.findElement(By.cssSelector("[data-test='add-to-cart-sauce-labs-backpack']")).click();
        sleep(500);

        Allure.step("Go to cart");
        driver.findElement(By.cssSelector(".shopping_cart_link")).click();
        Assert.assertTrue(driver.getCurrentUrl().contains("/cart"));

        Allure.step("Proceed to checkout");
        driver.findElement(By.cssSelector("[data-test='checkout']")).click();

        Allure.step("Fill checkout information");
        driver.findElement(By.cssSelector("[data-test='firstName']")).sendKeys("Bagas");
        driver.findElement(By.cssSelector("[data-test='lastName']")).sendKeys("Saputra");
        driver.findElement(By.cssSelector("[data-test='postalCode']")).sendKeys("12345");
        driver.findElement(By.cssSelector("[data-test='continue']")).click();

        Allure.step("Finish checkout");
        driver.findElement(By.cssSelector("[data-test='finish']")).click();

        Allure.step("Verify order complete on " + device.getName());
        WebElement header = driver.findElement(By.cssSelector(".complete-header"));
        Assert.assertTrue(header.isDisplayed());
        Assert.assertTrue(header.getText().contains("Thank you"),
                "Order complete message not found on " + device.getName());
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Cart Persistence")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify cart items persist after mobile page refresh")
    public void testCartPersistsAfterRefresh(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login and add item");
        login();
        driver.findElement(By.cssSelector("[data-test='add-to-cart-sauce-labs-backpack']")).click();
        sleep(500);

        Allure.step("Refresh page");
        driver.navigate().refresh();

        Allure.step("Verify cart still has item on " + device.getName());
        WebElement badge = driver.findElement(By.cssSelector(".shopping_cart_badge"));
        Assert.assertTrue(badge.isDisplayed());
        Assert.assertEquals(badge.getText(), "1");
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Remove from Cart")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify user can remove item from cart on mobile")
    public void testRemoveFromCart(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login and add item");
        login();
        driver.findElement(By.cssSelector("[data-test='add-to-cart-sauce-labs-backpack']")).click();
        sleep(500);

        Allure.step("Go to cart");
        driver.findElement(By.cssSelector(".shopping_cart_link")).click();

        Allure.step("Remove item on " + device.getName());
        driver.findElement(By.cssSelector("[data-test='remove-sauce-labs-backpack']")).click();
        sleep(500);

        Allure.step("Verify cart is empty");
        Assert.assertTrue(driver.findElements(By.cssSelector(".shopping_cart_badge")).isEmpty(),
                "Cart badge still visible after removing item on " + device.getName());
    }

    @Test(dataProvider = "mobileDevices")
    @Story("Checkout Validation")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify checkout form validation works on mobile - empty fields show error")
    public void testCheckoutValidation(DeviceConfig device) {
        initMobileDriver(device);
        navigateToBase();

        Allure.step("Login and add item");
        login();
        driver.findElement(By.cssSelector("[data-test='add-to-cart-sauce-labs-backpack']")).click();

        Allure.step("Navigate to checkout");
        driver.findElement(By.cssSelector(".shopping_cart_link")).click();
        driver.findElement(By.cssSelector("[data-test='checkout']")).click();

        Allure.step("Submit empty form");
        driver.findElement(By.cssSelector("[data-test='continue']")).click();

        Allure.step("Verify error message on " + device.getName());
        WebElement error = driver.findElement(By.cssSelector("[data-test='error']"));
        Assert.assertTrue(error.isDisplayed());
        Assert.assertTrue(error.getText().contains("First Name is required"),
                "Expected validation error on " + device.getName());
    }

    private void sleep(long millis) {
        try { Thread.sleep(millis); } catch (InterruptedException ignored) {}
    }
}
