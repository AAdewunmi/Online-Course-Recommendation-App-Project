"""
Shared pytest fixtures for the Online Course Recommendation App.

Provides:
- sample_df: a minimal DataFrame with required columns.
- client: a Flask test client whose app.read_data() is monkeypatched to return sample_df.

These tests do not hit the real CSV to keep CI fast and deterministic.
"""