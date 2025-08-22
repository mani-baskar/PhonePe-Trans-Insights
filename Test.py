import json
import pandas as pd
from pathlib import Path

INPUT_FILE = Path("src/india-districts-2019-734.json")
OUTPUT_FILE = Path("districts_states.csv")

def load_properties(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("Unexpected JSON root type.")

    # GeoJSON FeatureCollection
    if data.get("type") == "FeatureCollection":
        features = data.get("features", [])
        return [ (feat.get("properties") or {}) for feat in features ]

    # TopoJSON Topology
    if data.get("type") == "Topology":
        objects = data.get("objects") or {}
        if not objects:
            raise ValueError("Topology has no 'objects'.")
        # Pick the only/first object (here: 'india-districts-2019-734')
        obj_name = next(iter(objects.keys()))
        geoms = objects[obj_name].get("geometries") or []
        return [ (g.get("properties") or {}) for g in geoms ]

    raise ValueError("Unsupported JSON type; expected FeatureCollection or Topology.")

props_list = load_properties(INPUT_FILE)
if not props_list:
    raise ValueError("No features/geometries found in the file.")

# We know the exact keys from your file:
DISTRICT_KEY = "district"
STATE_KEY = "st_nm"

# If you want to be extra-safe, uncomment to auto-fallback:
# if STATE_KEY not in props_list[0]:
#     # common alternatives
#     for cand in ["ST_NM", "st_name", "STATE", "state", "NAME_1"]:
#         if cand in props_list[0]:
#             STATE_KEY = cand
#             break

rows = []
for props in props_list:
    d = props.get(DISTRICT_KEY)
    s = props.get(STATE_KEY)
    if d and s:
        rows.append({
            "district": str(d).strip(),
            "state": str(s).strip()
        })

df = pd.DataFrame(rows)
if df.empty:
    raise ValueError("No (district, state) pairs extracted—check keys and values.")

# Clean, dedupe, sort
df = (
    df.drop_duplicates()
      .sort_values(["state", "district"])
      .reset_index(drop=True)
)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"✅ Saved {len(df)} district–state pairs to {OUTPUT_FILE}")
