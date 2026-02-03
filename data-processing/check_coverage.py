import geopandas as gpd
from shapely.geometry import Point
import json

# Load substations
print("Loading substation data...")
with open('output/substations.json', 'r') as f:
    substations_data = json.load(f)

# Create point for N15 5QA
lat, lon = 51.58152, -0.083085
point = Point(lon, lat)
print(f"\nN15 5QA location: {lat}, {lon}")

# Check which DNO areas this is in (should be UKPN London)
print("\nChecking nearby substations...")

# Find closest substations
distances = []
for sub_id, sub_data in substations_data.items():
    if 'boundary' in sub_data and sub_data['boundary']:
        # Check DNO
        if 'UKPN' in sub_data.get('dno', '') or 'UK Power' in sub_data.get('dno', ''):
            print(f"  Found UKPN substation: {sub_data.get('name', sub_id)}")

print(f"\nTotal substations in data: {len(substations_data)}")

# Check if any UKPN substations exist
ukpn_count = sum(1 for sub in substations_data.values() if 'UKPN' in sub.get('dno', '') or 'UK Power' in sub.get('dno', ''))
print(f"UKPN substations: {ukpn_count}")
