"""Google Satellite Embeddings - Python package for satellite imagery analysis."""

__version__ = "0.1.0"

from .clustering import ClusteringAnalysis
from .change_detection import ChangeDetectionAnalysis
from .utils import setup_ee, get_satellite_embeddings

__all__ = [
    "ClusteringAnalysis",
    "ChangeDetectionAnalysis",
    "setup_ee",
    "get_satellite_embeddings",
]
