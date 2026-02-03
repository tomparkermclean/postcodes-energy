import pandas as pd
import json

# Check in ONSPD
print("Checking ONSPD file...")
df = pd.read_csv('raw/postcodes/ONSPD_Online_latest_Postcode_Centroids_.csv', usecols=['PCDS', 'LAT', 'LONG'])
n15_5qa = df[df['PCDS'] == 'N15 5QA']
print(f"N15 5QA in ONSPD: {len(n15_5qa) > 0}")
if len(n15_5qa) > 0:
    print(f"  LAT: {n15_5qa.iloc[0]['LAT']}, LONG: {n15_5qa.iloc[0]['LONG']}")

# Check in processed data
print("\nChecking processed data...")
with open('output/postcode_lookup.json', 'r') as f:
    lookup = json.load(f)

# Check N15 area
if 'N15' in lookup:
    print(f"N15 area found with {len(lookup['N15'])} postcodes")
    
    # Check for N15 5QA with space
    if 'N15 5QA' in lookup['N15']:
        print("  'N15 5QA' (with space) found!")
        print(f"  Substation: {lookup['N15']['N15 5QA']}")
    else:
        print("  'N15 5QA' (with space) NOT found")
    
    # Check for N155QA without space
    if 'N155QA' in lookup['N15']:
        print("  'N155QA' (without space) found!")
    else:
        print("  'N155QA' (without space) NOT found")
    
    # Show some sample N15 postcodes
    print(f"\n  Sample N15 postcodes: {list(lookup['N15'].keys())[:5]}")
else:
    print("N15 area NOT found in lookup")
