"""CSV reading functionality"""

import csv
import datetime
from dataclasses import dataclass, field
from typing import Tuple, Generator, TextIO

import dateutil.parser


@dataclass
class Reader:
    """The reader"""

    inputstream: TextIO = field()
    channel: int = field()

    def read(self) -> Generator[Tuple[datetime.datetime, bool], None, None]:
        """Return timestamps, bits from CSV file"""

        reader = csv.reader(self.inputstream)
        try:
            next(reader)  # skip header
        except StopIteration:
            return
        for row in reader:
            yield (
                dateutil.parser.parse(row[0]),
                bool(row[self.channel + 1]),
            )  # True if int(row[self.channel + 1]) else False)
