# PhonePe Transaction Insights Dashboard

An interactive **Streamlit** dashboard for exploring India’s PhonePe transaction data across insurance, transactions, and user metrics. The app connects to MySQL, fetches aggregated metrics, and visualizes them via dynamic bar/line charts and choropleth maps. Filters for **Year**, **Quarter**, and **State** let you drill into specific regions or periods, and *Top-10* views highlight leading states, districts, and pincodes.

---

<!-- Collapsible, numbered Table of Contents with subheadings that match the headers below -->
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
  - [4.2 Get the source code](#42-get-the-source-code)
  - [4.3 Create and activate a virtual environment](#43-create-and-activate-a-virtual-environment)
  - [4.4 Install dependencies](#44-install-dependencies)
  - [4.5 Project layout](#45-project-layout)
  - [4.6 Insert PhonePe data into MySQL](#46-insert-phonepe-data-into-mysql)
  - [4.7 Configure database connection](#47-configure-database-connection)
  - [4.8 Fix local file paths (one-time)](#48-fix-local-file-paths-one-time)
  - [4.9 Run the app](#49-run-the-app)
  - [4.10 Troubleshooting (quick)](#410-troubleshooting-quick)
- [5. Usage](#5-usage)
  - [5.1 Start the app](#51-start-the-app)
  - [5.2 Understand the layout](#52-understand-the-layout)
  - [5.3 Run a query (filters → process)](#53-run-a-query-filters--process)
  - [5.4 Insurance tab — what you’ll see](#54-insurance-tab--what-youll-see)
  - [5.5 Transaction tab — what you’ll see](#55-transaction-tab--what-youll-see)
  - [5.6 User tab — what you’ll see](#56-user-tab--what-youll-see)
  - [5.7 Clearing filters & switching tabs](#57-clearing-filters--switching-tabs)
  - [5.8 Notes & tips](#58-notes--tips)
- [6. Contact](#6-contact)

</details>

---

## 1. About the Project

**PhonePe Transaction Insights Dashboard** turns raw PhonePe-style aggregates into **clean, explorable insights** across three domains:
- **Insurance** (`agg_ins`, `top_ins`, `map_ins_hover`)
- **Transactions** (`agg_trans`, `top_trans`, `map_trans`)
- **Users** (`agg_user`, `top_user`, `map_user`)

It ships with a **modular codebase** (`StFiles/`) that separates **layout**, **database access**, and **visualization**:
- `stDBProcess.py` → MySQL access (SQLAlchemy + PyMySQL) + cached lookups  
- `stGraph.py` → Altair/Plotly charts, choropleth helpers, string normalization  
- `Layout.py` → tabbed UX, filters, orchestration  
- `Insurance.py`, `Transaction.py`, `User.py` → feature pages  
- `MyProfile.py` → sidebar profile card  

Geospatial visuals use **Plotly choropleths**, with optional **GeoPandas** for Geo/TopoJSON. Real-world naming inconsistencies are handled via mapping files in `src/`:
- `State Match.csv` (state normalization)
- `District Match.csv` (district ↔ GeoJSON reconciliation)

<p align="center">
  <img src="assets/Flow%20chart.png" width="980" alt="app Flow">
  <br><em>App Process Flow</em>
</p>

### 1.1 What problem it solves
- **Fragmented analytics** across levels (national/state/district/pincode) → unified, coherent stories.  
- **Hard cross-section comparisons** (time × geography × category) → one-click interactive charts.  
- **Messy labels & mismatched names** → built-in normalization & mapping.  
- **Static reporting loops** → a live, self-serve dashboard.

### 1.2 Why you built it
- Monitor India’s digital payments with **business-friendly visuals** and repeatable filters.  
- Provide a **template-quality** architecture you can reuse for other datasets.  
- Consolidate hands-on skills in **Streamlit, SQL, Altair/Plotly, Geo/TopoJSON**.  
- Bake **data hygiene** into the product.

### 1.3 Key highlights
- **Three lenses** (Insurance • Transactions • Users) with overviews, Top-10s, and maps.  
- **Dual-axis** bar+line insights (e.g., Amount vs Count).  
- **Heatmaps** with **Amount ↔ Count** toggles (or Registered Users ↔ App Opens).  
- **Smart filters** with **tab-locking** to avoid cross-filter confusion.  
- Caching with `@st.cache_data`, portable paths (`src/...`), and defensive parsing.

---

## 2. Features
- ✅ **Interactive exploration** across Insurance, Transactions, and Users.  
- ✅ **Dual-axis charts & Top-10 rankings** by year/quarter/state.  
- ✅ **Toggleable heatmaps** (Amount/Count; Registered Users/App Opens) with multi-select filters.

---

## 3. Tech Stack
- ✅ **Frontend/UI:** Streamlit  
- ✅ **Backend:** Python 3.10+  
- ✅ **Database:** MySQL (SQLAlchemy + PyMySQL)  
- ✅ **Libraries & Tools:** Pandas, NumPy, Altair, Plotly, Matplotlib, Requests, Pathlib/JSON  
  *(optional for district maps)* GeoPandas, Shapely, Fiona  
  Data assets: GeoJSON + `src/State Match.csv`, `src/District Match.csv`

---

## 4. Installation

Follow these steps to run the **PhonePe Transaction Insights Dashboard** locally.

### 4.1) Prerequisites
- **Python** 3.10 or newer  
- **MySQL** 8.x (or compatible) with network access  
- **Git** (optional, for cloning)  
- *(Optional, for Geo/TopoJSON)* **GDAL stack** via `geopandas`, `fiona`, `shapely`

> **Windows tip (Geo stack):** try `pip install geopandas` first. If it fails, use Conda:  
> `conda install -c conda-forge geopandas fiona shapely gdal`

### 4.2) Get the source code
**Option A — Clone (recommended)**
```bash
git clone https://github.com/mani-baskar/PhonePe-Trans-Insights.git
cd PhonePe-Trans-Insights
````

> Update later with: `git pull origin main`

**Option B — Download ZIP**

1. Open: [mani-baskar/PhonePe-Trans-Insights](https://github.com/mani-baskar/PhonePe-Trans-Insights)
2. **Code** → **Download ZIP**
3. Extract and open the folder in your workspace.

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

### 4.4) Install dependencies

```bash
pip install --upgrade pip
pip install streamlit pandas numpy sqlalchemy pymysql altair plotly requests matplotlib ipykernel
# Optional (district maps / GeoJSON convenience)
pip install geopandas shapely fiona
```


### 4.5) Project layout

Ensure your structure matches (move files if needed). For the latest, see the repo.

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
└─ assets/     # (optional: logos, images, avatar, etc.)
```

### 4.6) Insert PhonePe data into MySQL

* **Schema:** import `DBTable.sql` into MySQL (creates required tables).
* **Load:** run `phonepe_data_loader.ipynb` to download official PhonePe data and bulk-load it.
* Ensure these tables exist & are populated:
  `agg_ins`, `agg_trans`, `agg_user`, `map_ins_hover`, `map_trans`, `map_user`, `top_ins`, `top_trans`, `top_user`.



<details>
  <summary><Mark><strong>Screenshots (click to expand)</strong></Mark></summary>
<p align="center">
  <img src="assets/SQL%20Import%201.png" width="900" alt="Screenshot 1"><br>
  <img src="assets/SQL%20Import%202.png" width="900" alt="Screenshot 2"><br>
  <img src="assets/SQL%20Import%203.png" width="900" alt="Screenshot 3">
</p>

</details>


### 4.7) Configure database connection

Edit `StFiles/stDBProcess.py`:

```python
DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME = (
    "<user>", "<password>", "<host>", "3306", "<database_name>"
)
```

### 4.8) Fix local file paths (one-time)

Use project-relative paths under `src/`:

```python
# BEFORE
DISTRICTS_PATH = "Y:\\...\\src\\india-districts-2019-734.json"
# AFTER
DISTRICTS_PATH = "src/india-districts-2019-734.json"

# BEFORE
pd.read_csv("Y:\\...\\src\\State Match.csv")
pd.read_csv("Y:\\...\\src\\District Match.csv")
# AFTER
pd.read_csv("src/State Match.csv")
pd.read_csv("src/District Match.csv")
```

*(Optional)* In `MyProfile.py`:

```python
show_circular_image("assets/avatar.png", 180)
```

### 4.9) Run the app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (e.g., `http://localhost:8501`).

### 4.10) Troubleshooting (quick)

* **DB connection:** verify host/port, firewall, user privileges (`mysql -h <host> -u <user> -p`).
* **GeoJSON empty/invalid:** confirm `src/india-districts-2019-734.json`; install `geopandas` if needed.
* **`No module named StFiles`:** ensure `StFiles/` has `__init__.py` and you’re running from repo root.
* **Matplotlib/Altair warnings:** typically harmless; keep packages up to date.

---

## 5. Usage

Follow these steps to explore insights and reproduce the results shown in the screenshots.


### 5.1) Start the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal.

### 5.2) Understand the layout

* **Tabs:** `Insurance` • `Transaction` • `User`
* **Filters:** three expandable controls — **Year**, **Quarterly**, **State**
* **Actions:** per-tab **Process** button (e.g., *Insurance Process*) and **Clear** button

<p align="center">
  <img src="assets/Filter%201.png" width="980" alt="Landing view with filters and Process/Clear buttons">
  <br><em>Landing view with filters and the Process/Clear actions.</em>
</p>

> The **Filter Conditions** panel shows the SQL-style clauses generated from your selections.

### 5.3) Run a query (filters → process)

1. Expand **Year**, **Quarterly**, and/or **State** and choose values.
2. Click the tab’s **Process** button.
3. You’ll see either:

   * **National Overview** charts *(no filters)*, or
   * **Filtered** Overview + **Heatmaps** + **Top-10** *(with filters)*

If another tab shows a yellow banner that it’s disabled, **clear filters in the last used tab** (tab-locking prevents cross-tab conflicts).

<p align="center">
  <img src="assets/Filter%206.png" width="980" alt="User tab disabled notice">
  <br><em>Tab-locking notice: clear filters in the other tab to enable this one.</em>
</p>

<p align="center">
  <img src="assets/Filter%205.png" width="980" alt="Transaction tab disabled notice">
  <br><em>Another example of tab-locking.</em>
</p>

### 5.4) Insurance tab — what you’ll see

**A) National overview (no filters)** — yearly & quarterly trends + top states

<p align="center">
  <img src="assets/Ins%20Screenshot%201.png" width="980" alt="Insurance national overview">
</p>

**B) Heatmaps** — state & district choropleths; toggle **Amount ↔ Count**

<p align="center">
  <img src="assets/Ins%20Screenshot%202.png" width="980" alt="Insurance heatmaps">
</p>

**C) Top-10 entities** — state, district, and pincode with cumulative line

<p align="center">
  <img src="assets/Ins%20Screenshot%203.png" width="980" alt="Insurance Top 10">
</p>

**D) Filtered example** — after selecting years/states and clicking **Insurance Process**

<p align="center">
  <img src="assets/Filter%202.png" width="980" alt="Insurance filtered overview">
  <br><em>Filtered Overview: Yearly/Quarterly trends for your selection.</em>
</p>
<p align="center">
  <img src="assets/Filter%204.png" width="980" alt="Insurance filtered heatmaps">
  <br><em>Filtered Heatmaps: distribution across the selected geography.</em>
</p>
<p align="center">
  <img src="assets/Filter%203.png" width="980" alt="Insurance Top 10 filtered">
  <br><em>Filtered Top-10: leading State/District/Pincode entities.</em>
</p>

### 5.5) Transaction tab — what you’ll see

**A) National overview (no filters)**

<p align="center">
  <img src="assets/Trans%20Screenshot%201.png" width="980" alt="Transactions national overview">
</p>

**B) Heatmaps (Amount ↔ Count toggle)**

<p align="center">
  <img src="assets/Trans%20Screenshot%202.png" width="980" alt="Transactions heatmaps">
</p>

**C) Top-10 entities**

<p align="center">
  <img src="assets/Trans%20Screenshot%203.png" width="980" alt="Transactions Top 10">
</p>

### 5.6) User tab — what you’ll see

**A) National overview (no filters)**

<p align="center">
  <img src="assets/User%20Screenshot%201.png" width="980" alt="Users national overview">
</p>

**B) Heatmaps (Registered Users ↔ App Opens toggle)**

<p align="center">
  <img src="assets/User%20Screenshot%202.png" width="980" alt="Users heatmaps">
</p>

**C) Top-10 entities**

<p align="center">
  <img src="assets/User%20Screenshot%203.png" width="980" alt="Users Top 10">
</p>

### 5.7) Clearing filters & switching tabs

* Use **Clear Insurance / Clear Transaction / Clear User** to reset the active tab.
* If a tab is disabled, clear filters in the previously used tab, then return.

### 5.8) Notes & tips

* **Heatmap toggles:** switch the color scale metric in one click.
* **Tooltips:** hover bars/points/regions for exact values.
* **Performance:** heavy queries are cached (`@st.cache_data`) for faster repeat loads.

---

## 6. Contact

👤 **Manikandan Baskar**

* Email: [mani111355@gmail.com](mailto:mani111355@gmail.com)
* LinkedIn: [Manikandan Baskar](https://linkedin.com/in/mani-baskar)
* GitHub: [@mani-baskar](https://github.com/mani-baskar)
