"""
Integration tests for Classic ASP session management.

Covers:
    - session-simple.asp  (basic login/logout toggle)
    - session-login.asp   (login form with credential validation)

Session state is tracked via cookies; the tests use requests.Session
to maintain cookies across calls, verifying session persistence.
"""

import pytest
from bs4 import BeautifulSoup


pytestmark = pytest.mark.session


class TestSessionSimple:
    """Tests for session-simple.asp - basic session toggle."""

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("session-simple.asp"))
        assert resp.status_code == 200

    def test_initial_state_is_logged_out(self, fresh_session, url):
        """A new session should show the logged-out state."""
        resp = fresh_session.get(url("session-simple.asp"))
        assert resp.status_code == 200
        assert "you are not logged in" in resp.text.lower()

    def test_login_sets_session(self, fresh_session, url):
        """Clicking Login should set the session and greet the user."""
        resp = fresh_session.post(
            url("session-simple.asp"),
            data={"submit": "Login"},
        )
        assert resp.status_code == 200
        assert "Park Kwang Hoo!" in resp.text

    def test_login_shows_logout_button(self, fresh_session, url):
        """After login, a Logout button should be present."""
        fresh_session.post(
            url("session-simple.asp"),
            data={"submit": "Login"},
        )
        resp = fresh_session.get(url("session-simple.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        logout_btn = soup.find("input", {"value": "Logout"})
        assert logout_btn is not None

    def test_logout_clears_session(self, fresh_session, url):
        """After logout, the page should return to the logged-out state."""
        fresh_session.post(
            url("session-simple.asp"),
            data={"submit": "Login"},
        )
        resp = fresh_session.post(
            url("session-simple.asp"),
            data={"submit": "Logout"},
        )
        assert resp.status_code == 200
        assert "you are not logged in" in resp.text.lower()

    def test_session_persists_across_requests(self, fresh_session, url):
        """After login, subsequent GET requests should still be logged in."""
        fresh_session.post(
            url("session-simple.asp"),
            data={"submit": "Login"},
        )
        resp = fresh_session.get(url("session-simple.asp"))
        assert "Park Kwang Hoo!" in resp.text


class TestSessionLogin:
    """Tests for session-login.asp - login form with credential validation."""

    VALID_USERNAME = "user"
    VALID_PASSWORD = "user"

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("session-login.asp"))
        assert resp.status_code == 200

    def test_page_shows_login_form(self, fresh_session, url):
        resp = fresh_session.get(url("session-login.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form")
        assert form is not None
        username_input = soup.find("input", {"name": "username"})
        password_input = soup.find("input", {"name": "password"})
        assert username_input is not None
        assert password_input is not None

    def test_login_with_valid_credentials(self, fresh_session, url):
        """Valid credentials should log the user in and show greeting."""
        data = {
            "username": self.VALID_USERNAME,
            "password": self.VALID_PASSWORD,
            "submit": "Login",
        }
        resp = fresh_session.post(url("session-login.asp"), data=data)
        assert resp.status_code == 200
        assert f"Hello {self.VALID_USERNAME}" in resp.text

    def test_login_with_valid_credentials_shows_logout(self, fresh_session, url):
        """After valid login, a Logout button should be displayed."""
        data = {
            "username": self.VALID_USERNAME,
            "password": self.VALID_PASSWORD,
            "submit": "Login",
        }
        fresh_session.post(url("session-login.asp"), data=data)
        resp = fresh_session.get(url("session-login.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        logout_btn = soup.find("input", {"value": "Logout"})
        assert logout_btn is not None

    def test_login_with_invalid_credentials(self, fresh_session, url):
        """Wrong credentials should show an error message."""
        data = {
            "username": "wrong",
            "password": "wrong",
            "submit": "Login",
        }
        resp = fresh_session.post(url("session-login.asp"), data=data)
        assert resp.status_code == 200
        assert "wrong" in resp.text.lower() or "invalid" in resp.text.lower()

    def test_login_with_empty_username(self, fresh_session, url):
        """Empty username should trigger a validation message."""
        data = {
            "username": "",
            "password": self.VALID_PASSWORD,
            "submit": "Login",
        }
        resp = fresh_session.post(url("session-login.asp"), data=data)
        assert resp.status_code == 200
        assert "username is required" in resp.text.lower()

    def test_login_with_empty_password(self, fresh_session, url):
        """Empty password should trigger a validation message."""
        data = {
            "username": self.VALID_USERNAME,
            "password": "",
            "submit": "Login",
        }
        resp = fresh_session.post(url("session-login.asp"), data=data)
        assert resp.status_code == 200
        assert "password is required" in resp.text.lower()

    def test_login_with_both_empty(self, fresh_session, url):
        """Both empty fields should show both validation messages."""
        data = {
            "username": "",
            "password": "",
            "submit": "Login",
        }
        resp = fresh_session.post(url("session-login.asp"), data=data)
        assert resp.status_code == 200
        text_lower = resp.text.lower()
        assert "username is required" in text_lower
        assert "password is required" in text_lower

    def test_logout_clears_session(self, fresh_session, url):
        """After logout, the login form should be shown again."""
        data = {
            "username": self.VALID_USERNAME,
            "password": self.VALID_PASSWORD,
            "submit": "Login",
        }
        fresh_session.post(url("session-login.asp"), data=data)
        resp = fresh_session.post(
            url("session-login.asp"),
            data={"submit": "Logout"},
        )
        assert resp.status_code == 200
        soup = BeautifulSoup(resp.text, "html.parser")
        login_form = soup.find("input", {"name": "username"})
        assert login_form is not None, "After logout, the login form should be visible"

    def test_session_persists_across_pages(self, fresh_session, url):
        """After login on session-login.asp, session should persist on session-simple.asp."""
        data = {
            "username": self.VALID_USERNAME,
            "password": self.VALID_PASSWORD,
            "submit": "Login",
        }
        fresh_session.post(url("session-login.asp"), data=data)
        resp = fresh_session.get(url("session-simple.asp"))
        assert "Hello" in resp.text, (
            "Session should persist: user should appear logged in on session-simple.asp"
        )
