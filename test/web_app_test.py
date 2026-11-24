# this is the "test/web_app_test.py" file...

# testing a flask app. see:
# ... https://flask.palletsprojects.com/en/stable/testing/

import pytest
from bs4 import BeautifulSoup
from pandas import DataFrame

from web_app import create_app


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config.update({"TESTING": True})
    return app.test_client()


#
# HOME ROUTES
#

def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome Home" in response.data


def test_about(test_client):
    response = test_client.get("/about")
    assert response.status_code == 200
    assert b"About Me" in response.data


def test_hello(test_client):
    response = test_client.get("/hello")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

    # ... with url params
    response = test_client.get("/hello?name=Camille")
    assert response.status_code == 200
    assert b"Hello, Camille!" in response.data


#
# RPS ROUTES
#

def test_rps_form(test_client):
    response = test_client.get("/rps/form")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, features="html.parser")
    options = soup.find("select", {"name": "user_choice"}).find_all("option")
    assert [o["value"] for o in options] == ["rock", "paper", "scissors"]


def test_rps_results(test_client):
    response = test_client.post("/rps/results", data={"user_choice": "rock"})
    assert response.status_code == 200
    assert b"Game Result" in response.data
    assert b"ROCK" in response.data
    assert any(outcome in response.data for outcome in [b"USER WINS", b"COMPUTER WINS", b"TIE GAME"])


#
# STOCKS ROUTES
# (these use fake data instead of calling the API, so they don't use up our API requests)
#

FAKE_STOCKS_DF = DataFrame([
    {"timestamp": "2026-11-23", "open": 100.0, "high": 105.0, "low": 99.0, "close": 104.0, "adjusted_close": 104.0, "volume": 1000000},
    {"timestamp": "2026-11-20", "open": 98.0, "high": 101.0, "low": 97.0, "close": 100.0, "adjusted_close": 100.0, "volume": 900000},
])


def test_stocks_form(test_client):
    response = test_client.get("/stocks/form")
    assert response.status_code == 200
    assert b"Stocks Form" in response.data


def test_stocks_dashboard(test_client, monkeypatch):
    monkeypatch.setattr("web_app.routes.stocks_routes.fetch_stocks_csv", lambda symbol: FAKE_STOCKS_DF)

    response = test_client.post("/stocks/dashboard", data={"symbol": "msft"})
    assert response.status_code == 200
    assert b"Stocks Dashboard (MSFT)" in response.data
    assert b"Latest Close: $104.00" in response.data
    assert b"Fetched Real-time Market Data!" in response.data  # flash message

    soup = BeautifulSoup(response.data, features="html.parser")
    rows = soup.find("tbody").find_all("tr")
    assert len(rows) == 2
    assert soup.find(id="chart-container") is not None


def test_stocks_dashboard_invalid_symbol(test_client, monkeypatch):
    def fake_fetch(symbol):
        raise KeyError("adjusted_close")  # what happens when the API doesn't recognize the symbol

    monkeypatch.setattr("web_app.routes.stocks_routes.fetch_stocks_csv", fake_fetch)

    # redirects back to the form...
    response = test_client.post("/stocks/dashboard", data={"symbol": "OOPS"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/stocks/form")

    # ... where we see the flash message
    response = test_client.get("/stocks/form")
    assert b"Market Data Error" in response.data
