# Adding Population Data to postcodes.energy

## 🎯 Recommended Approach: Output Area Census Data

Since ONSPD no longer includes household counts directly, the best method is to:
1. Match postcodes to Output Areas (OAs)
2. Join with 2021 Census population data for OAs
3. Aggregate by substation

## 📊 Data Sources Needed

### 1. Output Area to Postcode Lookup (Already in ONSPD!)
The ONSPD file includes the column `OA21CD` (Output Area 2021 code)

### 2. Census 2021 Population Data
Download from: https://www.nomisweb.co.uk/
- Table: TS001 (Population by Output Area)
- Geography: Output Areas (England & Wales), Data Zones (Scotland)
- Free download, no API key needed

## 🔧 Implementation Steps

### Step 1: Modify `load_postcode_data()` function

```python
def load_postcode_data() -> gpd.GeoDataFrame:
    """
    Load UK postcode location data with Output Area codes.
    """
    print("\n=== Loading Postcode Data ===\n")
    
    postcode_files = list(RAW_POSTCODES.glob("*.csv"))
    
    if not postcode_files:
        print("ERROR: No postcode CSV file found in raw/postcodes/")
        return None
    
    postcode_file = postcode_files[0]
    print(f"Loading postcodes from {postcode_file.name}...")
    
    try:
        # Load with Output Area code (OA21CD for 2021 Census)
        df = pd.read_csv(
            postcode_file, 
            usecols=['PCDS', 'LAT', 'LONG', 'OA21CD'],  # ← Added OA21CD
            low_memory=False
        )
        df = df.dropna(subset=['LAT', 'LONG'])
        
        # Rename to standard names
        df = df.rename(columns={
            'PCDS': 'pcd', 
            'LAT': 'lat', 
            'LONG': 'long',
            'OA21CD': 'output_area'  # ← Keep OA code
        })
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df['long'], df['lat']),
            crs="EPSG:4326"
        )
        
        print(f"[OK] Loaded {len(gdf)} postcodes with Output Area codes")
        return gdf
        
    except Exception as e:
        print(f"ERROR loading postcodes: {e}")
        return None
```

### Step 2: Load Census Population Data

```python
def load_census_population() -> pd.DataFrame:
    """
    Load Census 2021 population data by Output Area.
    Expected CSV format: OA21CD, Population
    """
    print("\n=== Loading Census Population Data ===\n")
    
    census_file = Path("raw/census/TS001_population_by_oa.csv")
    
    if not census_file.exists():
        print("WARNING: Census population file not found")
        print(f"Expected: {census_file}")
        print("Download from: https://www.nomisweb.co.uk/")
        return pd.DataFrame(columns=['output_area', 'population', 'households'])
    
    try:
        # Adjust column names based on actual Nomis download format
        df = pd.read_csv(census_file)
        
        # Typical Nomis format:
        # - 'geography code' = Output Area code
        # - 'Observation' = Population count
        
        df = df.rename(columns={
            'geography code': 'output_area',
            'Observation': 'population'
        })
        
        # Estimate households (average ~2.4 people per household in UK)
        df['households'] = (df['population'] / 2.4).round().astype(int)
        
        print(f"[OK] Loaded population data for {len(df)} Output Areas")
        return df[['output_area', 'population', 'households']]
        
    except Exception as e:
        print(f"ERROR loading census data: {e}")
        return pd.DataFrame(columns=['output_area', 'population', 'households'])
```

### Step 3: Join and Aggregate

```python
def match_postcodes_to_substations(postcodes: gpd.GeoDataFrame, 
                                   substations: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Perform spatial join to match each postcode to its substation area.
    """
    print("\n=== Matching Postcodes to Substations ===\n")
    
    # Load census data
    census_pop = load_census_population()
    
    # Join postcodes with population data
    if not census_pop.empty:
        postcodes = postcodes.merge(
            census_pop, 
            left_on='output_area', 
            right_on='output_area', 
            how='left'
        )
        # Fill missing with average
        postcodes['population'] = postcodes['population'].fillna(2.4)
        postcodes['households'] = postcodes['households'].fillna(1)
    else:
        # Use rough estimates if census data not available
        print("Using rough estimates (2.4 people, 1 household per postcode)")
        postcodes['population'] = 2.4
        postcodes['households'] = 1
    
    print("Performing spatial join...")
    
    # Spatial join: find which substation polygon each postcode falls within
    matched = gpd.sjoin(
        postcodes,
        substations,
        how='left',
        predicate='within'
    )
    
    # Count matches
    matched_count = matched['substation_id'].notna().sum()
    unmatched_count = matched['substation_id'].isna().sum()
    
    print(f"\n[OK] Matched: {matched_count:,} postcodes")
    print(f"[!] Unmatched: {unmatched_count:,} postcodes")
    
    return matched
```

