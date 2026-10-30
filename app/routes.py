from datetime import date, datetime

from flask import Blueprint, current_app, jsonify, request

from .birthday import greeting
from .repository import RepositoryError, UserRepository

bp = Blueprint("api", __name__)


def _repository() -> UserRepository:
    return current_app.extensions["user_repository"]


def _today() -> date:
    return current_app.extensions["today"]()


def _error(message: str, status: int):
    return jsonify({"error": message}), status


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.put("/hello/<username>")
def save_user(username: str):
    if not username.isalpha():
        return _error("Username must contain only letters.", 400)

    payload = request.get_json(silent=True)
    raw_date = payload.get("dateOfBirth") if isinstance(payload, dict) else None
    if not isinstance(raw_date, str):
        return _error('Request body must be JSON like {"dateOfBirth": "YYYY-MM-DD"}.', 400)

    try:
        date_of_birth = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError:
        return _error("Invalid date format. Use YYYY-MM-DD.", 400)

    if date_of_birth >= _today():
        return _error("Date of birth must be in the past.", 400)

    try:
        _repository().save(username, date_of_birth)
    except RepositoryError:
        current_app.logger.exception("Could not save user %s", username)
        return _error("Storage is temporarily unavailable.", 503)
    return "", 204


@bp.get("/hello/<username>")
def get_greeting(username: str):
    if not username.isalpha():
        return _error("Username must contain only letters.", 400)

    try:
        date_of_birth = _repository().get(username)
    except RepositoryError:
        current_app.logger.exception("Could not load user %s", username)
        return _error("Storage is temporarily unavailable.", 503)

    if date_of_birth is None:
        return _error(f"User {username} not found.", 404)
    return jsonify({"message": greeting(username, date_of_birth, _today())})
