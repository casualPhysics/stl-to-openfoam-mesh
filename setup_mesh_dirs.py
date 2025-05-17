import os
import shutil
from pathlib import Path
from generate_blockMeshDict import write_blockMeshDict
from generate_surfaceFeatureExtractDict import write_surfaceFeatureExtractDict
from generate_snappyHexMeshDict import generate_snappyHexMeshDict

def create_meshQualityDict(output_path):
    """
    Create the meshQualityDict file with default settings.
    
    Args:
        output_path (str): Path where to write the meshQualityDict file
    """
    meshQualityDict_content = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  4.0                                   |
|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      meshQualityDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
#includeEtc "caseDicts/meshQualityDict"
// ************************************************************************* //"""
    
    with open(output_path, 'w') as f:
        f.write(meshQualityDict_content)

def create_fvSolution(output_path):
    """
    Create the fvSolution file with default settings.
    
    Args:
        output_path (str): Path where to write the fvSolution file
    """
    fvSolution_content = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  4.0                                   |
|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSolution;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// ************************************************************************* //"""
    
    with open(output_path, 'w') as f:
        f.write(fvSolution_content)

def create_fvSchemes(output_path):
    """
    Create the fvSchemes file with default settings.
    
    Args:
        output_path (str): Path where to write the fvSchemes file
    """
    fvSchemes_content = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  4.0                                   |
|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      fvSchemes;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

gradSchemes
{
}

divSchemes
{
}

laplacianSchemes
{
}

// ************************************************************************* //"""
    
    with open(output_path, 'w') as f:
        f.write(fvSchemes_content)

def create_controlDict(output_path):
    """
    Create the controlDict file with default settings.
    
    Args:
        output_path (str): Path where to write the controlDict file
    """
    controlDict_content = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  4.0                                   |
|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      controlDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

//Just dummy entries, don't worry

application     icoFoam;

startFrom       startTime;

startTime       0;

stopAt          endTime;

endTime         50;

deltaT          1;

writeControl    timeStep;

writeInterval   20;

purgeWrite      0;

writeFormat     ascii;

writePrecision  6;

writeCompression uncompressed;

timeFormat      general;

timePrecision   6;

runTimeModifiable yes;


// ************************************************************************* //"""
    
    with open(output_path, 'w') as f:
        f.write(controlDict_content)

def setup_mesh_directories(geometry_dir='geometry', meshes_dir='meshes'):
    """
    Set up mesh directories and generate configuration files for each geometry subdirectory.
    
    Args:
        geometry_dir (str): Path to the geometry directory
        meshes_dir (str): Path to the meshes directory
    """
    # Create main meshes directory if it doesn't exist
    os.makedirs(meshes_dir, exist_ok=True)
    
    # Get all subdirectories in the geometry directory
    geometry_path = Path(geometry_dir)
    if not geometry_path.exists():
        raise ValueError(f"Geometry directory '{geometry_dir}' does not exist")
    
    # Process each subdirectory in geometry
    for geom_subdir in geometry_path.iterdir():
        if not geom_subdir.is_dir():
            continue
            
        print(f"\nProcessing geometry subdirectory: {geom_subdir.name}")
        
        # Create corresponding mesh directory structure
        mesh_subdir = Path(meshes_dir) / geom_subdir.name
        constant_dir = mesh_subdir / 'constant' / 'triSurface'
        system_dir = mesh_subdir / 'system'
        
        # Create directories
        os.makedirs(constant_dir, exist_ok=True)
        os.makedirs(system_dir, exist_ok=True)
        
        # Copy STL files to constant/triSurface
        stl_files = list(geom_subdir.glob('*.stl'))
        if not stl_files:
            print(f"Warning: No STL files found in {geom_subdir}")
            continue
            
        for stl_file in stl_files:
            shutil.copy2(stl_file, constant_dir)
            print(f"Copied {stl_file.name} to {constant_dir}")
        
        # Generate blockMeshDict
        blockMeshDict_path = system_dir / 'blockMeshDict'
        write_blockMeshDict(
            output_path=str(blockMeshDict_path),
            stl_dir=str(geom_subdir),
            padding=1.0,
            cells=(20, 20, 30)
        )
        print(f"Generated blockMeshDict in {system_dir}")
        
        # Generate surfaceFeatureExtractDict
        surfaceFeatureExtractDict_path = system_dir / 'surfaceFeatureExtractDict'
        write_surfaceFeatureExtractDict(
            output_path=str(surfaceFeatureExtractDict_path),
            stl_dir=str(geom_subdir)
        )
        print(f"Generated surfaceFeatureExtractDict in {system_dir}")
        
        # Create controlDict
        controlDict_path = system_dir / 'controlDict'
        create_controlDict(str(controlDict_path))
        print(f"Created controlDict in {system_dir}")
        
        # Generate snappyHexMeshDict
        snappyHexMeshDict_path = system_dir / 'snappyHexMeshDict'
        generate_snappyHexMeshDict(
            stl_dir=str(geom_subdir),
            output_path=str(snappyHexMeshDict_path)
        )
        print(f"Generated snappyHexMeshDict in {system_dir}")
        
        # Create fvSchemes
        fvSchemes_path = system_dir / 'fvSchemes'
        create_fvSchemes(str(fvSchemes_path))
        print(f"Created fvSchemes in {system_dir}")
        
        # Create fvSolution
        fvSolution_path = system_dir / 'fvSolution'
        create_fvSolution(str(fvSolution_path))
        print(f"Created fvSolution in {system_dir}")
        
        # Create meshQualityDict
        meshQualityDict_path = system_dir / 'meshQualityDict'
        create_meshQualityDict(str(meshQualityDict_path))
        print(f"Created meshQualityDict in {system_dir}")

if __name__ == "__main__":
    setup_mesh_directories() 