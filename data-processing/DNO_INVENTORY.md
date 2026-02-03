# DNO Data Inventory

This file tracks which downloaded file corresponds to which DNO area.

## Files Downloaded

| File Name | DNO | License Area | Format | Status | Notes |
|-----------|-----|--------------|--------|--------|-------|
| ndp-spd-primary-substation-polygons.geojson | SPEN | SPD (Scotland) | GeoJSON | ✓ | |
| ndp-spm-primary-group-polygons.geojson | SPEN | SPMW (Manweb - Wales/NW) | GeoJSON | ✓ | |
| sepd_primarysubstation_esa_2025.geojson | SSEN | SEPD (Southern/Central) | GeoJSON | ✓ | |
| east_midlands_primary.gpkg | National Grid | East Midlands | GeoPackage | ✓ | |
| south_wales_primary.gpkg | National Grid | South Wales | GeoPackage | ✓ | |
| south_west_primary.gpkg | National Grid | South West | GeoPackage | ✓ | |
| west_midlands_primary.gpkg | National Grid | West Midlands | GeoPackage | ✓ | Found! |
| ukpn_primary_postcode_area (2).geojson | UKPN | EPN/LPN/SPN (East/London/SE) | GeoJSON | ✓ | |
| distribution-substation-service-areas.geojson | Northern Powergrid | NE/Yorkshire | GeoJSON | ✓ | Likely |
| dfes-primary-polygons.geojson | ENWL | Northwest | GeoJSON | ✓ | Likely |

## Coverage Status

### Complete ✓
- [x] SPEN Scotland (SPD)
- [x] SPEN Manweb (SPMW)
- [x] SSEN SEPD
- [x] National Grid East Midlands
- [x] National Grid South Wales
- [x] National Grid South West
- [x] National Grid West Midlands ✨ (Found!)
- [x] UKPN (all three areas)
- [x] Northern Powergrid (likely distribution-substation-service-areas.geojson)
- [x] Electricity North West (likely dfes-primary-polygons.geojson)

### Potentially Missing
- [ ] SSEN SHEPD (North Scotland/Highlands) - May need to download separately

## Next Steps

1. Identify the two unknown files
2. Check if any DNO areas are genuinely missing
3. If missing, download from respective DNO portals
4. Copy files from old location to `data-processing/raw/substations/`
