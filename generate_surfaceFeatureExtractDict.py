import os
from pathlib import Path

def generate_stl_section(stl_name):
    """
    Generate the section for a single STL file in surfaceFeatureExtractDict format.
    
    Args:
        stl_name (str): Name of the STL file
        
    Returns:
        str: Section for the STL file
    """
    return f"""{stl_name}
{{
    extractionMethod    extractFromSurface;

    extractFromSurfaceCoeffs
    {{
        includedAngle   180;
    }}

        writeObj                yes;
}}"""

def generate_surfaceFeatureExtractDict(stl_dir='geometry/basic_box'):
    """
    Generate a complete surfaceFeatureExtractDict file based on STL files.
    
    Args:
        stl_dir (str): Directory containing STL files
        
    Returns:
        str: Complete surfaceFeatureExtractDict content
    """
    # Get all STL files in the directory
    stl_files = list(Path(stl_dir).glob('*.stl'))
    
    if not stl_files:
        raise ValueError(f"No STL files found in {stl_dir}")
    
    # Generate sections for each STL file
    stl_sections = []
    for stl_file in stl_files:
        stl_sections.append(generate_stl_section(stl_file.name))
    
    # Combine all sections
    stl_content = "\n\n".join(stl_sections)
    
    # Generate the complete surfaceFeatureExtractDict content
    surfaceFeatureExtractDict_content = f"""/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      surfaceFeatureExtractDict;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

//JN: Here we define, which edges we want to use as features for the geometry. Usually we use all of them

{stl_content}

// ************************************************************************* //"""
    
    return surfaceFeatureExtractDict_content

def write_surfaceFeatureExtractDict(output_path='mesh/system/surfaceFeatureExtractDict', stl_dir='geometry/basic_box'):
    """
    Generate and write the surfaceFeatureExtractDict file.
    
    Args:
        output_path (str): Path where to write the surfaceFeatureExtractDict file
        stl_dir (str): Directory containing STL files
    """
    content = generate_surfaceFeatureExtractDict(stl_dir)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the file
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"surfaceFeatureExtractDict file has been written to: {output_path}")

if __name__ == "__main__":
    # Example usage
    write_surfaceFeatureExtractDict() 