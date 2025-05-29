
# 🌍 District-wise ESA LULC Data Visualization App

This Streamlit app allows users to interactively explore and visualize annual Land Use / Land Cover (LULC) class statistics from the ESA dataset across districts in India.

The app fetches high-resolution LULC data using the STAC API from Microsoft Planetary Computer and generates district-specific land cover percentage charts for selected years.

---

## 🚀 Features

- ✅ Select Indian **State** and **District**
- 🗺️ View boundary on an interactive map (Plotly-based)
- 📅 Choose a **LULC Year** (2020–2024)
- 📊 Generate **class-wise % distribution** bar chart
- 🔄 **Step-by-step progress feedback** during data processing:
  1. Getting STAC catalog
  2. Getting district bounding box
  3. Clipping to district geometry
  4. Extracting LULC statistics
  5. Chart ready!

---

## 📡 STAC Dataset Information

- **STAC Collection**: [`io-lulc-annual-v02`](https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc-annual-v02)
- **Providers**:
  - Esri (Licensor)
  - Impact Observatory (Processor, Producer, Licensor)
  - Microsoft (Host)
- **License**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

---

## 🧭 Sidebar Info (App)

- Instructions to use the app
- Source collection and license
- Provider credits

---

## 📁 Directory Structure

```
.
├── app.py                  # Main Streamlit app
├── utils/
│   └── utils.py            # Contains `get_items_from_stac()` logic
├── data/
│   └── 2011_Dist.shp       # Indian district boundaries shapefile (+ related files)
├── requirements.txt        # All Python dependencies
└── README.md               # This file
```

---

## 📦 Installation

### 1. Clone the repo:

```bash
git clone https://github.com/your-repo/esa-lulc-streamlit.git
cd esa-lulc-streamlit
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then, open your browser and go to [http://localhost:8501](http://localhost:8501)

---

## 🔧 Requirements

Sample `requirements.txt`:

```text
streamlit
geopandas
pandas
numpy
matplotlib
plotly
rasterio
shapely
pyproj
pystac-client
requests
```

---

## 📸 Example Output

> (Add screenshots of the dropdown selection, map, and bar chart outputs here)

---

## 📜 License

This app is released under the **MIT License**.

The ESA Land Cover dataset used is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## 🙌 Acknowledgements

- [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)
- [ESA](https://www.esa.int/)
- [Impact Observatory](https://impactobservatory.com/)
- [Esri](https://www.esri.com/)
- [Streamlit](https://streamlit.io/)

---

Enjoy exploring India's LULC history! 🌾🌍🛰️
