"""
Flask app for Online Course Recommendation / Search + Dashboard.

Home:
  - Keyword search over course_title (case-insensitive, literal match).
  - Renders matching courses as title -> URL button.

Dashboard:
  - Descriptive statistics visualised with Chart.js:
      * Subscribers by Subject (Domain)
      * Courses count by Level
      * Subscribers by Year
      * Profit by Year
      * Profit by Month
      * Subscribers by Month

Notes:
  - Uses UdemyCleanedTitle.csv (columns present in your upload).
  - Defensive handling for empty/missing inputs and NaNs.
"""

from flask import Flask, request, render_template
import logging
import pandas as pd

from dashboard import (
    get_value_counts,        # subscribers by subject
    get_level_count,         # courses count by level
    get_subjects_per_level,  # subject_level pair counts
    year_wise_profit         # profit & subscribers, year and month wise
)

app = Flask(__name__)
logging.getLogger().setLevel(logging.INFO)

CSV_PATH = "UdemyCleanedTitle.csv"


# -------------------------
# Data loading & utilities
# -------------------------
def read_data(path: str = CSV_PATH) -> pd.DataFrame:
    """
    Load Udemy dataset and ensure the essential columns exist.
    Returns a DataFrame with normalized column names.
    """
    df = pd.read_csv(path)

    # normalize names: strip whitespace only (keep original casings used by CSV)
    df.columns = [str(c).strip() for c in df.columns]

    required = [
        "course_title", "url", "price", "num_subscribers",
        "level", "published_timestamp", "subject"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"CSV missing required columns: {missing}. Available: {list(df.columns)}")

    return df


def search_courses(df: pd.DataFrame, term: str) -> pd.DataFrame:
    """
    Return rows where course_title contains `term` (case-insensitive, literal).
    If term is falsy (None/empty), return an empty DataFrame (no results).
    """
    if term is None or (isinstance(term, str) and term.strip() == ""):
        return df.iloc[0:0].copy()

    term_str = str(term)
    mask = df["course_title"].astype(str).str.contains(term_str, case=False, na=False, regex=False)
    return df[mask].copy()


# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home page: supports keyword search via form input name='course' OR query param 'q'.
    Renders a list of matched courses with 'View Course' links.
    """
    df = read_data()

    # accept both form and query inputs for convenience
    query = None
    if request.method == "POST":
        query = request.form.get("course") or request.form.get("q") or request.form.get("title")
    else:
        query = request.args.get("q") or request.args.get("course") or request.args.get("title")

    results = search_courses(df, query)
    showerror = False
    showtitle = False
    coursename = None

    if query is not None and str(query).strip() != "":
        coursename = str(query).strip()
        showtitle = True
        if results.empty:
            showerror = True

    # Build mapping expected by index.html:
    # coursemap: title -> url (STRING), because template uses href="{{coursemap[course]}}"
    if results.empty:
        coursemap = {}  # nothing to show if no results (or no query)
    else:
        coursemap = dict(zip(results["course_title"].astype(str), results["url"].astype(str)))

    return render_template(
        "index.html",
        coursemap=coursemap,
        showerror=showerror,
        showtitle=showtitle,
        coursename=coursename
    )


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """
    Dashboard page: computes summary statistics and passes maps to the template
    with the exact variable names used by dashboard.html.
    """
    df = read_data()

    # Subscribers by Subject (Domain)
    valuecounts = get_value_counts(df)  # dict: subject -> total_subscribers

    # Courses count by Level
    levelcounts = get_level_count(df)   # dict: level -> number_of_courses

    # Subjects per Level (pair counts)
    subjectsperlevel = get_subjects_per_level(df)  # dict: "Subject_Level" -> count

    # Profit/Subscribers Year-wise and Month-wise
    yearwiseprofitmap, subscriberscountmap, profitmonthwise, monthwisesub = year_wise_profit(df)

    return render_template(
        "dashboard.html",
        valuecounts=valuecounts,
        levelcounts=levelcounts,
        subjectsperlevel=subjectsperlevel,
        yearwiseprofitmap=yearwiseprofitmap,
        subscriberscountmap=subscriberscountmap,
        profitmonthwise=profitmonthwise,
        monthwisesub=monthwisesub
    )


if __name__ == "__main__":
    app.run(debug=True)
