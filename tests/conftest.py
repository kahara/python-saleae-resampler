"""Test fixtures"""
from typing import Any
import asyncio
from pathlib import Path
import logging

import tomlkit  # type: ignore
import pytest
from datastreamcorelib.testhelpers import nice_tmpdir  # pylint: disable=W0611
from datastreamcorelib.logging import init_logging
from datastreamservicelib.reqrep import REPMixin, REQMixin
from datastreamservicelib.service import SimpleService

from saleae_resampler.defaultconfig import DEFAULT_CONFIG_STR
from saleae_resampler.service import Saleae_resamplerService


# pylint: disable=W0621
init_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)


class ExampleREPlier(REPMixin, SimpleService):
    """Implement simple REPly interface, you can use this to mock some other services REPly API"""

    async def echo(self, *args: Any) -> Any:
        """return the args"""
        _ = self
        await asyncio.sleep(0.01)
        return args


class ExampleREQuester(REQMixin, SimpleService):
    """Can be used to test Saleae_resamplerService REP api via REQuests from outside"""


@pytest.fixture
@pytest.mark.asyncio
async def service_instance(nice_tmpdir):  # type: ignore
    """Create a service instance for use with tests"""
    parsed = tomlkit.parse(DEFAULT_CONFIG_STR)
    # Do not bind to TCP socket for testing and use test specific temp directory
    parsed["zmq"]["pub_sockets"] = ["ipc://" + str(Path(nice_tmpdir) / "saleae_resampler_pub.sock")]
    parsed["zmq"]["rep_sockets"] = ["ipc://" + str(Path(nice_tmpdir) / "saleae_resampler_rep.sock")]
    # Write a testing config file
    configpath = Path(nice_tmpdir) / "saleae_resampler_testing.toml"
    with open(configpath, "wt", encoding="utf-8") as fpntr:
        fpntr.write(tomlkit.dumps(parsed))
    # Instantiate service and return it
    serv = Saleae_resamplerService(configpath)
    return serv


@pytest.fixture
@pytest.mark.asyncio
async def replier_instance(nice_tmpdir):  # type: ignore
    """Create a replier instance for use with tests"""
    parsed = tomlkit.parse(DEFAULT_CONFIG_STR)
    # Do not bind to TCP socket for testing and use test specific temp directory
    parsed["zmq"]["pub_sockets"] = ["ipc://" + str(Path(nice_tmpdir) / "saleae_resampler_replier_pub.sock")]
    parsed["zmq"]["rep_sockets"] = ["ipc://" + str(Path(nice_tmpdir) / "saleae_resampler_replier_rep.sock")]
    # Write a testing config file
    configpath = Path(nice_tmpdir) / "saleae_resampler_testing_replier.toml"
    with open(configpath, "wt", encoding="utf-8") as fpntr:
        fpntr.write(tomlkit.dumps(parsed))
    # Instantiate service and return it
    serv = ExampleREPlier(configpath)
    return serv


@pytest.fixture
@pytest.mark.asyncio
async def requester_instance(nice_tmpdir):  # type: ignore
    """Create a requester instance for use with tests"""
    parsed = tomlkit.parse(DEFAULT_CONFIG_STR)
    # Do not bind to TCP socket for testing and use test specific temp directory
    parsed["zmq"]["pub_sockets"] = ["ipc://" + str(Path(nice_tmpdir) / "saleae_resampler_requester_pub.sock")]
    # Write a testing config file
    configpath = Path(nice_tmpdir) / "saleae_resampler_testing_requester.toml"
    with open(configpath, "wt", encoding="utf-8") as fpntr:
        fpntr.write(tomlkit.dumps(parsed))
    # Instantiate service and return it
    serv = ExampleREQuester(configpath)
    return serv


@pytest.fixture
@pytest.mark.asyncio
async def running_service_instance(service_instance):  # type: ignore
    """Yield a running service instance, shut it down after the test"""
    task = asyncio.create_task(service_instance.run())
    # Yield a moment so setup can do it's thing
    await asyncio.sleep(0.1)

    yield service_instance

    service_instance.quit()

    try:
        await asyncio.wait_for(task, timeout=2)
    except TimeoutError:
        task.cancel()
    finally:
        # Clear alarms and default exception handlers
        Saleae_resamplerService.clear_exit_alarm()
        asyncio.get_event_loop().set_exception_handler(None)


@pytest.fixture
@pytest.mark.asyncio
async def running_requester_instance(requester_instance):  # type: ignore
    """Yield a running service instance, shut it down after the test"""
    task = asyncio.create_task(requester_instance.run())
    # Yield a moment so setup can do it's thing
    await asyncio.sleep(0.1)

    yield requester_instance

    requester_instance.quit()

    try:
        await asyncio.wait_for(task, timeout=2)
    except TimeoutError:
        task.cancel()
    finally:
        # Clear alarms and default exception handlers
        ExampleREQuester.clear_exit_alarm()
        asyncio.get_event_loop().set_exception_handler(None)


@pytest.fixture
@pytest.mark.asyncio
async def running_replier_instance(replier_instance):  # type: ignore
    """Yield a running service instance, shut it down after the test"""
    task = asyncio.create_task(replier_instance.run())
    # Yield a moment so setup can do it's thing
    await asyncio.sleep(0.1)

    yield replier_instance

    replier_instance.quit()

    try:
        await asyncio.wait_for(task, timeout=2)
    except TimeoutError:
        task.cancel()
    finally:
        # Clear alarms and default exception handlers
        ExampleREPlier.clear_exit_alarm()
        asyncio.get_event_loop().set_exception_handler(None)
