"""
Simplify substations.json geometry to reduce file size
Reduces file size from 33.5 MB to under 25 MB for Cloudflare Pages
"""

import json
from pathlib import Path
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

def simplify_geometry(geom, tolerance=0.001):
    """
    Simplify geometry while preserving shape.
    tolerance: higher = more simplification (0.001 = good balance)
    """
    try:
        shapely_geom = shape(geom)
        simplified = shapely_geom.simplify(tolerance, preserve_topology=True)
        return mapping(simplified)
    except Exception as e:
        print(f"Error simplifying: {e}")
        return geom

def round_coordinates(geom, decimals=4):
    """
    Round coordinates to reduce file size.
    4 decimals = ~11 meter precision (good enough for substations)
    """
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
    """
    Load substations.json, simplify geometries, and save.
    """
    print(f"Loading {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} substations...")
    
    simplified_count = 0
    for substation_id, substation in data.items():
        if 'boundary' in substation or 'geometry' in substation:
            # Handle both possible field names
            geom_field = 'boundary' if 'boundary' in substation else 'geometry'
            
            # Simplify the geometry
            simplified_geom = simplify_geometry(substation[geom_field], tolerance=0.001)
            
            # Round coordinates to reduce precision
            simplified_geom = round_coordinates(simplified_geom, decimals=4)
            
            substation[geom_field] = simplified_geom
            simplified_count += 1
    
    print(f"Simplified {simplified_count} substation boundaries")
    
    # Save simplified version
    print(f"Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))  # Compact JSON (no spaces)
    
    # Check file sizes
    original_size = Path(input_path).stat().st_size / (1024 * 1024)
    new_size = Path(output_path).stat().st_size / (1024 * 1024)
    reduction = ((original_size - new_size) / original_size) * 100
    
    print(f"\n✅ Done!")
    print(f"Original size: {original_size:.2f} MB")
    print(f"New size: {new_size:.2f} MB")
    print(f"Reduction: {reduction:.1f}%")
    
    if new_size > 25:
        print(f"\n⚠️  WARNING: File is still {new_size:.2f} MB (over 25 MB limit)")
        print("Try increasing tolerance or reducing decimal places")
    else:
        print(f"\n🎉 Success! File is now under 25 MB limit")

if __name__ == "__main__":
    input_file = Path("public/data/substations.json")
    output_file = Path("public/data/substations_simplified.json")
    backup_file = Path("public/data/substations_original.json")
    
    if not input_file.exists():
        print(f"ERROR: {input_file} not found!")
        print("Make sure you're running this from the postcodes-energy directory")
        exit(1)
    
    # Create backup
    print(f"Creating backup at {backup_file}...")
    import shutil
    shutil.copy2(input_file, backup_file)
    
    # Simplify
    simplify_substations_file(input_file, output_file)
    
    # If successful and under 25 MB, replace original
    new_size = output_file.stat().st_size / (1024 * 1024)
    if new_size <= 25:
        print(f"\nReplacing original file with simplified version...")
        shutil.move(output_file, input_file)
        print(f"✅ Original file replaced. Backup saved at {backup_file}")
    else:
        print(f"\nSimplified file saved as {output_file}")
        print(f"Original file kept at {input_file}")
        print(f"Backup at {backup_file}")
