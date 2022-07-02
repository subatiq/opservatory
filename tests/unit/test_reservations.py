import pytest
from hypothesis import assume, given

from opservatory import app, models
from opservatory.exceptions import AccessDenied, MachineAlreadyReserved
from opservatory.state.adapters.fake_repo import FakeStateRepository
from tests.unit.strategies import reserved_machines, unreserved_machines


@given(machine=unreserved_machines(), reservation=...)
def test_reserve_free_machine(machine: models.Machine, reservation: models.Reservation):
    """Tests that unreserved machine can be reserved"""
    fleet = models.Fleet(machines=[machine])
    machine.reservation = None

    repo = FakeStateRepository()
    repo.save_fleet(fleet)

    app.reserve_machine(repo=repo, machine_ip=machine.ip, reservation=reservation)

    assert len(repo.read_fleet().machines) == 1
    assert repo.read_fleet().machines[0].reservation == reservation


@given(machine=reserved_machines(), reservation=...)
def test_cant_reserve_occupied(machine: models.Machine, reservation: models.Reservation):
    """Tests that reserved machine can't be reserved again"""
    fleet = models.Fleet(machines=[machine])

    repo = FakeStateRepository()
    repo.save_fleet(fleet)

    assert machine.reservation is not None

    with pytest.raises(MachineAlreadyReserved):
        app.reserve_machine(repo=repo, machine_ip=machine.ip, reservation=reservation)

    assert len(repo.read_fleet().machines) == 1
    assert machine.reservation == repo.read_fleet().machines[0].reservation


@given(machine=reserved_machines())
def test_cancel_reservation(machine: models.Machine):
    """Tests that reservation can be cancelled"""
    fleet = models.Fleet(machines=[machine])

    repo = FakeStateRepository()
    repo.save_fleet(fleet)

    assert machine.reservation is not None

    app.cancel_reservation(
        repo=repo, machine_ip=machine.ip, username=machine.reservation.user.credentials.username
    )

    assert len(repo.read_fleet().machines) == 1
    assert repo.read_fleet().machines[0].reservation is None


@given(machine=reserved_machines(), username=...)
def test_unauthorized_cancelation(machine: models.Machine, username: str):
    """Tests that unreserved machine can't be cancelled"""
    assert machine.reservation is not None
    assume(username != machine.reservation.user.credentials.username)

    fleet = models.Fleet(machines=[machine])

    repo = FakeStateRepository()
    repo.save_fleet(fleet)

    with pytest.raises(AccessDenied):
        app.cancel_reservation(repo=repo, machine_ip=machine.ip, username=username)

    assert len(repo.read_fleet().machines) == 1
    assert repo.read_fleet().machines[0].reservation == machine.reservation
