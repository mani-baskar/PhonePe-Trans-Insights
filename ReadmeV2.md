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

## License

Distributed under the MIT License. See `LICENSE` for details.

---

## Contact

👤 **Your Name**

* Email: [your.email@example.com](mailto:your.email@example.com)
* LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
* GitHub: [@username](https://github.com/username)

---

Do you want me to **customize this template for your PhonePe Transaction Insights project** (with your tech stack and sections filled in), so you can directly use it in GitHub?
```
