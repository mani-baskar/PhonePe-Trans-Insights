# PhonePe Transaction Insights Dashboard

An interactive **Streamlit** dashboard for exploring India’s PhonePe transaction data across insurance, general transactions and user metrics. The app connects to a MySQL database, fetches aggregated metrics and visualizes them through dynamic bar/line charts and choropleth maps. Filters for year, quarter and state allow you to drill into specific regions or periods, and the top‑10 views highlight leading states, districts and pincodes.

<details>
  <summary><strong>Table of Contents (click to expand)</strong></summary>

- [Why this project?](#why-this-project)
- [Installation](#installation)
- [Recommended configurations](#recommended-configurations)
- [Custom configurations](#custom-configurations)
- [Updating](#updating)
- [Uninstallation](#uninstallation)
- [Contributing](#contributing)
- [License](#license)

</details>

## Why this project?

Digital payments have exploded in India, and services like **PhonePe** generate enormous volumes of data. Understanding how transactions vary by **state**, **quarter**, or **product line** is valuable for businesses, analysts, and researchers.

This dashboard delivers:

- **Comprehensive views:** National overviews showing yearly and quarterly trends for payment volume and transaction counts.
- **Top entities:** Grouped bar/line charts highlighting the top ten states, districts, and pincodes by volume, count, or user registrations.
- **Interactive heatmaps:** Choropleth maps for states and districts to visualize the geographic distribution of amounts or counts *(with a simple toggle between metrics)*.
- **Flexible filtering:** Multi-select filters for year, quarter, and state; one tab locks at a time to avoid cross-filtering confusion. Clear a tab to unlock others and refresh the view.
- **Modular design:** Clean separation of concerns for database access, graph rendering, and UI logic—making the codebase easy to extend and maintain.


## Installation

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

```


## Recommended configurations
...

## Custom configurations
...

## Updating
...

## Uninstallation
...

## Contributing
...

## License
...
