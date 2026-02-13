# Methodology: Energy Postcodes Tool

## Overview
The Energy Postcodes tool matches UK postcodes to electricity distribution substations using spatial analysis. It allows users to identify which primary substation serves a given postcode and view all postcodes within that substation's service area.

---

## Data Sources

### 1. **Postcode Location Data**
- **Source**: ONS Postcode Directory (ONSPD) - May 2025
- **Type**: Point data (latitude/longitude coordinates)
- **What it contains**: Central point (centroid) for each UK postcode
- **Download**: https://geoportal.statistics.gov.uk/
- **Note**: We use **postcode centroids (points)**, NOT postcode polygons
- **Coverage**: ~1.8 million active UK postcodes

### 2. **Household Count Data**
- **Source**: Census 2021 Household Estimates
- **Type**: CSV file mapping postcodes to household counts
- **What it contains**: Number of households per postcode
- **Purpose**: Calculate total households served by each substation

### 3. **Substation Service Area Boundaries**
- **Source**: Distribution Network Operator (DNO) open data
- **Type**: Polygon geometries (GeoJSON/GeoPackage format)
- **What it contains**: Geographic boundaries of primary substation service areas
- **Coverage**: 6 DNOs covering Great Britain:
  - **SP Energy Networks** (Scotland, Merseyside, North Wales, Cheshire)
  - **Scottish & Southern Electricity Networks** (North & Central Scotland, Southern England)
  - **UK Power Networks** (London, South East, Eastern England)
  - **Northern Powergrid** (North East, Yorkshire)
  - **Electricity North West** (North West England)
  - **Western Power Distribution** (Midlands, South West, Wales)

**DNO Data Files Used:**
| DNO | License Area | File Name |
|-----|--------------|-----------|
| SPEN | SPD (Scotland) | `ndp-spd-primary-substation-polygons.geojson` |
| SPEN | SPMW (Manweb) | `ndp-spm-primary-group-polygons.geojson` |
| SSEN | SEPD (Southern) | `sepd_primarysubstation_esa_2025.geojson` |
| SSEN | SHEPD (Highlands) | `shepd_primarysubstation_esa_2025.geojson` |
| UKPN | LPN/SPN/EPN | `ukpn_primary_postcode_area.geojson` |
| NPG | North East/Yorkshire | `NPG Primary substation_combined_service_areas.geojson` |
| ENWL | North West | `enwl_primary_service_areas.gpkg` |
| WPD | Midlands/Wales/SW | `wpd_primary_service_areas.gpkg` |

---

## Processing Methodology

### Step 1: Load and Standardize DNO Data
- Load all DNO substation boundary files (GeoJSON/GeoPackage)
- Standardize field names across different DNOs
- Assign unique IDs to each substation
- Combine into single GeoDataFrame
- **Result**: ~4,443 primary substation service areas

### Step 2: Load Postcode Centroids
- Load ONSPD CSV file
- Extract postcode, latitude, longitude
- Convert to GeoDataFrame with point geometries
- Use WGS84 coordinate system (EPSG:4326)
- **Result**: ~1.8 million postcode points

### Step 3: Spatial Join (Point-in-Polygon)
- **Method**: Spatial join using "within" predicate
- **Logic**: If a postcode centroid point falls within a substation boundary polygon, that postcode is assigned to that substation
- **Technology**: GeoPandas spatial join
- **Result**: Each postcode matched to its substation ID

**To answer your question:** We use **postcode centroids (points)** from ONSPD, NOT Code-Point Polygons. The matching is done by checking if the postcode's central point falls within a substation's boundary polygon.

### Step 4: Calculate Household Counts
- Load Census 2021 household data
- For each substation, sum the household counts of all its postcodes
- **Result**: Total households served by each substation

### Step 5: Create Optimized Outputs

#### A) Substation Details (`substations.json`)
**Contains:**
- Substation ID, name, DNO, license area
- Postcode count and household count
- Boundary geometry (simplified for web performance)
- **Chunks list**: Array of postcode area codes (e.g., ["N1", "N5", "EC1"]) indicating which data files contain postcodes for this substation

