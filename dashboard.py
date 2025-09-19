"""
Dashboard helpers for descriptive statistics on the Udemy dataset.

Functions return plain Python dicts so they can be injected into Jinja templates
and consumed by Chart.js on the client side.
"""

import pandas as pd


def get_value_counts(df: pd.DataFrame) -> dict:
    """
    Number of Subscribers Domain (Subject) Wise.
    Sums num_subscribers per subject.
    """
    if "subject" not in df.columns or "num_subscribers" not in df.columns:
        return {}
    series = df.groupby("subject")["num_subscribers"].sum().sort_values(ascending=False)
    return series.to_dict()


def get_level_count(df: pd.DataFrame) -> dict:
    """
    Number of Courses Level Wise.
    Counts distinct rows per level (not subscribers).
    """
    if "level" not in df.columns:
        return {}
    series = df.groupby("level").size().sort_values(ascending=False)
    return series.to_dict()


def get_subjects_per_level(df: pd.DataFrame) -> dict:
    """
    Count of courses per (subject, level) pair.
    Keys formatted as 'Subject_Level'.
    """
    if "subject" not in df.columns or "level" not in df.columns:
        return {}
    vc = df.groupby(["subject", "level"]).size()
    labels = [f"{subj}_{lvl}" for (subj, lvl) in vc.index]
    return dict(zip(labels, vc.tolist()))


def year_wise_profit(df: pd.DataFrame):
    """
    Compute:
      - profit per year,
      - subscribers per year,
      - profit per month (across all years),
      - subscribers per month (across all years).

    price: strings like '$12.99', 'Free', 'TRUE' handled by coercion to 0.0 when non-numeric.
    published_timestamp: expected format like '2017-03-15T00:00:00Z' (we split on 'T' and parse date).
    """
    # Clean price -> numeric
    price = df["price"].astype(str).str.replace(r"TRUE|Free", "0", regex=True)
    # Remove currency symbols and commas if any, then coerce to float
    price = price.str.replace(r"[^\d\.]", "", regex=True)
    df = df.copy()
    df["price"] = pd.to_numeric(price, errors="coerce").fillna(0.0)

    # Profit = price * subscribers
    df["profit"] = df["price"] * df["num_subscribers"]

    # Extract date from published_timestamp
    # Robust to missing/odd rows; invalid parse -> NaT then dropped from time-based groupbys
    df["published_date"] = df["published_timestamp"].astype(str).str.split("T").str[0]
    df["published_date"] = pd.to_datetime(df["published_date"], format="%Y-%m-%d", errors="coerce")

    # Drop rows without valid dates for time aggregations
    time_df = df.dropna(subset=["published_date"]).copy()
    time_df["Year"] = time_df["published_date"].dt.year
    time_df["Month_name"] = time_df["published_date"].dt.month_name()

    # Year-wise
    profitmap = time_df.groupby("Year")["profit"].sum().to_dict()
    subscribersmap = time_df.groupby("Year")["num_subscribers"].sum().to_dict()

    # Month-wise (across all years)
    profitmonthwise = time_df.groupby("Month_name")["profit"].sum().to_dict()
    monthwisesub = time_df.groupby("Month_name")["num_subscribers"].sum().to_dict()

    # Optional: order months Jan..Dec for prettier charts
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    profitmonthwise = {m: profitmonthwise.get(m, 0) for m in month_order if m in profitmonthwise}
    monthwisesub = {m: monthwisesub.get(m, 0) for m in month_order if m in monthwisesub}

    return profitmap, subscribersmap, profitmonthwise, monthwisesub
