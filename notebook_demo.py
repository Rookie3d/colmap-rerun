"""
COLMAP Reconstruction Visualization for Notebooks (Google Colab, Jupyter, etc.)

Installation (run this in a cell first):
!pip install rerun-sdk[notebook]

For Google Colab, after installation, restart the runtime before running the visualization.
"""

import rerun as rr
from pathlib import Path
from typing import Optional, Tuple

from src.colmap_rerun.core.reconstruction import load_sparse_model
from src.colmap_rerun.visualization.visualizer import visualize_reconstruction


def visualize_colmap_in_notebook(
    sparse_model_path: str,
    images_path: str,
    dense_model_path: Optional[str] = None,
    resize: Optional[Tuple[int, int]] = None,
    unfiltered: bool = False,
    width: int = 800,
    height: int = 600,
    application_id: str = "colmap_notebook_demo"
) -> None:
    """
    Visualize COLMAP reconstruction in a notebook environment.
    
    Args:
        sparse_model_path: Path to sparse reconstruction (e.g., "/path/to/dataset/sparse")
        images_path: Path to images folder (e.g., "/path/to/dataset/images")
        dense_model_path: Optional path to dense reconstruction (e.g., "/path/to/dataset/dense")
        resize: Optional tuple (width, height) to resize images
        unfiltered: If True, don't filter noisy data
        width: Width of the embedded viewer
        height: Height of the embedded viewer
        application_id: Rerun application identifier
    """
    
    rr.init(application_id)
    
    sparse_model = Path(sparse_model_path)
    images_root = Path(images_path)
    dense_model = Path(dense_model_path) if dense_model_path else None
    
    depths_root = None
    if dense_model is not None:
        sparse_model = dense_model / "sparse"
        images_root = dense_model / "images" 
        depths_root = dense_model / "stereo" / "depth_maps"
    
    if not sparse_model.exists():
        raise ValueError(f"Sparse model path {sparse_model} does not exist.")
    if not images_root.exists():
        raise ValueError(f"Images path {images_root} does not exist.")
    
    print(f"Loading sparse model from: {sparse_model}")
    print(f"Loading images from: {images_root}")
    if depths_root:
        print(f"Loading depth maps from: {depths_root}")
    
    # Load the reconstruction data
    recon = load_sparse_model(
        model_path=sparse_model,
        images_root=images_root,
        depths_root=depths_root,
    )
    
    # Perform the visualization (this logs data to Rerun)
    visualize_reconstruction(
        recon.cameras,
        recon.images, 
        recon.points3D,
        recon.images_root,
        recon.depths_root,
        filter_output=not unfiltered,
        resize=resize,
    )
    
    # Display the viewer in the notebook
    rr.notebook_show(width=width, height=height)
    
    print("Visualization complete! The Rerun viewer should appear below.")


def demo_with_sample_data():
    """
    Example usage with sample data paths.
    Modify these paths to point to your actual COLMAP reconstruction.
    """
    
    # Example configuration - modify these paths for your data
    config = {
        "sparse_model_path": "content/colmap_output/sparse",
        "images_path": "content/colmap_output/images", 
        "resize": (640, 480),  # Optional: resize images
        "unfiltered": False,   # Set to True to show all data including noise
        "width": 1000,         # Viewer width in pixels
        "height": 700,         # Viewer height in pixels
    }

    
    try:
        visualize_colmap_in_notebook(**config)
    except Exception as e:
        print(f"Error: {e}")
        

def demo_with_dense_model(dense_model_path: str):
    """
    Example usage with a dense COLMAP reconstruction.
    This automatically configures sparse model and images paths.
    """
    
    config = {
        "sparse_model_path": "",  # Will be set automatically
        "images_path": "",        # Will be set automatically  
        "dense_model_path": dense_model_path,
        "resize": (640, 480),
        "width": 1000,
        "height": 700,
    }
    
    print("Starting COLMAP dense reconstruction visualization...")

    
    try:
        visualize_colmap_in_notebook(**config)
    except Exception as e:
        print(f"Error: {e}")




if __name__ == "__main__":
    demo_with_sample_data() 