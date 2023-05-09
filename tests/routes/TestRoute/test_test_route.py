import pytest
import inject
from flask import Flask
from flask.testing import FlaskClient
from src.routes.Route_test_api.Route_test_api import Route_Test

@pytest.fixture
def injector() -> None:
    inject.clear_and_configure()

@pytest.fixture
def client(injector: None) -> FlaskClient:
    application = Flask(__name__)
    application.testing = True
    application.register_blueprint(Route_Test())
    return application.test_client()


class TestRoute:
    def test_get_test_route(self, client: FlaskClient) -> None:
        response = client.get('/')
        assert response.json == {'body': 'Microsservice Running!!'}
