# PhonePe Transaction Insights Dashboard

An interactive Streamlit dashboard for exploring India’s PhonePe transaction data across insurance, general transactions and user metrics. The app connects to a MySQL database, fetches aggregated metrics and visualizes them through dynamic bar/line charts and choropleth maps. Filters for year, quarter and state allow you to drill into specific regions or periods, and the top‑10 views highlight leading states, districts and pincodes.

---

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Screenshots / Demo](#screenshots--demo)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## About the Project

**PhonePe Transaction Insights Dashboard** is an interactive Streamlit app that turns raw PhonePe-style aggregates into **clean, explorable insights** across three domains:
- **Insurance** (`agg_ins`, `top_ins`, `map_ins_hover`)
- **Transactions** (`agg_trans`, `top_trans`, `map_trans`)
- **Users** (`agg_user`, `top_user`, `map_user`)

It ships with a **modular codebase** (`StFiles/`) that cleanly separates **layout**, **database access**, and **visualization** logic:
- `stDBProcess.py` → secure MySQL access + cached lookups
- `stGraph.py` → Altair/Plotly charts, choropleth helpers, string normalization
- `Layout.py` → tabbed UX, filters, and orchestration
- `Insurance.py`, `Transaction.py`, `User.py` → feature pages
- `MyProfile.py` → sidebar profile card

Geospatial visuals are powered by **Plotly choropleths**, with optional **GeoPandas** support for robust reading of Geo/TopoJSON. Real-world naming inconsistencies are handled via mapping files in `src/`:
- `State Match.csv` (state normalization)
- `District Match.csv` (district ↔ GeoJSON reconciliation)

> (Optional) Add your flow illustration next to this section:  
> `<img src="src/Flow%20Chart.png" width="720" alt="App flow">`


### What problem it solves

- **Fragmented analytics:** Raw aggregates live across multiple tables and levels (national/state/district/pincode). The app **stitches them together** into coherent stories.
- **Hard cross-section comparisons:** It’s tough to compare **time (year/quarter)** against **geography (state/district)** and **category** in spreadsheets. Interactive charts make this **one-click**.
- **Messy labels & mismatched names:** Real datasets contain hyphens, casing issues, legacy or split districts. Built-in **normalization & mapping** fix them so visuals “just work.”
- **Static reporting loops:** Replaces static slides with a **live dashboard** so analysts and business users can self-serve, drill down, and export views instantly.


### Why you built it

- **Operational need:** To consistently monitor India’s digital payments story (adoption, usage, product mix) with **business-friendly visuals** and **repeatable filters**.
- **Reusability:** A **template-quality** architecture you can reuse for other public or enterprise datasets—swap the tables, keep the UX.
- **Learning & speed:** To consolidate hands-on skills in **Streamlit, SQL, Altair/Plotly, Geo/TopoJSON**, and deploy a tool that brings value **faster than ad-hoc notebooks**.
- **Data quality guardrails:** To encode data hygiene (state/district mapping, casing, hyphen handling) into the product, not as a one-off script.


### Key highlights

- **🧭 Three lenses, one app:** Insurance • Transactions • Users — each with **yearly/quarterly overviews**, **Top-10 entities**, and **maps**.
- **📈 Dual-axis insights:** Combined **bar + line** charts (e.g., Amount vs. Count) with sensible scales and tooltips for quick interpretation.
- **🗺️ State & district heatmaps:** Toggle between **amount** and **count**; district choropleths auto-detect keys and handle Geo/TopoJSON gracefully.
- **🎛️ Smart filters:** Multi-select **Year / Quarter / State** with **tab-locking** to avoid cross-filter confusion; clear to unlock and pivot quickly.
- **🧹 Name normalization:** `normalize_state_name()` + **State/District mapping CSVs** eliminate label noise (hyphens, case, legacy spellings).
- **⚡ Fast & cached:** `@st.cache_data(ttl=600)` keeps navigation snappy while hitting MySQL only when needed.
- **🧩 Clean separation of concerns:** DB queries isolated from charts; pages remain thin and readable; easy to extend a new chart or KPI.
- **🖥️ Portable paths:** Uses **project-relative** paths for GeoJSON/CSVs (`src/...`) so the app runs the same on Windows/macOS/Linux.
- **🧪 Real-world ready:** Error messages for missing Geo keys, safe identifier checks for SQL objects, and defensive parsing for numerics.
- **🛠️ Extensible:** Drop in new tables or KPIs (e.g., merchant segments, device mix) and reuse the same charting + mapping utilities.


---

## Features

- ✅ **Interactive exploration across three lenses:** Insurance, Transactions, and Users in one dashboard.
- ✅ **Dual-axis charts & Top-10 rankings:** Bar+line views (Amount vs Count) with quick comparisons by year/quarter/state.
- ✅ **Toggleable heatmaps with smart filters:** State & district choropleths (amount/count) plus multi-select filters with tab locking.


---

## Tech Stack

- ✅ **Frontend/UI:** Streamlit  
- ✅ **Backend:** Python 3.10+ (modular Streamlit app under `StFiles/`)  
- ✅ **Database:** MySQL (via SQLAlchemy + PyMySQL)  
- ✅ **Others (Libraries & Tools):** Pandas, NumPy, Altair, Plotly, Matplotlib, Requests, Pathlib/JSON; *(optional for district maps)* GeoPandas, Shapely, Fiona; Data assets: GeoJSON + `src/State Match.csv`, `src/District Match.csv`


---

## Installation
```bash
# Clone the repo
git clone https://github.com/username/repo-name.git

# Navigate to project folder
cd repo-name

# Install dependencies
pip install -r requirements.txt   # or npm install
````

## Installation

<details>
  <summary><strong><mark> Installation steps</mark></strong> — click to expand</summary>

- [1) Prerequisites](#1-prerequisites)
- [2) Project layout](#2-project-layout)
- [3) Create and activate a virtual environment](#3-create-and-activate-a-virtual-environment)
- [4) Install dependencies](#4-install-dependencies)
- [5) Configure database connection](#5-configure-database-connection)
- [6) Fix local file paths (one-time)](#6-fix-local-file-paths-one-time)
- [7) Run the app](#7-run-the-app)
- [8) Troubleshooting (quick)](#8-troubleshooting-quick)

</details>



Follow these steps to run the **PhonePe Transaction Insights Dashboard** locally.

### 1) Prerequisites
- **Python** 3.10 or newer
- **MySQL** 8.x (or compatible) server with network access
- **Git** (optional, for cloning)
- (Optional, for TopoJSON/GeoJSON handling) **GDAL stack** via `geopandas`, `fiona`, `shapely`

> Windows tip for Geo stack: prefer `pip install geopandas` first (it pulls prebuilt wheels). If it fails, install via Conda:  
> `conda install -c conda-forge geopandas fiona shapely gdal`

---

### 2) Project layout

Create this structure (move your files accordingly):

```

PhonePe-Trans-Insights/
├─ app.py
├─ StFiles/
│  ├─ **init**.py
│  ├─ Layout.py
│  ├─ Insurance.py
│  ├─ Transaction.py
│  ├─ User.py
│  ├─ stDBProcess.py
│  ├─ stGraph.py
│  └─ MyProfile.py
├─ src/
│  ├─ State Match.csv
│  ├─ District Match.csv
│  └─ india-districts-2019-734.json   # download/place this file here
└─ assets/ (optional: logos, avatars, etc.)

````

Create an empty `__init__.py` so `StFiles` is treated as a Python package.

---

### 3) Create and activate a virtual environment

**Windows (PowerShell)**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
````

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 4) Install dependencies

