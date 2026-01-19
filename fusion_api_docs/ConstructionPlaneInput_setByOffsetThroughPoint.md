# ConstructionPlaneInput.setByOffsetThroughPoint Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

Defines a construction plane that is offset from a planar face or construction plane and whose offset distance is defined by a vertex, sketch point, or construction point where the plane passes through the point.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByOffsetThroughPoint(planarEntity, point)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if construction plane definition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | A planar BRepFace, ConstructionPlane, or Plane object that the new construction plane will be offset from. A Plane object is only valid in a direct-edit design or a base feature. In that case a non-parametric result is created. |
| point | [Base](Base.md) | A BRepVertex, SketchPoint, ConstructionPoint, or Point3D that defines the offset distance. A Point3D is only valid in a direct-edit design. In that case a non-parametric result is created. |

## Version

Introduced in version January 2025  

