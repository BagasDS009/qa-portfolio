import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Stress Test - Push system beyond normal capacity.
 * Find breaking point by ramping up to 200 VUs.
 */
export const options = {
    stages: [
        { duration: '30s', target: 10 },
        { duration: '1m', target: 50 },
        { duration: '1m', target: 100 },
        { duration: '1m', target: 150 },
        { duration: '1m', target: 200 },   // Beyond normal capacity
        { duration: '30s', target: 0 },    // Recovery
    ],
    thresholds: {
        http_req_duration: ['p(95)<5000'],  // Relaxed: 5s at 95th
        http_req_failed: ['rate<0.15'],     // Allow up to 15% failure under stress
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://fakerestapi.azurewebsites.net/api/v1';

export default function () {
    const responses = http.batch([
        ['GET', `${BASE_URL}/Activities`],
        ['GET', `${BASE_URL}/Books`],
        ['GET', `${BASE_URL}/Authors`],
        ['GET', `${BASE_URL}/Users`],
    ]);

    responses.forEach((res, i) => {
        check(res, {
            [`batch[${i}]: status 200`]: (r) => r.status === 200,
        });
    });

    sleep(0.5);
}
