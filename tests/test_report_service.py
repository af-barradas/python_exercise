import io
import unittest
from contextlib import redirect_stdout

from services.report_service import num_report, str_length_report


class TestReportService(unittest.TestCase):
    def test_str_length_report_prints_expected_stats(self):
        data = [
            {"Name": "Al"},
            {"Name": "Alice"},
            {"Name": "John"},
        ]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = str_length_report(data, ["Name"])

        self.assertIsNone(result)
        self.assertEqual(buffer.getvalue().strip(), "Name: Max. 5, Min. 2, Avg. 3.7")

    def test_str_length_report_returns_data_when_columns_are_empty(self):
        data = [{"Name": "Alice"}]

        result = str_length_report(data, [])

        self.assertEqual(result, data)

    def test_num_report_prints_expected_stats(self):
        data = [
            {"Billing": "10"},
            {"Billing": "20.5"},
            {"Billing": "5"},
        ]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            result = num_report(data, ["Billing"])

        self.assertIsNone(result)
        self.assertEqual(
            buffer.getvalue().strip(),
            "Billing: Max. 20.50, Min. 5.00, Avg. 11.8",
        )

    def test_num_report_skips_non_numeric_values(self):
        data = [
            {"Billing": "10"},
            {"Billing": "not-a-number"},
            {"Billing": "20"},
        ]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            num_report(data, ["Billing"])

        self.assertEqual(
            buffer.getvalue().strip(),
            "Billing: Max. 20.00, Min. 10.00, Avg. 15.0",
        )

    def test_num_report_prints_zero_stats_when_no_numeric_values_exist(self):
        data = [
            {"Billing": "abc"},
            {"Billing": "def"},
        ]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            num_report(data, ["Billing"])

        self.assertEqual(
            buffer.getvalue().strip(),
            "Billing: Max. 0.00, Min. 0.00, Avg. 0.0",
        )


if __name__ == "__main__":
    unittest.main()