```bash
pip install --upgrade pip
pip install streamlit pandas numpy sqlalchemy pymysql altair plotly requests
# Optional (recommended for district maps & TopoJSON/GeoJSON convenience)
pip install geopandas shapely fiona
# If you see errors with the above on Windows, use conda-forge as noted in step 1.
# Also required by app.py charts:
pip install matplotlib
```

---

### 5) Configure database connection

Open `StFiles/stDBProcess.py` and set your MySQL credentials/host/database:

```python
DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME = (
    "<user>", "<password>", "<host>", "3306", "<database_name>"
)
```

> Security best-practice: don’t commit real credentials. You can refactor to read from environment variables:
>
> ```python
> import os
> DB_USER = os.getenv("PP_DB_USER", "root")
> DB_PASS = os.getenv("PP_DB_PASS", "")
> DB_HOST = os.getenv("PP_DB_HOST", "127.0.0.1")
> DB_PORT = os.getenv("PP_DB_PORT", "3306")
> DB_NAME = os.getenv("PP_DB_NAME", "PhonePe")
> ```

Ensure your DB has the required tables referenced by the app (examples used in queries):

* `agg_ins`, `agg_trans`, `agg_user`
* `map_ins_hover`, `map_trans`, `map_user`
* `top_ins`, `top_trans`, `top_user`

