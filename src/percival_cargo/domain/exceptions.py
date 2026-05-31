"""Domain exceptions."""


class OutOfBatchException(Exception):
    """Raises then order line is not allocated at batch."""


class OutOfStockException(OutOfBatchException):
    """Raises then order line is not allocated at stock."""
