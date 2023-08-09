import sys
import os

SUN = 365.242199
MOON = 29.530588853

MONTH_NAMES = {
    0: "Intercalary days",
    1: "Month 1",
    2: "Month 2",
    3: "Month 3",
    4: "Month 4",
    5: "Month 5",
    6: "Month 6",
    7: "Month 7",
    8: "Month 8",
    9: "Month 9",
    10: "Month 10",
    11: "Month 11",
    12: "Month 12",
    13: "Intercalary days"
}

SE_NAMES = {
    1: "Spring Equinox",
    2: "Summer Solstice",
    3: "Autumn Equinox",
    4: "Winter Solstice"
}

def daysInYears(years):
    return years * SUN

def getNumDaysInYear(year: int):
    if year < 1:
        raise IndexError("Invalid year.")
    if year == 1:
        return int(SUN)
    actual_days = daysInYears(year)
    predicted_days = int(daysInYears(year-1)) + int(SUN)
    return int(SUN) + 1 if predicted_days < int(actual_days) else int(SUN)

def getNumMonthsBeforeYear(year: int):
    if year < 1:
        raise IndexError("Invalid year or month.")
    return 0 if year == 1 else int((int(daysInYears(year-2)) + getNumDaysInYear(year-1)) / MOON)

def getNumDaysInMonth(*args: int):
    month = 0
    if len(args) == 1:
        month = args[0]
    if len(args) == 2:
        if args[0] < 1:
            raise IndexError("Invalid year.")
        month = getNumMonthsBeforeYear(args[0]) + args[1]
    if len(args) > 2:
        raise TypeError("Too many arguments.")
    if month < 1:
        raise IndexError("Invalid month.")
    if month == 1:
        return int(MOON)
    actual_days = month * MOON
    predicted_days = int((month-1) * MOON) + int(MOON)
    return int(MOON) + 1 if predicted_days < int(actual_days) else int(MOON)

def getFirstMonthStartDay(year: int):
    if year < 1:
        raise IndexError("Invalid year.")
    num_days = 0 if year == 1 else int(daysInYears(year-2)) + getNumDaysInYear(year-1)
    return int((MOON - num_days) % MOON) + 1 # the 1 is added to make the year start on day 1 instead of day 0

def getLastMonthEndDay(year: int):
    if year < 1:
        raise IndexError("Invalid year.")
    num_days = int(daysInYears(year-1)) + getNumDaysInYear(year)
    num_whole_cycles = int(num_days / MOON)
    return int(num_whole_cycles * MOON - daysInYears(year-1)) + 1 # the 1 is added to make the year start on day 1 instead of day 0

def getMonths(year: int):
    if year < 1:
        raise IndexError("Invalid year.")
    month_start_days = []
    current_month_start_day = getFirstMonthStartDay(year)
    month_num = 1
    while current_month_start_day < getLastMonthEndDay(year):
        month_start_days.append(current_month_start_day)
        current_month_start_day += getNumDaysInMonth(year, month_num)
        month_num += 1
    return month_start_days

def getEquinoxesAndSolstices(year: int):
    if year < 1:
        raise IndexError("Invalid year.")
    days_in_year = getNumDaysInYear(year)
    return [int(days_in_year / 4), int(days_in_year / 2), int(3 * days_in_year / 4), days_in_year]

def getMonthOfDay(year: int, day: int):
    if year < 1:
        raise IndexError("Invalid year.")
    months = getMonths(year)
    month = 0
    while month < len(months):
        if day < months[month]:
            return month
        month += 1
    if day <= getLastMonthEndDay(year):
        return months[-1]
    if day <= getNumDaysInYear(year):
        return len(months) + 1
    raise IndexError("Day is out of bounds.")

def dayToMonthAndDay(year: int, day: int):
    if year < 1:
        raise IndexError("Invalid year.")
    month = getMonthOfDay(year, day)
    months = getMonths(year)
    if month > len(months):
        return month, day - getLastMonthEndDay(year)
    day_in_month = day - months[month - 1] + 1
    if day_in_month > getNumDaysInMonth(year, month):
        raise IndexError("Day is out of bounds.")
    return month, day_in_month


def printCalendarYear(year: int):
    month_start_days = getMonths(year)
    equinoxes_and_solstices = getEquinoxesAndSolstices(year)
    calendar = {}

    sicd = month_start_days[0] - 1
    if sicd != 0:
        calendar[1] = f'{MONTH_NAMES[0]} ({sicd} days)'
    eicd = getLastMonthEndDay(year) + 1
    if eicd <= getNumDaysInYear(year):
        calendar[eicd] = f'{MONTH_NAMES[len(month_start_days) + 1]} ({getNumDaysInYear(year) - eicd + 1} days)'

    for i, start_day in enumerate(month_start_days):
        calendar[start_day] = f'{MONTH_NAMES[(i+1)]} ({getNumDaysInMonth(year, (i+1))} days)'

    for i, es in enumerate(equinoxes_and_solstices):
        month, day = dayToMonthAndDay(year, es)
        event = f'{SE_NAMES[(i+1)]} ({MONTH_NAMES[(month)]} {day})'
        if calendar.get(es) != None:
            calendar[es + 0.5] = event
        else:
            calendar[es] = event

    sorted_calendar = sorted(calendar.items())
    print(f'{year} AF ({getNumDaysInYear(year)} days)')
    for day, event in sorted_calendar:
        print(event)


if __name__ == "__main__":
    try:
        year = int(sys.argv[1])
    except IndexError:
        print("Usage: " + os.path.basename(__file__) + " <year>")
        sys.exit(1)
    printCalendarYear(year)