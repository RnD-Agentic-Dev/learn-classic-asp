"""
Smoke tests to verify basic connectivity to the Classic ASP application.

These are lightweight tests that confirm the server is reachable and
key pages return HTTP 200. Run these first to rule out infrastructure
issues before investigating functional test failures.
"""

import pytest


pytestmark = pytest.mark.smoke

PAGES = [
    "default.asp",
    "basic-comment.asp",
    "basic-conditional.asp",
    "basic-loops.asp",
    "basic-array.asp",
    "basic-function.asp",
    "basic-variable.asp",
    "sendingcontent.asp",
    "sendingcontent-json.asp",
    "sendingcontent-xml.asp",
    "form-get.asp",
    "form-post.asp",
    "form-get-validation.asp",
    "form-post-validation.asp",
    "session-simple.asp",
    "session-login.asp",
    "fso-list.asp",
    "database-read.asp",
    "database-write.asp",
    "database-update.asp",
    "server-variable.asp",
]


@pytest.mark.parametrize("page", PAGES)
def test_page_returns_200(session, url, page):
    """Each page should be reachable and return HTTP 200."""
    resp = session.get(url(page))
    assert resp.status_code == 200, f"{page} returned {resp.status_code}"


def test_default_page_contains_navigation_links(session, url):
    """The default page should list links to all demonstration pages."""
    resp = session.get(url("default.asp"))
    assert resp.status_code == 200
    for page in ["database-read.asp", "form-get.asp", "session-login.asp"]:
        assert page in resp.text, f"default.asp missing link to {page}"
