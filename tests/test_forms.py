"""
Integration tests for Classic ASP form processing.

Covers:
    - form-get.asp             (GET form submission)
    - form-post.asp            (POST form submission)
    - form-get-validation.asp  (GET form with server-side validation)
    - form-post-validation.asp (POST form with server-side validation)

All tests verify behaviour through HTTP requests and HTML response parsing.
"""

import pytest
from bs4 import BeautifulSoup


pytestmark = pytest.mark.forms


class TestFormGet:
    """Tests for form-get.asp - GET form submission via query strings."""

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("form-get.asp"))
        assert resp.status_code == 200

    def test_page_contains_form(self, session, url):
        resp = session.get(url("form-get.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form", {"method": "GET"})
        assert form is not None

    def test_submit_get_form_with_data(self, session, url):
        """Submit values via GET and verify they are echoed back."""
        params = {
            "title": "Test Title",
            "content": "Test Content",
            "category": "news",
            "status": "published",
        }
        resp = session.get(url("form-get.asp"), params=params)
        assert resp.status_code == 200
        assert "Test Title" in resp.text
        assert "Test Content" in resp.text
        assert "news" in resp.text
        assert "published" in resp.text

    def test_submit_get_form_with_multiple_categories(self, session, url):
        """Checkboxes can send multiple values for the same field."""
        params = [
            ("title", "Multi Category"),
            ("content", "Content"),
            ("category", "news"),
            ("category", "event"),
            ("status", "draft"),
        ]
        resp = session.get(url("form-get.asp"), params=params)
        assert resp.status_code == 200
        assert "news" in resp.text
        assert "event" in resp.text

    def test_submit_get_form_empty_fields(self, session, url):
        """Submitting empty fields should still return a 200 response."""
        resp = session.get(url("form-get.asp"), params={})
        assert resp.status_code == 200

    def test_response_section_present(self, session, url):
        """The page should have a 'Form GET Response' section."""
        resp = session.get(url("form-get.asp"))
        assert "Form GET Response" in resp.text


class TestFormPost:
    """Tests for form-post.asp - POST form submission."""

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("form-post.asp"))
        assert resp.status_code == 200

    def test_page_contains_form(self, session, url):
        resp = session.get(url("form-post.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form", {"method": "POST"})
        assert form is not None

    def test_submit_post_form_with_data(self, session, url):
        """Submit values via POST and verify they are echoed back."""
        data = {
            "title": "Post Title",
            "content": "Post Content",
            "category": "event",
            "status": "draft",
        }
        resp = session.post(url("form-post.asp"), data=data)
        assert resp.status_code == 200
        assert "Post Title" in resp.text
        assert "Post Content" in resp.text
        assert "event" in resp.text
        assert "draft" in resp.text

    def test_submit_post_form_empty_fields(self, session, url):
        """Submitting empty fields should still return a 200 response."""
        resp = session.post(url("form-post.asp"), data={})
        assert resp.status_code == 200

    def test_response_section_present(self, session, url):
        """The page should have a 'Form POST Response' section."""
        resp = session.get(url("form-post.asp"))
        assert "Form POST Response" in resp.text


class TestFormGetValidation:
    """Tests for form-get-validation.asp - GET form with server validation."""

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("form-get-validation.asp"))
        assert resp.status_code == 200

    def test_submit_valid_data(self, session, url):
        """Valid data should echo values without error messages."""
        params = {
            "title": "Valid Title",
            "content": "Valid Content",
            "status": "published",
            "submit": "Submit",
        }
        resp = session.get(url("form-get-validation.asp"), params=params)
        assert resp.status_code == 200
        assert "Valid Title" in resp.text
        assert "Valid Content" in resp.text
        assert "please write down the title" not in resp.text.lower()
        assert "please write down the content" not in resp.text.lower()

    def test_empty_title_shows_validation_error(self, session, url):
        """Empty title with submit should show title validation message."""
        params = {
            "title": "",
            "content": "Has content",
            "submit": "Submit",
        }
        resp = session.get(url("form-get-validation.asp"), params=params)
        assert resp.status_code == 200
        assert "please write down the title" in resp.text.lower()

    def test_empty_content_shows_validation_error(self, session, url):
        """Empty content with submit should show content validation message."""
        params = {
            "title": "Has title",
            "content": "",
            "submit": "Submit",
        }
        resp = session.get(url("form-get-validation.asp"), params=params)
        assert resp.status_code == 200
        assert "please write down the content" in resp.text.lower()

    def test_both_empty_shows_both_errors(self, session, url):
        """Both empty fields should show both validation messages."""
        params = {
            "title": "",
            "content": "",
            "submit": "Submit",
        }
        resp = session.get(url("form-get-validation.asp"), params=params)
        assert resp.status_code == 200
        text_lower = resp.text.lower()
        assert "please write down the title" in text_lower
        assert "please write down the content" in text_lower

    def test_no_errors_without_submit(self, session, url):
        """Without the submit parameter, no validation errors should show."""
        params = {"title": "", "content": ""}
        resp = session.get(url("form-get-validation.asp"), params=params)
        assert resp.status_code == 200
        text_lower = resp.text.lower()
        assert "please write down the title" not in text_lower
        assert "please write down the content" not in text_lower


class TestFormPostValidation:
    """Tests for form-post-validation.asp - POST form with server validation."""

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("form-post-validation.asp"))
        assert resp.status_code == 200

    def test_submit_valid_data(self, session, url):
        """Valid data should echo values without error messages."""
        data = {
            "title": "Valid Title",
            "content": "Valid Content",
            "status": "published",
            "submit": "Submit",
        }
        resp = session.post(url("form-post-validation.asp"), data=data)
        assert resp.status_code == 200
        assert "Valid Title" in resp.text
        assert "Valid Content" in resp.text
        assert "please write down the title" not in resp.text.lower()
        assert "please write down the content" not in resp.text.lower()

    def test_empty_title_shows_validation_error(self, session, url):
        data = {
            "title": "",
            "content": "Has content",
            "submit": "Submit",
        }
        resp = session.post(url("form-post-validation.asp"), data=data)
        assert resp.status_code == 200
        assert "please write down the title" in resp.text.lower()

    def test_empty_content_shows_validation_error(self, session, url):
        data = {
            "title": "Has title",
            "content": "",
            "submit": "Submit",
        }
        resp = session.post(url("form-post-validation.asp"), data=data)
        assert resp.status_code == 200
        assert "please write down the content" in resp.text.lower()

    def test_both_empty_shows_both_errors(self, session, url):
        data = {
            "title": "",
            "content": "",
            "submit": "Submit",
        }
        resp = session.post(url("form-post-validation.asp"), data=data)
        assert resp.status_code == 200
        text_lower = resp.text.lower()
        assert "please write down the title" in text_lower
        assert "please write down the content" in text_lower

    def test_no_errors_without_submit(self, session, url):
        """Without submit, no validation errors should appear."""
        data = {"title": "", "content": ""}
        resp = session.post(url("form-post-validation.asp"), data=data)
        assert resp.status_code == 200
        text_lower = resp.text.lower()
        assert "please write down the title" not in text_lower
        assert "please write down the content" not in text_lower
