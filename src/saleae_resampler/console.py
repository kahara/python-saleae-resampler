"""CLI entrypoints for python-saleae-resampler"""
from typing import Any
import asyncio
import sys
import logging
from pathlib import Path

import click

from datastreamcorelib.logging import init_logging
from saleae_resampler.defaultconfig import DEFAULT_CONFIG_STR
from saleae_resampler import __version__
from saleae_resampler.service import Saleae_resamplerService


LOGGER = logging.getLogger(__name__)


def dump_default_config(ctx: Any, param: Any, value: bool) -> None:  # pylint: disable=W0613
    """Print the default config and exit"""
    if not value:
        return
    click.echo(DEFAULT_CONFIG_STR)
    if ctx:
        ctx.exit()


@click.command()
@click.version_option(version=__version__)
@click.option("-l", "--loglevel", help="Python log level, 10=DEBUG, 20=INFO, 30=WARNING, 40=CRITICAL", default=30)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug loglevel (-v/-vv)")
@click.option(
    "--defaultconfig",
    is_flag=True,
    callback=dump_default_config,
    expose_value=False,
    is_eager=True,
    help="Show default config",
)
@click.argument("configfile", type=click.Path(exists=True))
def saleae_resampler_cli(configfile: Path, loglevel: int, verbose: int) -> None:
    """My "brilliant" desc"""
    if verbose == 1:
        loglevel = 20
    if verbose >= 2:
        loglevel = 10
    init_logging(loglevel)
    LOGGER.setLevel(loglevel)

    service_instance = Saleae_resamplerService(Path(configfile))

    exitcode = asyncio.get_event_loop().run_until_complete(service_instance.run())
    sys.exit(exitcode)
