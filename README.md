# 👷 Under Construction 🚧

# Online Course Recommendation App

Content-based course recommender built on real Udemy-style data. It cleans course titles, vectorises them (TF-IDF or similar), and serves “more-like-this” recommendations via a simple web UI. The repo also includes notebooks for EDA and a lightweight dashboard for quick data exploration. ([GitHub][1])

## Table of Contents

* Overview
* Features
* Project Structure
* Quickstart
* Usage
* Testing (pytest)
* Design Notes (Recommendation Approach)
* Data & Reproducibility
* Roadmap
* Contributing
* License

## Overview

This project demonstrates an end-to-end recommendation workflow:

1. load and clean course data,
2. build a vector space over course titles (and optionally metadata),
3. compute similarity,
4. serve ranked recommendations through a small web app, plus an interactive dashboard for exploration.
   Files currently include the web app (`app.py`), dashboard (`dashboard.py`), Jupyter notebooks, HTML templates, and CSV datasets. ([GitHub][1])

## Features

* Content-based recommendations using course title text (extendable to categories, price, ratings).
* Fast similarity lookup (cosine similarity over TF-IDF).
* Minimal web UI for searching/typing a course and getting similar ones.
* Optional interactive dashboard for exploring the dataset and recommendation quality.
* Reproducible EDA notebooks.

## Project Structure

```
.
├─ app.py                     # Web app entrypoint (Flask-style runner)
├─ dashboard.py               # Interactive dashboard (e.g., Streamlit)
├─ templates/                 # Jinja2 HTML templates for the web UI
├─ EDA_On_UdemyDataset.ipynb  # Exploratory data analysis
├─ Online_Course_Recommendation_Project.ipynb  # Modelling/prototyping
├─ udemy_course_data.csv      # Raw dataset (sample)
├─ UdemyCleanedTitle.csv      # Cleaned/derived data (e.g., titles)
├─ requirements.txt           # Python dependencies
└─ README.md
```

File names and folders reflect what’s currently in the repo. ([GitHub][1])

## Quickstart

### Prerequisites

* Python 3.10+ (3.11 recommended)
* macOS/Linux/Windows

### Setup

```bash
# 1) Clone
git clone https://github.com/AAdewunmi/Online-Course-Recommendation-App-Project.git
cd Online-Course-Recommendation-App-Project

# 2) Create & activate a virtual environment
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Web App

Most small Flask apps will run directly:

```bash
python app.py
# or (if the app uses Flask CLI)
# export FLASK_APP=app.py && flask run
# Windows (PowerShell): $env:FLASK_APP="app.py"; flask run
```

Then open the URL printed in your terminal (commonly [http://127.0.0.1:5000](http://127.0.0.1:5000)).

### Run the Dashboard (optional)

If `dashboard.py` uses Streamlit, run:

```bash
streamlit run dashboard.py
```

This will open a local browser window with interactive charts/filters.

## Usage

* Open the web app.
* Enter a course title or pick from examples (if provided).
* Submit to view top-N similar courses with basic metadata.

Tip: If you change the data CSVs, re-run the app so the vectoriser/similarity index is rebuilt.

## Testing (pytest)

Even for small data apps, tests are non-negotiable. Add a `tests/` package with unit tests for:

* text cleaning/tokenisation,
* vectoriser building (shape, non-empty vocabulary),
* similarity ranking (self-similarity highest, deterministic top-k),
* simple web route smoke tests.

Suggested layout:

```
tests/
  test_text_cleaning.py
  test_vectoriser.py
  test_similarity.py
  test_app_routes.py
```

Install pytest (if not already in `requirements.txt`) and run:

```bash
pip install pytest
pytest -q
```

Example assertions to include:

* Empty/short titles are handled without raising.
* Two identical titles return cosine similarity ≈ 1.0.
* Known query returns expected top-1 candidate.

## Design Notes (Recommendation Approach)

**Pipeline**

1. **Clean/normalise** titles (lowercasing, punctuation removal, optional stop-words).
2. **Vectorise** with TF-IDF over unigrams/bigrams; tune `min_df`, `max_df`, `ngram_range`.
3. **Similarity** via cosine similarity; precompute sparse matrix or use on-the-fly top-k with `sklearn.metrics.pairwise`.
4. **Ranking**: return top-k excluding the query item; optionally re-rank by auxiliary signals (rating, enrollments).
5. **Serving**: keep vectoriser and matrix in memory; expose a route that accepts a query and returns top-k.

**Why content-based first?**

* Works without user histories.
* Transparent and easy to explain.
* Fast to iterate and productionise.

**Extensions**

* Add fields (category/subject, price, rating) to the vector space via feature union.
* Add query expansion or approximate nearest neighbours (e.g., FAISS) for large datasets.
* Introduce collaborative filtering once you have user-item interactions.

## Data & Reproducibility

The repository includes CSVs for local experimentation (`udemy_course_data.csv`, `UdemyCleanedTitle.csv`). The notebooks (`EDA_On_UdemyDataset.ipynb`, `Online_Course_Recommendation_Project.ipynb`) document the cleaning and modelling steps so results can be reproduced and audited. ([GitHub][1])

When you change data:

* Re-run the modelling notebook to re-generate cleaned artifacts.
* Keep a data dictionary in the repo root (`DATA.md`) describing columns and assumptions.

## Roadmap

* [ ] Add proper error handling and input validation in the web layer.
* [ ] Persist vectoriser and similarity artifacts (e.g., `joblib`) for faster cold starts.
* [ ] Add ANN index for scalability (FAISS / ScaNN).
* [ ] Add basic analytics (top queries, CTR) to evaluate recommendation quality.
* [ ] Dockerfile + Compose for one-command local setup.
* [ ] CI with `pytest` and coverage gate.

## Contributing

1. Fork and create a feature branch.
2. Write tests for any change that touches logic.
3. Keep functions small and documented; prefer composition over giant scripts.
4. Run `pytest -q` before opening a PR.

## License

Add a `LICENSE` file (MIT or Apache-2.0 are common). Update this section once chosen.

---

[1]: https://github.com/AAdewunmi/Online-Course-Recommendation-App-Project "GitHub - AAdewunmi/Online-Course-Recommendation-App-Project: Online Course Recommendation App ||"

