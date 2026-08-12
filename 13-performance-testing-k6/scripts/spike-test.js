import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Spike Test - Sudden traffic surge.
 * Simulates flash sale or viral content scenario.
 */
export const options = {
    stages: [
        { duration: '10s', target: 5 },     // Normal traffic
        { duration: '10s', target: 150 },   // SPIKE!
        { duration: '30s', target: 150 },   // Sustain spike
        { duration: '10s', target: 5 },     // Back to normal
        { duration: '30s', target: 5 },     // Recovery period
    ],
    thresholds: {
        http_req_duration: ['p(95)<4000'],
        http_req_failed: ['rate<0.10'],
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://fakerestapi.azurewebsites.net/api/v1';

export default function () {
    const res = http.get(`${BASE_URL}/Activities`);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 4s': (r) => r.timings.duration < 4000,
    });

    sleep(0.3);
}
