"""
DS9 Scripting with Python Subprocesses
======================================

A script to automate the creation of RGB composite images from astronomical surveys
using SAO DS9 and Python subprocesses.

Author: Akash Gupta
Date: 2024
"""

import pandas as pd
from decimal import Decimal
import subprocess
import time
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from PIL import Image


def format_coordinates(ra, dec):
    """Format coordinates for filename matching."""
    return f"{ra:f}{dec:+f}"


def create_ds9_command(exe_path, red_fits, green_fits, blue_fits, output_path):
    """Create DS9 command for RGB composite generation."""
    return [
        exe_path,
        '-rgb',
        '-fits', red_fits, '-scale', 'ZScale',
        '-rgb', 'channel', 'green',
        '-fits', green_fits, '-scale', 'ZScale',
        '-rgb', 'channel', 'blue',
        '-fits', blue_fits, '-scale', 'ZScale',
        '-zoom', 'to', 'fit',
        '-colorbar', 'no',
        '-export', output_path, '100'
    ]


def process_survey(aprg, base_path, ds9_exe, survey_config):
    """Process a single survey for all targets."""
    survey_name = survey_config['name']
    red_band = survey_config['red']
    green_band = survey_config['green']
    blue_band = survey_config['blue']
    output_dir = survey_config['output_dir']
    
    print(f"Processing {survey_name} survey...")
    
    for i in range(aprg.shape[0]):
        radec = format_coordinates(aprg['ra'][i], aprg['dec'][i])
        print(f"  Processing {i+1}/{aprg.shape[0]}: {radec}")
        
        # Construct file paths
        red_fits = f"{base_path}/{radec}/fc_{radec}_{red_band}_reproj.fits"
        green_fits = f"{base_path}/{radec}/fc_{radec}_{green_band}_reproj.fits"
        blue_fits = f"{base_path}/{radec}/fc_{radec}_{blue_band}_reproj.fits"
        output_path = f"{output_dir}/{radec}_{survey_name.lower()}.jpeg"
        
        # Create and execute DS9 command
        cmd = create_ds9_command(ds9_exe, red_fits, green_fits, blue_fits, output_path)
        
        try:
            ds9 = subprocess.Popen(cmd)
            time.sleep(5.0)
            ds9.terminate()
        except Exception as e:
            print(f"    Error processing {radec}: {e}")


def create_visualization_grid(aprg, image_dir, output_path, max_images=20):
    """Create a grid visualization of processed images."""
    n_rows = 4
    n_cols = 5
    max_images = min(max_images, n_rows * n_cols, aprg.shape[0])
    
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(25, 20))
    
    for i in range(max_images):
        size = 150 / 3600  # Size in degrees
        ra, dec = aprg['ra'][i], aprg['dec'][i]
        ra, dec = round(Decimal(ra), 6), round(Decimal(dec), 6)
        radec = format_coordinates(aprg['ra'][i], aprg['dec'][i])
        
        # Convert to galactic coordinates
        gc = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='fk5', unit='deg')
        l, b = gc.galactic.l.value, gc.galactic.b.value

        # Load and display image
        img_path = f'{image_dir}/{radec}_glimpse.jpeg'
        try:
            img = Image.open(img_path)
            row, col = divmod(i, n_cols)
            
            ax[row, col].imshow(img, extent=[
                l - size * 0.5, l + size * 0.5, 
                b - size * 0.5, b + size * 0.5
            ])
            ax[row, col].set_title(f'APRG {i+1} ({l:.4f}, {b:.4f})', fontsize=15)
            ax[row, col].set_xlabel('Galactic Longitude')
            ax[row, col].set_ylabel('Galactic Latitude')
            
        except FileNotFoundError:
            print(f"Image not found: {img_path}")
            ax[row, col].text(0.5, 0.5, 'Image\nNot Found', 
                            ha='center', va='center', transform=ax[row, col].transAxes)
    
    # Hide unused subplots
    for i in range(max_images, n_rows * n_cols):
        row, col = divmod(i, n_cols)
        ax[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """Main execution function."""
    # Configuration
    data_file = 'C:/Users/akash/Downloads/APRG_All-part1/coords.csv'
    base_path = 'C:/Users/akash/Downloads/APRG_All-part1'
    ds9_exe = 'C:\\SAOImageDS9\\ds9.exe'
    
    # Survey configurations
    surveys = {
        'glimpse': {
            'name': 'GLIMPSE',
            'red': 'spitzer_seipirac4(2.4)',
            'green': 'spitzer_seipirac2(2.4)',
            'blue': 'spitzer_seipirac1(2.4)',
            'output_dir': 'C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE'
        },
        'wise': {
            'name': 'WISE',
            'red': 'wise_4',
            'green': 'wise_2',
            'blue': 'wise_1',
            'output_dir': 'C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/WISE'
        },
        'twomass': {
            'name': '2MASS',
            'red': '2mass_k',
            'green': '2mass_h',
            'blue': '2mass_j',
            'output_dir': 'C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/2MASS'
        }
    }
    
    # Load data
    print("Loading coordinate data...")
    aprg = pd.read_csv(data_file)
    print(f"Loaded {aprg.shape[0]} targets")
    
    # Process each survey
    for survey_key, survey_config in surveys.items():
        process_survey(aprg, base_path, ds9_exe, survey_config)
    
    # Create visualization
    print("Creating visualization grid...")
    create_visualization_grid(
        aprg, 
        surveys['glimpse']['output_dir'],
        "C:/Users/akash/Desktop/MIROCLS/Three_Color_Images/GLIMPSE_APRG.pdf"
    )
    
    print("Processing complete!")


if __name__ == "__main__":
    main()
