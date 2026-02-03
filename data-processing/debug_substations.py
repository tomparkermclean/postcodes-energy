import geopandas as gpd
import pandas as pd

print("Loading all substations...")

# Load from process_data.py logic
from process_data import load_all_substations

substations = load_all_substations()
print(f"\nTotal substations: {len(substations)}")
print(f"\nColumn names: {substations.columns.tolist()}")
print(f"\nFirst few substation IDs:")
print(substations[['substation_id', 'substation_name', 'dno_name']].head(10))

# Check for None/null IDs
null_count = substations['substation_id'].isna().sum()
print(f"\nSubstations with null ID: {null_count}")

# Check unique IDs
unique_ids = substations['substation_id'].nunique()
print(f"Unique substation IDs: {unique_ids}")

# Check if there are duplicates
duplicates = substations['substation_id'].value_counts()
print(f"\nMost common substation IDs:")
print(duplicates.head(10))
