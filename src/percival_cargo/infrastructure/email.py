"""Email infrastructure."""


def send(*args: object) -> None:
    """Send email."""
    print('SENDING EMAIL:', *args)
