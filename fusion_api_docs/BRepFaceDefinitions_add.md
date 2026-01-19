# BRepFaceDefinitions.add Method

Parent Object: [BRepFaceDefinitions](BRepFaceDefinitions.md)  

## Description

Creates a new BrepFaceDefinition within the parent BRepShellDefinition object.

## Syntax

"bRepFaceDefinitions_var" is a variable referencing a [BRepFaceDefinitions](BRepFaceDefinitions.md) object.

```python
returnValue = bRepFaceDefinitions_var.add(surfaceGeometry, isParamReversed)
```

## Return Value

| Type | Description |
|----|----|
| [BRepFaceDefinition](BRepFaceDefinition.md) | Returns the newly created BRepFaceDefinition object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| surfaceGeometry | [Surface](Surface.md) | Input surface object that defines the geometry of the face. Valid objects for input are NurbsSurface, Cone, Cylinder, EllipticalCone, EllipticalCylinder, Plane, Sphere, and Torus. |
| isParamReversed | boolean | Input Boolean that indicates if the normal of this face is reversed with respect to the surface geometry associated with this face definition. |

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

