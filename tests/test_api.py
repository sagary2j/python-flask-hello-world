from datetime import date

import pytest


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_put_then_get_round_trip(client, repository):
    response = client.put("/hello/alice", json={"dateOfBirth": "1990-07-05"})
    assert response.status_code == 204
    assert response.data == b""
    assert repository.users["alice"] == date(1990, 7, 5)

    response = client.get("/hello/alice")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, alice! Your birthday is in 5 day(s)"}


def test_put_overwrites_existing_user(client):
    client.put("/hello/alice", json={"dateOfBirth": "1990-07-05"})
    client.put("/hello/alice", json={"dateOfBirth": "1991-06-30"})
    assert client.get("/hello/alice").get_json() == {"message": "Hello, alice! Happy birthday!"}


@pytest.mark.parametrize("username", ["alice1", "al_ice", "al%20ice"])
def test_put_rejects_non_letter_usernames(client, username):
    response = client.put(f"/hello/{username}", json={"dateOfBirth": "1990-01-01"})
    assert response.status_code == 400
    assert "only letters" in response.get_json()["error"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"data": "not json", "content_type": "application/json"},
        {"json": ["1990-01-01"]},
        {"json": {}},
        {"json": {"dateOfBirth": 19900101}},
    ],
)
def test_put_rejects_missing_or_malformed_body(client, kwargs):
    response = client.put("/hello/alice", **kwargs)
    assert response.status_code == 400
    assert "dateOfBirth" in response.get_json()["error"]


@pytest.mark.parametrize("value", ["1990/01/01", "01-01-1990", "1990-02-30", ""])
def test_put_rejects_invalid_dates(client, value):
    response = client.put("/hello/alice", json={"dateOfBirth": value})
    assert response.status_code == 400
    assert "YYYY-MM-DD" in response.get_json()["error"]


@pytest.mark.parametrize("value", ["2026-06-30", "2026-07-01", "2999-01-01"])
def test_put_rejects_today_and_future_dates(client, value):
    response = client.put("/hello/alice", json={"dateOfBirth": value})
    assert response.status_code == 400
    assert "past" in response.get_json()["error"]


def test_get_unknown_user_returns_404(client):
    response = client.get("/hello/nobody")
    assert response.status_code == 404
    assert response.get_json() == {"error": "User nobody not found."}


def test_get_rejects_non_letter_username(client):
    assert client.get("/hello/bob42").status_code == 400


@pytest.mark.parametrize(
    "call",
    [
        lambda c: c.put("/hello/alice", json={"dateOfBirth": "1990-01-01"}),
        lambda c: c.get("/hello/alice"),
    ],
)
def test_storage_errors_return_503_without_leaking_details(failing_client, call):
    response = call(failing_client)
    assert response.status_code == 503
    assert response.get_json() == {"error": "Storage is temporarily unavailable."}


def test_unknown_route_returns_json_404(client):
    response = client.get("/nope")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_wrong_method_returns_json_405(client):
    response = client.post("/hello/alice")
    assert response.status_code == 405
    assert "error" in response.get_json()


def test_unexpected_errors_return_generic_500(repository):
    from app import create_app
    from app.config import Settings

    def explode(username):
        raise RuntimeError("internal detail")

    repository.get = explode
    app = create_app(settings=Settings(), repository=repository)
    response = app.test_client().get("/hello/alice")
    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}
