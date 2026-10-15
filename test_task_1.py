"""Tests for task 1.

Run this file in VS Code, or run: python test_task_1.py
Each test compares the actual result with the expected result.
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from task_1 import get_days_from_today

# A fixed "today" makes date tests independent of the day you run them.


class DaysFromTodayTests(unittest.TestCase):
    def test_past_today_and_future(self):
        with patch("task_1.datetime", wraps=datetime) as clock:
            clock.today.return_value = datetime(2021, 5, 5, 23, 59)
            self.assertEqual(get_days_from_today("2021-05-04"), 1)
            self.assertEqual(get_days_from_today("2021-05-05"), 0)
            self.assertEqual(get_days_from_today("2021-10-09"), -157)

    def test_leap_day_and_year_boundary(self):
        with patch("task_1.datetime", wraps=datetime) as clock:
            clock.today.return_value = datetime(2024, 3, 1)
            self.assertEqual(get_days_from_today("2024-02-28"), 2)
            self.assertEqual(get_days_from_today("2024-02-29"), 1)
            clock.today.return_value = datetime(2025, 1, 1)
            self.assertEqual(get_days_from_today("2024-12-31"), 1)

    def test_invalid_date_types(self):
        for value in (None, 123, 1.5, [], {}):
            with self.subTest(value=value):
                self.assertEqual(
                    get_days_from_today(value),
                    "Date must be a string, for example '2024-01-09'.",
                )

    def test_invalid_date_values(self):
        for value in ("bad date", "2023-02-29", "2024-02-30", "2024-13-01", "2024.01.01", "", "2024-01-01 "):
            with self.subTest(value=value):
                self.assertEqual(
                    get_days_from_today(value),
                    "Invalid date. Use YYYY-MM-DD and make sure the date exists.",
                )

    def test_missing_leading_zeros(self):
        for value in ("2024-1-01", "2024-01-1", "2024-1-1"):
            with self.subTest(value=value):
                self.assertEqual(
                    get_days_from_today(value),
                    "Use YYYY-MM-DD with a two-digit month and day, for example '2024-01-09'.",
                )

    def test_time_of_day_does_not_change_the_result(self):
        with patch("task_1.datetime", wraps=datetime) as clock:
            for hour, minute, second in ((0, 0, 0), (23, 59, 59)):
                with self.subTest(time=(hour, minute, second)):
                    clock.today.return_value = datetime(2024, 6, 15, hour, minute, second)
                    self.assertEqual(get_days_from_today("2024-06-14"), 1)
                    self.assertEqual(get_days_from_today("2024-06-15"), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
