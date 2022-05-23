from hypothesis import given

from opservatory import app
from opservatory.models import Fleet, MachineState
from opservatory.state.adapters.fake_repo import FakeStateRepository


@given(...)
def test_get_free_machines(fleet: Fleet):
    repo = FakeStateRepository()
    repo.save_fleet(fleet)

    free_machines = app.free_machines(repo=repo)

    for machine in free_machines:
        assert machine.reservation is None
        assert machine.state == MachineState.FREE
