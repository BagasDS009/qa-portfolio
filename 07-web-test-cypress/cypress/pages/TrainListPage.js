/**
 * TrainListPage Page Object - KAI Booking
 * XPath locators identical to Playwright train_list_page.py
 */
class TrainListPage {
  // Same XPaths as 01-web-automation-playwright/pages/train_list_page.py
  xpaths = {
    trainList: "//*[@class='data-wrapper']/div",
    trainCard: "//*[@class='data-wrapper']/div/form/a[@class='card-schedule']",
    trainName: ".//div[@class='name']",
    selectButton: ".//a[contains(@onclick,'submit')]",
    noResult: "//p[@style='text-align:center;']",
  };

  isTrainListDisplayed() {
    cy.xpath(this.xpaths.trainCard, { timeout: 15000 }).should('have.length.greaterThan', 0);
  }

  getTrainCount() {
    return cy.xpath(this.xpaths.trainCard).its('length');
  }

  isNoResult() {
    cy.xpath(this.xpaths.noResult).should('be.visible');
  }

  selectFirstTrain() {
    cy.xpath(this.xpaths.trainCard).first().click();
    cy.wait(2000);
  }
}

export default new TrainListPage();
