import http from 'k6/http';
import { check, sleep, group } from 'k6';

/**
 * Load Test - Simulate normal traffic patterns.
 * Ramp up to 50 VUs over 1 min, sustain for 3 min, ramp down.
 */
export const options = {
    stages: [
        { duration: '1m', target: 20 },   // Ramp up to 20 users
        { duration: '3m', target: 50 },   // Sustain 50 users
        { duration: '1m', target: 0 },    // Ramp down
    ],
    thresholds: {
        http_req_duration: ['p(95)<1500', 'p(99)<3000'],
        http_req_failed: ['rate<0.05'],
        http_reqs: ['rate>10'],           // At least 10 req/s
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://fakerestapi.azurewebsites.net/api/v1';

export default function () {
    group('Activities CRUD', () => {
        // GET all
        const listRes = http.get(`${BASE_URL}/Activities`);
        check(listRes, {
            'GET all: status 200': (r) => r.status === 200,
        });

        // GET by ID
        const getRes = http.get(`${BASE_URL}/Activities/1`);
        check(getRes, {
            'GET by ID: status 200': (r) => r.status === 200,
            'GET by ID: has id': (r) => JSON.parse(r.body).id === 1,
        });

        // POST create
        const payload = JSON.stringify({
            id: 0,
            title: 'k6 Load Test Activity',
            dueDate: '2026-08-17T00:00:00',
            completed: false,
        });
        const postRes = http.post(`${BASE_URL}/Activities`, payload, {
            headers: { 'Content-Type': 'application/json' },
        });
        check(postRes, {
            'POST: status 200': (r) => r.status === 200,
        });
    });

    group('Books API', () => {
        const res = http.get(`${BASE_URL}/Books`);
        check(res, {
            'GET books: status 200': (r) => r.status === 200,
            'GET books: is array': (r) => JSON.parse(r.body).length > 0,
        });
    });

    group('Authors API', () => {
        const res = http.get(`${BASE_URL}/Authors`);
        check(res, {
            'GET authors: status 200': (r) => r.status === 200,
        });
    });

    sleep(1);
}
