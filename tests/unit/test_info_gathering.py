from copy import deepcopy

from hypothesis import given
from hypothesis import strategies as st

from opservatory import app
from opservatory.infrastructure.fake_comm import FakeCommunicator
from opservatory.models import Fleet, MachineState
from opservatory.state.adapters.fake_repo import FakeStateRepository


@given(test_data=st.data(), fleet=...)
def test_fleet_facts_update(test_data, fleet: Fleet):
    repo = FakeStateRepository()
    comm = FakeCommunicator(test_data)

    repo.save_fleet(fleet)
    before_update = deepcopy(repo.read_fleet())

    updated = app.update_fleet_facts(repo=repo, comm=comm)

    assert len(updated.machines) == len(fleet.machines)
    assert len(repo.read_fleet().machines) == len(fleet.machines)

    for machine in updated.machines:
        if machine.state == MachineState.UNREACHABLE:
            continue
        assert before_update.ip2machine[machine.ip].state == machine.state


@given(test_data=st.data(), fleet=...)
def test_containers_info_update(test_data, fleet: Fleet):
    repo = FakeStateRepository()
    comm = FakeCommunicator(test_data)

    repo.save_fleet(fleet)
    updated = app.update_containers_info(repo=repo, comm=comm)

    assert len(updated.machines) == len(fleet.machines)
    assert len(repo.read_fleet().machines) == len(fleet.machines)

    for machine in updated.machines:
        if machine.reservation:
            assert machine.state == MachineState.RESERVED

        elif machine.state != MachineState.UNREACHABLE:
            if machine.containers:
                assert machine.state == MachineState.BUSY
            else:
                assert machine.state == MachineState.FREE

        else:
            assert machine.state == MachineState.UNREACHABLE
