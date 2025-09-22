"""
Unit tests for dashboard.py helper functions.
"""

import pandas as pd
from dashboard import (
    get_value_counts,
    get_level_count,
    get_subjects_per_level,
    year_wise_profit,
)


def _sample_df():
    return pd.DataFrame({
        "course_title": ["A", "B", "C", "D"],
        "url": ["u1", "u2", "u3", "u4"],
        "price": ["10", "Free", "TRUE", "25.5"],
        "num_subscribers": [100, 200, 300, 50],
        "level": ["Beginner", "Intermediate", "Beginner", "All Levels"],
        "published_timestamp": [
            "2019-01-01T00:00:00Z",
            "2020-05-10T00:00:00Z",
            "2020-07-20T00:00:00Z",
            "2020-03-15T00:00:00Z"
        ],
        "subject": ["Business", "Design", "Business", "IT & Software"]
    })


def test_get_value_counts_sums_subscribers_by_subject():
    df = _sample_df()
    vc = get_value_counts(df)
    # Business has 100 + 300 = 400 subscribers
    assert vc.get("Business", 0) == 400
    # IT & Software has 50 subscribers
    assert vc.get("IT & Software", 0) == 50


def test_get_level_count_counts_courses():
    df = _sample_df()
    lc = get_level_count(df)
    # Two Beginner courses, one Intermediate, one All Levels
    assert lc.get("Beginner", 0) == 2
    assert lc.get("Intermediate", 0) == 1
    assert lc.get("All Levels", 0) == 1


def test_get_subjects_per_level_pairs():
    df = _sample_df()
    pairs = get_subjects_per_level(df)
    # Expect keys like "Business_Beginner", "Design_Intermediate", etc.
    assert "Business_Beginner" in pairs
    assert pairs["Business_Beginner"] == 2  # A and C
    assert pairs["Design_Intermediate"] == 1