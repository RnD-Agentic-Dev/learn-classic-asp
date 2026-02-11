# Integration Test Suite for Classic ASP Application

Black-box integration/regression tests for the Classic ASP learning application. Designed to verify end-to-end behavior through HTTP interfaces, enabling comparison between the Classic ASP version and any future migrated version (e.g., ASP.NET Core).

## Structure

```
tests/
├── conftest.py              # Shared fixtures (base_url, session, url helper)
├── pytest.ini               # Pytest configuration and custom markers
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── test_smoke.py            # Smoke tests — basic connectivity for all pages
├── test_database.py         # Database CRUD operations (read, write, update, delete, restore)
├── test_forms.py            # Form processing (GET, POST, validation)
├── test_session.py          # Session management (login, logout, persistence)
└── fixtures/
    ├── seed_posts.sql       # SQL to insert known test posts
    ├── seed_countries.sql   # SQL to ensure known country rows exist
    └── cleanup_posts.sql    # SQL to remove test data after runs
```

## Test Categories

| Marker     | File                | What it covers                                          |
|------------|---------------------|---------------------------------------------------------|
| `smoke`    | `test_smoke.py`     | All pages return HTTP 200; default.asp has nav links    |
| `database` | `test_database.py`  | Read countries, create/update/soft-delete/restore posts |
| `forms`    | `test_forms.py`     | GET/POST form submission and server-side validation     |
| `session`  | `test_session.py`   | Login/logout, session persistence, credential checks    |

## Prerequisites

- Python 3.8+
- A running instance of the Classic ASP application (IIS + SQL Server) **or** a migrated version
- The `tb_countries` table populated (run `files/tb_countries.sql`)
- The `tb_posts` table created (run `files/tb_posts.sql`)

## Setup

```bash
cd tests
pip install -r requirements.txt
```

## Running the Tests

Set `BASE_URL` to point at your application instance, then run pytest:

```bash
# Against Classic ASP on IIS
export BASE_URL=http://localhost/learn-classic-asp
pytest

# Against the ASP.NET Core migration
export BASE_URL=http://localhost:5000
pytest

# Run only smoke tests
pytest -m smoke

# Run only database tests
pytest -m database

# Run only form tests
pytest -m forms

# Run only session tests
pytest -m session

# Verbose output
pytest -v
```

## Database Fixtures

Before running the full suite, optionally seed known test data:

```sql
-- Run against your SQL Server instance
sqlcmd -S YOUR_SERVER -d learnasp -i fixtures/seed_posts.sql
```

After the run, clean up test data (posts with titles starting `__test_`):

```sql
sqlcmd -S YOUR_SERVER -d learnasp -i fixtures/cleanup_posts.sql
```

The database tests create their own posts (prefixed `__test_`) during execution, so fixtures are optional but recommended for a predictable starting state.

## Design Decisions

- **Black-box testing**: Tests interact only through HTTP and inspect HTML responses. No direct database connections are required from the test runner.
- **Migration-friendly**: The same tests can run against any implementation that serves the same URLs with equivalent behavior (Classic ASP, ASP.NET Core, etc.).
- **Unique test data**: Database write tests use UUID-based titles (`__test_<uuid>`) to avoid collisions with real data.
- **Session isolation**: Each test that needs a clean session uses the `fresh_session` fixture.
- **No browser required**: Tests use `requests` + `BeautifulSoup` instead of Selenium/Playwright for speed and simplicity.

## Adding New Tests

1. Create or edit a `test_*.py` file in the `tests/` directory.
2. Use the `session` fixture for a shared session or `fresh_session` for an isolated one.
3. Use the `url` fixture to build full URLs: `url("page-name.asp")`.
4. Mark tests with the appropriate marker (`@pytest.mark.database`, etc.).
