from flask import Flask
from flask_migrate import Migrate
from .database import db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/hotel_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app