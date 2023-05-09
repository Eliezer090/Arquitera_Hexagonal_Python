import pytest
import inject
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import Mock
from pytest_mock import MockFixture
from src.routes.Example.Example import Example
from src.domains.actions import Example_action


@pytest.fixture
def example(mocker: MockFixture) -> Mock:
    return mocker.patch('src.routes.Example.Example.Example')


@pytest.fixture
def injector(example: Mock) -> None:
    inject.clear_and_configure(lambda binder: binder
                               .bind(Example_action, example))


@pytest.fixture
def client(injector: None) -> FlaskClient:
    application = Flask(__name__)
    application.testing = True
    application.register_blueprint(Example())
    return application.test_client()


class TestExample:
    def test_example_record_once(self, client: FlaskClient, example: Mock):
        example.example_record_once()
        assert example.example_record_once.called_once()
