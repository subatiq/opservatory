from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy

from opservatory.models import Machine, Reservation


def unreserved_machines() -> SearchStrategy[Machine]:
    """
    Returns a machine with no reservation
    """
    return st.builds(Machine, reservation=st.none())


def reserved_machines() -> SearchStrategy[Machine]:
    """
    Returns a machine with a reservation
    """
    return st.builds(Machine, reservation=st.builds(Reservation))
