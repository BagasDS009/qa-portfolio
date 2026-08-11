describe('Activities API - CRUD', () => {
  const baseEndpoint = '/Activities';

  it('GET - Get all activities', () => {
    cy.request('GET', baseEndpoint).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      expect(response.body.length).to.be.greaterThan(0);
    });
  });

  it('GET - Get activity by ID', () => {
    cy.request('GET', `${baseEndpoint}/1`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('id', 1);
      expect(response.body).to.have.property('title');
      expect(response.body).to.have.property('dueDate');
      expect(response.body).to.have.property('completed');
    });
  });

  it('GET - Non-existent activity returns 404', () => {
    cy.request({ method: 'GET', url: `${baseEndpoint}/99999`, failOnStatusCode: false }).then((response) => {
      expect(response.status).to.eq(404);
    });
  });

  it('POST - Create a new activity', () => {
    cy.fixture('testData').then((data) => {
      cy.request('POST', baseEndpoint, data.activity).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.id).to.eq(data.activity.id);
        expect(response.body.title).to.eq(data.activity.title);
        expect(response.body.completed).to.eq(data.activity.completed);
      });
    });
  });

  it('PUT - Update an existing activity', () => {
    cy.fixture('testData').then((data) => {
      const updated = { ...data.activity, title: 'Updated Activity', completed: true };
      cy.request('PUT', `${baseEndpoint}/${data.activity.id}`, updated).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.title).to.eq('Updated Activity');
        expect(response.body.completed).to.eq(true);
      });
    });
  });

  it('DELETE - Delete an activity', () => {
    cy.fixture('testData').then((data) => {
      cy.request('DELETE', `${baseEndpoint}/${data.activity.id}`).then((response) => {
        expect(response.status).to.eq(200);
      });
    });
  });
});
