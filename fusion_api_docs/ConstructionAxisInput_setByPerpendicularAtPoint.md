# ConstructionAxisInput.setByPerpendicularAtPoint Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method is for creating an axis that is normal to a face at a specified point.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByPerpendicularAtPoint(face, pointEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | A face (BRepFace object) to create the axis normal to. |
| pointEntity | [Base](Base.md) | A construction point, sketch point or vertex the axis is to pass through. |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

