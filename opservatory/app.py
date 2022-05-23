from contextlib import contextmanager
from ipaddress import IPv4Address
from typing import Iterator

from opservatory.exceptions import AccessDenied, MachineAlreadyReserved
from opservatory.infrastructure.communicator import InfrastructureCommunicator
from opservatory.models import Fleet, Machine, Reservation
from opservatory.state.state_repo import StateRepository


@contextmanager
def fleet_context(repo: StateRepository) -> Iterator[Fleet]:
    fleet = repo.read_fleet()
    yield fleet
    repo.save_fleet(fleet)


def update_fleet_facts(comm: InfrastructureCommunicator, repo: StateRepository) -> Fleet:
    with fleet_context(repo) as fleet:
        fleet = comm.gather_facts(fleet)
        return fleet


def update_containers_info(comm: InfrastructureCommunicator, repo: StateRepository) -> Fleet:
    with fleet_context(repo) as fleet:
        fleet = comm.update_machines_info(fleet)
        return fleet


def reserve_machine(repo: StateRepository, machine_ip: IPv4Address, reservation: Reservation):
    with fleet_context(repo) as fleet:
        machine = fleet.find(machine_ip)

        if machine.reservation is not None:
            raise MachineAlreadyReserved(machine_ip)

        machine.reservation = reservation


def cancel_reservation(repo: StateRepository, machine_ip: IPv4Address, username: str):
    with fleet_context(repo) as fleet:
        machine = fleet.find(machine_ip)

        if machine.reservation and machine.reservation.user.credentials.username != username:
            raise AccessDenied(action="Cancellation", username=username)

        machine.reservation = None


def get_fleet_state(repo: StateRepository) -> Fleet:
    return repo.read_fleet()


def free_machines(repo: StateRepository) -> list[Machine]:
    machines = repo.read_fleet().machines
    return [machine for machine in machines if machine.reservation is None and machine.is_free()]
