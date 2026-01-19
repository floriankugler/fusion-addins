# GraphOutputNodeTypes Enumerator

## Description

Types of graph output nodes for the main graph.  

## Methods

| Name | Value | Description |
|----|----|----|
| BoundarySDFOutputNodeType | 0 | Scalar. Distance field of the boundary object of the model. Only used in the primary graph. |
| CellLatticeShapeOutputNodeType | 6 | Scalar. Defines the shape of the volumetric lattice cell. Only used in the cell graph. |
| CellTextureShapeOutputNodeType | 7 | Scalar. Defines the shape of the volumetric texture cell. Only used in the cell graph. |
| ColorOutputNodeType | 2 | RGBA. The color of the model at all points within it. Only used in the primary graph. |
| LatticeCoordinatesOutputNodeType | 3 | Vector3. The coordinate system for the lattice cells. Mapping from the global xyz coordinates to lattice cell coordinates. Only used in the primary graph. |
| LatticeDensityOutputNodeType | 1 | Scalar. Density/solidity of the volumetric model lattice at all points within it. Only used in the primary graph. |
| TextureCoordinatesOutputNodeType | 5 | Vector3. The coordinate system for the volumetric texture cells. Mapping from the global xyz coordinates to texture cell coordinates. Only used in the primary graph. |
| TextureDensityOutputNodeType | 4 | Scalar. Strength of the volumetric model texture at all points within it. Only used in the primary graph. |

## Version

Introduced in version May 2025  

