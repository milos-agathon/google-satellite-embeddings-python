"""Change detection analysis using satellite embeddings."""

import ee
import geemap
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional


class ChangeDetectionAnalysis:
    """Perform change detection analysis between two time periods."""

    def __init__(
        self,
        embeddings_t1: ee.Image,
        embeddings_t2: ee.Image,
        region: ee.Geometry
    ):
        """
        Initialize change detection analysis.

        Args:
            embeddings_t1: Embeddings for first time period
            embeddings_t2: Embeddings for second time period
            region: Area of interest geometry
        """
        self.embeddings_t1 = embeddings_t1
        self.embeddings_t2 = embeddings_t2
        self.region = region

    def compute_mean_absolute_difference(self) -> ee.Image:
        """
        Compute mean absolute difference across all embedding bands.

        Returns:
            Single-band image with mean absolute difference values
        """
        return (
            self.embeddings_t2
            .subtract(self.embeddings_t1)
            .abs()
            .reduce(ee.Reducer.mean())
        )

    def compute_cosine_similarity(self) -> ee.Image:
        """
        Compute cosine similarity between embeddings.

        Returns:
            Single-band image with cosine similarity values [-1, 1]
        """
        a = self.embeddings_t1.toArray()
        b = self.embeddings_t2.toArray()

        # Dot product
        dot = a.multiply(b).arrayReduce(ee.Reducer.sum(), [0]).arrayGet([0])

        # Norms
        na = a.multiply(a).arrayReduce(ee.Reducer.sum(), [0]).arrayGet([0]).sqrt()
        nb = b.multiply(b).arrayReduce(ee.Reducer.sum(), [0]).arrayGet([0]).sqrt()

        # Cosine similarity (avoid divide-by-zero)
        den = na.multiply(nb)
        cos = dot.divide(den).clamp(-1, 1).updateMask(den.neq(0)).rename('cosine')

        return cos

    def export_change_map(
        self,
        change_image: ee.Image,
        output_path: Path,
        scale: int = 10
    ) -> Path:
        """
        Export change detection results as GeoTIFF.

        Args:
            change_image: Change detection image to export
            output_path: Path for output GeoTIFF file
            scale: Scale in meters for export

        Returns:
            Path to exported file
        """
        geemap.ee_export_image(
            change_image,
            str(output_path),
            scale=scale,
            region=self.region
        )
        return output_path

    @staticmethod
    def visualize_change_map(
        tif_path: Path,
        title: str,
        output_path: Optional[Path] = None,
        cmap: str = "magma",
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        figsize: tuple = (7.5, 6),
        dpi: int = 600
    ) -> Optional[Path]:
        """
        Create visualization of change detection map.

        Args:
            tif_path: Path to input GeoTIFF
            title: Plot title
            output_path: Optional path for output PNG (if None, displays interactively)
            cmap: Matplotlib colormap name
            vmin: Minimum value for colormap
            vmax: Maximum value for colormap
            figsize: Figure size (width, height)
            dpi: Resolution in dots per inch

        Returns:
            Path to output PNG if output_path provided, None otherwise
        """
        with rasterio.open(tif_path) as src:
            arr = src.read(1)

        fig = plt.figure(figsize=figsize)
        plt.imshow(arr, cmap=cmap, vmin=vmin, vmax=vmax)
        plt.title(title)
        plt.xticks([])
        plt.yticks([])
        plt.colorbar()

        if output_path is not None:
            plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
            plt.close(fig)
            return output_path
        else:
            plt.show()
            return None
