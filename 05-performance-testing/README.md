# 05 - Performance Testing

## Overview
Performance and load testing using Apache JMeter to validate system behavior under various load conditions.

## Tech Stack
- Apache JMeter
- JMeter Plugins (Graphs, Throughput)
- HTML Report Dashboard

## Project Structure
```
05-performance-testing/
├── jmeter/       # JMeter test plan files (.jmx)
└── reports/      # Performance test results & graphs
```

## Test Types
| Type | Description | Target |
|------|-------------|--------|
| Load Test | Normal expected load | 100 concurrent users |
| Stress Test | Beyond expected load | 500 concurrent users |
| Spike Test | Sudden burst of traffic | 0 → 300 users in 10s |
| Endurance | Sustained load over time | 50 users for 30 min |

## How to Run
```bash
# Run load test
jmeter -n -t jmeter/load-test-plan.jmx -l reports/results.jtl -e -o reports/dashboard

# Generate HTML report from existing results
jmeter -g reports/results.jtl -o reports/dashboard
```

## Key Metrics
- Response Time (avg, 90th, 95th percentile)
- Throughput (requests/sec)
- Error Rate (%)
- Concurrent Users