These tables should contain the columns used by the queries (e.g., `year`, `quarter`, `state`, `payment_count`, `payment_amount`, etc.).

---

### 6) Fix local file paths (one-time)

In `StFiles/Insurance.py`, `StFiles/Transaction.py`, and `StFiles/User.py`, update any absolute Windows paths to use the `src/` folder. Example:

```python
# BEFORE (absolute path)
DISTRICTS_PATH = "Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\india-districts-2019-734.json"

# AFTER (project-relative path)
DISTRICTS_PATH = "src/india-districts-2019-734.json"
```

Do the same for the CSVs:

```python
# BEFORE
pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\State Match.csv")
pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\District Match.csv")

# AFTER
pd.read_csv("src/State Match.csv")
pd.read_csv("src/District Match.csv")
```

**Profile image (optional):** In `StFiles/MyProfile.py`, replace the hardcoded path with a project asset, e.g.:

```python
show_circular_image("assets/avatar.png", 180)
```

---

### 7) Run the app

From the project root:

```bash
streamlit run app.py
```

Streamlit will print a local URL (e.g., `http://localhost:8501`). Open it in your browser.

---

### 8) Troubleshooting (quick)

* **Cannot connect to DB**: verify host/port, firewall rules, and user privileges. Try `mysql -h <host> -u <user> -p`.
* **GeoJSON errors / empty maps**: confirm `src/india-districts-2019-734.json` exists and has valid features; ensure `geopandas` is installed if reading TopoJSON.
* **Import errors like `No module named StFiles`**: ensure the folder name is `StFiles/` and `__init__.py` exists; run from repo root.
* **Matplotlib/Altair rendering warnings**: usually harmless; ensure the latest `streamlit`, `altair`, `plotly`, `matplotlib`.

You’re all set! Launch the app, select a tab (Insurance/Transactions/Users), and explore India’s digital payments story interactively.

---

## Usage

```bash
# Run the app
python app.py      # or streamlit run app.py
```

---

## Configuration

* `.env` file setup (if any)
* API keys or database connection info
* Custom configs

---

## Screenshots / Demo

(Add images or GIFs here for better presentation)

---

## Project Structure

```
repo-name/
│-- src/
│-- data/
│-- docs/
│-- tests/
│-- README.md
│-- requirements.txt
```

---

## Contributing

Contributions are welcome!

1. Fork the repo
2. Create a branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push branch (`git push origin feature-name`)
5. Create Pull Request

---

## Contact

👤 **Your Name**

* Email: [mani111355@gmail.com](mailto:mani111355@gmail.com)
* LinkedIn: [Manikandan Baskar](https://linkedin.com/in/mani-baskar)
* GitHub: [@mani-baskar](https://github.com/mani-baskar)

---
