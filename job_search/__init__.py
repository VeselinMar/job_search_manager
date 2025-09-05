from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import time
import psycopg2

db = SQLAlchemy()
migrate = Migrate()

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.environ["POSTGRES_DB"],
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                host="db"
            )
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            print("Db not ready, retrying in 2 seconds...")
            time.sleep(2)

def create_app():

    database_url = os.environ.get("DATABASE_URL")
    secret_key = os.environ.get("SECRET_KEY")

    if not database_url or not secret_key:
        raise RuntimeError("DATABASE_URL and SECRET_KEY must be set in the environment!")

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = secret_key

    wait_for_db()
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    return app