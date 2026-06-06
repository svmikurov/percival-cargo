"""Flask entrypoint."""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def allocate_endpoint() -> str:
    """Allocate."""
    # session = start_session
    return '201'
