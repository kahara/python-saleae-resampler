"""Resampling functionality"""

import logging
import datetime
from dataclasses import dataclass, field
from typing import TextIO, BinaryIO

from saleae_resampler.reader import Reader

LOGGER = logging.getLogger(__name__)


@dataclass
class Resampler:  # pylint: disable=R0902
    """The resampler"""

    inputstream: TextIO = field()
    outputstream: BinaryIO = field()
    channel: int = field()
    samplerate: float = field()

    def __post_init__(self) -> None:
        """Set up"""

        self.wallclock = datetime.datetime
        self.timestamp = datetime.datetime
        self.next_timestamp = datetime.datetime
        self.bit = False

    def resample(self) -> int:
        """Resample"""

        print(f"{self.inputstream} {self.outputstream} {self.channel} {self.samplerate}")
        reader = Reader(inputstream=self.inputstream, channel=self.channel)

        for (timestamp, sample) in reader.read():
            print(f"{timestamp} {sample}")

        return 0
