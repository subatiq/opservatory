# This test code was written by the `hypothesis.extra.ghostwriter` module
# and is provided under the Creative Commons Zero public domain dedication.

from datetime import datetime
from ipaddress import IPv4Address
from typing import Optional

from hypothesis import given
from hypothesis import strategies as st
from pydantic.types import SecretStr

import opservatory.auth.models
import opservatory.infrastructure.models
import opservatory.models
from opservatory.auth.models import ContactInfo, Credentials, User
from opservatory.models import (OS, AuthConfig, DockerContainer, Machine,
                                MachineState, Memory, Processor, Reservation)


@given(...)
def test_fuzz_AuthConfig(secret_key: SecretStr):
    opservatory.models.AuthConfig(secret_key=secret_key)


@given(...)
def test_fuzz_Config(company_name: str, auth: AuthConfig):
    opservatory.models.Config(company_name=company_name, auth=auth)


@given(tag=st.text(), name=st.text(), uptime=st.integers())
def test_fuzz_DockerContainer(tag, name, uptime):
    opservatory.models.DockerContainer(tag=tag, name=name, uptime=uptime)


@given(...)
def test_fuzz_Fleet(machines: list[Machine]):
    opservatory.models.Fleet(machines=machines)


@given(...)
def test_fuzz_FrontendContext(machines: list[Machine], company_name: str):
    opservatory.models.FrontendContext(machines=machines, company_name=company_name)


@given(...)
def test_fuzz_Machine(
    ip: IPv4Address,
    hostname: str,
    ram: Memory,
    os: OS,
    processor: Processor,
    containers: list[DockerContainer],
    reservation: Optional[Reservation],
    updated_at: datetime,
    state: MachineState,
):
    opservatory.models.Machine(
        ip=ip,
        hostname=hostname,
        ram=ram,
        os=os,
        processor=processor,
        containers=containers,
        reservation=reservation,
        updated_at=updated_at,
        state=state,
    )


@given(...)
def test_fuzz_Memory(free: int, total: int):
    opservatory.models.Memory(free=free, total=total)


@given(...)
def test_fuzz_OS(distribution: str, version: str):
    opservatory.models.OS(distribution=distribution, version=version)


@given(...)
def test_fuzz_Processor(architecture: str, name: str, cores: int):
    opservatory.models.Processor(architecture=architecture, name=name, cores=cores)


@given(...)
def test_fuzz_Reservation(user: User, reason: str):
    opservatory.models.Reservation(user=user, reason=reason)


@given(...)
def test_fuzz_ReservationRequest(reason: str, machine_ip: IPv4Address):
    opservatory.models.ReservationRequest(reason=reason, machine_ip=machine_ip)


@given(...)
def test_fuzz_User(
    name: str, credentials: Credentials, contacts: ContactInfo, privilege: opservatory.auth.models.Privilege
):
    opservatory.models.User(name=name, credentials=credentials, contacts=contacts, privilege=privilege)


@given(...)
def test_fuzz_InventoryMachine(name: str, ip: IPv4Address, username: SecretStr, password: SecretStr):
    opservatory.infrastructure.models.InventoryMachine(name=name, ip=ip, username=username, password=password)
