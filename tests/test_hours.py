import unittest
from datetime import datetime

import pandas as pd

import time_tracking_synchronisation.troi_api.projects as constants
from tests.tools.mocked_client_testcase import MockedClientTestCase
from time_tracking_synchronisation.troi_api.hours import BILLING_HOUR_EMPLOYEE_ID, BILLING_HOUR_DATE, \
    BILLING_HOUR_QUANTITY, BILLING_HOUR_TAGS, BILLING_HOUR_ANNOTATION, get_billing_hours, add_billing_entry, get_remark, \
    BILLING_HOUR_RECORD_ID, BILLING_HOUR_DISPLAY_PATH


class GetBillingHoursEmptyTestCase(MockedClientTestCase):
    def test_billing_hours_for_day_empty(self):
        df = get_billing_hours(client=self.client, project_id=1, client_id=3, user_id=1, position_id=211,
                               date_from=datetime(2024, 1, 1),
                               date_to=datetime(2024, 1, 2))

        self.assertTrue(df.empty)


class GetBillingHoursTestCase(MockedClientTestCase):
    def setUp(self):
        super().setUp()
        self.client.setup_billing_hours(
            user_id=1,
            position_id=111,
            date=datetime(2024, 1, 1),
            hours=0.5,
            remark="work, varia @Some text"
        )
        self.client.setup_billing_hours(
            user_id=1,
            position_id=211,
            date=datetime(2024, 1, 1),
            hours=0.5,
            remark="work, varia @More text"
        )
        self.client.setup_billing_hours(
            user_id=1,
            position_id=211,
            date=datetime(2024, 1, 1),
            hours=2.0,
            remark="other, stuff"
        )
        self.client.setup_billing_hours(
            user_id=2,
            position_id=211,
            date=datetime(2024, 1, 1),
            hours=2.0,
            remark="@No tags"
        )
        # self.client.setup_billing_hours(
        #     user_id=1,
        #     position_id=211,
        #     date=datetime(2024, 1, 2),
        #     hours=2.0,
        #     remark="other, stuff"
        # )

    def assertDataFrameEqual(self, expected_df: pd.DataFrame, df_test: pd.DataFrame):
        self.assertIsNotNone(df_test)
        self.assertIsInstance(df_test, pd.DataFrame)
        self.assertFalse(df_test.empty)
        compare = expected_df.compare(df_test)
        self.assertTrue(compare.empty)

    def test_billing_hours_for_day(self):
        expected_df = pd.DataFrame(
            {
                BILLING_HOUR_RECORD_ID: [1, 2],
                BILLING_HOUR_DISPLAY_PATH: ["project / subproject / position"] * 2,
                constants.SUBPOSITION_ID: [211, 211],
                BILLING_HOUR_EMPLOYEE_ID: [1, 1],
                BILLING_HOUR_DATE: ["2024-01-01", "2024-01-01"],
                BILLING_HOUR_QUANTITY: [0.5, 2.0],
                BILLING_HOUR_TAGS: ["work, varia", "other, stuff"],
                BILLING_HOUR_ANNOTATION: [ "More text", ""]
            },
            index=[1, 2]
        )

        df = get_billing_hours(client=self.client, project_id=1, client_id=3, user_id=1, position_id=211,
                               date_from=datetime(2024, 1, 1),
                               date_to=datetime(2024, 1, 2))
        self.assertDataFrameEqual(expected_df, df)

    def test_billing_hours_user_not_set(self):
        expected_df = pd.DataFrame(
            {
                BILLING_HOUR_RECORD_ID: [1, 2, 3],
                BILLING_HOUR_DISPLAY_PATH: ["project / subproject / position"] * 3,
                constants.SUBPOSITION_ID: [211, 211, 211],
                BILLING_HOUR_EMPLOYEE_ID: [1, 1, 2],
                BILLING_HOUR_DATE: ["2024-01-01", "2024-01-01", "2024-01-01"],
                BILLING_HOUR_QUANTITY: [0.5, 2.0, 2.0],
                BILLING_HOUR_TAGS: ["work, varia", "other, stuff", ""],
                BILLING_HOUR_ANNOTATION: ["More text", "", "No tags"]
            },
            index=[1, 2, 3]
        )

        df = get_billing_hours(client=self.client, project_id=1, client_id=3, position_id=211,
                               date_from=datetime(2024, 1, 1),
                               date_to=datetime(2024, 1, 2))

        self.assertDataFrameEqual(expected_df, df)

    def test_billing_hours_position_id_not_set(self):
        expected_df = pd.DataFrame(
            {
                BILLING_HOUR_RECORD_ID: [0, 1, 2],
                BILLING_HOUR_DISPLAY_PATH: ["project / subproject / position"] * 3,
                constants.SUBPOSITION_ID: [111, 211, 211],
                BILLING_HOUR_EMPLOYEE_ID: [1, 1, 1],
                BILLING_HOUR_DATE: ["2024-01-01", "2024-01-01", "2024-01-01"],
                BILLING_HOUR_QUANTITY: [0.5, 0.5, 2.0],
                BILLING_HOUR_TAGS: ["work, varia", "work, varia", "other, stuff"],
                BILLING_HOUR_ANNOTATION: ["Some text", "More text", ""]
            },
            index=[0, 1, 2]
        )

        df = get_billing_hours(client=self.client, project_id=1, client_id=3, user_id=1,
                               date_from=datetime(2024, 1, 1),
                               date_to=datetime(2024, 1, 2))

        self.assertDataFrameEqual(expected_df, df)

    def test_billing_hours_user_and_position_id_not_set(self):
        expected_df = pd.DataFrame(
            {
                BILLING_HOUR_RECORD_ID: [0, 1, 2, 3],
                BILLING_HOUR_DISPLAY_PATH: ["project / subproject / position"] * 4,
                constants.SUBPOSITION_ID: [111, 211, 211, 211],
                BILLING_HOUR_EMPLOYEE_ID: [1, 1, 1, 2],
                BILLING_HOUR_DATE: ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01"],
                BILLING_HOUR_QUANTITY: [0.5, 0.5, 2.0, 2.0],
                BILLING_HOUR_TAGS: ["work, varia", "work, varia", "other, stuff", ""],
                BILLING_HOUR_ANNOTATION: ["Some text", "More text", "", "No tags"]
            },
            index=[0, 1, 2, 3]
        )

        df = get_billing_hours(client=self.client, project_id=1, client_id=3,
                               date_from=datetime(2024, 1, 1),
                               date_to=datetime(2024, 1, 2))

        self.assertDataFrameEqual(expected_df, df)


