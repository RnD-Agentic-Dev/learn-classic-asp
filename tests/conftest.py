"""
Shared fixtures and configuration for the Classic ASP integration test suite.

Configuration:
    Set the BASE_URL environment variable to point to your Classic ASP or
    migrated application instance. Defaults to http://localhost/learn-classic-asp.

    Example:
        export BASE_URL=http://localhost/learn-classic-asp
        pytest
"""

import os

import pytest
import requests


BASE_URL = os.environ.get("BASE_URL", "http://localhost/learn-classic-asp")


@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the application under test."""
    return BASE_URL


@pytest.fixture()
def session():
    """Return a requests.Session that persists cookies across requests."""
    with requests.Session() as s:
        yield s


@pytest.fixture()
def fresh_session():
    """Return a brand-new requests.Session with no prior cookies."""
    with requests.Session() as s:
        yield s


def _url(path):
    """Build a full URL from a relative path."""
    return f"{BASE_URL}/{path}"


@pytest.fixture(scope="session")
def url():
    """Return a helper that builds full URLs from relative page paths."""
    return _url
