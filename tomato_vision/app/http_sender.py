import urllib.request

from tomato_vision.control.align import Command
from tomato_vision.control.protocol import http_query


def send_state(base_url: str, command: Command, timeout_s: float) -> int:
    with urllib.request.urlopen(base_url + http_query(command), timeout=timeout_s) as response:
        return response.status
