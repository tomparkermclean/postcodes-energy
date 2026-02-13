"""
Aggressive simplification to get under 25 MB
"""

import json
from pathlib import Path
from shapely.geometry import shape, mapping

def simplify_geometry(geom, tolerance=0.001):
    """Very minimal simplification for high quality"""
    try:
        shapely_geom = shape(geom)
        simplified = shapely_geom.simplify(tolerance, preserve_topology=True)
        return mapping(simplified)
    except Exception as e:
        print(f"Error: {e}")
        return geom

def round_coordinates(geom, decimals=4):
    """Round to 4 decimals = ~11m precision"""
    def round_coords(coords):
        if isinstance(coords[0], (list, tuple)):
            return [round_coords(c) for c in coords]
        else:
            return [round(c, decimals) for c in coords]
    
    if geom['type'] == 'Polygon':
        geom['coordinates'] = [round_coords(ring) for ring in geom['coordinates']]
    elif geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [[round_coords(ring) for ring in polygon] for polygon in geom['coordinates']]
    
    return geom

def simplify_substations_file(input_path, output_path):
    print(f"Loading {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} substations...")
    print("Using very minimal simplification:")
    print("  - Tolerance: 0.001 (very minimal)")
    print("  - Decimals: 4 (~11m precision)")
    print("  - Removing non-essential fields")
    
    for substation_id, substation in data.items():
        # Keep essential fields for frontend
        fields_to_keep = {'id', 'name', 'dno_id', 'dno_name', 'dno', 'license_area', 'postcode_count', 'household_count', 'chunks', 'centroid', 'boundary', 'geometry'}
        fields_to_remove = [k for k in list(substation.keys()) if k not in fields_to_keep]
        for field in fields_to_remove:
            del substation[field]
        
        if 'boundary' in substation or 'geometry' in substation:
            geom_field = 'boundary' if 'boundary' in substation else 'geometry'
            
            # Very minimal simplification
            simplified_geom = simplify_geometry(substation[geom_field], tolerance=0.001)
            simplified_geom = round_coordinates(simplified_geom, decimals=4)
            
            substation[geom_field] = simplified_geom
    
    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
    
    original_size = Path(input_path).stat().st_size / (1024 * 1024)
    new_size = Path(output_path).stat().st_size / (1024 * 1024)
    reduction = ((original_size - new_size) / original_size) * 100
    
    print(f"\nDone!")
    print(f"Original size: {original_size:.2f} MB")
    print(f"New size: {new_size:.2f} MB")
    print(f"Reduction: {reduction:.1f}%")
    
    if new_size > 25:
        print(f"\nWARNING: Still {new_size:.2f} MB (over limit)")
    else:
        print(f"\nSuccess! Under 25 MB!")

if __name__ == "__main__":
    # Use the original backup
    input_file = Path("public/data/substations_original.json")
    output_file = Path("public/data/substations.json")
    
    if not input_file.exists():
        print("ERROR: substations_original.json not found!")
        print("Using substations.json instead...")
        input_file = Path("public/data/substations.json")
    
    simplify_substations_file(input_file, output_file)
    
    new_size = output_file.stat().st_size / (1024 * 1024)
    if new_size <= 25:
        print(f"\nsubstations.json is now ready for deployment!")
