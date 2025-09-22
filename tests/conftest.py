"""
Shared pytest fixtures for the Online Course Recommendation App.

Provides:
- sample_df: a minimal DataFrame with required columns.
- client: a Flask test client whose app.read_data() is monkeypatched to return sample_df.

These tests do not hit the real CSV to keep CI fast and deterministic.
"""

import pytest
import pandas as pd


@pytest.fixture()
def sample_df() -> pd.DataFrame:
    """
    Minimal, deterministic DataFrame with required columns:
    course_title, url, price, num_subscribers, level, published_timestamp, subject
    """
    return pd.DataFrame({
        "course_title": [
            "Python for Beginners",
            "Advanced Excel Analytics",
            "Finance 101"
        ],
        "url": [
            "https://example.com/python-beginners",
            "https://example.com/excel-analytics",
            "https://example.com/finance-101"
        ],
        "price": ["10.0", "Free", "TRUE"],
        "num_subscribers": [150, 300, 120],
        "level": ["Beginner", "Intermediate", "Beginner"],
        "published_timestamp": [
            "2019-01-01T00:00:00Z",
            "2020-05-10T00:00:00Z",
            "2020-07-20T00:00:00Z"
        ],
        "subject": ["Development", "Business", "Finance"]
    })


@pytest.fixture()
def client(monkeypatch, sample_df):
    """
    Flask test client with app.read_data() monkeypatched to return sample_df.
    Ensures route handlers operate on a small, known dataset during tests.
    """
    import importlib
    import app as app_module

    # Reload in case app.py was imported earlier (ensures fresh monkeypatching)
    importlib.reload(app_module)

    # Monkeypatch read_data to avoid reading the real CSV
    monkeypatch.setattr(app_module, "read_data", lambda path=app_module.CSV_PATH: sample_df)

    flask_app = app_module.app
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as test_client:
        yield test_client
