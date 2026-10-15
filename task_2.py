"""Task 2: generate a sorted lottery ticket with unique numbers."""

import random


def get_numbers_ticket(min, max, quantity):
    """Return a sorted ticket; print an error and return [] for invalid input."""
    # The assignment requires an empty list when parameters are invalid.
    for name, value in (("min", min), ("max", max), ("quantity", quantity)):
        if type(value) is not int:
            print(f"{name} must be an integer, without decimals or quotation marks. True and False are not accepted.")
            return []

    if min < 1:
        print("min must be at least 1.")
        return []

    if max > 1000:
        print("max must be no greater than 1000.")
        return []

    if min > max:
        print("min must be less than or equal to max.")
        return []

    # The assignment specifies that quantity must be between min and max.
    if not min <= quantity <= max:
        print(f"quantity must be between min ({min}) and max ({max}), inclusive.")
        return []

    available_numbers = max - min + 1
    if quantity > available_numbers:
        print(f"Cannot choose {quantity} unique numbers: the range contains only {available_numbers}.")
        return []

    # sample selects without replacement; max + 1 includes the upper limit.
    return sorted(random.sample(range(min, max + 1), quantity))


if __name__ == "__main__":
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Your lottery numbers:", lottery_numbers)

    # Check this task and print a clear pass/fail summary.
    from test_homework import run_tests

    run_tests(2)
