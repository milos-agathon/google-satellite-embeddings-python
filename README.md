# Revolutionizing Land Cover Analysis with Google Satellite Embeddings and Python

A Python package for analyzing satellite imagery using Google Earth Engine embeddings. This package provides tools for k-means clustering and change detection analysis with clear visualizations.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🛰️ **Satellite Embeddings**: Load and process Google Earth Engine satellite embeddings
- 📊 **Clustering Analysis**: K-means clustering with sensible defaults and diagnostics
- 🔍 **Change Detection**: Temporal analysis using mean absolute difference and cosine similarity
- 🗺️ **Visualization**: Interactive maps and publication-quality static visualizations
- 🎯 **Smart Sampling**: Efficient sampling strategies for large imagery datasets

## Installation

### From source

```bash
git clone https://github.com/milos-agathon/google-satellite-embeddings-python.git
cd google-satellite-embeddings-python
pip install -e .
```

### Development installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
import ee
from google_satellite_embeddings import (
    setup_ee,
    create_region,
    get_satellite_embeddings,
    ClusteringAnalysis,
    ChangeDetectionAnalysis
)

# Initialize Earth Engine
setup_ee(project="your-ee-project")

# Define area of interest
region = create_region(xmin=83.919067, ymin=28.190059,
                       xmax=83.977776, ymax=28.235137)

# Get satellite embeddings
embeddings = get_satellite_embeddings(region, year_start=2024, year_end=2025)

# Perform clustering analysis
clustering = ClusteringAnalysis(embeddings, region, n_samples=1000)
clusters = clustering.get_clusters(n_clusters=5)
clustering.export_clusters(5, "clusters_k5.tif")

# Create interactive map
clustering.create_interactive_map(5, "map.html")
```

## Examples

### PART I: CLUSTERING ANALYSIS

Demonstrates unsupervised classification of satellite embeddings using k-means clustering.

![Clustering Analysis](docs/images/clusters_panel.png)

### PART II: CHANGE DETECTION ANALYSIS

Demonstrates temporal analysis using satellite embeddings to detect changes between 2018 and 2024.

![Change Detection](docs/images/mean_absolute_difference.png)

See the [examples directory](examples/) for complete Jupyter notebook demonstrations.

## Project Structure

```
google-satellite-embeddings-python/
├── src/
│   └── google_satellite_embeddings/
│       ├── __init__.py              # Package initialization
│       ├── clustering.py            # Clustering analysis module
│       ├── change_detection.py      # Change detection module
│       └── utils.py                 # Utility functions
├── examples/
│   ├── google-embeddings.ipynb      # Complete example notebook
│   └── README.md                    # Examples documentation
├── docs/
│   ├── images/                      # Visualization outputs
│   └── README.md                    # Documentation
├── tests/                           # Unit tests
├── pyproject.toml                   # Package configuration
├── setup.py                         # Setup script
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development dependencies
└── README.md                        # This file
```

## API Overview

### Utilities (`utils.py`)
- `setup_ee()` - Initialize Earth Engine with authentication
- `get_satellite_embeddings()` - Fetch satellite embeddings for a region and time period
- `create_region()` - Create Earth Engine geometry from coordinates

### Clustering (`clustering.py`)
- `ClusteringAnalysis` - Main class for k-means clustering analysis
  - `get_clusters()` - Perform clustering with specified k
  - `export_clusters()` - Export results as GeoTIFF
  - `create_interactive_map()` - Generate interactive HTML map
  - `create_cluster_panel()` - Multi-panel visualization

### Change Detection (`change_detection.py`)
- `ChangeDetectionAnalysis` - Main class for temporal change analysis
  - `compute_mean_absolute_difference()` - Calculate MAD between time periods
  - `compute_cosine_similarity()` - Calculate cosine similarity
  - `export_change_map()` - Export results as GeoTIFF
  - `visualize_change_map()` - Create visualization

## Requirements

- Python 3.8+
- earthengine-api >= 0.1.300
- geemap >= 0.20.0
- folium >= 0.14.0
- rasterio >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.5.0

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black src/ tests/
isort src/ tests/
```

### Type checking

```bash
mypy src/
```

## Earth Engine Setup

Before using this package, you need to:

1. Create a Google Earth Engine account at https://earthengine.google.com
2. Authenticate Earth Engine:
   ```python
   import ee
   ee.Authenticate()
   ```
3. Set your Earth Engine project ID when initializing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{popovic2024satellite,
  author = {Popovic, Milos},
  title = {Google Satellite Embeddings Python Package},
  year = {2024},
  url = {https://github.com/milos-agathon/google-satellite-embeddings-python}
}
```

## Credits

Created with ☕ by **Milos Popovic** • [YouTube channel](https://www.youtube.com/@milos-makes-maps) – subscribe for more R + GIS tutorials.

## Acknowledgments

This package uses Google Earth Engine's satellite embedding dataset and the excellent geemap library for Earth Engine integration.
