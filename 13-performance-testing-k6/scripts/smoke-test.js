import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Smoke Test - Verify system is alive and responding.
 * Minimal load: 1 VU, 30s duration.
 */
export const options = {
    vus: 1,
    duration: '30s',
    thresholds: {
        http_req_duration: ['p(95)<2000'],  // 95% requests under 2s
        http_req_failed: ['rate<0.01'],     // Less than 1% failure
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://fakerestapi.azurewebsites.net/api/v1';

export default function () {
    // GET all activities
    const res = http.get(`${BASE_URL}/Activities`);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 2s': (r) => r.timings.duration < 2000,
        'body is array': (r) => JSON.parse(r.body).length > 0,
    });

    sleep(1);
}
