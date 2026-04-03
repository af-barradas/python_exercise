import unittest
from unittest.mock import mock_open, patch

from sources.csv_source import CSVDataSource


class TestCSVDataSource(unittest.TestCase):
    def test_init_rejects_non_string_path(self):
        with self.assertRaises(TypeError):
            CSVDataSource(file_path=123)

    def test_init_rejects_empty_path(self):
        with self.assertRaises(ValueError):
            CSVDataSource(file_path="")

    def test_read_rejects_invalid_filename_type(self):
        source = CSVDataSource("files/")

        with self.assertRaises(TypeError):
            source.read(123)

    def test_read_rejects_empty_filename(self):
        source = CSVDataSource("files/")

        with self.assertRaises(ValueError):
            source.read("")

    def test_read_raises_for_missing_file(self):
        source = CSVDataSource("files/")

        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                source.read("does_not_exist.csv")

    def test_read_returns_list_of_dicts(self):
        source = CSVDataSource("files/")
        file_content = "ID,Name,Billing\n1,Alice,10\n2,Bob,20\n"

        with patch("builtins.open", mock_open(read_data=file_content)):
            result = source.read("customers.csv")

        self.assertEqual(
            result,
            [
                {"ID": "1", "Name": "Alice", "Billing": "10"},
                {"ID": "2", "Name": "Bob", "Billing": "20"},
            ],
        )

    def test_read_strips_whitespace_from_headers(self):
        source = CSVDataSource("files/")
        file_content = "ID, Name , Billing \n1,Alice,10\n"

        with patch("builtins.open", mock_open(read_data=file_content)):
            result = source.read("customers.csv")

        self.assertEqual(
            result,
            [{"ID": "1", "Name": "Alice", "Billing": "10"}],
        )

    def test_read_rejects_duplicate_headers(self):
        source = CSVDataSource("files/")
        file_content = "ID,Name,Name\n1,Alice,Bob\n"

        with patch("builtins.open", mock_open(read_data=file_content)):
            with self.assertRaises(ValueError):
                source.read("customers.csv")

    def test_read_fills_missing_values_with_empty_strings(self):
        source = CSVDataSource("files/")
        file_content = "ID,Name,Billing\n1,Alice\n"

        with patch("builtins.open", mock_open(read_data=file_content)):
            result = source.read("customers.csv")

        self.assertEqual(
            result,
            [{"ID": "1", "Name": "Alice", "Billing": ""}],
        )

    def test_read_raises_for_rows_with_too_many_columns(self):
        source = CSVDataSource("files/")
        file_content = "ID,Name\n1,Alice,Extra\n"

        with patch("builtins.open", mock_open(read_data=file_content)):
            with self.assertRaises(ValueError):
                source.read("customers.csv")

    def test_read_raises_for_empty_file(self):
        source = CSVDataSource("files/")

        with patch("builtins.open", mock_open(read_data="")):
            with self.assertRaises(ValueError):
                source.read("customers.csv")

    def test_read_raises_for_missing_headers(self):
        source = CSVDataSource("files/")

        with patch("builtins.open", mock_open(read_data="\n1,Alice,10\n")):
            with self.assertRaises(ValueError):
                source.read("customers.csv")

    def test_write_rejects_non_list_data(self):
        source = CSVDataSource("files/")

        with self.assertRaises(TypeError):
            source.write("not-a-list", "out.csv")

    def test_write_returns_without_opening_file_when_data_is_empty(self):
        source = CSVDataSource("files/")

        with patch("builtins.open", mock_open()) as mocked_open:
            source.write([], "out.csv")

        mocked_open.assert_not_called()

    def test_write_rejects_non_string_filename(self):
        source = CSVDataSource("files/")

        with self.assertRaises(TypeError):
            source.write([{"ID": "1"}], 123)

    def test_write_rejects_empty_filename(self):
        source = CSVDataSource("files/")

        with self.assertRaises(ValueError):
            source.write([{"ID": "1"}], "")

    def test_write_outputs_csv_content(self):
        source = CSVDataSource("files/")
        data = [
            {"ID": "1", "Name": "Alice", "Billing": "15.0"},
            {"ID": "2", "Name": "Bob", "Billing": "25.0"},
        ]
        mocked_file = mock_open()

        with patch("builtins.open", mocked_file):
            source.write(data, "out.csv")

        mocked_file.assert_called_once_with(
            "files/out.csv",
            "w",
            newline="",
            encoding="utf-8",
        )
        handle = mocked_file()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        self.assertEqual(
            written,
            "ID,Name,Billing\n"
            "1,Alice,15.0\n"
            "2,Bob,25.0\n",
        )


if __name__ == "__main__":
    unittest.main()
