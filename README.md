# postcodes.energy

> Find which electricity distribution substation serves your UK postcode and see all other postcodes in the same area.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🔌 About

**postcodes.energy** is an open-source web tool that allows anyone in the UK to:

- Look up any UK postcode
- Find which electricity distribution substation area it belongs to
- See all other postcodes served by the same substation
- Visualize substation boundaries on an interactive map
- Export postcode lists as CSV

This tool is useful for:
- Understanding electricity distribution infrastructure
- Energy network planning and analysis
- Research into grid capacity and development
- Community energy projects
- Educational purposes

## 🚀 Live Demo

Visit: **[postcodes.energy](https://postcodes.energy)** *(Coming soon)*

## 📊 Data Sources

This project uses open data from:

- **Distribution Network Operators (DNOs)**: Substation boundary polygons from all 14 UK DNO license areas
- **Office for National Statistics (ONS)**: UK Postcode Directory (ONSPD)
- **Ordnance Survey**: OS Open Code-Point data

All data is used under appropriate open licenses. See [DATA_SOURCES.md](docs/DATA_SOURCES.md) for details.

## 🛠️ Technology Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Mapping**: Leaflet.js
- **Data Processing**: Python (GeoPandas, Shapely)
- **Hosting**: Cloudflare Pages / Netlify
- **Data Format**: GeoJSON, optimized JSON lookups

## 📁 Project Structure

```
postcodes-energy/
├── data-processing/          # Data processing pipeline
│   ├── process_data.py       # Main processing script
│   ├── requirements.txt      # Python dependencies
│   ├── raw/                  # Raw data files (not committed)
│   │   ├── substations/      # DNO GeoJSON/GeoPackage files
│   │   └── postcodes/        # ONSPD or Code-Point data
│   └── output/               # Processed data (committed)
│       ├── postcode_lookup.json
│       └── substations.json
├── public/                   # Static website files
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── data/                 # Processed data for web app
├── docs/                     # Documentation
└── README.md
```

## 🏗️ Setup & Installation

### Prerequisites

- Python 3.9+
- Node.js (optional, for local dev server)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/postcodes-energy.git
cd postcodes-energy
```

### 2. Download Raw Data

#### Substation Boundaries

Download substation boundary data from each DNO:

- [SP Energy Networks](https://spenergynetworks.opendatasoft.com/)
- [SSEN](https://www.ssen.co.uk/about-ssen/dso-information-and-data/)
- [National Grid](https://www.nationalgrid.co.uk/electricity-distribution/distribution-data-portal)
- [Northern Powergrid](https://www.northernpowergrid.com/open-data)
- [Electricity North West](https://www.enwl.co.uk/open-data)
- [UK Power Networks](https://ukpowernetworks.opendatasoft.com/)

Place files in `data-processing/raw/substations/`

#### Postcode Location Data

Download from:
- [ONS Postcode Directory](https://geoportal.statistics.gov.uk/search?q=ONSPD) (free, requires registration)
- [OS Open Code-Point](https://www.ordnancesurvey.co.uk/products/code-point-open) (free, requires license acceptance)

Place CSV file in `data-processing/raw/postcodes/`

### 3. Process Data

```bash
cd data-processing
pip install -r requirements.txt
python process_data.py
```

This will:
- Load all DNO substation boundaries
- Match each postcode to its substation area
- Create optimized lookup files in `output/`

### 4. Copy Processed Data

```bash
# Copy processed data to public folder
cp output/*.json ../public/data/
```

### 5. Run Locally

```bash
# Option 1: Python simple server
cd public
python -m http.server 8000

# Option 2: Node.js http-server
npx http-server public -p 8000
```

Visit `http://localhost:8000`

## 🚀 Deployment

### Deploy to Cloudflare Pages

1. Push to GitHub
2. Connect repository to Cloudflare Pages
3. Set build settings:
   - Build command: *(none)*
   - Build output directory: `public`
4. Deploy!

### Deploy to Netlify

1. Push to GitHub
2. Connect repository to Netlify
3. Set build settings:
   - Build command: *(none)*
   - Publish directory: `public`
4. Deploy!

## 📝 Data Updates

Substation boundaries and postcodes change over time. To update:

1. Download latest data from DNOs and ONS
2. Replace files in `data-processing/raw/`
3. Run `python process_data.py`
4. Copy new files to `public/data/`
5. Commit and push

Recommended update frequency: **Quarterly** (aligned with ONSPD releases)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- Report bugs or suggest features via [Issues](https://github.com/yourusername/postcodes-energy/issues)
- Improve documentation
- Add missing DNO data
- Enhance the frontend UI
- Optimize data processing

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

### Data Licenses

- DNO data: Various open licenses (OGL, Creative Commons) - see individual DNO portals
- ONSPD: Contains public sector information licensed under the Open Government Licence v3.0
- OS Code-Point: Contains OS data © Crown copyright and database right (2026)

## ⚠️ Disclaimer

This tool is provided **for informational purposes only**. 

- Data accuracy is not guaranteed
- Not suitable for critical infrastructure decisions
- Substation boundaries are approximate
- Some postcodes may not be matched due to data limitations

For official information, contact your local Distribution Network Operator.

## 📧 Contact

- Website: [postcodes.energy](https://postcodes.energy)
- GitHub: [@yourusername](https://github.com/yourusername)
- Issues: [GitHub Issues](https://github.com/yourusername/postcodes-energy/issues)

## 🙏 Acknowledgments

- All UK Distribution Network Operators for providing open data
- Office for National Statistics for postcode data
- OpenStreetMap contributors for map tiles
- Leaflet.js for mapping library

---

**Made with ⚡ for the UK energy community**
