# ConstructionAxisInput.setByNormalToFaceAtPoint Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method if for creating a construction axis normal to a specified face or sketch profile and that passes through a specified point. This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByNormalToFaceAtPoint(face, pointEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The face (BRepFace object) to create the axis normal to. |
| pointEntity | [Base](Base.md) | A construction point, sketch point or vertex the axis passes through. This point does not have to lie on the face. |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

