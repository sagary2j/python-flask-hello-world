"""Hello-birthday API: stores a user's date of birth and greets them."""

import logging
from collections.abc import Callable
from datetime import date

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .config import Settings
from .repository import UserRepository, build_repository
from .routes import bp


def create_app(
    settings: Settings | None = None,
    repository: UserRepository | None = None,
    today: Callable[[], date] = date.today,
) -> Flask:
    settings = settings or Settings.from_env()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    app = Flask(__name__)
    app.extensions["user_repository"] = repository or build_repository(settings)
    app.extensions["today"] = today
    app.register_blueprint(bp)

    @app.errorhandler(HTTPException)
    def handle_http_error(err: HTTPException):
        return jsonify({"error": err.description}), err.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(err: Exception):
        app.logger.exception("Unhandled error")
        return jsonify({"error": "Internal server error"}), 500

    return app
