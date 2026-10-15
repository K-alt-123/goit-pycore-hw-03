"""Task 1: calculate the number of days between a date and today."""

from datetime import datetime


def get_days_from_today(date):
    """Return days since YYYY-MM-DD, or an error message for invalid input."""
    try:
        given_date = datetime.strptime(date, "%Y-%m-%d").date()
    except TypeError:
        return "Date must be a string, for example '2024-01-09'."
    except ValueError:
        return "Invalid date. Use YYYY-MM-DD and make sure the date exists."

    # Require the exact format, including leading zeros in month and day.
    if given_date.isoformat() != date:
        return "Use YYYY-MM-DD with a two-digit month and day, for example '2024-01-09'."

    today = datetime.today().date()
    return (today - given_date).days


if __name__ == "__main__":
    print(get_days_from_today("2021-10-09"))
    print(get_days_from_today("invalid date"))

    # Check this task and print a clear pass/fail summary.
    from test_homework import run_tests

    run_tests(1)
