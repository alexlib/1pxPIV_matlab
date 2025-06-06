#!/usr/bin/env python3
"""
Example script for PIV analysis using PIVSuite Python.

This script demonstrates how to use the PIVSuite Python package to analyze
a pair of PIV images and visualize the results.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add the parent directory to the path so we can import the pivsuite package
sys.path.append(str(Path(__file__).parent.parent))

from pivsuite.core import analyze_image_pair, piv_params
from pivsuite.visualization import quiver_plot, vector_plot, streamline_plot


def main():
    """Run the PIV analysis example."""
    print("\nRUNNING EXAMPLE_PIV_ANALYSIS...")
    
    # Define paths to images
    data_dir = Path(__file__).parent.parent.parent / "Data" / "Test PIVChallenge3A1"
    im1_path = str(data_dir / "A1000_a.tif")
    im2_path = str(data_dir / "A1000_b.tif")
    
    # Check if the image files exist
    if not os.path.exists(im1_path) or not os.path.exists(im2_path):
        print(f"Error: Image files not found. Please check the paths.")
        return
    
    print(f"Image paths:\n  {im1_path}\n  {im2_path}")
    
    # Set PIV parameters
    piv_par = {}
    piv_par = piv_params(None, piv_par, 'defaults')
    
    # Customize parameters
    piv_par['ia_size_x'] = [64, 32, 16]  # Interrogation area size in x
    piv_par['ia_size_y'] = [64, 32, 16]  # Interrogation area size in y
    piv_par['ia_step_x'] = [32, 16, 8]   # Interrogation area step in x
    piv_par['ia_step_y'] = [32, 16, 8]   # Interrogation area step in y
    piv_par['ia_method'] = 'defspline'   # Interrogation method ('basic', 'offset', 'defspline')
    piv_par['cc_window'] = 'welch'       # Window function for cross-correlation
    piv_par['vl_thresh'] = 2.0           # Threshold for median test
    piv_par['rp_method'] = 'linear'      # Method for replacing spurious vectors
    piv_par['sm_method'] = 'gaussian'    # Smoothing method
    piv_par['sm_sigma'] = 1.0            # Smoothing parameter
    
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Analyze image pair
    print("Analyzing image pair...")
    piv_data, _ = analyze_image_pair(im1_path, im2_path, None, piv_par)
    
    # Print some statistics
    print(f"Number of vectors: {piv_data['n']}")
    print(f"Number of masked vectors: {piv_data['masked_n']}")
    print(f"Number of spurious vectors: {piv_data['spurious_n']}")
    
    # Load the first image for background
    from skimage import io
    im1 = io.imread(im1_path)
    
    # Create quiver plot
    print("Creating quiver plot...")
    quiver_plot(
        piv_data,
        scale=1.0,
        skip=2,
        color='r',
        background_image=im1,
        title='PIV Velocity Field',
        output_path=str(output_dir / "piv_quiver_plot.png"),
        show=False
    )
    
    # Create vector plot of velocity magnitude
    print("Creating vector plot of velocity magnitude...")
    vector_plot(
        piv_data,
        component='magnitude',
        cmap='jet',
        title='PIV Velocity Magnitude',
        output_path=str(output_dir / "piv_velocity_magnitude.png"),
        show=False
    )
    
    # Create vector plot of vorticity
    print("Creating vector plot of vorticity...")
    vector_plot(
        piv_data,
        component='vorticity',
        cmap='RdBu_r',
        title='PIV Vorticity',
        output_path=str(output_dir / "piv_vorticity.png"),
        show=False
    )
    
    # Create streamline plot
    print("Creating streamline plot...")
    streamline_plot(
        piv_data,
        density=1.0,
        color='b',
        background_image=im1,
        title='PIV Streamlines',
        output_path=str(output_dir / "piv_streamlines.png"),
        show=False
    )
    
    print("All plots saved to the output directory.")
    print("EXAMPLE_PIV_ANALYSIS... FINISHED\n")


if __name__ == "__main__":
    main()
