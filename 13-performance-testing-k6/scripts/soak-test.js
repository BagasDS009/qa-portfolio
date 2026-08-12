import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Soak Test (Endurance Test) - Sustained load over extended period.
 * Detects memory leaks, connection pool exhaustion, gradual degradation.
 * Note: For CI, use short duration. For real soak, run 1-4 hours.
 */
export const options = {
    stages: [
        { duration: '1m', target: 30 },    // Ramp up
        { duration: '5m', target: 30 },    // Sustain (short for CI; use 1-4h for real soak)
        { duration: '30s', target: 0 },    // Ramp down
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000', 'p(99)<3000'],
        http_req_failed: ['rate<0.02'],    // Very low failure rate expected
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://fakerestapi.azurewebsites.net/api/v1';

export default function () {
    const res = http.get(`${BASE_URL}/Activities/1`);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response body valid': (r) => JSON.parse(r.body).id === 1,
    });

    sleep(1);
}
