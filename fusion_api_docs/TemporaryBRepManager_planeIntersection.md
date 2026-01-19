# TemporaryBRepManager.planeIntersection Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Calculates the intersection between the input body and plane and creates a wire body that represents the intersection curves.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.planeIntersection(body, plane)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns a BRepBody that contains a wire body that represents the intersection. |

## Parameters

| Name | Type | Description |
|----|----|----|
| body | [BRepBody](BRepBody.md) | The BRepBody to intersection. |
| plane | [Plane](Plane.md) | The geometry Plane to intersect with the body. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

