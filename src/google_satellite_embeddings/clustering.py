"""K-means clustering analysis for satellite embeddings."""

import ee
import geemap
import geemap.foliumap as geefolium
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Tuple
from matplotlib.colors import ListedColormap, BoundaryNorm


# Kelly's 22 maximally distinct colors
KELLY_COLORS = [
    "#F3C300", "#875692", "#F38400", "#A1CAF1", "#BE0032", "#C2B280", "#848482", "#008856",
    "#E68FAC", "#0067A5", "#F99379", "#604E97", "#F6A600", "#B3446C", "#DCD300", "#882D17",
    "#8DB600", "#654522", "#E25822", "#2B3D26", "#F2F3F4", "#222222"
]


class ClusteringAnalysis:
    """Perform K-means clustering analysis on satellite embeddings."""

    def __init__(
        self,
        embeddings_image: ee.Image,
        region: ee.Geometry,
        n_samples: int = 1000,
        scale: int = 10,
        seed: int = 100
    ):
        """
        Initialize clustering analysis.

        Args:
            embeddings_image: Earth Engine image with satellite embeddings
            region: Area of interest geometry
            n_samples: Number of samples for training
            scale: Scale in meters for sampling
            seed: Random seed for reproducibility
        """
        self.embeddings_image = embeddings_image
        self.region = region
        self.n_samples = n_samples
        self.scale = scale
        self.seed = seed
        self.training = None
        self._generate_training_data()

    def _generate_training_data(self) -> None:
        """Generate training data from the embeddings image."""
        self.training = self.embeddings_image.sample(
            region=self.region,
            scale=self.scale,
            numPixels=self.n_samples,
            seed=self.seed,
            geometries=False
        )

    def get_clusters(self, n_clusters: int) -> ee.Image:
        """
        Perform K-means clustering.

        Args:
            n_clusters: Number of clusters

        Returns:
            Earth Engine image with cluster assignments
        """
        clusterer = ee.Clusterer.wekaKMeans(nClusters=int(n_clusters)).train(self.training)
        return self.embeddings_image.cluster(clusterer)

    def export_clusters(
        self,
        n_clusters: int,
        output_path: Path,
        scale: int = 10
    ) -> Path:
        """
        Export cluster results as GeoTIFF.

        Args:
            n_clusters: Number of clusters
            output_path: Path for output GeoTIFF file
            scale: Scale in meters for export

        Returns:
            Path to exported file
        """
        img = self.get_clusters(n_clusters).toInt().clip(self.region)
        geemap.ee_export_image(
            img,
            str(output_path),
            scale=scale,
            region=self.region,
            file_per_band=False
        )
        return output_path

    def create_interactive_map(
        self,
        n_clusters: int,
        output_path: Path,
        zoom_start: int = 13
    ) -> Path:
        """
        Create interactive map with cluster visualization.

        Args:
            n_clusters: Number of clusters
            output_path: Path for output HTML file
            zoom_start: Initial zoom level

        Returns:
            Path to HTML file
        """
        clustered = self.get_clusters(n_clusters)

        # Get region bounds
        coords = self.region.bounds().getInfo()['coordinates'][0]
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        center_lat = (min(lats) + max(lats)) / 2
        center_lon = (min(lons) + max(lons)) / 2

        # Create map
        vis_params = {
            'min': 0,
            'max': n_clusters - 1,
            'palette': KELLY_COLORS[:n_clusters]
        }

        m = geefolium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            control_scale=True
        )
        m.add_basemap("SATELLITE")
        m.addLayer(clustered.toInt(), vis_params, f"K={n_clusters} clusters")
        m.fit_bounds([[min(lats), min(lons)], [max(lats), max(lons)]])
        m.save(str(output_path))

        return output_path

    @staticmethod
    def read_cluster_raster(path: Path) -> Tuple[np.ndarray, tuple, object, object]:
        """
        Read cluster raster from file.

        Args:
            path: Path to GeoTIFF file

        Returns:
            Tuple of (array, extent, transform, crs)
        """
        with rasterio.open(path) as src:
            arr = src.read(1)
            extent = (src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top)
            transform = src.transform
            crs = src.crs
        return arr, extent, transform, crs

    @staticmethod
    def create_cluster_panel(
        cluster_paths: List[Path],
        cluster_values: List[int],
        output_path: Path,
        figsize: Tuple[int, int] = (12, 4),
        dpi: int = 300
    ) -> Path:
        """
        Create multi-panel visualization of different cluster counts.

        Args:
            cluster_paths: List of paths to cluster GeoTIFF files
            cluster_values: List of K values corresponding to each path
            output_path: Path for output PNG file
            figsize: Figure size (width, height)
            dpi: Resolution in dots per inch

        Returns:
            Path to output PNG file
        """
        fig, axs = plt.subplots(1, len(cluster_paths), figsize=figsize, constrained_layout=True)

        if len(cluster_paths) == 1:
            axs = [axs]

        for ax, path, k in zip(axs, cluster_paths, cluster_values):
            arr, _, _, _ = ClusteringAnalysis.read_cluster_raster(path)

            cmap = ListedColormap(KELLY_COLORS[:k])
            bounds = np.arange(-0.5, k + 0.5, 1)
            norm = BoundaryNorm(bounds, cmap.N)

            ax.imshow(arr, cmap=cmap, norm=norm)
            ax.set_title(f"K = {k}")
            ax.set_xticks([])
            ax.set_yticks([])

        plt.savefig(output_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)

        return output_path
