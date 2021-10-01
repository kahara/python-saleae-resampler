"""Resampling functionality"""

import logging
import datetime
from dataclasses import dataclass, field
from typing import Dict, TextIO, BinaryIO

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

        stats: Dict[str, Dict[str, float]] = {
            "input": {
                "min": float("inf"),
                "max": float("-inf"),
            },
            "bytes": {
                "0": int(0),
                "1": int(0),
            },
        }

        print(f"{self.inputstream} {self.outputstream} {self.channel} {self.samplerate}")
        reader = Reader(inputstream=self.inputstream, channel=self.channel)

        for (timestamp, sample) in reader.read():
            print(f"{timestamp} {sample}")

        print(f"""input:\n  min:\t{stats["input"]["min"]}\n  max:\t{stats["input"]["max"]}""")
        print(f"""bytes:\n    0:\t{stats["bytes"]["0"]}\n    1:\t{stats["bytes"]["1"]}""")

        return 0
