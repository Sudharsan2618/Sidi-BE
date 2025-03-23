
from flask import Flask
from flask_cors import CORS
from app.routes.populationDataRoute import population_bp
from app.routes.auth_routes import auth_bp
from app.routes.signup_routes import signup_bp
from app.routes.populationMasterRoute import population_percentage_bp
from app.routes.user_details_route import userdetails_bp



app = Flask(__name__)
CORS(app,origins="*")

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(population_bp)
app.register_blueprint(population_percentage_bp)
app.register_blueprint(userdetails_bp)


if __name__ == '__main__':
    app.run(debug=True)
