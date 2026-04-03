import unittest

from services.mask_data_service import calc_avg, mask_values


class TestMaskDataService(unittest.TestCase):
    def test_mask_values_masks_only_requested_columns(self):
        data = [
            {"Name": "John Smith", "Email": "john@mail.com", "Location": "Boston"},
        ]

        result = mask_values(data, ["Name", "Email"])

        self.assertIs(result, data)
        self.assertEqual(data[0]["Name"], "XXXX XXXXX")
        self.assertEqual(data[0]["Email"], "XXXX@XXXX.XXX")
        self.assertEqual(data[0]["Location"], "Boston")

    def test_mask_values_returns_original_data_when_columns_are_empty(self):
        data = [{"Name": "John Smith"}]

        result = mask_values(data, [])

        self.assertEqual(result, data)
        self.assertEqual(data[0]["Name"], "John Smith")

    def test_mask_values_masks_non_ascii_letters(self):
        data = [
            {"Name": "João Silva", "Email": "joão@mail.com"},
        ]

        result = mask_values(data, ["Name", "Email"])

        self.assertIs(result, data)
        self.assertEqual(data[0]["Name"], "XXXX XXXXX")
        self.assertEqual(data[0]["Email"], "XXXX@XXXX.XXX")

    def test_mask_values_raises_when_row_is_not_a_dict(self):
        with self.assertRaises(TypeError):
            mask_values(["not-a-dict"], ["Name"])

    def test_calc_avg_overwrites_column_with_average(self):
        data = [
            {"Billing": "10"},
            {"Billing": "20"},
            {"Billing": "30"},
        ]

        result = calc_avg(data, ["Billing"])

        self.assertIs(result, data)
        self.assertEqual(
            data,
            [
                {"Billing": "20.0"},
                {"Billing": "20.0"},
                {"Billing": "20.0"},
            ],
        )

    def test_calc_avg_skips_non_numeric_values(self):
        data = [
            {"Billing": "10"},
            {"Billing": "not-a-number"},
            {"Billing": "20"},
        ]

        calc_avg(data, ["Billing"])

        self.assertEqual(
            data,
            [
                {"Billing": "15.0"},
                {"Billing": "15.0"},
                {"Billing": "15.0"},
            ],
        )

    def test_calc_avg_leaves_data_unchanged_when_column_missing(self):
        data = [{"Billing": "10"}]

        result = calc_avg(data, ["Age"])

        self.assertIs(result, data)
        self.assertEqual(data, [{"Billing": "10"}])

    def test_calc_avg_leaves_data_unchanged_when_no_numeric_values_exist(self):
        data = [
            {"Billing": "abc"},
            {"Billing": "def"},
        ]

        result = calc_avg(data, ["Billing"])

        self.assertIs(result, data)
        self.assertEqual(
            data,
            [
                {"Billing": "abc"},
                {"Billing": "def"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
