from flask import Flask
from .configuration import configure_inject
from .routes.Route_test_api import Route_Test
from .routes.Example import Example

app = Flask(__name__)
configure_inject(app)

app.register_blueprint(Route_Test(), url_prefix='/')
app.register_blueprint(Example())

if __name__ == '__main__':
    app.run(port=8080)
