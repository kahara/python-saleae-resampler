"""Resampling functionality"""
# pylint: disable=W1203,W1309

import logging
import datetime
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Union, TextIO, BinaryIO

import yaml

from saleae_resampler.reader import Reader
from saleae_resampler.writer import Writer

LOGGER = logging.getLogger(__name__)


@dataclass
class Resampler:  # pylint: disable=R0902
    """The resampler"""

    inputstream: TextIO = field()
    outputstream: BinaryIO = field()
    channel: int = field()
    samplerate: float = field()

    def resample(self) -> int:
        """Resample"""

        timestep: datetime.timedelta = datetime.timedelta(seconds=1.0 / self.samplerate)
        wallclock: datetime.datetime
        timestamp: datetime.datetime
        next_timestamp: datetime.datetime
        bit: bool = False
        next_bit: bool = False
        points: List[Tuple[float, bool]] = []
        output_points: List[bool] = []
        count: int = 1

        reader = Reader(inputstream=self.inputstream, channel=self.channel)
        records = reader.read()
        writer = Writer(outputstream=self.outputstream)

        try:
            (wallclock, bit) = next(records)
            timestamp = wallclock
            writer.write(bit)
            points.append((0.0, bit))
            output_points.append(bit)
        except StopIteration:
            LOGGER.error("Could not read records, failing.")
            return 1

        for (next_timestamp, next_bit) in records:
            LOGGER.debug(f"{timestamp} {bit}")
            points.append(((next_timestamp - timestamp).total_seconds(), bit))

            while wallclock < next_timestamp:
                LOGGER.debug(f"{wallclock} {bit}")
                writer.write(bit)
                output_points.append(bit)
                count += 1
                if not count % 100000:
                    self.outputstream.flush()
                    LOGGER.info(f"at: {count}")
                wallclock += timestep

            timestamp = next_timestamp
            bit = next_bit

        del writer  # flush

        self.stats(points, output_points)

        return 0

    @classmethod
    def stats(cls, points: List[Tuple[float, bool]], output_points: List[bool]) -> None:
        """Report stats"""

        stats: Dict[str, Union[int, float]] = {
            "0": int(0),
            "1": int(0),
            "min": float("inf"),
            "max": float("-inf"),
            "med": 0.0,
            "1st": 0.0,
            "3rd": 0.0,
        }

        intervals: List[float] = [point[0] for point in points[1:]]

        stats["0"] = sum([not bit for bit in output_points])
        stats["1"] = sum(list(output_points))
        stats["min"], stats["1st"], stats["med"], stats["3rd"], stats["max"] = cls.fivenum(intervals)

        stats[f"minf"] = 1.0 / (stats["max"] * 2) if stats["max"] else 0.0
        stats[f"1stf"] = 1.0 / (stats["3rd"] * 2) if stats["3rd"] else 0.0
        stats[f"medf"] = 1.0 / (stats["med"] * 2) if stats["med"] else 0.0
        stats[f"3rdf"] = 1.0 / (stats["1st"] * 2) if stats["1st"] else 0.0
        stats[f"maxf"] = 1.0 / (stats["min"] * 2) if stats["min"] else 0.0

        print(yaml.safe_dump(stats))

    @classmethod
    def fivenum(cls, intervals: List[float]) -> List[float]:
        """Five-number summary"""

        # count: int = len(intervals)
        # even: bool = not count % 2
        # lower: List[float] = intervals[:count] if even else intervals[: count + 1]
        # upper: List[float] = intervals[count:] if even else intervals[: count + 1]
        summary: List[float] = [0.0 for _ in range(5)]

        intervals = sorted(intervals)

        # min
        summary[0] = intervals[0]

        # FIXME: these
        # 1st
        summary[1] = 0.0
        # median
        summary[2] = 0.0
        # 3rd
        summary[3] = 0.0

        # max
        summary[4] = intervals[-1]

        return summary
