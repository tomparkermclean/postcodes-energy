# Data Sources

This document details all data sources used in postcodes.energy and their licensing terms.

## Substation Boundary Data

### SP Energy Networks (SPEN)

**Coverage**: Scotland (SPD), Wales & Northwest England (Manweb)

- **Portal**: https://spenergynetworks.opendatasoft.com/
- **Datasets**:
  - NDP SPD Primary Substation Polygons
  - NDP SPM Grid Group Polygons
- **License**: Open Data License
- **Attribution**: SP Energy Networks
- **Update Frequency**: Quarterly

### Scottish and Southern Electricity Networks (SSEN)

**Coverage**: North Scotland (SHEPD), Southern England & Central/North England (SEPD)

- **Portal**: https://www.ssen.co.uk/about-ssen/dso-information-and-data/
- **Datasets**: Primary Substation Electrical Service Areas
- **License**: Open Government Licence v3.0
- **Attribution**: Scottish and Southern Electricity Networks
- **Update Frequency**: Annual

### National Grid (formerly Western Power Distribution)

**Coverage**: South Wales, South West England, East Midlands, West Midlands

- **Portal**: https://www.nationalgrid.co.uk/electricity-distribution/distribution-data-portal
- **Datasets**: Primary Substation Boundaries (GeoPackage)
- **License**: Open Government Licence v3.0
- **Attribution**: National Grid Electricity Distribution
- **Update Frequency**: Annual

### Northern Powergrid

**Coverage**: Northeast England, Yorkshire

- **Portal**: https://www.northernpowergrid.com/open-data
- **Datasets**: Distribution Substation Service Areas
- **License**: Open Government Licence v3.0
- **Attribution**: Northern Powergrid
- **Update Frequency**: Annual

### Electricity North West (ENWL)

**Coverage**: Northwest England (excluding SPEN Manweb area)

- **Portal**: https://www.enwl.co.uk/open-data
- **Datasets**: DFES Primary Polygons
- **License**: Creative Commons Attribution 4.0
- **Attribution**: Electricity North West
- **Update Frequency**: Annual

### UK Power Networks (UKPN)

**Coverage**: Eastern England (EPN), London (LPN), Southeast England (SPN)

- **Portal**: https://ukpowernetworks.opendatasoft.com/
- **Datasets**: Primary Substation Postcode Areas
- **License**: Open Data License
- **Attribution**: UK Power Networks
- **Update Frequency**: Quarterly

## Postcode Location Data

### Office for National Statistics (ONS) Postcode Directory

**Coverage**: England, Wales, Scotland, Northern Ireland

- **Portal**: https://geoportal.statistics.gov.uk/search?q=ONSPD
- **Dataset**: ONS Postcode Directory (ONSPD)
- **Fields Used**: Postcode, Latitude, Longitude
- **License**: Open Government Licence v3.0
- **Attribution**: Contains public sector information licensed under the Open Government Licence v3.0
- **Update Frequency**: Quarterly (February, May, August, November)

### Ordnance Survey Code-Point Open (Alternative)

**Coverage**: Great Britain (England, Wales, Scotland)

- **Portal**: https://www.ordnancesurvey.co.uk/products/code-point-open
- **Dataset**: Code-Point Open
- **Fields Used**: Postcode, Eastings, Northings (converted to Lat/Long)
- **License**: Open Government Licence v3.0
- **Attribution**: Contains OS data © Crown copyright and database right (2026)
- **Update Frequency**: Quarterly

## Base Map Tiles

### OpenStreetMap

- **Provider**: OpenStreetMap Contributors
- **Tile Server**: https://tile.openstreetmap.org
- **License**: Open Database License (ODbL)
- **Attribution**: © OpenStreetMap contributors
- **Usage Policy**: https://operations.osmfoundation.org/policies/tiles/

## License Summary

All data used in this project is available under open licenses that permit:
- Commercial and non-commercial use
- Modification and adaptation
- Distribution

**Requirements**:
- Attribution (provided in application footer and documentation)
- Share-alike where applicable
- No warranty or liability claims

## Attribution Requirements

The following attribution must be displayed:

```
Data Sources:
- Distribution Network Operators (DNOs) open data
- Contains public sector information licensed under the Open Government Licence v3.0
- Contains OS data © Crown copyright and database right (2026)
- © OpenStreetMap contributors
```

## Data Processing Notes

1. **Coordinate Systems**: All data is converted to WGS84 (EPSG:4326) for web mapping
2. **Geometry Simplification**: Substation boundaries are simplified to reduce file size
3. **Spatial Join**: Postcodes matched to substations using point-in-polygon analysis
4. **Unmatched Postcodes**: Some postcodes cannot be matched due to:
   - Data gaps in DNO boundaries
   - Offshore postcodes
   - New postcodes not yet in ONSPD
   - Postcodes on exact boundaries

## Update Process

To update data:

1. Download latest files from each DNO portal (quarterly or annually)
2. Download latest ONSPD (quarterly)
3. Run data processing pipeline
4. Review match statistics
5. Deploy updated files

## Contact DNOs

For questions about DNO data:

- **SPEN**: spenopendatateam@spenergynetworks.co.uk
- **SSEN**: ssen@sse.com
- **National Grid**: networkdata@nationalgrid.com
- **Northern Powergrid**: opendata@northernpowergrid.com
- **ENWL**: opendata@enwl.co.uk
- **UKPN**: ukpowernetworks@ukpowernetworks.co.uk

## Disclaimer

While we strive to use the most recent and accurate data, users should be aware:

- Data may contain errors or omissions
- Boundaries are approximate and may not reflect exact service areas
- Real-world infrastructure changes may not be immediately reflected
- For authoritative information, contact your local DNO directly

## Data Retention

- **Raw data**: Not stored in repository (download fresh each update)
- **Processed data**: Stored in repository with version control
- **Historical data**: Not retained (use git history if needed)

---

Last updated: January 2026
