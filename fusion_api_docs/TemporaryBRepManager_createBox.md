# TemporaryBRepManager.createBox Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a new temporary solid box BRepBody object.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createBox(box)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created temporary BRepBody object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| box | [OrientedBoundingBox3D](OrientedBoundingBox3D.md) | The OrientedBoundingBox3D object that defines the position, orientation, and size of the box to crate. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