**Optimization:**
- Geometry simplified (0.001 degree tolerance)
- Coordinates rounded to 4 decimal places (~11m precision)
- Non-essential fields removed
- Final size: ~7.8 MB (under Cloudflare's 25 MB limit)

#### B) Postcode Lookup Chunks (`chunks/*.json`)
**Structure:**
- Postcodes grouped by outward code (e.g., "N1", "SW1", "EH3")
- Each chunk is a separate JSON file
- **Total chunks**: ~2,414 files

**Each chunk contains:**
```json
{
  "N1 0AA": {
    "substation_id": "LPN-S00000000461",
    "lat": 51.5365,
    "lng": -0.1025
  },
  "N1 0AB": {
    "substation_id": "LPN-S00000000461",
    "lat": 51.5368,
    "lng": -0.1028
  }
}
```

**Why chunks?**
- Loading all 1.8M postcodes at once would be ~160 MB
- Chunking allows on-demand loading (only load what's needed)
- Typical user session loads 5-20 chunks (~500 KB total)

---

## Web Application Architecture

### Frontend Loading Process:
1. **Initial Load**:
   - Load `substations.json` (~7.8 MB) - contains all substation boundaries
   - No postcode chunks loaded yet

2. **User Searches Postcode** (e.g., "N1 2XH"):
   - Extract outward code ("N1")
   - Load chunk `data/chunks/N1.json` (~100 KB)
   - Find postcode in chunk → get substation_id and coordinates
   - Look up substation details in `substations.json`

3. **Display Results**:
   - Show substation info (name, DNO, postcode count, households)
   - Load ALL chunk files listed in `substation.chunks` array
   - Scan loaded chunks to find all postcodes for this substation
   - Display paginated list + enable CSV export

4. **Map Display**:
   - Draw substation boundary polygon on Leaflet map
   - Add marker at searched postcode coordinates
   - Fit map bounds to boundary

---

## Key Technical Decisions

### Why Postcode Points (not Polygons)?
- **ONSPD centroids are sufficient**: For substation matching, we need to know the approximate location, not the exact boundary
- **File size**: Point data is much smaller than polygon data
- **Processing speed**: Point-in-polygon is faster than polygon-polygon intersection
- **Data availability**: ONSPD is free and regularly updated; Code-Point Polygons are premium

### Why Primary Substations (not Distribution)?
- **Relevant scale**: Primary substations serve 5,000-50,000 households (neighborhood/town level)
- **Data availability**: All DNOs publish primary substation boundaries
- **User context**: Primary level is most relevant for community energy planning
- **Distribution substations**: Too granular (serve 50-500 households), data less complete

### Why Client-Side Processing?
- **No backend required**: Static site hosted on Cloudflare Pages
- **Fast loading**: Chunks load in milliseconds
- **Scalability**: CDN handles all traffic, no server costs
- **Privacy**: No user data sent to server

---

## Limitations

1. **Postcode Centroids**: We use the central point of each postcode, so postcodes on substation boundaries may be misclassified
2. **Data Currency**: DNO boundaries are updated periodically (typically annually)
3. **Coverage**: Only covers Great Britain (not Northern Ireland - different DNO data structure)
4. **Unmatched Postcodes**: Some postcodes fall outside substation boundaries (islands, offshore, data gaps)

---

## Data Processing Pipeline Summary

```
Input Data:
├── ONSPD (1.8M postcodes) → Point geometries
├── Census 2021 → Household counts
└── DNO Files (6 DNOs) → Substation boundaries

      ↓ [Spatial Join: Point-in-Polygon]

Matched Data:
└── Each postcode → Substation ID + Coordinates

      ↓ [Group & Optimize]

Output Files:
├── substations.json (4,443 substations with boundaries)
└── chunks/*.json (2,414 files, postcodes grouped by outward code)

      ↓ [Web Application]

User Experience:
└── Search postcode → See substation + all postcodes in area
```

---

## Reproducibility

All processing code is available in `/data-processing/process_data.py`

To reproduce:
1. Download ONSPD from ONS Geoportal
2. Download Census 2021 household data
3. Download DNO substation boundary files (links in script)
4. Run `python process_data.py`
5. Run `python simplify_substations_aggressive.py`
6. Copy output files to `public/data/`

**Processing time**: ~10-15 minutes on standard laptop
**Output size**: ~200 MB of chunk files + 7.8 MB substations file

---

## Contact
For questions about methodology: energy-postcodes.uk
