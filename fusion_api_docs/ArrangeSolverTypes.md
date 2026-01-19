# ArrangeSolverTypes Enumerator

## Description

Defines the different types of arrangement solvers that are supported.  

## Methods

| Name | Value | Description |
|----|----|----|
| Arrange2DRectangularSolverType | 1 | Rectangular 2D arrangement solver. This is an arrangement type where the rectangular bounding box of the component is used to calculate the arrangement, not the actual shape of the part. |
| Arrange2DTrueShapeSolverType | 0 | True Shape 2D arrangement solver. This is an arrangement type where the components are arranged on a plane so they fit tightly together honoring the arrangement definition. |
| Arrange3DSolverType | 2 | 3D arrangement solver. This is an arrangement type where the parts are arranged within a 3D rectangular volume where the bounding box of the parts is used to determine the size of the part. |

## Version

Introduced in version January 2025  

