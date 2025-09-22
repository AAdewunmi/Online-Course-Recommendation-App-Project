# Online Course Recommendation App

A lightweight Flask application for searching Udemy courses by keyword and exploring dataset insights via an interactive dashboard. The app uses `pandas` for data wrangling and `Chart.js` for visualisations.

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-2.x-000000?logo=flask&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white">
  <img alt="scikit-learn" src="https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green">
</p>

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Architecture](#architecture)
* [Dataset](#dataset)
* [Quick Start](#quick-start)
* [Project Structure](#project-structure)
* [Usage](#usage)
* [Testing](#testing)
* [Configuration](#configuration)
* [Screenshots](#screenshots)
* [Roadmap](#roadmap)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

The application has two main surfaces:

1. **Home** – Keyword search across `course_title` (case-insensitive, literal match).
2. **Dashboard** – Descriptive statistics, including:

   * Number of **Subscribers** Domain (Subject) Wise
   * Number of **Courses** Level Wise
   * **Subscribers** Year Wise
   * **Profit** Year Wise
   * **Profit** Month Wise
   * **Subscribers** Month Wise

The repo includes a ready-to-use CSV (`UdemyCleanedTitle.csv`) and simple Flask views that render Bootstrap-powered templates.

---

## Features

* 🔎 **Fast keyword search** over course titles
* 📊 **Interactive charts** (Chart.js) for quick insights
* 🧹 **Robust CSV handling** (column normalisation, safe parsing)
* 🧩 **Modular dashboard helpers** (clean Pandas groupbys)
* 🧪 **Test-ready** structure with `pytest` examples (optional)

---

## Tech Stack

* **Backend:** Flask (Python)
* **Data:** pandas, numpy
* **ML/Text utils:** scikit-learn (optional TF-IDF), neattext
* **Frontend:** Bootstrap 4, Chart.js

---

## Architecture

* `app.py`

  * `/` (Home): reads CSV, performs keyword search in `course_title`, renders `index.html`
  * `/dashboard`: computes aggregates via `dashboard.py`, renders `dashboard.html`
* `dashboard.py`

  * Pure-Python helpers that return dictionaries used by the charts
* `templates/`

  * `index.html` – search form + results list
  * `dashboard.html` – six charts driven by injected dictionaries

---

## Dataset

* **File:** `UdemyCleanedTitle.csv`
* **Required columns:**
  `course_title`, `url`, `price`, `num_subscribers`, `level`, `published_timestamp`, `subject`
* **Notes:**

  * `price` is coerced to numeric (non-numeric like “Free/TRUE” become 0)
  * `published_timestamp` parsed as date (YYYY-MM-DD from `YYYY-MM-DDTHH:MM:SSZ`)

---

## Quick Start

### 1) Clone

```bash
git clone https://github.com/AAdewunmi/Online-Course-Recommendation-App-Project.git
cd Online-Course-Recommendation-App-Project
```

### 2) Create & activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate           # macOS/Linux
# .\venv\Scripts\activate          # Windows (PowerShell)
```

### 3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install the essentials:

```bash
pip install flask pandas numpy scikit-learn neattext
```

### 4) Run the app

```bash
export FLASK_APP=app.py            # macOS/Linux
export FLASK_ENV=development
flask run

# or simply
python app.py
```

Open: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Project Structure

```
Online-Course-Recommendation-App-Project/
├─ app.py
├─ dashboard.py
├─ UdemyCleanedTitle.csv
├─ templates/
│  ├─ index.html
│  └─ dashboard.html
├─ static/                      # (optional)
├─ requirements.txt             # (recommended)
├─ tests/
├─ test_app_routes.py
├─ test_dashboard_helpers.py
└─ conftest.py
```

---

## Usage

### Home (Search)

* Navigate to `/`
* Enter keywords (e.g. “excel”, “python”, “finance”)
* Results show course titles with a **View Course** button linking to `url`

### Dashboard (Descriptive Stats)

* Navigate to `/dashboard`
* Six charts render using aggregated dictionaries injected by Flask:

  * `valuecounts`, `levelcounts`, `subjectsperlevel`
  * `yearwiseprofitmap`, `subscriberscountmap`
  * `profitmonthwise`, `monthwisesub`

---

## Testing

Run tests:

```bash
pytest -q
```

---

## Configuration

No environment variables are required for basic usage. Place `UdemyCleanedTitle.csv` in the repository root (or update the path in `app.py`).

---

## Screenshots

> Add your screenshots/gifs here once the app is running locally.

* **Home (Search)**

<img width="1910" height="673" alt="Image" src="https://github.com/user-attachments/assets/b9c1d814-3610-4566-89cb-115e8219f8be" />

* **Dashboard (Charts)**

<img width="1906" height="761" alt="Image" src="https://github.com/user-attachments/assets/3922351b-d956-4c67-bcd1-ab83d34b41ff" />

---

## Roadmap

* TF-IDF–based **“Similar Courses”** recommendations as a secondary mode
* Search over additional fields (e.g., subject, level)
* Pagination / client-side filtering for large result sets
* Dockerfile + Compose for one-command setup
* GitHub Actions for CI (`pytest`, lint)

---

## Troubleshooting

* **Black & white charts**: ensure you’re using the latest `dashboard.html` with color palette (Chart.js dataset `backgroundColor`/`borderColor` explicitly set).
* **KeyError on columns**: confirm the CSV contains required columns:
  `course_title, url, price, num_subscribers, level, published_timestamp, subject`
* **Unicode/CSV errors**: try `encoding="utf-8"` in `pd.read_csv` or clean the CSV.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue to discuss what you’d like to change. If you add dependencies, update `requirements.txt`.

**Suggested workflow**

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/something`
3. Commit changes with clear messages
4. Add/Update tests
5. Open a PR

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

