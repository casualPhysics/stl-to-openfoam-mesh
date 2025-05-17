# OpenFOAM Mesh Generation Assistant

This tool helps automate the generation of OpenFOAM meshes from STL files.

## Setup

1. Place your STL files in a subdirectory under the `geometry` folder. For example:
   ```
   geometry/
   └── your_model/
       ├── part1.stl
       ├── part2.stl
       └── ...
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the setup script to generate the mesh directory structure:
   ```bash
   python mesh/setup_mesh_dirs.py
   ```
   This will create a `meshes` directory with subdirectories matching your geometry structure.

## Mesh Generation Steps

For each model in the `meshes` directory, follow these steps:

1. Navigate to the model's directory:
   ```bash
   cd meshes/your_model
   ```

2. Run the mesh generation commands in sequence:
   ```bash
   surfaceFeatureExtract
   blockMesh
   snappyHexMesh -overwrite
   ```

   These commands will:
   - Extract surface features from your STL files
   - Create the initial block mesh
   - Generate the final mesh using snappyHexMesh

3. You can then view the meshes in paraview by opening the foam.foam file. 

## Directory Structure

After running the setup script, you'll have:
```
meshes/
└── your_model/
    ├── foam.foam
    ├── constant/
    │   └── triSurface/
    │       └── [your STL files]
    └── system/
        ├── blockMeshDict
        ├── surfaceFeatureExtractDict
        ├── snappyHexMeshDict
        ├── controlDict
        ├── fvSchemes
        ├── fvSolution
        └── meshQualityDict
```

## Notes

- Make sure your STL files are in the correct units (meters)
- The mesh quality can be adjusted by modifying the parameters in `snappyHexMeshDict`
- If you need to regenerate the mesh, you can run `snappyHexMesh -overwrite` again
- The `-overwrite` flag ensures the previous mesh is replaced with the new one

## Troubleshooting

If you encounter issues:
1. Check that your STL files are valid and in the correct units
2. Verify that the `blockMeshDict` has appropriate dimensions for your geometry
3. Adjust the refinement settings in `snappyHexMeshDict` if needed
4. Check the OpenFOAM logs for specific error messages 