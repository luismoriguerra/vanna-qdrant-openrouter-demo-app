from flask import Flask, jsonify
from app.api.routes.question_routes import question_bp
from app.models.responses import success_response

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(question_bp, url_prefix='/api')
    
    # Root endpoint
    @app.route('/')
    def hello():
        return jsonify(success_response({
            "message": "Hello world, welcome to Railway!"
        }))
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 