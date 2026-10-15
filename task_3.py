"""Task 3: normalize phone numbers using a regular expression."""

import re


def normalize_phone(phone_number):
    """Return a normalized phone number, or an error message for invalid input."""
    if not isinstance(phone_number, str):
        return "Phone number must be a string, for example '0501234567'."

    phone = re.sub(r"[^0-9+]", "", phone_number)
    phone = phone[:1] + phone[1:].replace("+", "")

    if phone in ("", "+"):
        return "Phone number must contain digits, for example '0501234567'."

    if phone.startswith("+"):
        return phone

    if phone.startswith("380"):
        return "+" + phone

    return "+38" + phone


if __name__ == "__main__":
    raw_numbers = [
        "067\t123 4567",
        "(095) 234-5678\n",
        "+380 44 123 4567",
        "380501234567",
        "    +38(050)123-32-34",
        "     0503451234",
        "(050)8889900",
        "38050-111-22-22",
        "38050 111 22 11   ",
    ]
    sanitized_numbers = [normalize_phone(number) for number in raw_numbers]
    print("Normalized phone numbers:", sanitized_numbers)

    # Check this task and print a clear pass/fail summary.
    from test_homework import run_tests

    run_tests(3)
