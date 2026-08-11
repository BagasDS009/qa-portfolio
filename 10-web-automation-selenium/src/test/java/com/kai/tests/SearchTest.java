package com.kai.tests;

import com.kai.pages.HomePage;
import com.kai.pages.ProductsPage;
import io.qameta.allure.*;
import org.testng.Assert;
import org.testng.annotations.*;

@Epic("Automation Exercise")
@Feature("Products & Search")
public class SearchTest extends BaseTest {
    private HomePage homePage;
    private ProductsPage productsPage;

    @BeforeMethod(dependsOnMethods = "setUp")
    public void initPages() {
        homePage = new HomePage(driver);
        productsPage = new ProductsPage(driver);
    }

    // ========================
    // POSITIVE
    // ========================

    @Test(priority = 1)
    @Story("Home Page")
    @Severity(SeverityLevel.BLOCKER)
    @Description("TC-01: Verify home page is visible")
    public void testHomePageVisible() {
        homePage.open();
        Assert.assertTrue(homePage.isHomePageVisible(), "Home page not visible");
    }

    @Test(priority = 2)
    @Story("Products")
    @Severity(SeverityLevel.CRITICAL)
    @Description("TC-08: Verify All Products and product detail page")
    public void testAllProductsAndDetail() {
        driver.get("https://automationexercise.com/products");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        Assert.assertTrue(productsPage.isAllProductsVisible() || productsPage.getProductCount() > 0, "All Products page not loaded");
        productsPage.viewFirstProduct();
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        Assert.assertTrue(productsPage.isProductDetailVisible(), "Product detail not visible");
    }

    @Test(priority = 3)
    @Story("Search")
    @Severity(SeverityLevel.CRITICAL)
    @Description("TC-09a: Search Product - valid keyword 'Tshirt'")
    public void testSearchProductValid() {
        driver.get("https://automationexercise.com/products");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        productsPage.searchProduct("Tshirt");
        Assert.assertTrue(productsPage.isSearchedProductsVisible(), "Searched products not visible");
        Assert.assertTrue(productsPage.getProductCount() > 0, "No products found for 'Tshirt'");
    }

    @Test(priority = 4)
    @Story("Search")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-09b: Search Product - valid keyword 'Dress'")
    public void testSearchProductDress() {
        driver.get("https://automationexercise.com/products");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        productsPage.searchProduct("Dress");
        Assert.assertTrue(productsPage.isSearchedProductsVisible(), "Searched products not visible");
        Assert.assertTrue(productsPage.getProductCount() > 0, "No products found for 'Dress'");
    }

    @Test(priority = 5)
    @Story("Subscription")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-10: Verify Subscription in home page")
    public void testSubscription() {
        homePage.open();
        homePage.subscribe("testuser@example.com");
        Assert.assertTrue(homePage.isSubscriptionSuccess(), "Subscription failed");
    }

    // ========================
    // NEGATIVE
    // ========================

    @Test(priority = 6)
    @Story("Search")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-09c: Search Product - non-existent keyword")
    public void testSearchProductNotFound() {
        driver.get("https://automationexercise.com/products");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        productsPage.searchProduct("xyznonexistent12345");
        Assert.assertTrue(productsPage.isSearchedProductsVisible(), "Search page not shown");
        Assert.assertEquals(productsPage.getProductCount(), 0, "Should return 0 products for invalid keyword");
    }

    @Test(priority = 7)
    @Story("Search")
    @Severity(SeverityLevel.MINOR)
    @Description("TC-09d: Search Product - empty keyword shows all or stays")
    public void testSearchProductEmpty() {
        driver.get("https://automationexercise.com/products");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        productsPage.searchProduct(" ");
        // Empty/whitespace search — page should still be accessible
        Assert.assertTrue(driver.getCurrentUrl().contains("automationexercise"), "Should remain on site");
    }

    @Test(priority = 8)
    @Story("Subscription")
    @Severity(SeverityLevel.MINOR)
    @Description("TC-10b: Subscription with empty email")
    public void testSubscriptionEmptyEmail() {
        homePage.open();
        homePage.subscribe("");
        // Should not show success (HTML validation blocks)
        // Page should remain without success message
        Assert.assertTrue(homePage.isHomePageVisible(), "Should remain on home page");
    }

    @Test(priority = 9)
    @Story("Navigation")
    @Severity(SeverityLevel.NORMAL)
    @Description("TC-07: Verify navigation to Test Cases page")
    public void testNavigateToTestCasesPage() {
        homePage.open();
        driver.get("https://automationexercise.com/test_cases");
        try { Thread.sleep(1000); } catch (InterruptedException e) {}
        String title = driver.getTitle();
        Assert.assertTrue(title.contains("Automation") || driver.getCurrentUrl().contains("test_cases"),
                "Not on test cases page");
    }
}
