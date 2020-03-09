import sys
from datetime import datetime
from time import sleep

import requests


def get_timestamp() -> str:
    return f'[{datetime.now().__str__()}]'


def _log_with_timestamp(message: str, line_ending='\n') -> None:
    print(f'{get_timestamp()} {message}', end=line_ending)


def _get_status_icon(status: int) -> str:
    return '🟩' if status < 400 else '🟥'


def _log_status(url: str, status: int, latency: int) -> None:
    message = 'No response 👻'

    if status:
        message = f'{url} {_get_status_icon(status)} ⏱ {latency}ms'

    _log_with_timestamp(message, line_ending='\r')


def _perform_get(url: str):
    try:
        return requests.head(url)
    except requests.exceptions.ConnectionError:
        return None


if __name__ == '__main__':
    url = sys.argv[1]
    seconds_delay_between_attempts = 5

    _log_with_timestamp(
        f'Probing {url} every {seconds_delay_between_attempts} seconds...',
    )

    try:
        previous_status = None

        while True:
            response = _perform_get(url)
            latency = status = None

            if response is not None:
                latency = response.elapsed.microseconds / 10000
                status = response.status_code

            if status != previous_status:
                _log_with_timestamp(f'{url} ⚠️ {previous_status} -> {status}')

            _log_status(url, status, latency)

            previous_status = status

            sleep(seconds_delay_between_attempts)
    except KeyboardInterrupt:
        print('\r')
        _log_with_timestamp('Goodbye')
