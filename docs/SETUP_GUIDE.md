# Setup Guide

Complete guide to setting up and running postcodes.energy.

## Prerequisites

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **Git** (for version control)
- **Text editor** (VS Code, Sublime, etc.)

## Step-by-Step Setup

### 1. Clone or Download Project

```bash
cd "C:\Users\blueb\OneDrive\Documents"
# If you have the project folder, you're already good!
```

### 2. Install Python Dependencies

Open terminal in project directory:

```bash
cd postcodes-energy/data-processing
pip install -r requirements.txt
```

This will install:
- `geopandas` - Geographic data processing
- `shapely` - Geometric operations
- `pandas` - Data manipulation
- `fiona` - File I/O for geographic data
- `pyogrio` - Fast geographic file reading
- `tqdm` - Progress bars

**Note**: GeoPandas can be tricky on Windows. If you encounter issues:

```bash
# Install from conda-forge instead
conda install -c conda-forge geopandas
```

### 3. Copy Your Downloaded DNO Files

You already have DNO files. Let's copy them to the correct location:

```bash
# Copy from old location to new project structure
copy "C:\Users\blueb\OneDrive\Documents\UK Postcode matching tool\data-processingrawsubstations\*.*" "C:\Users\blueb\OneDrive\Documents\postcodes-energy\data-processing\raw\substations\"
```

Or manually:
1. Go to your old location with the DNO files
2. Copy all files (9 files you downloaded)
3. Paste into `postcodes-energy\data-processing\raw\substations\`

### 4. Download Postcode Location Data

You need UK postcode latitude/longitude data.

#### Option A: ONS Postcode Directory (Recommended)

1. Visit: https://geoportal.statistics.gov.uk/
2. Search for "ONSPD"
3. Download latest version (requires free registration)
4. Extract the ZIP file
5. Find the file named something like `ONSPD_FEB_2026_UK.csv`
6. Copy to `data-processing\raw\postcodes\`

#### Option B: OS Code-Point Open

1. Visit: https://www.ordnancesurvey.co.uk/products/code-point-open
2. Download (requires accepting license)
3. Extract and convert to CSV with postcode, lat, long columns
4. Copy to `data-processing\raw\postcodes\`

### 5. Update DNO File Mapping

Open `data-processing\process_data.py` and verify the `DNO_FILES` dictionary matches your actual files.

Current mapping in the script:
```python
DNO_FILES = {
    "SPEN_SPD": {
        "file": "ndp-spd-primary-substation-polygons.geojson",
        ...
    },
    # etc.
}
```

If your filenames are different, update them here.

### 6. Run Data Processing

```bash
cd data-processing
python process_data.py
```

This will:
1. Load all DNO substation boundaries (~2-5 minutes)
2. Load postcode data (~2-3 minutes)
3. Match postcodes to substations (~15-30 minutes)
4. Create optimized output files (~2 minutes)

**Total time**: ~20-40 minutes depending on your computer

Watch for any errors. If you see warnings about unmatched postcodes, that's normal (some postcodes are offshore, new, or on boundaries).

### 7. Copy Processed Data to Frontend

```bash
# From data-processing folder
copy output\postcode_lookup.json ..\public\data\
copy output\substations.json ..\public\data\
```

### 8. Test Locally

```bash
cd ..\public
python -m http.server 8000
```

Open browser to: `http://localhost:8000`

Try searching for a postcode like `SW1A 1AA` (Buckingham Palace) or `LS1 4DY` (Leeds).

### 9. Set Up Git Repository (Optional but Recommended)

```bash
cd ..
git init
git add .
git commit -m "Initial commit - postcodes.energy project"
```

Create repository on GitHub and push:

```bash
git remote add origin https://github.com/yourusername/postcodes-energy.git
git branch -M main
git push -u origin main
```

### 10. Deploy to Cloudflare Pages

1. Go to https://dash.cloudflare.com/
2. Click "Pages" → "Create a project"
3. Connect your GitHub repository
4. Configure build:
   - **Framework preset**: None
   - **Build command**: (leave empty)
   - **Build output directory**: `public`
5. Click "Save and Deploy"

Your site will be live at: `https://postcodes-energy.pages.dev`

### 11. Configure Custom Domain (Optional)

If you registered `postcodes.energy`:

1. In Cloudflare Pages, go to "Custom domains"
2. Click "Set up a custom domain"
3. Enter: `postcodes.energy`
4. Follow DNS configuration instructions
5. Wait for SSL certificate (automatic, ~15 minutes)

## Troubleshooting

### GeoPandas Installation Issues

**Problem**: `pip install geopandas` fails on Windows

**Solution**: Use Conda
```bash
conda create -n postcodes python=3.10
conda activate postcodes
conda install -c conda-forge geopandas
pip install tqdm
```

### File Not Found Errors

**Problem**: `FileNotFoundError` when running process_data.py

**Solution**:
1. Check files are in correct folders
2. Verify filenames in `DNO_FILES` dictionary match actual files
3. Check paths use correct slashes for your OS

### Memory Errors

**Problem**: Script crashes with `MemoryError`

**Solution**:
1. Process in chunks (modify script)
2. Close other applications
3. Use a computer with more RAM
4. Process subsets of data first

### Spatial Join Too Slow

**Problem**: Matching takes hours

**Solution**:
- This is normal for ~1.7M postcodes
- Use spatial index (already implemented with GeoPandas)
- Run overnight if needed
- Consider upgrading CPU

### Map Not Showing

**Problem**: Blank map in web app

**Solution**:
1. Check browser console for errors (F12)
2. Verify data files are in `public/data/`
3. Check file sizes (should be several MB each)
4. Try hard refresh (Ctrl+Shift+R)

### Postcodes Not Found

**Problem**: Valid postcodes return "not found"

**Solution**:
1. Check postcode data is loaded (see console)
2. Verify postcode is in ONSPD (some new postcodes take time)
3. Check case/formatting (app normalizes, but verify)

## Next Steps

After successful setup:

1. ✅ Test with multiple postcodes
2. ✅ Verify map visualization works
3. ✅ Test export to CSV
4. ✅ Check mobile responsiveness
5. ✅ Review data attribution in footer
6. ✅ Update README with your GitHub username
7. ✅ Deploy to production
8. ✅ Share with community!

## Data Updates

To update data quarterly:

1. Download latest ONSPD (quarterly releases)
2. Check DNO portals for updated boundaries
3. Replace files in `raw/` folders
4. Re-run `python process_data.py`
5. Copy new output files to `public/data/`
6. Commit and push changes
7. Cloudflare Pages will auto-deploy

## Getting Help

- Check [README.md](../README.md) for overview
- See [DATA_SOURCES.md](DATA_SOURCES.md) for data info
- Open issue on GitHub
- Review Python script comments

---

Good luck! ⚡ Feel free to reach out if you hit any issues.
