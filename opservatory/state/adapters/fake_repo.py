from opservatory.models import Fleet
from opservatory.state.state_repo import StateRepository


class FakeStateRepository(StateRepository):
    def __init__(self):
        self.state = Fleet(machines=[])
        super().__init__()

    def save_fleet(self, fleet: Fleet):
        self.state = fleet

    def read_fleet(self) -> Fleet:
        return self.state
