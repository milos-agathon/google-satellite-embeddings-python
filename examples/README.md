# Examples

This directory contains example notebooks and scripts demonstrating how to use the google-satellite-embeddings package.

## Jupyter Notebook

### [google-embeddings.ipynb](google-embeddings.ipynb)

The original Jupyter notebook showing:
- Part I: Clustering Analysis - Unsupervised classification of satellite embeddings
- Part II: Change Detection Analysis - Temporal analysis using satellite embeddings

This notebook demonstrates the complete workflow from data acquisition to visualization.

## Running the Examples

1. Install the package:
   ```bash
   pip install -e ..
   ```

2. Set up Earth Engine authentication:
   ```python
   import ee
   ee.Authenticate()
   ```

3. Open the notebook:
   ```bash
   jupyter notebook google-embeddings.ipynb
   ```
