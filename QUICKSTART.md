# Quick Start Guide

Get postcodes.energy running in 10 minutes!

## ⚡ Fast Track

### 1. You Already Have DNO Files ✓

Your substation files are being copied to:
```
postcodes-energy/data-processing/raw/substations/
```

### 2. Download Postcode Data

**Fastest option**: ONS Postcode Directory

1. Go to: https://geoportal.statistics.gov.uk/
2. Search: "ONSPD"
3. Download latest (requires free registration)
4. Extract and find: `ONSPD_XXX_2026_UK.csv`
5. Copy to: `postcodes-energy/data-processing/raw/postcodes/`

**Alternative**: If you already have postcode lat/long data, use that!

### 3. Install Python Dependencies

```bash
cd "C:\Users\blueb\OneDrive\Documents\postcodes-energy\data-processing"
pip install -r requirements.txt
```

If GeoPandas installation fails, try:
```bash
conda install -c conda-forge geopandas
pip install tqdm
```

### 4. Check Your DNO Files

Open `process_data.py` and verify the filenames in `DNO_FILES` match your actual files.

You have these files:
- `dfes-primary-polygons.geojson`
- `distribution-substation-service-areas.geojson`
- `east_midlands_primary.gpkg`
- `ndp-spd-primary-substation-polygons.geojson`
- `ndp-spm-primary-group-polygons.geojson`
- `sepd_primarysubstation_esa_2025.geojson`
- `south_wales_primary.gpkg`
- `south_west_primary.gpkg`
- `ukpn_primary_postcode_area (2).geojson`

**TO DO**: Identify which DNO the first two files belong to (see `DNO_INVENTORY.md`)

### 5. Process the Data

```bash
cd data-processing
python process_data.py
```

⏱️ This takes 20-40 minutes. Go make a cup of tea!

### 6. Copy Output to Frontend

```bash
copy output\postcode_lookup.json ..\public\data\
copy output\substations.json ..\public\data\
```

### 7. Test Locally

```bash
cd ..\public
python -m http.server 8000
```

Open: http://localhost:8000

Try searching: `SW1A 1AA` (Buckingham Palace)

### 8. Deploy to Cloudflare Pages

1. Push to GitHub
2. Connect to Cloudflare Pages
3. Set publish directory: `public`
4. Deploy!

## 🎯 What You Have Now

```
postcodes-energy/
├── data-processing/
│   ├── process_data.py          ✓ Ready
│   ├── requirements.txt         ✓ Ready
│   ├── DNO_INVENTORY.md         ✓ Ready (update with unknowns)
│   ├── raw/
│   │   ├── substations/         ✓ Files copied!
│   │   └── postcodes/           ⚠️ ADD ONSPD FILE HERE
│   └── output/                  ⏳ Will be created by script
├── public/
│   ├── index.html               ✓ Ready
│   ├── styles.css               ✓ Ready
│   ├── app.js                   ✓ Ready
│   └── data/                    ⏳ Copy processed files here
├── docs/
│   ├── DATA_SOURCES.md          ✓ Ready
│   └── SETUP_GUIDE.md           ✓ Ready (detailed version)
├── README.md                    ✓ Ready
├── LICENSE                      ✓ Ready
├── CONTRIBUTING.md              ✓ Ready
└── .gitignore                   ✓ Ready
```

## 📋 Checklist

- [x] Project structure created
- [x] DNO files copied
- [ ] Install Python dependencies (`pip install -r requirements.txt`)
- [ ] Download ONSPD and place in `raw/postcodes/`
- [ ] Identify unknown DNO files (update `DNO_INVENTORY.md`)
- [ ] Update `process_data.py` with correct filenames if needed
- [ ] Run data processing script
- [ ] Copy output files to `public/data/`
- [ ] Test locally
- [ ] Initialize git repository
- [ ] Push to GitHub
- [ ] Deploy to Cloudflare Pages
- [ ] Configure custom domain (postcodes.energy)

## 🚨 Common Issues

**Problem**: Can't install GeoPandas
**Fix**: Use conda instead of pip (see above)

**Problem**: Script says file not found
**Fix**: Check filenames in `DNO_FILES` match actual files

**Problem**: Map doesn't show
**Fix**: Make sure data files are in `public/data/` and browser console has no errors

**Problem**: Postcodes not found
**Fix**: Verify ONSPD is loaded and postcode format is correct

## 📚 More Help

- **Detailed setup**: See `docs/SETUP_GUIDE.md`
- **Data info**: See `docs/DATA_SOURCES.md`
- **Contributing**: See `CONTRIBUTING.md`
- **Overview**: See `README.md`

## 🎉 Next Steps After Launch

1. Register `postcodes.energy` domain (if not already)
2. Configure DNS to point to Cloudflare Pages
3. Set up analytics (optional - Plausible, Cloudflare Analytics)
4. Share on social media / Reddit / HN
5. Monitor GitHub issues for bug reports
6. Plan quarterly data updates

---

**Need help?** Open an issue on GitHub or check the detailed setup guide!

Good luck! ⚡
