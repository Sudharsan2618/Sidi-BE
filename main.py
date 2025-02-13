
from flask import Flask
from flask_cors import CORS
from app.routes.populationDataRoute import population_bp

app = Flask(__name__)
CORS(app,origins="*")

# Register blueprints
app.register_blueprint(population_bp)


if __name__ == '__main__':
    app.run(debug=True)
