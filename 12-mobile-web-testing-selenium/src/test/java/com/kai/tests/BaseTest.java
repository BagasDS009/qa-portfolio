package com.kai.tests;

import com.kai.config.DeviceConfig;
import io.github.bonigarcia.wdm.WebDriverManager;
import io.qameta.allure.Allure;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeSuite;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.time.Duration;
import java.util.Properties;

/**
 * Base test class providing WebDriver setup with Firefox mobile emulation.
 * Uses Firefox responsive design mode via viewport resizing and user agent override.
 */
public class BaseTest {

    protected static Properties config;
    protected static String BASE_URL;

    protected WebDriver driver;
    protected JavascriptExecutor js;

    @BeforeSuite
    public void setupDriver() throws Exception {
        WebDriverManager.firefoxdriver().setup();

        // Load config
        config = new Properties();
        InputStream configStream = getClass().getClassLoader().getResourceAsStream("config.properties");
        if (configStream == null) {
            throw new IllegalStateException("config.properties not found in classpath");
        }
        config.load(configStream);
        BASE_URL = config.getProperty("base.url");
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

    /**
     * Navigate to target application and wait for page load.
     */
    protected void navigateToBase() {
        driver.get(BASE_URL);
    }

    /**
     * Login with credentials from config.properties.
     */
    protected void login() {
        String username = config.getProperty("username");
        String password = config.getProperty("password");
        driver.findElement(By.id("user-name")).sendKeys(username);
        driver.findElement(By.id("password")).sendKeys(password);
        driver.findElement(By.id("login-button")).click();
    }

    @AfterMethod
    public void tearDown(ITestResult result) {
        // Capture screenshot on failure
        if (result.getStatus() == ITestResult.FAILURE && driver != null) {
            try {
                byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
                Allure.addAttachment("Screenshot on Failure",
                        "image/png",
                        new ByteArrayInputStream(screenshot),
                        ".png");
            } catch (Exception e) {
                // Ignore screenshot errors
            }
        }

        if (driver != null) {
            driver.quit();
        }
    }
}
