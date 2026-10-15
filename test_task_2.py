"""Tests for task 2.

Run this file in VS Code, or run: python test_task_2.py
Each test compares the actual result with the expected result.
"""

from contextlib import redirect_stdout
from io import StringIO
import unittest
from task_2 import get_numbers_ticket


class LotteryTests(unittest.TestCase):
    def test_sorted_unique_numbers_in_range(self):
        for _ in range(20):
            result = get_numbers_ticket(1, 49, 6)
            self.assertEqual(len(result), 6)
            self.assertEqual(result, sorted(set(result)))
            self.assertTrue(all(1 <= number <= 49 for number in result))

    def test_inclusive_limits_and_full_range(self):
        self.assertEqual(get_numbers_ticket(1, 1, 1), [1])
        self.assertEqual(get_numbers_ticket(2, 5, 4), [2, 3, 4, 5])
        self.assertEqual(get_numbers_ticket(1, 1000, 1000), list(range(1, 1001)))

    def test_invalid_parameters(self):
        cases = [
            ((0, 49, 6), "min must be at least 1."),
            ((1, 1001, 6), "max must be no greater than 1000."),
            ((10, 5, 2), "min must be less than or equal to max."),
            ((1, 0, 1), "min must be less than or equal to max."),
            ((1, 49, 0), "quantity must be between min (1) and max (49), inclusive."),
            ((1, 49, -1), "quantity must be between min (1) and max (49), inclusive."),
            ((1, 49, 50), "quantity must be between min (1) and max (49), inclusive."),
            ((5, 10, 3), "quantity must be between min (5) and max (10), inclusive."),
            ((10, 12, 10), "Cannot choose 10 unique numbers: the range contains only 3."),
        ]
        for values, expected_message in cases:
            with self.subTest(values=values):
                output = StringIO()
                with redirect_stdout(output):
                    result = get_numbers_ticket(*values)
                self.assertEqual(result, [])
                self.assertEqual(output.getvalue().strip(), expected_message)

    def test_invalid_parameter_types_name_the_parameter(self):
        for position, name in enumerate(("min", "max", "quantity")):
            for value in (None, "6", 1.5, True, False, [], {}):
                with self.subTest(parameter=name, value=value):
                    arguments = [1, 49, 6]
                    arguments[position] = value
                    output = StringIO()
                    with redirect_stdout(output):
                        result = get_numbers_ticket(*arguments)
                    self.assertEqual(result, [])
                    self.assertEqual(
                        output.getvalue().strip(),
                        f"{name} must be an integer, without decimals or quotation marks. True and False are not accepted.",
                    )

    def test_valid_input_does_not_print_an_error(self):
        output = StringIO()
        with redirect_stdout(output):
            result = get_numbers_ticket(1, 49, 6)
        self.assertEqual(len(result), 6)
        self.assertEqual(output.getvalue(), "")

    def test_valid_range_starting_above_one(self):
        result = get_numbers_ticket(10, 49, 10)
        self.assertEqual(len(result), 10)
        self.assertEqual(result, sorted(set(result)))
        self.assertTrue(all(type(number) is int and 10 <= number <= 49 for number in result))


if __name__ == "__main__":
    unittest.main(verbosity=2)
