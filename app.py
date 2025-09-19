"""
Flask app for Online-Course-Recommendation-App-Project.

This file:
 - normalises dataframe columns after reading UdemyCleanedTitle.csv
 - safely creates/uses a Clean_title column (neattext)
 - builds TF-IDF and cosine similarity matrices
 - provides robust search and recommendation helpers that avoid KeyErrors / TypeErrors
 - constructs a coursemap dict: title -> {'url', 'price'}
 - defends against missing/empty form input (uses regex=False for .str.contains)

Usage:
    pip install pandas scikit-learn flask neattext
    python app.py
"""
from flask import Flask, request, render_template
import logging
from itertools import zip_longest
import pandas as pd
import numpy as np

# text cleaning & ML
import neattext.functions as nfx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

CSV_PATH = "UdemyCleanedTitle.csv"


# -------------------------
# Data loading & utilities
# -------------------------
def read_data(path: str = CSV_PATH) -> pd.DataFrame:
    """
    Read the Udemy CSV and normalise column names to canonical names.

    Returns:
        pd.DataFrame with at least 'course_title' present.
    Raises:
        FileNotFoundError if the CSV file is missing.
        KeyError if a usable title column cannot be inferred.
    """
    df = pd.read_csv(path)
    app.logger.debug("Loaded CSV columns: %s", df.columns.tolist())
    df = ensure_columns(df)
    return df


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise and rename likely column variants to canonical names:
      - course_title
      - url
      - price
      - Clean_title (kept if present)

    If 'course_title' cannot be found or inferred, raises KeyError with available columns.
    """
    # Strip whitespace from column names
    df = df.rename(columns={c: str(c).strip() for c in df.columns})

    # Build lowercase lookup: lowercase_name -> actual column name
    cols_lower = {c.lower(): c for c in df.columns}

    # Candidate alternatives for canonical names (lowercase)
    candidates = {
        'course_title': ['course_title', 'title', 'course title', 'clean_title', 'clean title'],
        'url': ['url', 'course_url', 'link', 'course link'],
        'price': ['price', 'course_price', 'cost', 'course cost'],
    }

    rename_map = {}
    for canon, alts in candidates.items():
        for alt in alts:
            if alt in cols_lower:
                rename_map[cols_lower[alt]] = canon
                break

    if rename_map:
        df = df.rename(columns=rename_map)

    # If some optional columns are missing, add them as empty to avoid KeyErrors later
    for optional in ('url', 'price'):
        if optional not in df.columns:
            df[optional] = ""

    if 'course_title' not in df.columns:
        raise KeyError(
            "Required column 'course_title' not found after normalisation. "
            f"Available columns: {list(df.columns)}"
        )

    return df


# -------------------------
# Title cleaning & TF-IDF
# -------------------------
def get_clean_title(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure 'Clean_title' exists. If present, coerce to string; otherwise create it from 'course_title'
    using neattext.functions.remove_special_characters.

    Returns:
        modified DataFrame with 'Clean_title'
    """
    if 'Clean_title' in df.columns:
        df['Clean_title'] = df['Clean_title'].astype(str)
        return df

    if 'course_title' not in df.columns:
        raise KeyError("'course_title' required to create 'Clean_title'")

    df['Clean_title'] = df['course_title'].astype(str).apply(nfx.remove_special_characters)
    return df


def build_tfidf_matrix(df: pd.DataFrame, col: str = 'Clean_title'):
    """
    Build TF-IDF matrix for `col` and return (tfidf_matrix, cosine_similarity_matrix).
    Raises KeyError if column missing.
    """
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not present in DataFrame to build TF-IDF.")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df[col].astype(str))
    cosine_mat = cosine_similarity(tfidf_matrix)
    return tfidf_matrix, cosine_mat


# -------------------------
# Search & Recommendation
# -------------------------
def search_term(term, df: pd.DataFrame) -> pd.DataFrame:
    """
    Return rows where course_title contains `term`. Case-insensitive, ignores NaN.
    Defensive:
      - If term is falsy (None, empty), returns empty DataFrame with same columns.
      - Uses regex=False so input with regex special chars (e.g. C++) is handled literally.
    """
    if 'course_title' not in df.columns:
        raise KeyError(f"search_term expected 'course_title' in df; available: {list(df.columns)}")

    # Handle no-term safely
    if term is None or (isinstance(term, str) and term.strip() == ""):
        return df.iloc[0:0].copy()

    term_str = str(term)
    mask = df['course_title'].astype(str).str.contains(term_str, case=False, na=False, regex=False)
    return df[mask].copy()


