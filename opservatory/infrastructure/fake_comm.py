from datetime import datetime

from hypothesis import strategies as st
from hypothesis.strategies import DataObject

from opservatory.infrastructure.communicator import InfrastructureCommunicator
from opservatory.models import OS, DockerContainer, Fleet, Machine, Memory, Processor


class FakeCommunicator(InfrastructureCommunicator):
    def __init__(self, test_data: DataObject) -> None:
        self._test_data = test_data
        super().__init__()

    def _cheak_reachability(self, machine: Machine) -> bool:
        reachable = self._test_data.draw(st.booleans())
        if not reachable:
            machine.connection_broken()

        return reachable

    def gather_facts(self, fleet: Fleet) -> Fleet:
        for machine in fleet.machines:
            if not self._cheak_reachability(machine):
                continue

            machine.os = self._test_data.draw(st.builds(OS))
            machine.ram = self._test_data.draw(st.builds(Memory))
            machine.processor = self._test_data.draw(st.builds(Processor))
            machine.hostname = self._test_data.draw(st.text())
            machine.updated_at = datetime.now()

        return fleet

    def update_machines_info(self, fleet: Fleet) -> Fleet:
        for machine in fleet.machines:
            if not self._cheak_reachability(machine):
                continue

            machine.containers = self._test_data.draw(st.lists(st.builds(DockerContainer)))

        return fleet
