import os
import shutil
from pathlib import Path
from generate_blockMeshDict import write_blockMeshDict
from generate_surfaceFeatureExtractDict import write_surfaceFeatureExtractDict

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

if __name__ == "__main__":
    setup_mesh_directories() 