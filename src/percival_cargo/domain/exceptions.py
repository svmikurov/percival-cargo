"""Domain exceptions."""


class OutOfBatch(Exception):
    """Raises then order line is not allocated at batch."""


class OutOfStock(OutOfBatch):
    """Raises then order line is not allocated at stock."""
