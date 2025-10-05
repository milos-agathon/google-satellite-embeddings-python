"""Utility functions for Earth Engine setup and data acquisition."""

import ee
from pathlib import Path
from typing import Optional


def setup_ee(project: Optional[str] = None) -> None:
    """
    Initialize Earth Engine with authentication.

    Args:
        project: Optional Earth Engine project ID
    """
    try:
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()
    except Exception:
        ee.Authenticate()
        if project:
            ee.Initialize(project=project)
        else:
            ee.Initialize()


def get_satellite_embeddings(
    region: ee.Geometry,
    year_start: int,
    year_end: int
) -> ee.Image:
    """
    Get satellite embeddings for a specific time period.

    Args:
        region: Earth Engine geometry defining the area of interest
        year_start: Start year for data collection
        year_end: End year for data collection (exclusive)

    Returns:
        Earth Engine image with satellite embeddings
    """
    return (
        ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
        .filterDate(f"{year_start}-01-01", f"{year_end}-01-01")
        .filterBounds(region)
        .mosaic()
        .clip(region)
        .toFloat()
    )


def create_region(xmin: float, ymin: float, xmax: float, ymax: float) -> ee.Geometry:
    """
    Create an Earth Engine geometry from bounding box coordinates.

    Args:
        xmin: Minimum longitude
        ymin: Minimum latitude
        xmax: Maximum longitude
        ymax: Maximum latitude

    Returns:
        Earth Engine polygon geometry
    """
    return ee.Geometry.Polygon([[
        [xmin, ymin], [xmin, ymax],
        [xmax, ymax], [xmax, ymin]
    ]])


def ensure_output_dir(outdir: Path) -> Path:
    """
    Ensure output directory exists.

    Args:
        outdir: Path to output directory

    Returns:
        Path object for the output directory
    """
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir
