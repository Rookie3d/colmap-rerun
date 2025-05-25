# COLMAP + Rerun Notebook Demo

This demo shows how to visualize COLMAP reconstructions using Rerun in notebook environments like Jupyter Lab, Jupyter Notebook, VSCode, and Google Colab.

## Quick Start

### Clone the repository

Clone this repository:

```
git clone https://github.com/Rookie3d/colmap-rerun.git
cd colmap-rerun
```

### For Google Colab
1. Open `colmap_visualization_notebook.ipynb` in Google Colab
2. Run the installation cell: `!pip install rerun-sdk[notebook]`
3. Restart the runtime (Runtime → Restart Runtime)
4. Update the paths in the configuration cell
5. Run the visualization cell

### For Local Jupyter
```
pip install -r notebook_requirements.txt
jupyter notebook colmap_visualization_notebook.ipynb
```

### For VSCode
1. Install Python extension and Jupyter extension
2. Install requirements: `pip install -r notebook_requirements.txt`
3. Open `colmap_visualization_notebook.ipynb`
4. Select Python kernel and run cells

### Notebook install
If you are running in a notebook environment, install the requirements with:
```
!pip install -r notebook_requirements.txt
```

## File Structure

```
colmap-rerun/
├── notebook_demo.py                    # Core notebook functions
├── colmap_visualization_notebook.ipynb # Interactive notebook
├── notebook_requirements.txt           # Dependencies
├── README_notebook_demo.md             # This file
└── src/                               # Your existing COLMAP code
    └── colmap_rerun/
        ├── core/
        │   └── reconstruction.py
        └── visualization/
            └── visualizer.py
```

## Key Features

- Interactive 3D Visualization: Navigate through your COLMAP reconstruction with mouse controls
- Real-time Streaming: See updates immediately as you log new data
- Custom Layouts: Create custom viewer layouts with blueprints
- Performance Options: Resize images and filter noise for better performance
- Easy Configuration: Simple Python functions instead of command-line arguments

## Data Requirements

Your COLMAP reconstruction should have this structure:

```
dataset/
├── sparse/                 # COLMAP sparse reconstruction
│   ├── cameras.bin        # Camera parameters
│   ├── images.bin         # Image metadata
│   └── points3D.bin       # 3D points
├── images/                # Original images
│   ├── image001.jpg
│   ├── image002.jpg
│   └── ...
└── dense/ (optional)      # Dense reconstruction
    ├── sparse/           # Same as above
    ├── images/           # Same as above  
    └── stereo/
        └── depth_maps/   # Depth maps
```

## Main Functions

### `visualize_colmap_in_notebook()`
The main function for visualization:

```python
visualize_colmap_in_notebook(
    sparse_model_path="/path/to/sparse",
    images_path="/path/to/images",
    resize=(640, 480),        # Optional: resize for performance
    unfiltered=False,         # Optional: filter noise
    width=1000,              # Viewer width
    height=700               # Viewer height
)
```

### `demo_with_dense_model()`
Simplified function for dense reconstructions:

```python
demo_with_dense_model("/path/to/dense")
```

## Customization

### Custom Viewer Layout
```python
import rerun.blueprint as rrb

blueprint = rrb.Blueprint(
    rrb.Horizontal(
        rrb.Spatial3DView(origin="/world"),
        rrb.Spatial2DView(origin="/world/camera"),
        column_shares=[2, 1]
    )
)
rr.notebook_show(blueprint=blueprint)
```

### Real-time Data Streaming
```python
import rerun as rr

rr.init("my_app")
rr.notebook_show()

# Any subsequent rr.log() calls update the viewer immediately
for i in range(100):
    rr.set_time("frame", i)
    rr.log("points", rr.Points3D(generate_points(i)))
```

## Troubleshooting

### Common Issues

1. Module not found: Restart runtime after installing packages (especially in Colab)
2. Empty viewer: Check file paths and COLMAP data format
3. Performance issues: Use smaller image sizes with `resize` parameter
4. Path errors: Ensure paths exist and contain proper COLMAP files

### Performance Tips

- Use `resize=(640, 480)` for large images
- Set `unfiltered=False` to hide noisy points
- For huge datasets, process a subset first
- Close other tabs if memory becomes an issue

### File Format Support

The demo supports both binary and text COLMAP formats:
- Binary: `cameras.bin`, `images.bin`, `points3D.bin`
- Text: `cameras.txt`, `images.txt`, `points3D.txt`

## Google Colab Tips

1. Always restart runtime after installing packages
2. Upload your data to Colab or mount Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. Use smaller datasets due to memory limitations
4. Download results before session expires

## References

- https://rerun.io/docs/howto/integrations/embed-notebooks
- https://colmap.github.io/
- https://jupyter-notebook.readthedocs.io/

## Contributing

Feel free to improve this demo by:
- Adding more visualization options
- Improving error handling
- Adding support for additional COLMAP features
- Optimizing performance for large datasets

## License

This demo follows the same license as the main project. 