describe('Users API - CRUD', () => {
  const baseEndpoint = '/Users';

  it('GET - Get all users', () => {
    cy.request('GET', baseEndpoint).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      expect(response.body.length).to.be.greaterThan(0);
    });
  });

  it('GET - Get user by ID', () => {
    cy.request('GET', `${baseEndpoint}/1`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('id', 1);
      expect(response.body).to.have.property('userName');
      expect(response.body).to.have.property('password');
    });
  });

  it('GET - Non-existent user returns 404', () => {
    cy.request({ method: 'GET', url: `${baseEndpoint}/99999`, failOnStatusCode: false }).then((response) => {
      expect(response.status).to.eq(404);
    });
  });

  it('POST - Create a new user', () => {
    cy.fixture('testData').then((data) => {
      cy.request('POST', baseEndpoint, data.user).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.id).to.eq(data.user.id);
        expect(response.body.userName).to.eq(data.user.userName);
        expect(response.body.password).to.eq(data.user.password);
      });
    });
  });

  it('PUT - Update an existing user', () => {
    cy.fixture('testData').then((data) => {
      const updated = { ...data.user, userName: 'updateduser', password: 'Updated@456' };
      cy.request('PUT', `${baseEndpoint}/${data.user.id}`, updated).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.userName).to.eq('updateduser');
        expect(response.body.password).to.eq('Updated@456');
      });
    });
  });

  it('DELETE - Delete a user', () => {
    cy.fixture('testData').then((data) => {
      cy.request('DELETE', `${baseEndpoint}/${data.user.id}`).then((response) => {
        expect(response.status).to.eq(200);
      });
    });
  });
});
