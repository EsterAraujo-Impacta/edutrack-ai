"""
Testes unitários para o script de cálculo de progresso (scripts/calculate_progress.py).
Utiliza unittest (módulo padrão da biblioteca padrão do Python).
"""

import json
import os
import unittest
from unittest.mock import patch, MagicMock
from scripts.calculate_progress import (
    calculate_subject_progress,
    calculate_progress_json,
    fetch_tasks_for_subject
)


class TestCalculateProgress(unittest.TestCase):

    def test_calculate_subject_progress_mixed(self):
        tasks = [
            {"id": 1, "subject_id": 1, "status": "completed"},
            {"id": 2, "subject_id": 1, "status": "completed"},
            {"id": 3, "subject_id": 1, "status": "completed"},
            {"id": 4, "subject_id": 1, "status": "pending"},
            {"id": 5, "subject_id": 2, "status": "completed"}  # Outra disciplina
        ]
        res = calculate_subject_progress(1, tasks=tasks)
        self.assertEqual(res["subject_id"], 1)
        self.assertEqual(res["total_tasks"], 4)
        self.assertEqual(res["completed_tasks"], 3)
        self.assertEqual(res["progress_percentage"], 75.0)
        self.assertEqual(res["status"], "in_progress")

    def test_calculate_subject_progress_zero_tasks(self):
        res = calculate_subject_progress(1, tasks=[])
        self.assertEqual(res["subject_id"], 1)
        self.assertEqual(res["total_tasks"], 0)
        self.assertEqual(res["completed_tasks"], 0)
        self.assertEqual(res["progress_percentage"], 0.0)
        self.assertEqual(res["status"], "no_tasks")

    def test_calculate_subject_progress_all_completed(self):
        tasks = [
            {"id": 1, "subject_id": 1, "status": "completed"},
            {"id": 2, "subject_id": 1, "status": "concluida"}
        ]
        res = calculate_subject_progress(1, tasks=tasks)
        self.assertEqual(res["total_tasks"], 2)
        self.assertEqual(res["completed_tasks"], 2)
        self.assertEqual(res["progress_percentage"], 100.0)
        self.assertEqual(res["status"], "completed")

    def test_calculate_subject_progress_not_started(self):
        tasks = [
            {"id": 1, "subject_id": 1, "status": "pending"}
        ]
        res = calculate_subject_progress(1, tasks=tasks)
        self.assertEqual(res["total_tasks"], 1)
        self.assertEqual(res["completed_tasks"], 0)
        self.assertEqual(res["progress_percentage"], 0.0)
        self.assertEqual(res["status"], "not_started")

    def test_calculate_progress_json(self):
        tasks = [
            {"id": 1, "subject_id": 5, "status": "completed"}
        ]
        json_str = calculate_progress_json(5, tasks=tasks)
        data = json.loads(json_str)
        self.assertEqual(data["subject_id"], 5)
        self.assertEqual(data["total_tasks"], 1)
        self.assertEqual(data["completed_tasks"], 1)
        self.assertEqual(data["progress_percentage"], 100.0)
        self.assertEqual(data["status"], "completed")

    def test_invalid_subject_id(self):
        with self.assertRaises(ValueError):
            calculate_subject_progress(0, tasks=[])

    @patch("urllib.request.urlopen")
    def test_fetch_tasks_with_auth_token_param(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps([
            {"id": 1, "subject_id": 10, "status": "completed"}
        ]).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        tasks = fetch_tasks_for_subject(10, api_base="http://fake-api.com", auth_token="token_param_123")
        self.assertEqual(len(tasks), 1)

        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.headers.get("Authorization"), "Bearer token_param_123")

    @patch("urllib.request.urlopen")
    def test_fetch_tasks_with_xano_token_env(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.read.return_value = json.dumps([
            {"id": 2, "subject_id": 20, "status": "pending"}
        ]).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        with patch.dict(os.environ, {"XANO_TOKEN": "token_from_env_456"}):
            tasks = fetch_tasks_for_subject(20, api_base="http://fake-api.com")
            self.assertEqual(len(tasks), 1)

            req = mock_urlopen.call_args[0][0]
            self.assertEqual(req.headers.get("Authorization"), "Bearer token_from_env_456")


if __name__ == "__main__":
    unittest.main()
