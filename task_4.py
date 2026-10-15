"""Task 4: find upcoming birthdays and move weekend greetings to Monday."""

from datetime import datetime, timedelta


def _birthday_in_year(birthday, year):
    """Use February 28 for a February 29 birthday in a non-leap year."""
    try:
        return birthday.replace(year=year)
    except ValueError:
        return birthday.replace(year=year, day=28)


def get_upcoming_birthdays(users):
    """Return upcoming greetings, or an error message for the first invalid entry."""
    if not isinstance(users, list):
        return "Users must be a list of dictionaries with 'name' and 'birthday' fields."

    today = datetime.today().date()
    upcoming_birthdays = []

    for position, user in enumerate(users, start=1):
        if not isinstance(user, dict):
            return f"User {position} must be a dictionary with 'name' and 'birthday' fields."

        try:
            name = user["name"]
            birthday_text = user["birthday"]
        except KeyError as error:
            return f"User {position} is missing the '{error.args[0]}' field."

        if not isinstance(name, str):
            return f"User {position}: name must be a string."
        if not name.strip():
            return f"User {position}: name must not be empty."

        try:
            birthday = datetime.strptime(birthday_text, "%Y.%m.%d").date()
        except TypeError:
            return f"User {position}: birthday must be a string, for example '1990.01.09'."
        except ValueError:
            return f"User {position}: invalid birthday. Use YYYY.MM.DD and make sure the date exists."

        if birthday.isoformat().replace("-", ".") != birthday_text:
            return f"User {position}: use YYYY.MM.DD with a two-digit month and day, for example '1990.01.09'."

        next_birthday = _birthday_in_year(birthday, today.year)

        if next_birthday < today:
            next_birthday = _birthday_in_year(birthday, today.year + 1)

        days_until_birthday = (next_birthday - today).days
        if 0 <= days_until_birthday <= 7:
            congratulation_date = next_birthday

            # weekday(): Monday is 0, Saturday is 5, Sunday is 6.
            if congratulation_date.weekday() >= 5:
                days_until_monday = 7 - congratulation_date.weekday()
                congratulation_date += timedelta(days=days_until_monday)

            upcoming_birthdays.append({
                "name": name,
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
            })

    return upcoming_birthdays


if __name__ == "__main__":
    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
    ]
    print("Upcoming birthday greetings:", get_upcoming_birthdays(users))

    # Check this task and print a clear pass/fail summary.
    from test_homework import run_tests

    run_tests(4)
