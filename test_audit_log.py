"""
Comprehensive Unit Tests for Audit Log System
Tests log creation, retrieval, filtering, and edge cases.
"""

import pytest
from audit_log import AuditLogManager


class TestAuditLogCreation:
    def test_log_creation_success(self):
        """Should create a new audit log entry."""
        audit = AuditLogManager()
        assert audit.log_export(user_id="user-1", export_type="PDF", file_name="report.pdf") is True

    def test_log_stores_correct_data(self):
        """Should store the correct user ID, export type, and timestamp."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="CSV", file_name="data.csv")
        logs = audit.get_all_logs()
        assert logs[0]["user_id"] == "user-1"
        assert logs[0]["export_type"] == "CSV"
        assert logs[0]["file_name"] == "data.csv"
        assert "timestamp" in logs[0]

    def test_log_status_success(self):
        """Should mark the status as SUCCESS by default."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="report.pdf")
        assert audit.get_all_logs()[0]["status"] == "SUCCESS"

    def test_log_status_failed(self):
        """Should mark the status as FAILED when specified."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="report.pdf", success=False)
        assert audit.get_all_logs()[0]["status"] == "FAILED"


class TestAuditLogRetrieval:
    def test_get_logs_by_user(self):
        """Should retrieve logs for a specific user."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="a.pdf")
        audit.log_export(user_id="user-2", export_type="CSV", file_name="b.csv")
        user_logs = audit.get_logs_by_user("user-1")
        assert len(user_logs) == 1
        assert user_logs[0]["user_id"] == "user-1"

    def test_get_logs_by_user_empty(self):
        """Should return an empty list for a user with no logs."""
        audit = AuditLogManager()
        assert audit.get_logs_by_user("nonexistent") == []

    def test_get_all_logs(self):
        """Should retrieve all logs."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="a.pdf")
        audit.log_export(user_id="user-2", export_type="CSV", file_name="b.csv")
        assert len(audit.get_all_logs()) == 2


class TestAuditLogJSONExport:
    def test_json_export_success(self):
        """Should export logs as JSON."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="a.pdf")
        json_str = audit.export_logs_to_json()
        assert json_str is not None
        assert "user-1" in json_str

    def test_json_export_is_valid(self):
        """Should produce valid JSON."""
        import json
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="a.pdf")
        json_str = audit.export_logs_to_json()
        data = json.loads(json_str)
        assert len(data) == 1


class TestAuditLogEdgeCases:
    def test_multiple_logs(self):
        """Should handle multiple logs."""
        audit = AuditLogManager()
        for i in range(10):
            audit.log_export(user_id=f"user-{i}", export_type="PDF", file_name=f"{i}.pdf")
        assert len(audit.get_all_logs()) == 10

    def test_empty_audit(self):
        """Should handle an empty audit log."""
        audit = AuditLogManager()
        assert audit.get_all_logs() == []
        assert audit.export_logs_to_json() == "[]"

    def test_unique_event_ids(self):
        """Should generate unique event IDs."""
        audit = AuditLogManager()
        audit.log_export(user_id="user-1", export_type="PDF", file_name="a.pdf")
        audit.log_export(user_id="user-1", export_type="PDF", file_name="b.pdf")
        logs = audit.get_all_logs()
        assert logs[0]["event_id"] != logs[1]["event_id"]