def recommend_course(df: pd.DataFrame, titlename: str, cosine_mat: np.ndarray, num_rec: int = 10) -> pd.DataFrame:
    """
    Given df with 'course_title' and a cosine similarity matrix, return top `num_rec` recommendations.
    Behavior:
      - If titlename not found exactly in titles, raises KeyError (caller can catch and treat as no-exact-match).
      - Returns DataFrame of recommended rows (with an added 'score' column).
    """
    if 'course_title' not in df.columns:
        raise KeyError(f"recommend_course expected 'course_title' in df; available: {list(df.columns)}")

    titles = df['course_title'].astype(str)
    course_index = pd.Series(df.index, index=titles).drop_duplicates()

    if titlename not in course_index.index:
        raise KeyError(f"Title '{titlename}' not found in course list. Examples: {list(course_index.index)[:5]}")

    idx = int(course_index[titlename])
    sim_scores = list(enumerate(cosine_mat[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Exclude itself (first element)
    sim_scores = sim_scores[1:num_rec+1]
    rec_indices = [i for i, s in sim_scores]
    recommendations = df.iloc[rec_indices].copy()
    recommendations['score'] = [s for i, s in sim_scores]
    return recommendations


# -------------------------
# Flask routes
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Main route:
      - loads data, builds TF-IDF / cosine matrices
      - builds coursemap: title -> {'url', 'price'}
      - if a 'title' (or 'q') is sent via POST/GET, performs search and, if exact match exists, recommendations
    """
    # Load & prepare data
    df = read_data()
    df = get_clean_title(df)
    tfidf_matrix, cosine_mat = build_tfidf_matrix(df, col='Clean_title')

    # Build coursemap safely (title -> {url, price})
    course_titles = df['course_title'].astype(str).tolist()
    course_urls = df['url'].astype(str).tolist() if 'url' in df.columns else [''] * len(course_titles)
    course_prices = df['price'].astype(str).tolist() if 'price' in df.columns else [''] * len(course_titles)

    coursemap = {}
    for t, u, p in zip_longest(course_titles, course_urls, course_prices, fillvalue=""):
        coursemap[t] = {'url': u, 'price': p}

    # Prefer 'title' form field, fallback to 'q' query param
    titlename = None
    if request.method == 'POST':
        titlename = request.form.get('title') or request.form.get('q')
    else:
        titlename = request.args.get('q') or request.args.get('title')

    recommendations = None
    search_results = None

    # Only run search/recommendations if a non-empty title was supplied
    if titlename is not None and str(titlename).strip() != "":
        # Safe search (returns empty df if no matches)
        search_results = search_term(titlename, df)
        # Attempt recommendations — only if exact title exists (recommend_course raises KeyError otherwise)
        try:
            recommendations = recommend_course(df, titlename, cosine_mat, num_rec=10)
        except KeyError:
            recommendations = None

    # Render template. Templates should gracefully handle None values.
    return render_template(
        'index.html',
        coursemap=coursemap,
        recommendations=recommendations,
        search_results=search_results
    )


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    Dashboard route preserved from original. Relies on external dashboard.py helpers.
    """
    df = read_data()
    value_counts = None
    level_counts = None
    subjects_per_level = None
    try:
        from dashboard import (get_value_counts, get_level_count,
                               get_subjects_per_level, year_wise_profit)
        value_counts = get_value_counts(df)
        level_counts = get_level_count(df)
        subjects_per_level = get_subjects_per_level(df)
        year_wise_profit_map, subscribers_count_map, profit_month_wise, month_wise_subscribers = year_wise_profit(df)
    except Exception as e:
        app.logger.warning("Dashboard utilities not available or failed: %s", e)
        year_wise_profit_map = subscribers_count_map = None

    return render_template('dashboard.html',
                           value_counts=value_counts,
                           level_counts=level_counts,
                           subjects_per_level=subjects_per_level,
                           year_wise_profit_map=year_wise_profit_map,
                           subscribers_count_map=subscribers_count_map)


if __name__ == "__main__":
    # Run the Flask dev server
    app.run(debug=True)
