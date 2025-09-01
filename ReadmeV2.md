# PhonePe Transaction Insights Dashboard

An interactive **Streamlit** dashboard for exploring India’s PhonePe transaction data across insurance, general transactions and user metrics. The app connects to a MySQL database, fetches aggregated metrics and visualizes them through dynamic bar/line charts and choropleth maps. Filters for year, quarter and state allow you to drill into specific regions or periods, and the top-10 views highlight leading states, districts and pincodes.

---

<!-- Collapsible, numbered Table of Contents with subheadings -->
<details>
  <summary><strong><mark>Table of Contents</mark></strong></summary>

- [1. About the Project](#1-about-the-project)
  - [1.1 What problem it solves](#11-what-problem-it-solves)
  - [1.2 Why you built it](#12-why-you-built-it)
  - [1.3 Key highlights](#13-key-highlights)
- [2. Features](#2-features)
- [3. Tech Stack](#3-tech-stack)
- [4. Installation](#4-installation)
  - [4.1 Prerequisites](#41-prerequisites)
  - [4.2 Project layout](#42-project-layout)
  - [4.3 Create and activate a virtual environment](#43-create-and-activate-a-virtual-environment)
  - [4.4 Install dependencies](#44-install-dependencies)
  - [4.5 Configure database connection](#45-configure-database-connection)
  - [4.6 Fix local file paths (one-time)](#46-fix-local-file-paths-one-time)
  - [4.7 Run the app](#47-run-the-app)
  - [4.8 Troubleshooting (quick)](#48-troubleshooting-quick)
- [5. Usage](#5-usage)
- [6. Configuration](#6-configuration)
- [7. Screenshots / Demo](#7-screenshots--demo)
- [8. Project Structure](#8-project-structure)
- [9. Contributing](#9-contributing)
- [10. License](#10-license)
- [11. Contact](#11-contact)

</details>


---

## 1. About the Project

**PhonePe Transaction Insights Dashboard** is an interactive Streamlit app that turns raw PhonePe-style aggregates into **clean, explorable insights** across three domains:
- **Insurance** (`agg_ins`, `top_ins`, `map_ins_hover`)
- **Transactions** (`agg_trans`, `top_trans`, `map_trans`)
- **Users** (`agg_user`, `top_user`, `map_user`)

It ships with a **modular codebase** (`StFiles/`) that cleanly separates **layout**, **database access**, and **visualization** logic:
- `stDBProcess.py` → MySQL access (SQLAlchemy + PyMySQL) + cached lookups
- `stGraph.py` → Altair/Plotly charts, choropleth helpers, string normalization
- `Layout.py` → tabbed UX, filters, orchestration
- `Insurance.py`, `Transaction.py`, `User.py` → feature pages
- `MyProfile.py` → sidebar profile card

Geospatial visuals are powered by **Plotly choropleths**, with optional **GeoPandas** support for robust reading of Geo/TopoJSON. Real-world naming inconsistencies are handled via mapping files in `src/`:
- `State Match.csv` (state normalization)
- `District Match.csv` (district ↔ GeoJSON reconciliation)

> (Optional) Add your flow illustration next to this section:  
> `<img src="src/Flow%20Chart.png" width="720" alt="App flow">`


### 1.1 What problem it solves

- **Fragmented analytics:** Raw aggregates live across multiple tables and levels (national/state/district/pincode). The app **stitches them together** into coherent stories.
- **Hard cross-section comparisons:** It’s tough to compare **time (year/quarter)** against **geography (state/district)** and **category** in spreadsheets. Interactive charts make this **one-click**.
- **Messy labels & mismatched names:** Real datasets contain hyphens, casing issues, legacy or split districts. Built-in **normalization & mapping** fix them so visuals “just work.”
- **Static reporting loops:** Replaces static slides with a **live dashboard** so analysts and business users can self-serve, drill down, and export views instantly.


### 1.2 Why you built it

- **Operational need:** Monitor India’s digital payments story (adoption, usage, product mix) with **business-friendly visuals** and **repeatable filters**.
- **Reusability:** A **template-quality** architecture you can reuse for other datasets—swap the tables, keep the UX.
- **Learning & speed:** Consolidate hands-on skills in **Streamlit, SQL, Altair/Plotly, Geo/TopoJSON** and deliver value **faster than ad-hoc notebooks**.
- **Data quality guardrails:** Bake state/district mapping, casing, and hyphen handling into the product—not as one-off scripts.


### 1.3 Key highlights

- **🧭 Three lenses, one app:** Insurance • Transactions • Users — each with **yearly/quarterly overviews**, **Top-10 entities**, and **maps**.
- **📈 Dual-axis insights:** Combined **bar + line** charts (e.g., Amount vs. Count) with sensible scales and tooltips.
- **🗺️ State & district heatmaps:** Toggle between **amount** and **count**; district choropleths auto-detect keys and handle Geo/TopoJSON.
- **🎛️ Smart filters:** Multi-select **Year / Quarter / State** with **tab-locking** to avoid cross-filter confusion.
- **🧹 Name normalization:** `normalize_state_name()` + **State/District mapping CSVs** eliminate label noise (hyphens, case, legacy spellings).
- **⚡ Fast & cached:** `@st.cache_data(ttl=600)` keeps navigation snappy while hitting MySQL only when needed.
- **🧩 Clean separation of concerns:** DB queries isolated from charts; pages remain thin and readable.
- **🖥️ Portable paths:** Uses **project-relative** paths for GeoJSON/CSVs (`src/...`) across OSes.
- **🧪 Real-world ready:** Helpful errors for missing Geo keys, safe identifier checks for SQL objects, defensive parsing.

---

## 2. Features

- ✅ **Interactive exploration across three lenses:** Insurance, Transactions, and Users in one dashboard.
- ✅ **Dual-axis charts & Top-10 rankings:** Bar+line views (Amount vs Count) with quick comparisons by year/quarter/state.
- ✅ **Toggleable heatmaps with smart filters:** State & district choropleths (amount/count) plus multi-select filters with tab locking.

---

## 3. Tech Stack

- ✅ **Frontend/UI:** Streamlit  
- ✅ **Backend:** Python 3.10+  
- ✅ **Database:** MySQL (via SQLAlchemy + PyMySQL)  
- ✅ **Libraries & Tools:** Pandas, NumPy, Altair, Plotly, Matplotlib, Requests, Pathlib/JSON; *(optional for district maps)* GeoPandas, Shapely, Fiona; Data assets: GeoJSON + `src/State Match.csv`, `src/District Match.csv`

---

## 4. Installation

Follow these steps to run the **PhonePe Transaction Insights Dashboard** locally.

### 4.1) Prerequisites
- **Python** 3.10 or newer  
- **MySQL** 8.x (or compatible) with network access  
- **Git** (optional, for cloning)  
- *(Optional, for Geo/TopoJSON)* **GDAL stack** via `geopandas`, `fiona`, `shapely`

> **Windows tip (Geo stack):** try `pip install geopandas` first (prebuilt wheels). If it fails, use Conda:  
> `conda install -c conda-forge geopandas fiona shapely gdal`

---

### 4.2) Get the source code

**Option A — Clone the repository (recommended)**
```bash
git clone https://github.com/mani-baskar/PhonePe-Trans-Insights.git
cd PhonePe-Trans-Insights
````

> To update later: `git pull origin main`

**Option B — Download as ZIP**

1. Open: [mani-baskar/PhonePe-Trans-Insights](https://github.com/mani-baskar/PhonePe-Trans-Insights)
2. Click **Code** → **Download ZIP**
3. Extract and open the folder in your workspace (e.g., VS Code).

---

### 4.3) Create and activate a virtual environment

**Windows (PowerShell)**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 4.4) Install dependencies

```bash
pip install --upgrade pip
pip install streamlit pandas numpy sqlalchemy pymysql altair plotly requests matplotlib ipykernel
# Optional (recommended for district maps & TopoJSON/GeoJSON handling)
pip install geopandas shapely fiona
```

---

### 4.5) Project layout

Ensure your folder structure matches (move files if needed).
For the latest structure, see the repo: [mani-baskar/PhonePe-Trans-Insights.git](https://github.com/mani-baskar/PhonePe-Trans-Insights.git)

```
PhonePe-Trans-Insights/
├─ app.py
├─ StFiles/
│  ├─ __init__.py
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
└─ assets/            # (optional: logos, images, avatar, etc.)
```

> Create an empty `StFiles/__init__.py` so `StFiles` is treated as a package.

---

### 4.6) Insert PhonePe data into MySQL

* **Schema:** Import tables from `DBTable.sql` (in the repo) into your MySQL database.
  This will create the required tables with correct names.
* **Load data:** Use `phonepe_data_loader.ipynb` (in the repo) to download the official PhonePe data into your local folder and bulk-load it into the newly created tables.
* After the data load completes successfully, proceed to the next steps.

> Ensure the following tables exist and are populated (as referenced by the app):
> `agg_ins`, `agg_trans`, `agg_user`, `map_ins_hover`, `map_trans`, `map_user`, `top_ins`, `top_trans`, `top_user`.

---

### 4.7) Configure database connection

Open `StFiles/stDBProcess.py` and set your MySQL credentials/host/database:

```python
DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME = (
    "<user>", "<password>", "<host>", "3306", "<database_name>"
)
```

These tables must include the columns used in queries (e.g., `year`, `quarter`, `state`, `payment_count`, `payment_amount`, etc.).

> **Best practice:** don’t commit credentials. You can read from environment variables:
>
> ```python
> import os
> DB_USER = os.getenv("PP_DB_USER", "root")
> DB_PASS = os.getenv("PP_DB_PASS", "")
> DB_HOST = os.getenv("PP_DB_HOST", "127.0.0.1")
> DB_PORT = os.getenv("PP_DB_PORT", "3306")
> DB_NAME = os.getenv("PP_DB_NAME", "PhonePe")
> ```

---

### 4.8) Fix local file paths (one-time)

Update any absolute Windows paths to project-relative paths under `src/`.

```python
# BEFORE (absolute path)
DISTRICTS_PATH = "Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\india-districts-2019-734.json"

# AFTER (project-relative path)
DISTRICTS_PATH = "src/india-districts-2019-734.json"
```

Do the same for CSVs:

```python
# BEFORE
pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\State Match.csv")
pd.read_csv("Y:\\Manikandan\\Guvi Class\\Projects\\PhonePe-Trans-Insights\\src\\District Match.csv")

# AFTER
pd.read_csv("src/State Match.csv")
pd.read_csv("src/District Match.csv")
```

**Optional (profile image):** In `StFiles/MyProfile.py`:

```python
show_circular_image("assets/avatar.png", 180)
```

---

### 4.9) Run the app

From the project root:

```bash
streamlit run app.py
```

Then open the URL printed by Streamlit (e.g., `http://localhost:8501`).

---

### 4.10) Troubleshooting (quick)

* **Cannot connect to DB:** verify host/port, firewall, and user privileges. Try `mysql -h <host> -u <user> -p`.
* **GeoJSON errors / empty maps:** confirm `src/india-districts-2019-734.json` exists and is valid; ensure `geopandas` if reading TopoJSON.
* **`No module named StFiles`:** make sure `StFiles/` exists with `__init__.py`, and you’re running from repo root.
* **Matplotlib/Altair warnings:** usually harmless; keep `streamlit`, `altair`, `plotly`, `matplotlib` up to date.

## Usage

```bash
# Preferred
streamlit run app.py
```

---

## Configuration

* Use environment variables (recommended) for DB credentials (see Installation §4.5).
* Place Geo/CSV assets in `src/`.
* Optional: `.env` + a small loader if you prefer (`python-dotenv`).

---

## Screenshots / Demo

> Add screenshots or GIFs here for better presentation.
>
> Example embed:
>
> ```md
> <p align="center">
>   <img src="src/Flow%20Chart.png" alt="App flow" width="720">
> </p>
> ```

---

## Project Structure

```
PhonePe-Trans-Insights/
├─ app.py
├─ StFiles/
│  ├─ __init__.py
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
│  └─ india-districts-2019-734.json
└─ assets/
```

---

## Contributing

Contributions are welcome! 🎉 Bug fixes, new charts/pages, docs, and state/district mapping improvements are all appreciated.

### How to contribute

1. **Fork** this repository
2. **Create a branch**

   ```bash
   git checkout -b feature/<short-title>
   ```
3. **Set up your env** (from repo root)

   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate

   pip install --upgrade pip
   pip install streamlit pandas numpy sqlalchemy pymysql altair plotly requests matplotlib
   # Optional for district maps:
   pip install geopandas shapely fiona
   ```
4. **Run locally**

   ```bash
   streamlit run app.py
   ```
5. **Commit**

   ```bash
   git add -A
   git commit -m "feat: add <what> to <where>"
   ```
6. **Push**

   ```bash
   git push origin feature/<short-title>
   ```
7. **Open a Pull Request (PR)** with a clear title and description

### Project conventions

* **Structure:** keep app code under `StFiles/`; use project-relative paths
* **Database:** never commit real credentials; prefer environment variables
* **Charts/Maps:** reuse helpers in `stGraph.py`; cache heavy calls with `@st.cache_data`
* **Data hygiene:** use provided state/district normalization & mapping CSVs

### PR checklist

* [ ] Works in relevant tab(s) (Insurance/Transactions/Users)
* [ ] No hard-coded credentials or absolute paths
* [ ] Reuses chart/map helpers where possible
* [ ] Queries return non-empty data for example filters
* [ ] README/docs updated if behavior/setup changed

---

## License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

## Contact

👤 **Manikandan Baskar**

* Email: [mani111355@gmail.com](mailto:mani111355@gmail.com)
* LinkedIn: [Manikandan Baskar](https://linkedin.com/in/mani-baskar)
* GitHub: [@mani-baskar](https://github.com/mani-baskar)

