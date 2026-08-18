"""Test suite for /report endpoint — Read only (requires auth)."""

import allure
import pytest

from api.report_client import ReportClient
from config.settings import Config


@allure.epic("Restful Booker Platform")
@allure.feature("Report")
class TestReportRead:
    """GET /report — report aggregation (requires auth)."""

    @allure.title("TC-RPT-001: GET /report returns report data")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.wave1
    def test_get_report(self, report_client: ReportClient):
        with allure.step("GET /report"):
            response = report_client.get_report()

        with allure.step("Verify 200 + report array"):
            assert response.status_code == 200
            data = response.json()
            assert "report" in data
            assert isinstance(data["report"], list)

    @allure.title("TC-RPT-002: GET /report without auth returns 401")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_get_report_no_auth(self, report_client_unauth: ReportClient):
        with allure.step("GET /report without auth"):
            response = report_client_unauth.get_report()

        with allure.step("Verify 401"):
            assert response.status_code == 401

    @allure.title("TC-RPT-003: GET /report response time < 2s")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.performance
    def test_get_report_response_time(self, report_client: ReportClient):
        import time

        with allure.step("GET /report and measure time"):
            start = time.time()
            response = report_client.get_report()
            elapsed_ms = (time.time() - start) * 1000

        with allure.step(f"Verify response time {elapsed_ms:.0f}ms < {Config.RESPONSE_TIME_BUDGET_MS}ms"):
            assert response.status_code == 200
            assert elapsed_ms < Config.RESPONSE_TIME_BUDGET_MS


@allure.epic("Restful Booker Platform")
@allure.feature("Report")
class TestReportContract:
    """Schema/contract validation for report responses."""

    @allure.title("TC-RPT-004: Report entries have start, end, title fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.contract
    def test_report_entry_schema(self, report_client: ReportClient):
        with allure.step("GET /report"):
            response = report_client.get_report()

        with allure.step("Verify report entry schema"):
            assert response.status_code == 200
            data = response.json()
            assert "report" in data

            if len(data["report"]) > 0:
                entry = data["report"][0]
                assert "start" in entry
                assert "end" in entry
                assert "title" in entry
                assert isinstance(entry["start"], str)
                assert isinstance(entry["end"], str)
                assert isinstance(entry["title"], str)
