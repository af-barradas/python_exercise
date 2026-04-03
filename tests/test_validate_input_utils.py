import unittest

from utils.validate_input_utils import validate_inputs


class TestValidateInputs(unittest.TestCase):
    def test_returns_true_for_valid_inputs(self):
        result = validate_inputs([{"Name": "Alice"}], ["Name"])

        self.assertTrue(result)

    def test_raises_when_data_is_not_a_list(self):
        with self.assertRaises(TypeError):
            validate_inputs("not-a-list", ["Name"])

    def test_raises_when_data_is_empty(self):
        with self.assertRaises(ValueError):
            validate_inputs([], ["Name"])

    def test_raises_when_columns_is_not_a_list(self):
        with self.assertRaises(TypeError):
            validate_inputs([{"Name": "Alice"}], "Name")

    def test_returns_false_when_columns_are_empty(self):
        result = validate_inputs([{"Name": "Alice"}], [])

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
