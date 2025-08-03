from datetime import (
    datetime,
    timedelta,
    timezone,
)

from backend.configuration.settings import settings


def get_server_time(
        with_server_timezone: bool = False,
) -> datetime:
    """Возвращает текущее серверное время в указанной временной зоне.

    При вызове функции без параметров возвращает время в UTC (UTC+0).
    Если параметр `with_server_timezone` установлен в `True`, возвращается
    время с учётом часового пояса сервера, заданного в настройках (`settings.SERVER_TIMEZONE_UTC_DELTA`).

    Args:
        with_server_timezone (bool): Если True — возвращать время в часовом поясе сервера.
                                     Если False — возвращать время в UTC.

    Returns:
        datetime: Текущее время с соответствующей временной зоной.
    """

    utc_time_delta = timezone(timedelta(hours=0))

    if with_server_timezone:
        utc_timezone_utc_delta = settings.SERVER_TIMEZONE_UTC_DELTA
        utc_time_delta = timezone(timedelta(hours=utc_timezone_utc_delta))

    current_time = datetime.now(utc_time_delta)

    return current_time