### Step 4: Aggregate Population by Substation

```python
def create_substation_details(matched: pd.DataFrame, 
                              substations: gpd.GeoDataFrame) -> Dict:
    """
    Create detailed information for each substation including population.
    """
    print("\n=== Creating Substation Details with Population ===\n")
    
    substation_details = {}
    
    for sub_id in tqdm(substations['substation_id'].unique()):
        # Get all postcodes in this substation
        sub_postcodes = matched[matched['substation_id'] == sub_id]
        
        # Get substation metadata
        sub_info = substations[substations['substation_id'] == sub_id].iloc[0]
        
        # Aggregate population data
        total_population = sub_postcodes['population'].sum()
        total_households = sub_postcodes['households'].sum()
        postcode_count = len(sub_postcodes)
        
        substation_details[sub_id] = {
            'substation_id': sub_id,
            'name': sub_info['substation_name'],
            'dno': sub_info['dno_name'],
            'license_area': sub_info['license_area'],
            'postcode_count': int(postcode_count),
            'estimated_population': int(total_population),  # ← NEW
            'estimated_households': int(total_households),  # ← NEW
            'geometry': json.loads(sub_info.geometry.to_json())
        }
    
    print(f"[OK] Created details for {len(substation_details)} substations")
    return substation_details
```

## 📋 Data Download Instructions

### Get Census 2021 Population Data:

1. Go to: https://www.nomisweb.co.uk/
2. Navigate to: Census 2021 → Population → TS001 (Total population)
3. Select:
   - Geography: Output Areas (England & Wales) 
   - Add Scotland Data Zones if needed
4. Download as CSV
5. Save to: `data-processing/raw/census/TS001_population_by_oa.csv`

### Alternative: Use Rough Estimates

If you don't want to download census data, you can use these UK averages:
- **2.4 people per postcode** (varies by area type)
- **1 household per postcode** (rough estimate)
- This gives ballpark figures quickly

## 🎨 Update Frontend Display

Modify `public/index.html` to show population:

```html
<div class="info-card">
    <h2>Substation Information</h2>
    <div id="substation-info">
        <p class="info-item"><strong>Substation:</strong> <span id="sub-name">-</span></p>
        <p class="info-item"><strong>DNO:</strong> <span id="sub-dno">-</span></p>
        <p class="info-item"><strong>License Area:</strong> <span id="sub-area">-</span></p>
        <p class="info-item"><strong>Postcodes in Area:</strong> <span id="sub-count">-</span></p>
        
        <!-- NEW POPULATION FIELDS -->
        <p class="info-item"><strong>Estimated Population:</strong> <span id="sub-population">-</span></p>
        <p class="info-item"><strong>Estimated Households:</strong> <span id="sub-households">-</span></p>
    </div>
</div>
```

Update `public/app.js`:

```javascript
function displaySubstationInfo(substation) {
    document.getElementById('sub-name').textContent = substation.name;
    document.getElementById('sub-dno').textContent = substation.dno;
    document.getElementById('sub-area').textContent = substation.license_area;
    document.getElementById('sub-count').textContent = substation.postcode_count.toLocaleString();
    
    // NEW: Display population
    document.getElementById('sub-population').textContent = 
        substation.estimated_population.toLocaleString();
    document.getElementById('sub-households').textContent = 
        substation.estimated_households.toLocaleString();
    
    // ... rest of function
}
```

## 📊 Expected Results

After implementation, each substation will show:
- **Postcodes**: 1,234
- **Estimated Population**: 2,962 people
- **Estimated Households**: 1,234 households

This helps users understand the market size for community energy projects!

## ⚠️ Important Notes

1. **Accuracy**: These are estimates based on 2021 Census
2. **Coverage**: Some postcodes may not have OA codes (offshore, new developments)
3. **Scotland**: Uses Data Zones (DZ) instead of Output Areas (OA)
4. **Updates**: Census data updated every 10 years, population changes between censuses

## 🚀 Quick Start (Without Census Data)

If you want to add this feature quickly without downloading census data:

1. Use rough estimates: **2.4 people per postcode**
2. This gives ballpark figures immediately
3. Can upgrade to census data later for accuracy

Just add this to your processing script:
```python
matched['population'] = 2.4  # UK average
matched['households'] = 1.0  # Rough estimate
```

Then aggregate by substation as shown above!
