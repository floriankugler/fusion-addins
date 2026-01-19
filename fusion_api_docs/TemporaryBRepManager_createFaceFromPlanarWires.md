# TemporaryBRepManager.createFaceFromPlanarWires Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a body from multiple wires that all lie within the same plane. Multiple wires are used when creating a plane with interior holes. One wire defines the outer shape and the other wires define the interior loops of the created face.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createFaceFromPlanarWires(wireBodies)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns a BRepBody containing the created BRepFace object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| wireBodies | BRepBody\[\] | An array of bodies that contain planar wires. Each wire must be closed, they should not overlap, and they should all lie on the same plane. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

