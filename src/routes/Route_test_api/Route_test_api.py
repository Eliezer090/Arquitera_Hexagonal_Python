import inject
from flask import Blueprint, jsonify, Response

@inject.autoparams()
def Route_Test() -> Blueprint:
    test_route_blueprint = Blueprint('Route_Test', __name__)

    @test_route_blueprint.route('/', methods=['GET'])
    def get_test_route() -> Response:
        return jsonify({
            'body': 'Microsservice Running!!'
        })
    
    return test_route_blueprint