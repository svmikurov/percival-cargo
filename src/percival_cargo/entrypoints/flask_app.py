"""Flask entrypoint."""

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from percival_cargo import config
from percival_cargo.adapters import orm, repository
from percival_cargo.application import services
from percival_cargo.domain import model

orm.start_mappers()

get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route('/allocate', methods=['GET', 'POST'])
def allocate_endpoint():  # type: ignore
    """Allocate."""
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json['order_id'],
        request.json['sku'],
        request.json['qty'],
    )
    try:
        batch_ref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({'message': str(e)}), 400

    return jsonify({'batch_ref': batch_ref}), 201
