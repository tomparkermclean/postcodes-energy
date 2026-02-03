"""
UK Postcode to Substation Matching Tool - Data Processing Script

This script processes DNO substation boundary data and UK postcode location data
to create optimized lookup files for the web application.

Process:
1. Load all DNO substation GeoJSON/GeoPackage files
2. Standardize data structure and naming
3. Load UK postcode location data (ONSPD or Code-Point)
4. Perform spatial join to match postcodes to substations
5. Output optimized JSON files for frontend

Author: postcodes.energy
License: MIT
"""

import geopandas as gpd
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List
import warnings
from tqdm import tqdm

warnings.filterwarnings('ignore')

# Paths
RAW_SUBSTATIONS = Path("raw/substations")
RAW_POSTCODES = Path("raw/postcodes")
OUTPUT_DIR = Path("output")

# DNO file mapping - update this based on your actual files
DNO_FILES = {
    "SPEN_SPD": {
        "file": "ndp-spd-primary-substation-polygons.geojson",
        "dno_name": "SP Energy Networks",
        "license_area": "SPD - Scotland"
    },
    "SPEN_SPMW": {
        "file": "ndp-spm-primary-group-polygons.geojson",
        "dno_name": "SP Energy Networks",
        "license_area": "SPMW - Manweb (Wales & Northwest)"
    },
    "SSEN_SEPD": {
        "file": "sepd_primarysubstation_esa_2025.geojson",
        "dno_name": "Scottish & Southern Electricity Networks",
        "license_area": "SEPD - Southern & Central"
    },
    "SSEN_SHEPD": {
        "file": "shepd_primarysubstation_esa_2025.geojson",
        "dno_name": "Scottish & Southern Electricity Networks",
        "license_area": "SHEPD - North Scotland & Highlands"
    },
    "NGRID_EM": {
        "file": "east_midlands_primary.gpkg",
        "dno_name": "National Grid",
        "license_area": "East Midlands"
    },
    "NGRID_SW_WALES": {
        "file": "south_wales_primary.gpkg",
        "dno_name": "National Grid",
        "license_area": "South Wales"
    },
    "NGRID_SW": {
        "file": "south_west_primary.gpkg",
        "dno_name": "National Grid",
        "license_area": "South West"
    },
    "NGRID_WM": {
        "file": "west_midlands_primary.gpkg",
        "dno_name": "National Grid",
        "license_area": "West Midlands"
    },
    "UKPN": {
        "file": "ukpn_primary_postcode_area (2).geojson",
        "dno_name": "UK Power Networks",
        "license_area": "EPN/LPN/SPN - East/London/Southeast"
    },
    "NPG": {
        "file": "NPG Primary substation_combined_service_areas.geojson",
        "dno_name": "Northern Powergrid",
        "license_area": "Northeast & Yorkshire"
    },
    "ENWL": {
        "file": "dfes-primary-polygons.geojson",
        "dno_name": "Electricity North West",
        "license_area": "Northwest England"
    },
}


def load_substation_data(file_path: Path, dno_id: str, dno_info: Dict) -> gpd.GeoDataFrame:
    """
    Load substation boundary data from GeoJSON or GeoPackage.
    Standardize field names and add DNO metadata.
    """
    print(f"Loading {dno_id} from {file_path.name}...")
    
    try:
        # Read file (handles both GeoJSON and GeoPackage)
        gdf = gpd.read_file(file_path)
        
        # Ensure it's in WGS84 (EPSG:4326) for web mapping
        if gdf.crs != "EPSG:4326":
            print(f"  Converting from {gdf.crs} to EPSG:4326")
            gdf = gdf.to_crs("EPSG:4326")
        
        # Add standardized metadata
        gdf['dno_id'] = dno_id
        gdf['dno_name'] = dno_info['dno_name']
        gdf['license_area'] = dno_info['license_area']
        
        # Try to identify substation name/ID from existing fields
        # Check multiple possible field names
        name_candidates = ['primary', 'name', 'substation', 'site_name', 'Sub_Name', 'SUBSTATION_NAME']
        id_candidates = ['primary_floc', 'id', 'substation_id', 'site_id', 'Sub_ID', 'SUBSTATION_ID']
        
        gdf['substation_name'] = None
        for col in name_candidates:
            if col in gdf.columns:
                gdf['substation_name'] = gdf[col].astype(str)
                print(f"  Using '{col}' for substation name")
                break
        
        gdf['substation_id'] = None
        for col in id_candidates:
            if col in gdf.columns:
                gdf['substation_id'] = gdf[col].astype(str)
                print(f"  Using '{col}' for substation ID")
                break
        
        # If no ID found, create one from DNO + index
        if gdf['substation_id'].isna().all() or (gdf['substation_id'] == 'None').all():
            print(f"  No ID field found, creating IDs from index")
            gdf['substation_id'] = [f"{dno_id}_{i:04d}" for i in range(len(gdf))]
        
        # If no name found, use ID as name
        if gdf['substation_name'].isna().all() or (gdf['substation_name'] == 'None').all():
            print(f"  No name field found, using ID as name")
            gdf['substation_name'] = gdf['substation_id']
        
        # Keep only essential columns
        essential_cols = ['substation_id', 'substation_name', 'dno_id', 'dno_name', 'license_area', 'geometry']
        gdf = gdf[essential_cols]
        
        print(f"  Loaded {len(gdf)} substations")
        return gdf
        
    except Exception as e:
        print(f"  ERROR loading {file_path}: {e}")
        return None


