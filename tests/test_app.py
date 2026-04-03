import unittest
from unittest.mock import Mock, patch

from app import DataProcesserApp


class ConfigStub:
    INPUT_FILE = "customers.csv"
    OUTPUT_FILE = "masked_clients.csv"
    STRING_REPORT_COLUMNS = ["Name"]
    NUMERIC_REPORT_COLUMNS = ["Billing"]
    MASK_COLUMNS = ["Name", "Email"]
    AVG_COLUMNS = ["Billing"]


class TestDataProcesserApp(unittest.TestCase):
    def test_run_reads_processes_and_writes_data(self):
        source = Mock()
        data = [{"Name": "Alice", "Billing": "10"}]
        source.read.return_value = data

        app = DataProcesserApp(source)

        with patch("app.report_service.str_length_report") as str_report, \
                patch("app.report_service.num_report") as num_report, \
                patch("app.mask_data_service.mask_values") as mask_values, \
                patch("app.mask_data_service.calc_avg") as calc_avg:
            app.run(ConfigStub)

        source.read.assert_called_once_with(ConfigStub.INPUT_FILE)
        str_report.assert_called_once_with(data, ConfigStub.STRING_REPORT_COLUMNS)
        num_report.assert_called_once_with(data, ConfigStub.NUMERIC_REPORT_COLUMNS)
        mask_values.assert_called_once_with(data, ConfigStub.MASK_COLUMNS)
        calc_avg.assert_called_once_with(data, ConfigStub.AVG_COLUMNS)
        source.write.assert_called_once_with(data, ConfigStub.OUTPUT_FILE)


if __name__ == "__main__":
    unittest.main()
