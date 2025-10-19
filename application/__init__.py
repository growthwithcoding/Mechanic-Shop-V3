from flask import Flask
from config import config
from application.extensions import db, ma, limiter, cache, jwt, migrate
from flasgger import Swagger


def create_app(config_name='default'):
    """
    Application Factory Pattern
    Creates and configures the Flask application instance
    
    Args:
        config_name (str): The configuration to use ('development', 'testing', 'production', 'default')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Mechanic Shop API V3",
            "description": "A comprehensive RESTful API for managing a mechanic shop, including customers, vehicles, mechanics, inventory, and service tickets",
            "version": "3.0.0",
            "contact": {
                "name": "API Support",
                "email": "support@mechanicshop.com"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register blueprints
    from application.blueprints.customer import customer_bp
    from application.blueprints.auth import auth_bp
    from application.blueprints.service_ticket import service_ticket_bp
    from application.blueprints.mechanic import mechanic_bp
    from application.blueprints.inventory import inventory_bp
    
    app.register_blueprint(customer_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(service_ticket_bp)
    app.register_blueprint(mechanic_bp)
    app.register_blueprint(inventory_bp)
    
    # Register error handlers for JSON responses
    register_error_handlers(app)
    
    return app


def register_error_handlers(app):
    """
    Register error handlers to ensure all errors return JSON responses
    This is critical for API consistency - all responses must be JSON
    """
    from flask import jsonify
    from werkzeug.exceptions import HTTPException
    from marshmallow import ValidationError
    from sqlalchemy.exc import SQLAlchemyError
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        return jsonify({
            "error": "Bad Request",
            "message": str(error.description) if hasattr(error, 'description') else "Invalid request"
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors"""
        return jsonify({
            "error": "Unauthorized",
            "message": str(error.description) if hasattr(error, 'description') else "Authentication required"
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        return jsonify({
            "error": "Forbidden",
            "message": str(error.description) if hasattr(error, 'description') else "Access denied"
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            "error": "Not Found",
            "message": str(error.description) if hasattr(error, 'description') else "Resource not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        return jsonify({
            "error": "Method Not Allowed",
            "message": str(error.description) if hasattr(error, 'description') else "HTTP method not allowed"
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        return jsonify({
            "error": "Internal Server Error",
            "message": "An internal error occurred"
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle all other HTTP exceptions"""
        return jsonify({
            "error": error.name,
            "message": error.description
        }), error.code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors"""
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        """Handle database errors"""
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "A database error occurred"
        }), 500
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle all other exceptions"""
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error) if app.debug else "An unexpected error occurred"
        }), 500
