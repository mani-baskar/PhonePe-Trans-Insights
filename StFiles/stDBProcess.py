# stDBProcess.py
import re
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# ====================== DB CONFIG ======================
DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME = (
    "root", "RajaSri%4007", "192.168.1.4", "3306", "PhonePe"
)

ENGINE = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True, future=True
)

ALLOWED_AGG = {"sum", "avg", "count", "min", "max"}

# ====================== Small utils ======================
def _safe_ident(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", name or ""):
        raise ValueError(f"Unsafe identifier: {name}")
    return name

# ====================== Data APIs ======================
@st.cache_data(ttl=600)
def get_lists(table: str) -> list[list[str]]:
    """Return [years, quarters, states] for a table where `quarter` is TINYINT."""
    t = _safe_ident(table)
    sql_years   = text(f"SELECT DISTINCT `year`    FROM `{t}` WHERE `year`  IS NOT NULL ORDER BY `year`;")
    sql_quarters= text(f"SELECT DISTINCT `quarter` FROM `{t}` WHERE `quarter` BETWEEN 1 AND 4 ORDER BY `quarter`;")
    sql_states  = text(f"SELECT DISTINCT `state`   FROM `{t}` WHERE `state` IS NOT NULL AND `state` <> '' ORDER BY `state`;")
    with ENGINE.connect() as conn:
        years    = [str(r[0])         for r in conn.execute(sql_years)]
        quarters = [f"Q{int(r[0])}"   for r in conn.execute(sql_quarters)]  # tinyint -> Q1..Q4
        states   = [str(r[0])         for r in conn.execute(sql_states)]
    return [years, quarters, states]

@st.cache_data(ttl=600)
def fetch_grouped(
    table: str,
    x_col: str,
    metrics: dict[str, tuple[str, str]],
) -> pd.DataFrame:
    """
    metrics: { alias: (source_col, agg) }  -> SELECT x, AGG(col) AS alias, ...
    Returns df with columns: ['x', *aliases]
    """
    table = _safe_ident(table)
    x_col = _safe_ident(x_col)

    selects = []
    for alias, (col, agg) in metrics.items():
        alias = _safe_ident(alias)
        col = _safe_ident(col)
        agg = agg.lower()
        if agg not in ALLOWED_AGG:
            raise ValueError(f"agg must be one of {sorted(ALLOWED_AGG)}")
        selects.append(f"{agg.upper()}(`{col}`) AS `{alias}`")

    sql = text(
        f"SELECT `{x_col}` AS x, {', '.join(selects)} "
        f"FROM `{table}` GROUP BY `{x_col}` ORDER BY `{x_col}`"
    )

    with ENGINE.connect() as conn:
        rows = conn.execute(sql).fetchall()

    return pd.DataFrame(rows, columns=["x"] + list(metrics.keys()))
