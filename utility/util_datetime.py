import pytz
import calendar
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import dateutil.relativedelta

month_name = {
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
    "Jan": "1",
    "Feb": "2",
    "Mar": "3",
    "Apr": "4",
    "May": "5",
    "Jun": "6",
    "Jul": "7",
    "Aug": "8",
    "Sep": "9",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return dt_mtn


def get_expired_date():
    today = tzware_datetime()
    dates = today + dateutil.relativedelta.relativedelta(months=2)
    return dates


def before_month():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    # return datetime.now(pytz.utc)
    today = date.today()
    day = today - dateutil.relativedelta.relativedelta(months=3)
    return day


def days_between(d1, d2, issue):
    results = ''
    d1 = datetime.strptime(str(d1), '%Y-%m-%d %H:%M:%S.%f')
    d2 = datetime.strptime(str(d2), '%Y-%m-%d %H:%M:%S.%f')
    d3 = (d1 - d2)
    seconds = d3.total_seconds()
    # hours = seconds // 3600
    # minutes = (seconds % 3600) // 60
    # seconds = seconds % 60
    if issue:
        if issue.remarks == '30min':
            if seconds <= 1800:
                results = 'On_Time'
            else:
                results = 'Not_On_Time'
        elif issue.remarks == '3hours':
            if seconds <= 10800:
                results = 'On_Time'
            else:
                results = 'Not_On_Time'
        elif issue.remarks == '1hours':
            if seconds <= 3600:
                results = 'On_Time'
            else:
                results = 'Not_On_Time'
    return results


def technical_ticket_ots(d1, d2, issue_days):
    results = ''
    d1 = datetime.strptime(str(d1), '%Y-%m-%d %H:%M:%S.%f')
    d2 = datetime.strptime(str(d2), '%Y-%m-%d %H:%M:%S.%f')
    d3 = (d1 - d2)
    seconds = d3.total_seconds()
    # hours = seconds // 3600
    # minutes = (seconds % 3600) // 60
    # seconds = seconds % 60
    if issue_days:
        if seconds <= issue_days * 86400:
            results = 'On_Time'
        else:
            results = 'Not_On_Time'
    return results


def args_to_date(date_string):
    if len(date_string) == 19:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    elif len(date_string) == 16:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
    else:
        return None


def shift_day():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    today = date.today()
    hour = datetime.now().hour
    if hour in [0, 1, 2, 3, 4, 5, 6]:
        # today = today - dateutil.relativedelta.relativedelta(day=1)
        startday = today - timedelta(days=1)
        return startday.strftime('%b%d%Y')
    else:
        return today.strftime('%b%d%Y')


def bill_month_name(today=date.today()):
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    if today.day > 5:
        return today.strftime('%b%Y')
    else:
        day = today - dateutil.relativedelta.relativedelta(months=1)
        return day.strftime('%b%Y')


def pub_bill_close_month_name(journal_date):
    t = datetime.strptime(journal_date, '%d-%m-%Y')
    day = datetime.strptime(journal_date, '%d-%m-%Y') - dateutil.relativedelta.relativedelta(months=1)
    return day.strftime('%b%Y')


def bill_month_name_discount_budget(today=date.today()):
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    if today.day > 10:
        return today.strftime('%b%Y')
    else:
        day = today - dateutil.relativedelta.relativedelta(months=1)
        return day.strftime('%b%Y')


def date_months_name_range(date1, date2):
    date1 = date1.replace(day=1)
    date2 = date2.replace(day=1)
    months_str = calendar.month_name
    range_months = []
    first_month = date1.strftime('%b%Y')
    last_month = ''
    while date1 < date2:
        month = date1.month
        year = date1.year
        month_str = months_str[month][0:3]
        range_months.append("{0}{1}".format(month_str, str(year)[-0:]))
        last_month = date1.strftime('%b%Y')
        next_month = month + 1 if month != 12 else 1
        next_year = year + 1 if next_month == 1 else year
        date1 = date1.replace(month=next_month, year=next_year)
    return first_month, last_month, range_months


def date_months_name_range_with_dash(date1, date2):
    date1 = date1.replace(day=1)
    date2 = date2.replace(day=1)
    months_str = calendar.month_name
    range_months = []
    first_month = date1.strftime('%b-%Y')
    last_month = ''
    while date1 < date2:
        month = date1.month
        year = date1.year
        month_str = months_str[month][0:3]
        range_months.append("{0}-{1}".format(month_str, str(year)[-0:]))
        last_month = date1.strftime('%b-%Y')
        next_month = month + 1 if month != 12 else 1
        next_year = year + 1 if next_month == 1 else year
        date1 = date1.replace(month=next_month, year=next_year)
    return first_month, last_month, range_months


def bill_justified_close(end_date=date.today()):
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    if end_date.day > 24:
        start_date = end_date.replace(day=25)
    else:
        start_date = end_date - dateutil.relativedelta.relativedelta(months=1)
        start_date = start_date.replace(day=25)
    return start_date, end_date


def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def bill_extra_name(bill_month):
    month = bill_month[:3]
    year = bill_month[3:]
    month_index = int(month_name[month])
    month_list = []
    for i in range(1, month_index):
        month_list.append(month_name[str(i)] + year)
    return year, month_list


def journal_id():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return dt_mtn.strftime('%b%d%Y')


def payment_month_number():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return int(dt_mtn.strftime('%m'))


def year_number():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return dt_mtn.strftime('%Y')


def jour_date():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return dt_mtn


def tz_datetime_Mogadishu():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return dt_mtn


def journal_id_meter_change():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    dt_utcnow = datetime.now(tz=pytz.UTC)
    dt_mtn = dt_utcnow.astimezone(pytz.timezone('Africa/Mogadishu'))
    return dt_mtn.strftime('%b%Y%d')


def tran_month_name(journal):
    """
    Return a timezone aware datetime.
    :return: Datetime
    """
    today = datetime.strptime(journal, '%b%d%Y')
    if today.day <= 24:
        return today.strftime('%b%Y')
    else:
        day = today + dateutil.relativedelta.relativedelta(months=1)
        return day.strftime('%b%Y')


def get_close_journal():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    today = date.today()
    if today.day > 24:
        today = today.replace(day=25)
        return today.strftime('%b%d%Y')
    else:
        today = today - dateutil.relativedelta.relativedelta(months=1)
        today = today.replace(day=25)
    return today.strftime('%b%d%Y')


def payment_month_name(journal):
    """
    Return a timezone aware datetime.
    :return: Datetime
    """
    today = datetime.strptime(journal, '%b%d%Y')

    return today.strftime('%b%Y')


def timedelta_months(months, compare_date=None):
    """
    Return a new datetime with a month offset applied.

    :param months: Amount of months to offset
    :type months: int
    :param compare_date: Date to compare at
    :type compare_date: date
    :return: datetime
    """
    if compare_date is None:
        compare_date = date.today()

    delta = months * 365 / 12
    compare_date_with_delta = compare_date + timedelta(delta)

    return compare_date_with_delta


def to_date(date_string):
    """

    :param date_string:
    :return:
    """
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def to_date_end(date_string):
    """
    :param date_string:
    :return:
    """
    end_date = datetime.strptime(date_string, "%Y-%m-%d").date()
    end_date = datetime.combine(end_date, datetime.min.time())
    return end_date.replace(minute=59, hour=23, second=59)


def start_range(year, m):
    return to_date(year + "-{:02d}".format(m) + "-25")


def end_range(year, m):
    if m >= 12:
        n = 1
        year = str(int(year) + 1)
    else:
        n = m + 1
    return to_date(year + "-{:02d}".format(n) + "-24")


def get_prev_bill_month(month):
    mydate = datetime.strptime(str(month), "%b%Y")
    prem = mydate + dateutil.relativedelta.relativedelta(months=-1)
    return prem.strftime("%b%Y")


def get_month_day_range(date):
    """
    For a date 'date' returns the start and end date for the month of 'date'.
    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))
    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    last_day = date + relativedelta(day=1, months=+1, days=-1)
    first_day = date + relativedelta(day=1)
    return first_day, last_day


def date_diff_of_days(end_date, start_date):
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
    date1 = str(end_date.strftime('%Y-%m-%d %H:%M:%S.%f'))
    date2 = str(start_date.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return datetime.strptime(date1, datetimeFormat) - datetime.strptime(date2, datetimeFormat)
