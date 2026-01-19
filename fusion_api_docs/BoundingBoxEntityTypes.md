# BoundingBoxEntityTypes Enumerator

## Description

Specifies the various types of entities that can be included in bounding box calculations. This is a bitwise friendly enum so types can be combined to specify more than one type.  

## Methods

| Name | Value | Description |
|----|----|----|
| AllEntitiesBoundingBoxEntityType | 0 | Will include all types of geometry in the calculation. |
| ConstructionBoundingBoxEntityType | 16 | Includes the visible portion of construction geometry in the bounding box calculation. |
| MeshBodyBoundingBoxEntityType | 4 | Includes mesh bodies in the bounding box calculation. |
| SketchBoundingBoxEntityType | 8 | Includes sketch geometry in the bounding box calculation. |
| SolidBRepBodyBoundingBoxEntityType | 1 | Includes Solid B-Rep bodies in the bounding box calculation. |
| SurfaceBodyBoundingBoxEntityType | 2 | Includes B-Rep bodies that are not watertight (surfaces) in the bounding box calculation. |

## Version

Introduced in version January 2024  

