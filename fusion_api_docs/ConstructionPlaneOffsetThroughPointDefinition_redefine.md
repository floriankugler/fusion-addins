# ConstructionPlaneOffsetThroughPointDefinition.redefine Method

Parent Object: [ConstructionPlaneOffsetThroughPointDefinition](ConstructionPlaneOffsetThroughPointDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneOffsetThroughPointDefinition_var" is a variable referencing a [ConstructionPlaneOffsetThroughPointDefinition](ConstructionPlaneOffsetThroughPointDefinition.md) object.

```python
returnValue = constructionPlaneOffsetThroughPointDefinition_var.redefine(planarEntity, point)
```

## Return Value

| Type    | Description                                 |
|---------|---------------------------------------------|
| boolean | Returns true is the operation is successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntity | [Base](Base.md) | A planar BRepFace or ConstructionPlane that the new construction plane will be offset from. |
| point | [Base](Base.md) | A BRepVertex, SketchPoint, or ConstructionPoint that defines the offset distance. |

## Version

Introduced in version January 2025  

