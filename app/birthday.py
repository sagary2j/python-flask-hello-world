from datetime import date


def _birthday_in(year: int, date_of_birth: date) -> date:
    try:
        return date_of_birth.replace(year=year)
    except ValueError:
        # 29 February in a non-leap year: celebrate on 28 February.
        return date(year, 2, 28)


def days_until_birthday(date_of_birth: date, today: date) -> int:
    next_birthday = _birthday_in(today.year, date_of_birth)
    if next_birthday < today:
        next_birthday = _birthday_in(today.year + 1, date_of_birth)
    return (next_birthday - today).days


def greeting(username: str, date_of_birth: date, today: date) -> str:
    days = days_until_birthday(date_of_birth, today)
    if days == 0:
        return f"Hello, {username}! Happy birthday!"
    return f"Hello, {username}! Your birthday is in {days} day(s)"
