import os
from pathlib import Path

def generate_snappyHexMeshDict(stl_dir='geometry/basic_box', output_path='mesh/system/snappyHexMeshDict'):
    """
    Generate a snappyHexMeshDict file based on STL files in the directory.
    
    Args:
        stl_dir (str): Directory containing STL files
        output_path (str): Path where to write the snappyHexMeshDict file
    """
    # Get all STL files in the directory
    stl_files = list(Path(stl_dir).glob('*.stl'))
    
    if not stl_files:
        raise ValueError(f"No STL files found in {stl_dir}")
    
    # Generate geometry section
    geometry_section = "geometry\n{\n"
    for stl_file in stl_files:
        stl_name = stl_file.stem
        geometry_section += f"""    {stl_file.name}
    {{
        type triSurfaceMesh;
        name {stl_name};
    }}
"""
    geometry_section += "};\n\n"
    
    # Generate features section
    features_section = "    features\n    (\n"
    for stl_file in stl_files:
        stl_name = stl_file.stem
        features_section += f"""        {{
            file "{stl_name}.eMesh";
            level 0;
        }}
"""
    features_section += "    );\n\n"
    
    # Generate refinementSurfaces section
    refinement_section = "    refinementSurfaces\n    {\n"
    for stl_file in stl_files:
        stl_name = stl_file.stem
        refinement_section += f"""        {stl_name}
        {{
            // Surface-wise min and max refinement level
            level (0 0);
        }}
"""
    refinement_section += "    }\n"
    
    # Generate the complete snappyHexMeshDict content
    snappyHexMeshDict_content = f"""/*--------------------------------*- C++ -*----------------------------------*\\
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
    object      snappyHexMeshDict;
}}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Which of the steps to run
castellatedMesh true;
snap            true;
addLayers       false;

{geometry_section}

// Settings for the castellatedMesh generation.
castellatedMeshControls
{{
    // Refinement parameters
    // ~~~~~~~~~~~~~~~~~~~~~

    maxLocalCells 100000;
    maxGlobalCells 2000000;
    minRefinementCells 0;
    nCellsBetweenLevels 10;

    // Explicit feature edge refinement
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{features_section}

    // Surface based refinement
    // ~~~~~~~~~~~~~~~~~~~~~~~~
{refinement_section}

    resolveFeatureAngle 30;

    // Region-wise refinement
    // ~~~~~~~~~~~~~~~~~~~~~~
    refinementRegions
    {{
    }}

    // Mesh selection
    // ~~~~~~~~~~~~~~
    locationInMesh (0 0 0);
    allowFreeStandingZoneFaces true;
}}

// Settings for the snapping.
snapControls
{{
    nSmoothPatch 3;
    tolerance 1.0;
    nSolveIter 300;
    nRelaxIter 5;

    // Feature snapping
    nFeatureSnapIter 10;
    implicitFeatureSnap false;
    explicitFeatureSnap true;
    multiRegionFeatureSnap true;
}}

// Settings for the layer addition.
addLayersControls
{{
    relativeSizes true;

    layers
    {{
        "flange_.*"
        {{
            nSurfaceLayers 1;
        }}
    }}

    expansionRatio 1.0;
    finalLayerThickness 0.3;
    minThickness 0.25;
    nGrow 0;

    // Advanced settings
    featureAngle 30;
    nRelaxIter 5;
    nSmoothSurfaceNormals 1;
    nSmoothNormals 3;
    nSmoothThickness 10;
    maxFaceThicknessRatio 0.5;
    maxThicknessToMedialRatio 0.3;
    minMedianAxisAngle 90;
    nBufferCellsNoExtrude 0;
    nLayerIter 50;
    nRelaxedIter 20;
}}

// Generic mesh quality settings
meshQualityControls
{{
    #include "meshQualityDict"

    relaxed
    {{
        maxNonOrtho 75;
    }}

    nSmoothScale 4;
    errorReduction 0.75;
}}

// Advanced
writeFlags
(
    scalarLevels
    layerSets
    layerFields
);

mergeTolerance 1E-6;

// ************************************************************************* //"""
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the file
    with open(output_path, 'w') as f:
        f.write(snappyHexMeshDict_content)
    
    print(f"snappyHexMeshDict file has been written to: {output_path}")

if __name__ == "__main__":
    generate_snappyHexMeshDict() 