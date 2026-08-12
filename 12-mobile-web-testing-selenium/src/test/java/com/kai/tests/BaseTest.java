package com.kai.tests;

import com.kai.config.DeviceConfig;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeSuite;

import java.time.Duration;

/**
 * Base test class providing WebDriver setup with Firefox mobile emulation.
 * Uses Firefox responsive design mode via viewport resizing and user agent override.
 */
public class BaseTest {

    protected static final String BASE_URL = "https://www.saucedemo.com";

    protected WebDriver driver;
    protected JavascriptExecutor js;

    @BeforeSuite
    public void setupDriver() {
        WebDriverManager.firefoxdriver().setup();
    }

    /**
     * Create a Firefox driver with mobile device emulation.
     * Emulates mobile by: viewport size, user agent, touch events preference.
     */
    protected void initMobileDriver(DeviceConfig device) {
        FirefoxOptions options = new FirefoxOptions();
        options.addArguments("--headless");
        options.addArguments("--width=" + device.getWidth());
        options.addArguments("--height=" + device.getHeight());

        // Override user agent and enable touch
        FirefoxProfile profile = new FirefoxProfile();
        profile.setPreference("general.useragent.override", device.getUserAgent());
        profile.setPreference("dom.w3c_touch_events.enabled", 1);
        profile.setPreference("layout.css.devPixelsPerPx", String.valueOf(device.getDeviceScaleFactor()));
        options.setProfile(profile);

        driver = new FirefoxDriver(options);
        // Set viewport size to match device
        driver.manage().window().setSize(new Dimension(device.getWidth(), device.getHeight()));
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        js = (JavascriptExecutor) driver;
    }

    /**
     * Create a Firefox driver with custom viewport (no user agent override).
     */
    protected void initCustomViewport(int width, int height, boolean isMobile, boolean hasTouch) {
        FirefoxOptions options = new FirefoxOptions();
        options.addArguments("--headless");
        options.addArguments("--width=" + width);
        options.addArguments("--height=" + height);

        FirefoxProfile profile = new FirefoxProfile();
        if (hasTouch) {
            profile.setPreference("dom.w3c_touch_events.enabled", 1);
        }
        profile.setPreference("layout.css.devPixelsPerPx", "3.0");
        options.setProfile(profile);

        driver = new FirefoxDriver(options);
        driver.manage().window().setSize(new Dimension(width, height));
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        js = (JavascriptExecutor) driver;
    }

    private FirefoxOptions buildBaseOptions() {
        FirefoxOptions options = new FirefoxOptions();
        options.addArguments("--headless");
        return options;
    }

    /**
     * Navigate to SauceDemo and wait for page load.
     */
    protected void navigateToBase() {
        driver.get(BASE_URL);
    }

    /**
     * Login with standard_user credentials.
     */
    protected void login() {
        driver.findElement(org.openqa.selenium.By.id("user-name")).sendKeys("standard_user");
        driver.findElement(org.openqa.selenium.By.id("password")).sendKeys("secret_sauce");
        driver.findElement(org.openqa.selenium.By.id("login-button")).click();
    }

    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
