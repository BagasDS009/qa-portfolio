import HomePage from '../pages/HomePage';
import TrainListPage from '../pages/TrainListPage';

describe('TC-003: Search Train', () => {
  beforeEach(() => {
    HomePage.visit();
  });

  it('TC-003e: Search form is visible on homepage', () => {
    HomePage.isSearchFormVisible();
  });

  it('TC-003a: Search train valid route (PSE → BD)', () => {
    cy.fixture('testData').then((data) => {
      HomePage.searchTrain(
        data.validSearch.origin,
        data.validSearch.destination,
        data.validSearch.tgl,
        data.validSearch.adults
      );
      TrainListPage.isTrainListDisplayed();
    });
  });

  it('TC-003b: Search train alternative route (GMR → YK)', () => {
    cy.fixture('testData').then((data) => {
      HomePage.searchTrain(
        data.validSearchAlt.origin,
        data.validSearchAlt.destination,
        data.validSearchAlt.tgl,
        data.validSearchAlt.adults
      );
      TrainListPage.isTrainListDisplayed();
    });
  });

  it('TC-003c: Search train with multiple passengers (2 adults + 2 babies)', () => {
    cy.fixture('testData').then((data) => {
      HomePage.searchTrain(
        data.validSearch.origin,
        data.validSearch.destination,
        data.validSearch.tgl,
        2,
        2
      );
      TrainListPage.isTrainListDisplayed();
    });
  });

  it('TC-003d: Search with no results (route not found)', () => {
    cy.fixture('testData').then((data) => {
      HomePage.searchTrain(
        data.validSearchNotFound.origin,
        data.validSearchNotFound.destination,
        data.validSearchNotFound.tgl,
        data.validSearchNotFound.adults
      );
      TrainListPage.isNoResult();
    });
  });

  it('TC-003f: Baby cannot exceed adult passengers', () => {
    HomePage.getAdultCount().should('eq', '1');
    HomePage.clickBabyPlus(); // baby = 1 (ok, same as adult)
    HomePage.clickBabyPlus(); // baby = 2 (exceeds adult=1, tooltip should show)
    HomePage.getBabyTooltip().should('contain', 'Tidak bisa melebihi penumpang dewasa');
  });
});