def load_all_substations() -> gpd.GeoDataFrame:
    """Load and combine all DNO substation data."""
    print("\n=== Loading All DNO Substation Data ===\n")
    
    all_substations = []
    
    for dno_id, dno_info in DNO_FILES.items():
        file_path = RAW_SUBSTATIONS / dno_info['file']
        
        if not file_path.exists():
            print(f"WARNING: {file_path} not found, skipping...")
            continue
        
        gdf = load_substation_data(file_path, dno_id, dno_info)
        if gdf is not None:
            all_substations.append(gdf)
    
    # Combine all substations
    if all_substations:
        combined = gpd.GeoDataFrame(pd.concat(all_substations, ignore_index=True))
        print(f"\n[OK] Total substations loaded: {len(combined)}")
        return combined
    else:
        raise ValueError("No substation data could be loaded!")


def load_postcode_data() -> gpd.GeoDataFrame:
    """
    Load UK postcode location data.
    Expects ONSPD or Code-Point CSV with postcode, latitude, longitude columns.
    """
    print("\n=== Loading Postcode Data ===\n")
    
    # Look for postcode file in raw/postcodes
    postcode_files = list(RAW_POSTCODES.glob("*.csv"))
    
    if not postcode_files:
        print("ERROR: No postcode CSV file found in raw/postcodes/")
        print("Please download ONSPD or OS Code-Point data and place in raw/postcodes/")
        return None
    
    postcode_file = postcode_files[0]
    print(f"Loading postcodes from {postcode_file.name}...")
    
    # Read CSV (adjust column names based on your data source)
    # ONSPD typical columns: 'pcd', 'lat', 'long'
    # Code-Point: different format, may need adjustment
    
    try:
        # Try ONSPD column names (PCDS, LAT, LONG)
        df = pd.read_csv(postcode_file, usecols=['PCDS', 'LAT', 'LONG'])
        df = df.dropna(subset=['LAT', 'LONG'])
        
        # Rename to standard names
        df = df.rename(columns={'PCDS': 'pcd', 'LAT': 'lat', 'LONG': 'long'})
        
        # Create GeoDataFrame from lat/long
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df['long'], df['lat']),
            crs="EPSG:4326"
        )
        
        print(f"[OK] Loaded {len(gdf)} postcodes")
        return gdf
        
    except Exception as e:
        print(f"ERROR loading postcodes: {e}")
        print("Make sure your CSV has columns: 'PCDS', 'LAT', 'LONG' (ONSPD format)")
        return None


