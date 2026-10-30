from datetime import date

import pytest

from app.birthday import days_until_birthday, greeting


@pytest.mark.parametrize(
    ("date_of_birth", "today", "expected"),
    [
        (date(1990, 6, 30), date(2026, 6, 30), 0),
        (date(1990, 7, 1), date(2026, 6, 30), 1),
        (date(1990, 6, 29), date(2026, 6, 30), 364),
        (date(1990, 12, 31), date(2026, 1, 1), 364),
        # The next birthday falls after 29 Feb 2028, so the gap is 366 days.
        (date(1990, 3, 4), date(2027, 3, 5), 365),
        (date(1990, 3, 5), date(2027, 3, 5), 0),
        # Leap-day birthdays are celebrated on 28 Feb in non-leap years.
        (date(2000, 2, 29), date(2027, 2, 28), 0),
        (date(2000, 2, 29), date(2027, 2, 27), 1),
        (date(2000, 2, 29), date(2027, 3, 1), 365),
        (date(2000, 2, 29), date(2028, 2, 29), 0),
        (date(2000, 2, 29), date(2028, 2, 28), 1),
    ],
)
def test_days_until_birthday(date_of_birth, today, expected):
    assert days_until_birthday(date_of_birth, today) == expected


def test_greeting_on_birthday():
    assert greeting("alice", date(1990, 3, 5), date(2027, 3, 5)) == "Hello, alice! Happy birthday!"


def test_greeting_before_birthday():
    assert (
        greeting("alice", date(1990, 7, 5), date(2026, 6, 30))
        == "Hello, alice! Your birthday is in 5 day(s)"
    )
