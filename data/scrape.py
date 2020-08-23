import requests
from typing import Optional

historical_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
live_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv"


def get_historical():
    """
    Fetch a bunch of historical data from the New York Times' GitHub Repository and save it to disk
    """
    request = requests.get(historical_url)
    text = request.text
    i = 0
    while text[i] != '\n':
        i += 1

    first = text[0:i]
    columns = first.split(",")
    date_column = columns.index('date')
    text = text[i+1:]

    lines = Queue()

    line = ""
    for char in text:
        if char == '\n':
            lines.enqueue(line)
            line = ""
        else:
            line += char

    kek = lines.dequeue()
    f = None
    root = "historical"
    while kek is not None:
        if f is not None:
            if str(f.name) != root + "/" + kek.split(",")[date_column] + ".csv":
                f = open(root + "/" + kek.split(",")[date_column] + ".csv", "w")
        else:
            f = open(root + "/" + kek.split(",")[date_column] + ".csv", "w")
        f.write(kek + "\n")

        kek = lines.dequeue()

    f.close()

def get_historical_in_one():
    request = requests.get(historical_url)
    f = open("all_historical.csv", "w")
    f.write(request.text)


def get_live():
    """
    Fetch today's data from the New York Times' GitHub repository and save it to disk
    """
    request = requests.get(live_url)
    f = open("live.csv", "w")
    f.write(request.text)
    f.close()


class Queue:
    class _Node:
        def __init__(self, val: str):
            self.next = None
            self.val = val

    def __init__(self):
        self._first = None
        self._tail = None

    def enqueue(self, val: str):
        if self._tail is None:
            self._tail = self._Node(val)
            self._first = self._tail
        else:
            self._tail.next = self._Node(val)
            self._tail = self._tail.next

    def dequeue(self) -> Optional[str]:
        if self._first is None:
            return None
        else:
            val = self._first.val
            self._first = self._first.next
            if self._first is None:
                self._tail = None
            return val


if __name__ == "__main__":
    get_historical()
    get_live()
    # get_historical_in_one()