class AddBillingEntryTestCase(MockedClientTestCase):
    def test_get_remark(self):
        expected_remark = "tag1, tag2, tag3 @Some text"
        remark = get_remark(["tag1", "tag2", "tag3"], "Some text")

        self.assertEqual(expected_remark, remark)

    def test_get_remark_empty(self):
        expected_remark = ""
        remark = get_remark(None, None)
        self.assertEqual(expected_remark, remark)

    def test_get_remark_no_tags(self):
        expected_remark = "@No tags"
        remark = get_remark([], "No tags")
        self.assertEqual(expected_remark, remark)

    def test_get_remark_no_text(self):
        expected_remark = "tag1, tag2, tag3"
        remark = get_remark(["tag1", "tag2", "tag3"], None)
        self.assertEqual(expected_remark, remark)

    def test_add_billing_entry(self):
        add_billing_entry(client=self.client,
                          task_id=1,
                          date=datetime(2024, 1, 1),
                          hours=1.0,
                          user_id=1,
                          tags=["tag1", "tag2", "tag3"],
                          annotation="Some text",
                          client_id=3)

        self.assertEqual(len(self.client.added_billing_hours), 1)

    def test_add_billing_entry_error(self):
        self.client.set_error(ValueError("test"))

        with self.assertRaises(ValueError):
            add_billing_entry(client=self.client,
                              task_id=1,
                              date=datetime(2024, 1, 1),
                              hours=1.0,
                              user_id=1,
                              tags=["tag1", "tag2", "tag3"],
                              annotation="Some text",
                              client_id=3
            )


if __name__ == '__main__':
    unittest.main()
