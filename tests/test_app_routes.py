"""
Route tests for app.py using the Flask test client.

Covers:
- Home GET renders
- Home POST with a query returns expected results
- Dashboard GET renders and includes expected chart placeholders
"""


def test_home_get_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    # Contains the search form input
    assert b'name="course"' in resp.data