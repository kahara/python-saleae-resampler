"""CLI entrypoints for python-saleae-resampler"""
from typing import TextIO, BinaryIO
import sys
import logging
from pathlib import Path

import click
from libadvian.logging import init_logging

from saleae_resampler import __version__
from saleae_resampler.resampler import Resampler


LOGGER = logging.getLogger(__name__)


@click.command()
@click.version_option(version=__version__)
@click.option("-l", "--loglevel", help="Python log level, 10=DEBUG, 20=INFO, 30=WARNING, 40=CRITICAL", default=30)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug loglevel (-v/-vv)")
@click.option("-c", "--channel", required=True, help="Channel number 0..")
@click.option("-r", "--samplerate", required=True, help="Resampling rate")
@click.argument("inputpath", type=click.Path())
@click.argument("outputpath", type=click.Path())
def saleae_resampler_cli(  # pylint: disable=R0913
    inputpath: Path,
    outputpath: Path,
    channel: int,
    samplerate: float,
    loglevel: int,
    verbose: int,
) -> None:
    """Resample input to output at given rate"""

    inputstream: TextIO
    outputstream: BinaryIO

    if verbose == 1:
        loglevel = 20
    if verbose >= 2:
        loglevel = 10

    init_logging(loglevel)
    LOGGER.setLevel(loglevel)

    with open(inputpath, "r", encoding="utf8") as inputstream:
        with open(outputpath, "wb") as outputstream:
            resampler = Resampler(
                inputstream=inputstream, outputstream=outputstream, channel=int(channel), samplerate=float(samplerate)
            )
            sys.exit(resampler.resample())
