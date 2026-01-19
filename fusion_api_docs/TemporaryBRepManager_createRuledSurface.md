# TemporaryBRepManager.createRuledSurface Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates a new body by creating a ruled surface between the two input wire bodies.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createRuledSurface(sectionOne, sectionTwo)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the created ruled surface as a BRepBody object. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sectionOne | [BRepWire](BRepWire.md) | BRepWire that defines the shape of the first section. |
| sectionTwo | [BRepWire](BRepWire.md) | BRepWire that defines the shape of the second section. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

