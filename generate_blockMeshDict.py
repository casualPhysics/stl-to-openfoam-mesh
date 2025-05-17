import numpy as np
from stl import mesh
import os
from pathlib import Path

def get_stl_bounding_box(stl_dir='geometry/basic_box', padding=1.0):
    """
    Calculate the bounding box that envelopes all STL files in the specified directory
    with additional padding.
    
    Args:
        stl_dir (str): Directory containing STL files
        padding (float): Padding to add to the bounding box in all directions
        
    Returns:
        tuple: (min_coords, max_coords) where each is a numpy array of [x, y, z]
    """
    # Initialize min and max coordinates
    min_coords = np.array([float('inf'), float('inf'), float('inf')])
    max_coords = np.array([float('-inf'), float('-inf'), float('-inf')])
    
    # Get all STL files in the directory
    stl_files = list(Path(stl_dir).glob('*.stl'))
    
    if not stl_files:
        raise ValueError(f"No STL files found in {stl_dir}")
    
    # Process each STL file
    for stl_file in stl_files:
        # Read the STL file
        stl_mesh = mesh.Mesh.from_file(str(stl_file))
        
        # Get the min and max coordinates for this mesh
        min_coords = np.minimum(min_coords, stl_mesh.vectors.min(axis=(0, 1)))
        max_coords = np.maximum(max_coords, stl_mesh.vectors.max(axis=(0, 1)))
    
    # Add padding
    min_coords -= padding
    max_coords += padding
    
    return min_coords, max_coords

def generate_blockMeshDict(stl_dir='geometry/basic_box', padding=1.0, cells=(20, 20, 30)):
    """
    Generate a complete blockMeshDict file based on STL files.
    
    Args:
        stl_dir (str): Directory containing STL files
        padding (float): Padding to add to the bounding box in all directions
        cells (tuple): Number of cells in x, y, z directions
        
    Returns:
        str: Complete blockMeshDict content
    """
    min_coords, max_coords = get_stl_bounding_box(stl_dir, padding)
    
    # Format the vertices
    vertices_str = f"""    ( {min_coords[0]:.1f} {min_coords[1]:.1f} {min_coords[2]:.1f})
    ( {max_coords[0]:.1f} {min_coords[1]:.1f} {min_coords[2]:.1f})
    ( {max_coords[0]:.1f} {max_coords[1]:.1f} {min_coords[2]:.1f})
    ( {min_coords[0]:.1f} {max_coords[1]:.1f} {min_coords[2]:.1f})
    ( {min_coords[0]:.1f} {min_coords[1]:.1f} {max_coords[2]:.1f})
    ( {max_coords[0]:.1f} {min_coords[1]:.1f} {max_coords[2]:.1f})
    ( {max_coords[0]:.1f} {max_coords[1]:.1f} {max_coords[2]:.1f})
    ( {min_coords[0]:.1f} {max_coords[1]:.1f} {max_coords[2]:.1f})"""

    # Generate the complete blockMeshDict content
    blockMeshDict_content = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  4.0                                   |
|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

convertToMeters 1;

//These vertices define the block below. It envelopes the stl files. The block can be even bigger than the stl files
//Watch out if the stl files are created in mm or m!

vertices
(
{vertices_str}
);

blocks
(
    hex (0 1 2 3 4 5 6 7) ({cells[0]} {cells[1]} {cells[2]}) simpleGrading (1 1 1)//coarse grid - we will refine in snappyHexMeshDict
);

edges
(
);

boundary
(
    allBoundary//Don't worry about these settings
    {{
        type patch;
        faces
        (
            (3 7 6 2)
            (0 4 7 3)
            (2 6 5 1)
            (1 5 4 0)
            (0 3 2 1)
            (4 5 6 7)
        );
    }}
);

// ************************************************************************* //"""
    
    return blockMeshDict_content

def write_blockMeshDict(output_path='mesh/system/blockMeshDict', stl_dir='geometry/basic_box', padding=1.0, cells=(20, 20, 30)):
    """
    Generate and write the blockMeshDict file.
    
    Args:
        output_path (str): Path where to write the blockMeshDict file
        stl_dir (str): Directory containing STL files
        padding (float): Padding to add to the bounding box in all directions
        cells (tuple): Number of cells in x, y, z directions
    """
    content = generate_blockMeshDict(stl_dir, padding, cells)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the file
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"blockMeshDict file has been written to: {output_path}")

if __name__ == "__main__":
    # Example usage
    write_blockMeshDict() 