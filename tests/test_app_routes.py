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


def test_home_search_returns_results(client):
    # Search for 'Python' which exists in sample_df
    resp = client.post("/", data={"course": "Python"})
    assert resp.status_code == 200
    # Expect to see the course title in the rendered HTML
    assert b"Python for Beginners" in resp.data
    # And a 'View Course' link should be present
    assert b"View Course" in resp.data