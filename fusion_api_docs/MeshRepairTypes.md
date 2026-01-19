# MeshRepairTypes Enumerator

## Description

Specify the main repair type for the mesh. If RebuildMeshRepairType is chosen, other parameters can be set.  

## Methods

| Name | Value | Description |
|----|----|----|
| CloseHolesMeshRepairType | 0 | Simplest and fastest type of repair, only close holes and fix flipped triangles are used to fix the part. |
| RebuildMeshRepairType | 3 | Reconstructs the mesh body using one of 4 MeshRepairRebuildTypes. All inner structures are destroyed. |
| StitchAndRemoveMeshRepairType | 1 | Makes the same changes as CloseHolesMeshRepairType, and also stitches triangles, removes double triangles, removes degenerated faces, and removes tiny shells. |
| WrapMeshRepairType | 2 | Uses in addition to the methods in StitchAndRemoveMeshRepairType also the wrapped method. This methods takes time and removes internal structure. |

## Version

Introduced in version March 2024  

