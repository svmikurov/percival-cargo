"""API tests."""

import uuid

import pytest
import requests

import percival_cargo.config as config


def random_suffix() -> str:
    return uuid.uuid4().hex[:6]


def random_sku(name: str = '') -> str:
    return f'sku-{name}-{random_suffix()}'


def random_batch_ref(name: str = '') -> str:
    return f'batch-{name}-{random_suffix()}'


def random_order_id(name: str = '') -> str:
    return f'order-{name}-{random_suffix()}'


@pytest.mark.skip('deprecated then application layer service has been added')
@pytest.mark.e2e
@pytest.mark.usefixtures('restart_api')
def test_api_returns_allocation(add_stock) -> None:  # type: ignore
    sku, other_sku = random_sku(), random_sku('other')
    early_batch = random_batch_ref('1')
    later_batch = random_batch_ref('2')
    other_batch = random_batch_ref('3')

    add_stock(
        [
            (later_batch, sku, 100, '2011-01-02'),
            (early_batch, sku, 100, '2011-01-01'),
            (other_batch, other_sku, 100, None),
        ]
    )

    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()

    r = requests.post(f'{url}/allocate', json=data)  # type: ignore

    assert r.status_code == 201
    assert r.json()['batch_ref'] == early_batch


@pytest.mark.e2e
@pytest.mark.usefixtures('restart_api')
def test_happy_path_returns_201_and_allocated_batch(add_stock) -> None:  # type: ignore
    # Arrange
    sku, other_sku = random_sku(), random_sku('other')
    early_batch = random_batch_ref('1')
    later_batch = random_batch_ref('2')
    other_batch = random_batch_ref('3')
    add_stock(
        [
            (later_batch, sku, 100, '2011-01-02'),
            (early_batch, sku, 100, '2011-01-01'),
            (other_batch, other_sku, 100, None),
        ]
    )
    data = {'order_id': random_order_id(), 'sku': sku, 'qty': 3}
    url = config.get_api_url()

    # Act
    r = requests.post(f'{url}/allocate', json=data)  # type: ignore

    # Assert
    assert r.status_code == 201
    assert r.json()['batch_ref'] == early_batch


@pytest.mark.e2e
@pytest.mark.usefixtures('restart_api')
def test_unhappy_path_returns_400_and_error_message() -> None:
    # Arrange
    unknown_sku, order_id = random_sku(), random_order_id()
    data = {'order_id': order_id, 'sku': unknown_sku, 'qty': 20}
    url = config.get_api_url()

    # Act
    r = requests.post(f'{url}/allocate', json=data)  # type: ignore

    # Assert
    assert r.status_code == 400
    assert r.json()['message'] == f'Недопустимый артикул {unknown_sku}'
