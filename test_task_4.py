"""Tests for task 4.

Run this file in VS Code, or run: python test_task_4.py
Each test compares the actual result with the expected result.
"""

import unittest
import copy
from datetime import datetime
from unittest.mock import patch

from task_4 import get_upcoming_birthdays

# A fixed "today" makes date tests independent of the day you run them.


class BirthdayTests(unittest.TestCase):
    def calculate(self, today, users):
        with patch("task_4.datetime", wraps=datetime) as clock:
            clock.today.return_value = datetime.strptime(today, "%Y.%m.%d")
            return get_upcoming_birthdays(users)

    def test_assignment_example(self):
        users = [
            {"name": "John Doe", "birthday": "1985.01.23"},
            {"name": "Jane Smith", "birthday": "1990.01.27"},
        ]
        self.assertEqual(self.calculate("2024.01.22", users), [
            {"name": "John Doe", "congratulation_date": "2024.01.23"},
            {"name": "Jane Smith", "congratulation_date": "2024.01.29"},
        ])

    def test_today_day_seven_and_day_eight(self):
        users = [
            {"name": "Today", "birthday": "1990.01.22"},
            {"name": "Day seven", "birthday": "1990.01.29"},
            {"name": "Day eight", "birthday": "1990.01.30"},
            {"name": "Already passed", "birthday": "1990.01.21"},
        ]
        self.assertEqual(self.calculate("2024.01.22", users), [
            {"name": "Today", "congratulation_date": "2024.01.22"},
            {"name": "Day seven", "congratulation_date": "2024.01.29"},
        ])

    def test_both_weekend_days(self):
        users = [
            {"name": "Saturday", "birthday": "1990.01.27"},
            {"name": "Sunday", "birthday": "1990.01.28"},
        ]
        self.assertEqual(self.calculate("2024.01.27", users), [
            {"name": "Saturday", "congratulation_date": "2024.01.29"},
            {"name": "Sunday", "congratulation_date": "2024.01.29"},
        ])

    def test_next_year_and_weekend_crossing_year_end(self):
        users = [
            {"name": "December birthday", "birthday": "1990.12.31"},
            {"name": "January birthday", "birthday": "1990.01.01"},
        ]
        self.assertEqual(self.calculate("2023.12.29", users), [
            {"name": "December birthday", "congratulation_date": "2024.01.01"},
            {"name": "January birthday", "congratulation_date": "2024.01.01"},
        ])

    def test_leap_day_in_leap_and_non_leap_years(self):
        users = [{"name": "Leap birthday", "birthday": "2000.02.29"}]
        self.assertEqual(self.calculate("2024.02.26", users), [
            {"name": "Leap birthday", "congratulation_date": "2024.02.29"},
        ])
        self.assertEqual(self.calculate("2025.02.24", users), [
            {"name": "Leap birthday", "congratulation_date": "2025.02.28"},
        ])

    def test_empty_list_and_input_is_not_modified(self):
        self.assertEqual(self.calculate("2024.01.22", []), [])
        users = [{"name": "John", "birthday": "1985.01.23"}]
        before = copy.deepcopy(users)
        self.calculate("2024.01.22", users)
        self.assertEqual(users, before)

    def test_weekend_greeting_can_move_beyond_the_seven_day_window(self):
        users = [{"name": "Sunday birthday", "birthday": "1990.01.28"}]
        self.assertEqual(self.calculate("2024.01.21", users), [
            {"name": "Sunday birthday", "congratulation_date": "2024.01.29"},
        ])

    def test_users_must_be_a_list(self):
        for value in (None, "users", 123, {}, ()):
            with self.subTest(value=value):
                self.assertEqual(
                    self.calculate("2024.01.22", value),
                    "Users must be a list of dictionaries with 'name' and 'birthday' fields.",
                )

    def test_each_user_must_be_a_dictionary(self):
        for value in (None, "John", 123, []):
            with self.subTest(value=value):
                self.assertEqual(
                    self.calculate("2024.01.22", [value]),
                    "User 1 must be a dictionary with 'name' and 'birthday' fields.",
                )

    def test_missing_required_fields(self):
        cases = [
            ({}, "name"),
            ({"birthday": "1990.01.23"}, "name"),
            ({"name": "John"}, "birthday"),
        ]
        for user, missing_field in cases:
            with self.subTest(user=user):
                self.assertEqual(
                    self.calculate("2024.01.22", [user]),
                    f"User 1 is missing the '{missing_field}' field.",
                )

    def test_name_must_be_a_non_empty_string(self):
        cases = [
            (None, "name must be a string."),
            (123, "name must be a string."),
            ([], "name must be a string."),
            ("", "name must not be empty."),
            ("   ", "name must not be empty."),
        ]
        for name, message in cases:
            with self.subTest(name=name):
                users = [{"name": name, "birthday": "1990.01.23"}]
                self.assertEqual(self.calculate("2024.01.22", users), f"User 1: {message}")

    def test_birthday_must_be_a_string(self):
        for value in (None, 19900123, [], {}, True):
            with self.subTest(value=value):
                users = [{"name": "John", "birthday": value}]
                self.assertEqual(
                    self.calculate("2024.01.22", users),
                    "User 1: birthday must be a string, for example '1990.01.09'.",
                )

    def test_invalid_birthday_values(self):
        for value in ("", "not a date", "1990-01-23", "1990.02.30", "1991.02.29", "1990.13.01"):
            with self.subTest(value=value):
                users = [{"name": "John", "birthday": value}]
                self.assertEqual(
                    self.calculate("2024.01.22", users),
                    "User 1: invalid birthday. Use YYYY.MM.DD and make sure the date exists.",
                )

    def test_birthday_requires_leading_zeros(self):
        for value in ("1990.1.23", "1990.01.9", "1990.1.9"):
            with self.subTest(value=value):
                users = [{"name": "John", "birthday": value}]
                self.assertEqual(
                    self.calculate("2024.01.22", users),
                    "User 1: use YYYY.MM.DD with a two-digit month and day, for example '1990.01.09'.",
                )

    def test_later_invalid_user_returns_an_error_without_modifying_input(self):
        cases = [
            (None, "User 2 must be a dictionary with 'name' and 'birthday' fields."),
            ({"name": "Jane"}, "User 2 is missing the 'birthday' field."),
            (
                {"name": "Jane", "birthday": "1990.02.30"},
                "User 2: invalid birthday. Use YYYY.MM.DD and make sure the date exists.",
            ),
        ]
        for invalid_user, expected in cases:
            with self.subTest(user=invalid_user):
                users = [{"name": "John", "birthday": "1990.01.23"}, invalid_user]
                before = copy.deepcopy(users)
                self.assertEqual(self.calculate("2024.01.22", users), expected)
                self.assertEqual(users, before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
