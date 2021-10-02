"""CSV reading functionality"""
# pylint: disable=W1203

# import ctypes
import logging
from dataclasses import dataclass, field
from typing import BinaryIO

LOGGER = logging.getLogger(__name__)


@dataclass
class Writer:
    """The writer"""

    outputstream: BinaryIO = field()

    def __post_init__(self) -> None:
        """Byte to write out"""

        self.byte: int = 0
        self.bit: int = 0

    def write(self, bit: bool) -> None:
        """Pack bits into bytes"""

        self.byte = self.byte | (bit << self.bit)
        LOGGER.debug(f"0x{self.byte:X} {bit:x}")
        self.bit += 1
        if self.bit == 8:
            self.outputstream.write(bytes([self.byte]))
            LOGGER.info(f"wrote 0x{self.byte:X}")
            self.byte = 0
            self.bit = 0

    def __del__(self) -> None:
        """Write out zeros if mid-byte at exit"""

        if self.bit:
            for _ in range(self.bit, 8):
                self.write(False)
