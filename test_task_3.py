"""Tests for task 3.

Run this file in VS Code, or run: python test_task_3.py
Each test compares the actual result with the expected result.
"""

import unittest
from task_3 import normalize_phone


class PhoneTests(unittest.TestCase):
    def test_assignment_examples(self):
        cases = [
            ("067\t123 4567", "+380671234567"),
            ("(095) 234-5678\n", "+380952345678"),
            ("+380 44 123 4567", "+380441234567"),
            ("380501234567", "+380501234567"),
            ("    +38(050)123-32-34", "+380501233234"),
            ("     0503451234", "+380503451234"),
            ("(050)8889900", "+380508889900"),
            ("38050-111-22-22", "+380501112222"),
            ("38050 111 22 11   ", "+380501112211"),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(normalize_phone(raw), expected)

    def test_existing_international_number_and_extra_plus_signs(self):
        self.assertEqual(normalize_phone("+44 20 1234 5678"), "+442012345678")
        self.assertEqual(normalize_phone("++380(50)+123-45-67"), "+380501234567")
        self.assertEqual(normalize_phone("050+1234567"), "+380501234567")

    def test_input_without_digits(self):
        for value in ("", "   ", "(+) ---", "not a phone number"):
            with self.subTest(value=value):
                self.assertEqual(
                    normalize_phone(value),
                    "Phone number must contain digits, for example '0501234567'.",
                )

    def test_invalid_input_types(self):
        for value in (None, 501234567, 1.5, True, [], {}, b"0501234567"):
            with self.subTest(value=value):
                self.assertEqual(
                    normalize_phone(value),
                    "Phone number must be a string, for example '0501234567'.",
                )

    def test_literal_escape_characters(self):
        self.assertEqual(normalize_phone(r"067\t123 4567"), "+380671234567")

    def test_already_normalized_numbers_stay_unchanged(self):
        for number in ("+380501234567", "+442012345678"):
            with self.subTest(number=number):
                self.assertEqual(normalize_phone(number), number)


if __name__ == "__main__":
    unittest.main(verbosity=2)
