import unittest
from unittest.mock import patch
from datetime import datetime

from tests.constant import TROI_PROJECT_RESPONSE_ITEM, TROI_PROJECT_CALC_POSITION_RESPONSE_ITEM
from troi.troi_api.api import Client


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client('http://localhost', 'username', 'token')

    @patch('troi.troi_api.api.requests')
    def test_list_projects(self, mock_requests):
        # Setup
        mock_requests.request.return_value.json.return_value = [TROI_PROJECT_RESPONSE_ITEM]

        # Exercise
        result = self.client.list_projects(1)

        # Verify
        mock_requests.request.assert_called_once()
        self.assertIsNotNone(result)

    @patch('troi.troi_api.api.requests')
    def test_get_project(self, mock_requests):
        # Setup
        mock_requests.request.return_value.json.return_value = TROI_PROJECT_RESPONSE_ITEM

        # Exercise
        result = self.client.get_project(1)

        # Verify
        mock_requests.request.assert_called_once()
        self.assertIsNotNone(result)

    @patch('troi.troi_api.api.requests')
    def test_list_calc_pos(self, mock_requests):
        # Setup
        mock_requests.request.return_value.json.return_value = [TROI_PROJECT_CALC_POSITION_RESPONSE_ITEM]

        # Exercise
        result = self.client.list_calc_pos(1, 1)

        # Verify
        mock_requests.request.assert_called_once()
        self.assertIsNotNone(result)

    @patch('troi.troi_api.api.requests')
    def test_list_billing_hours(self, mock_requests):
        # Setup
        mock_requests.request.return_value.json.return_value = {}

        # Exercise
        result = self.client.list_billing_hours(1, 1, datetime.now(), datetime.now())

        # Verify
        mock_requests.request.assert_called_once()
        self.assertIsNotNone(result)

    @patch('troi.troi_api.api.requests')
    def test_add_billing_hours(self, mock_requests):
        # Setup
        mock_requests.request.return_value.json.return_value = {}

        # Exercise
        result = self.client.add_billing_hours(1, 1, 1, datetime.now(), 1.0, 'test')

        # Verify
        mock_requests.request.assert_called_once()
        self.assertIsNone(result)

    @patch('troi.troi_api.api.requests')
    def test_update_billing_hours(self, mock_requests):
        # Setup
        mock_requests.request.return_value.json.return_value = {}

        # Exercise
        result = self.client.update_billing_hours(1, 1, 1, 1, datetime.now(), 1.0, 'test')

        # Verify
        mock_requests.request.assert_called_once()
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()