def match_postcodes_to_substations(postcodes: gpd.GeoDataFrame, 
                                   substations: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Perform spatial join to match each postcode to its substation area.
    """
    print("\n=== Matching Postcodes to Substations ===\n")
    print("This may take several minutes...")
    
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
    print(f"  (Unmatched postcodes are likely on boundaries, offshore, or in data gaps)")
    
    return matched


def create_postcode_lookup(matched: pd.DataFrame) -> Dict:
    """
    Create optimized postcode lookup structure.
    Groups postcodes by outward code (e.g., "SW1") for efficient loading.
    Now includes coordinates for map markers.
    """
    print("\n=== Creating Postcode Lookup ===\n")
    
    # Remove unmatched postcodes
    matched = matched[matched['substation_id'].notna()].copy()
    
    # Extract outward code (first part of postcode)
    matched['outward'] = matched['pcd'].str.extract(r'^([A-Z]{1,2}\d{1,2}[A-Z]?)', expand=False)
    
    lookup = {}
    
    for outward in tqdm(matched['outward'].unique(), desc="Building lookup"):
        outward_data = matched[matched['outward'] == outward]
        
        lookup[outward] = {
            postcode: {
                'substation_id': substation_id,
                'lat': lat,
                'lng': lng
            }
            for postcode, substation_id, lat, lng in zip(
                outward_data['pcd'],
                outward_data['substation_id'],
                outward_data['lat'],
                outward_data['long']
            )
        }
    
    print(f"[OK] Created lookup for {len(lookup)} postcode areas")
    return lookup


def create_substation_details(substations: gpd.GeoDataFrame, 
                              matched: pd.DataFrame) -> Dict:
    """
    Create substation details with simplified boundaries, postcode counts, and postcode lists.
    """
    print("\n=== Creating Substation Details ===\n")
    
    # Get postcodes per substation
    postcode_groups = matched.groupby('substation_id')['pcd'].apply(list).to_dict()
    
    # Simplify geometries for faster web rendering
    substations['geometry'] = substations['geometry'].simplify(tolerance=0.001)
    
    details = {}
    
    for _, row in tqdm(substations.iterrows(), total=len(substations), desc="Processing substations"):
        substation_id = row['substation_id']
        postcodes = postcode_groups.get(substation_id, [])
        
        details[substation_id] = {
            'name': row['substation_name'],
            'dno': row['dno_name'],
            'license_area': row['license_area'],
            'postcode_count': len(postcodes),
            'postcodes': sorted(postcodes),  # Include sorted list of all postcodes
            'boundary': json.loads(gpd.GeoSeries([row['geometry']]).to_json())['features'][0]['geometry']
        }
    
    print(f"[OK] Created details for {len(details)} substations")
    return details


def save_outputs(postcode_lookup: Dict, substation_details: Dict):
    """Save processed data as JSON files - split by postcode area."""
    print("\n=== Saving Output Files ===\n")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    CHUNKS_DIR = OUTPUT_DIR / "chunks"
    CHUNKS_DIR.mkdir(exist_ok=True)
    
    # Save individual chunk files (one per postcode area)
    print(f"Saving {len(postcode_lookup)} chunk files...")
    total_size = 0
    
    for area, postcodes in tqdm(postcode_lookup.items(), desc="Saving chunks"):
        chunk_file = CHUNKS_DIR / f"{area}.json"
        with open(chunk_file, 'w') as f:
            json.dump(postcodes, f, separators=(',', ':'))
        total_size += chunk_file.stat().st_size
    
    print(f"[OK] Saved {len(postcode_lookup)} chunk files ({total_size / 1024 / 1024:.1f} MB total)")
    
    # Save index of available chunks
    index_file = OUTPUT_DIR / "chunks_index.json"
    chunk_index = {
        "areas": list(postcode_lookup.keys()),
        "total_areas": len(postcode_lookup),
        "generated": str(pd.Timestamp.now())
    }
    with open(index_file, 'w') as f:
        json.dump(chunk_index, f, indent=2)
    print(f"[OK] Saved chunk index ({len(postcode_lookup)} areas)")
    
    # Save substation details (unchanged)
    details_file = OUTPUT_DIR / "substations.json"
    with open(details_file, 'w') as f:
        json.dump(substation_details, f, separators=(',', ':'))
    print(f"[OK] Saved {details_file} ({details_file.stat().st_size / 1024 / 1024:.1f} MB)")


def main():
    """Main processing pipeline."""
    print("\n" + "="*60)
    print("UK POSTCODE TO SUBSTATION MATCHING - DATA PROCESSING")
    print("="*60)
    
    # Load all substation boundaries
    substations = load_all_substations()
    
    # Load postcode locations
    postcodes = load_postcode_data()
    if postcodes is None:
        print("\n[ERROR] Cannot proceed without postcode data")
        return
    
    # Match postcodes to substations
    matched = match_postcodes_to_substations(postcodes, substations)
    
    # Create output files
    postcode_lookup = create_postcode_lookup(matched)
    substation_details = create_substation_details(substations, matched)
    
    # Save to disk
    save_outputs(postcode_lookup, substation_details)
    
    print("\n" + "="*60)
    print("[SUCCESS] PROCESSING COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review output files in data-processing/output/")
    print("2. Copy output files to public/data/ for the web app")
    print("3. Test the web application")
    print()


if __name__ == "__main__":
    main()
