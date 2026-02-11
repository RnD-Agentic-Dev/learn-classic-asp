"""
Integration tests for Classic ASP database operations.

Covers:
    - database-read.asp   (SELECT from tb_countries)
    - database-write.asp  (INSERT into tb_posts, form validation)
    - database-update.asp (UPDATE, soft-delete, restore on tb_posts)

These tests verify behaviour through the HTTP interface and inspect the
HTML responses for expected content.  They are intentionally black-box so
the same suite can run against a migrated application.
"""

import uuid

import pytest
from bs4 import BeautifulSoup


pytestmark = pytest.mark.database


class TestDatabaseRead:
    """Tests for database-read.asp - reading countries from tb_countries."""

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("database-read.asp"))
        assert resp.status_code == 200

    def test_page_contains_countries_table(self, session, url):
        resp = session.get(url("database-read.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        table = soup.find("table")
        assert table is not None, "Expected an HTML table of countries"

    def test_table_has_expected_headers(self, session, url):
        resp = session.get(url("database-read.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        headers = [th.get_text(strip=True) for th in soup.find_all("th")]
        for expected in ("Name", "Code", "Capital", "Currency", "Population"):
            assert expected in headers, f"Missing table header: {expected}"

    def test_table_contains_country_rows(self, session, url):
        resp = session.get(url("database-read.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("table tbody tr")
        assert len(rows) > 0, "Expected at least one country row in the table"

    def test_known_country_present(self, session, url):
        """Verify a well-known country appears in the listing."""
        resp = session.get(url("database-read.asp"))
        assert "Japan" in resp.text or "Tokyo" in resp.text

    def test_page_title_contains_database_read(self, session, url):
        resp = session.get(url("database-read.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        h1 = soup.find("h1")
        assert h1 is not None
        assert "database read" in h1.get_text(strip=True).lower()


class TestDatabaseWrite:
    """Tests for database-write.asp - inserting posts into tb_posts."""

    def _unique_title(self):
        return f"__test_{uuid.uuid4().hex[:8]}"

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("database-write.asp"))
        assert resp.status_code == 200

    def test_page_contains_write_form(self, session, url):
        resp = session.get(url("database-write.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form")
        assert form is not None, "Expected a form for creating posts"

    def test_submit_valid_post(self, session, url):
        """Submit a new post with all required fields and verify success."""
        title = self._unique_title()
        data = {
            "title": title,
            "content": "Integration test content",
            "status": "published",
            "submit": "Submit",
        }
        resp = session.post(url("database-write.asp"), data=data)
        assert resp.status_code == 200
        assert "success" in resp.text.lower(), (
            "Expected a success message after valid submission"
        )

    def test_submitted_post_appears_in_listing(self, session, url):
        """After inserting a post, it should appear in the posts table."""
        title = self._unique_title()
        data = {
            "title": title,
            "content": "Appears in listing test",
            "status": "draft",
            "submit": "Submit",
        }
        resp = session.post(url("database-write.asp"), data=data)
        assert resp.status_code == 200
        assert title in resp.text, (
            "Newly created post should appear in the response listing"
        )

    def test_empty_title_shows_validation_error(self, session, url):
        """Submitting with an empty title should show a validation message."""
        data = {
            "title": "",
            "content": "Some content",
            "status": "published",
            "submit": "Submit",
        }
        resp = session.post(url("database-write.asp"), data=data)
        assert resp.status_code == 200
        assert "please write down the title" in resp.text.lower(), (
            "Expected title validation message"
        )

    def test_empty_content_shows_validation_error(self, session, url):
        """Submitting with empty content should show a validation message."""
        data = {
            "title": "Has a title",
            "content": "",
            "status": "published",
            "submit": "Submit",
        }
        resp = session.post(url("database-write.asp"), data=data)
        assert resp.status_code == 200
        assert "please write down the content" in resp.text.lower(), (
            "Expected content validation message"
        )

    def test_empty_title_and_content_shows_both_errors(self, session, url):
        """Both validation messages should appear when both fields are empty."""
        data = {
            "title": "",
            "content": "",
            "status": "published",
            "submit": "Submit",
        }
        resp = session.post(url("database-write.asp"), data=data)
        assert resp.status_code == 200
        text_lower = resp.text.lower()
        assert "please write down the title" in text_lower
        assert "please write down the content" in text_lower

    def test_posts_table_has_expected_columns(self, session, url):
        resp = session.get(url("database-write.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        headers = [th.get_text(strip=True) for th in soup.find_all("th")]
        for expected in ("Title", "Content", "Status"):
            assert expected in headers, f"Missing column header: {expected}"


class TestDatabaseUpdate:
    """Tests for database-update.asp - update, soft-delete, restore."""

    def _create_post(self, session, url_fn, title=None):
        """Helper: create a post via database-write.asp and return its title."""
        title = title or f"__test_{uuid.uuid4().hex[:8]}"
        data = {
            "title": title,
            "content": f"Content for {title}",
            "status": "published",
            "submit": "Submit",
        }
        session.post(url_fn("database-write.asp"), data=data)
        return title

    def _find_post_seq(self, session, url_fn, title):
        """Helper: find the seq of a post by its title from database-update.asp."""
        resp = session.get(url_fn("database-update.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a"):
            if title in link.get_text():
                href = link.get("href", "")
                if "seq=" in href:
                    return href.split("seq=")[-1]
        return None

    def test_page_loads_successfully(self, session, url):
        resp = session.get(url("database-update.asp"))
        assert resp.status_code == 200

    def test_page_lists_active_posts(self, session, url):
        resp = session.get(url("database-update.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        h3_tags = [h3.get_text(strip=True) for h3 in soup.find_all("h3")]
        assert any("List of Posts" in t for t in h3_tags)

    def test_page_lists_deleted_posts_section(self, session, url):
        resp = session.get(url("database-update.asp"))
        soup = BeautifulSoup(resp.text, "html.parser")
        h3_tags = [h3.get_text(strip=True) for h3 in soup.find_all("h3")]
        assert any("Deleted Posts" in t for t in h3_tags)

    def test_select_post_for_editing(self, session, url):
        """Clicking a post (via ?seq=) should show the update form."""
        title = self._create_post(session, url)
        seq = self._find_post_seq(session, url, title)
        assert seq is not None, f"Could not find seq for post '{title}'"

        resp = session.get(url(f"database-update.asp?seq={seq}"))
        assert resp.status_code == 200
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form", class_="uk-form-stacked")
        assert form is not None, "Expected update form when seq is provided"
        title_input = soup.find("input", {"name": "title"})
        assert title_input is not None
        assert title_input.get("value") == title

    def test_update_post(self, session, url):
        """Update a post's title and verify success message."""
        original_title = self._create_post(session, url)
        seq = self._find_post_seq(session, url, original_title)
        assert seq is not None

        new_title = f"__test_updated_{uuid.uuid4().hex[:8]}"
        data = {
            "seq": seq,
            "title": new_title,
            "content": "Updated content",
            "status": "published",
            "submit": "Update",
        }
        resp = session.post(url(f"database-update.asp?seq={seq}"), data=data)
        assert resp.status_code == 200
        assert "update post success" in resp.text.lower()

    def test_update_post_empty_title_shows_error(self, session, url):
        """Updating with an empty title should show validation error."""
        title = self._create_post(session, url)
        seq = self._find_post_seq(session, url, title)
        assert seq is not None

        data = {
            "seq": seq,
            "title": "",
            "content": "Some content",
            "status": "published",
            "submit": "Update",
        }
        resp = session.post(url(f"database-update.asp?seq={seq}"), data=data)
        assert resp.status_code == 200
        assert "please write down the title" in resp.text.lower()

    def test_soft_delete_post(self, session, url):
        """Soft-deleting a post should show success and move it to deleted list."""
        title = self._create_post(session, url)
        seq = self._find_post_seq(session, url, title)
        assert seq is not None

        data = {"seq": seq, "submit": "Delete"}
        resp = session.post(url(f"database-update.asp?seq={seq}"), data=data)
        assert resp.status_code == 200
        assert "delete post success" in resp.text.lower()

        resp2 = session.get(url("database-update.asp"))
        soup = BeautifulSoup(resp2.text, "html.parser")
        deleted_section = soup.find_all("table")
        deleted_text = ""
        if len(deleted_section) >= 2:
            deleted_text = deleted_section[-1].get_text()
        assert title in deleted_text, (
            "Deleted post should appear in the Deleted Posts section"
        )

    def test_restore_post(self, session, url):
        """Restoring a soft-deleted post should return it to the active list."""
        title = self._create_post(session, url)
        seq = self._find_post_seq(session, url, title)
        assert seq is not None

        session.post(
            url(f"database-update.asp?seq={seq}"), data={"seq": seq, "submit": "Delete"}
        )

        data = {"seq": seq, "submit": "Restore"}
        resp = session.post(url(f"database-update.asp?seq={seq}"), data=data)
        assert resp.status_code == 200
        assert "restore post success" in resp.text.lower()

        resp2 = session.get(url("database-update.asp"))
        soup = BeautifulSoup(resp2.text, "html.parser")
        first_table = soup.find("table")
        assert first_table is not None
        assert title in first_table.get_text(), (
            "Restored post should appear in the active posts list"
        )
