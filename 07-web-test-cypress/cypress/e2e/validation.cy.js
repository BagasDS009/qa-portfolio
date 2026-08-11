import HomePage from '../pages/HomePage';
import TrainListPage from '../pages/TrainListPage';
import PassengerPage from '../pages/PassengerPage';

describe('TC-007: Form Validation (blur trigger)', () => {

  /**
   * Helper: Navigate to passenger form
   * Search → Select first train → Passenger form
   */
  const navigateToPassengerForm = () => {
    cy.fixture('testData').then((data) => {
      HomePage.visit();
      HomePage.searchTrain(
        data.validSearch.origin,
        data.validSearch.destination,
        data.validSearch.tgl,
        data.validSearch.adults
      );
      TrainListPage.selectFirstTrain();
    });
  };

  it('TC-007: Submit button disabled when form is empty', () => {
    navigateToPassengerForm();
    PassengerPage.isFormDisplayed();
    PassengerPage.isSubmitButtonDisabled();
  });

  it('TC-007b: Validation - Mohon isi Nama (blur)', () => {
    navigateToPassengerForm();
    PassengerPage.triggerBlurName();
    PassengerPage.verifyErrorMohonIsiNama();
  });

  it('TC-007c: Validation - Mohon isi Nomor Identitas (blur)', () => {
    navigateToPassengerForm();
    PassengerPage.triggerBlurIdNumber();
    PassengerPage.verifyErrorMohonIsiNoId();
  });

  it('TC-007d: Search without filling origin station', () => {
    HomePage.visit();
    HomePage.clickSearch();
    cy.url().should('include', 'booking.kai.id');
  });

  it('TC-007e: Validation - Mohon diisi Email (blur)', () => {
    navigateToPassengerForm();
    PassengerPage.triggerBlurEmail();
    PassengerPage.verifyErrorMohonIsiEmail();
  });

  it('TC-007f: Validation - Nomor Identitas Wajib Diisi (Passenger blur)', () => {
    navigateToPassengerForm();
    PassengerPage.triggerBlurPassengerId();
    PassengerPage.verifyErrorPassengerNoId();
  });

  it('TC-007g: Passenger name field has required attribute', () => {
    navigateToPassengerForm();
    PassengerPage.verifyPassengerNameRequired();
  });
});
