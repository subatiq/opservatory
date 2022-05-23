class MachineAlreadyReserved(Exception):
    pass


class MachineNotFound(Exception):
    pass


class AccessDenied(Exception):
    def __init__(self, action: str, username: str):
        super().__init__(f"Access denied for user {username}: {action}")
