package com.kai.pages;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.*;
import java.time.Duration;

public class BasePage {
    protected WebDriver driver;
    protected WebDriverWait wait;
    protected static final String BASE_URL = "https://automationexercise.com";

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(15));
    }

    protected void navigate() {
        driver.get(BASE_URL);
        dismissAds();
    }

    protected void navigate(String path) {
        driver.get(BASE_URL + "/" + path);
        dismissAds();
    }

    /**
     * Remove Google Ads iframes that block element clicks.
     */
    public void dismissAds() {
        try {
            Thread.sleep(1000);
            ((JavascriptExecutor) driver).executeScript(
                "document.querySelectorAll('iframe[id^=\"aswift\"], iframe[id^=\"google_ads\"], ins.adsbygoogle, .adsbygoogle').forEach(el => el.remove());"
            );
            ((JavascriptExecutor) driver).executeScript(
                "document.querySelectorAll('#dismissible, .ad-overlay, #ad_position_box').forEach(el => el.remove());"
            );
        } catch (Exception e) {
            // Ads not present, continue
        }
    }

    protected void click(By locator) {
        dismissAds();
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
    }

    protected void type(By locator, String text) {
        WebElement el = wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        el.clear();
        el.sendKeys(text);
    }

    protected String getText(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText();
    }

    protected boolean isVisible(By locator) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    protected void scrollTo(By locator) {
        WebElement el = driver.findElement(locator);
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", el);
    }

    public String getTitle() {
        return driver.getTitle();
    }
}
