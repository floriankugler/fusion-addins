# ConstructionAxisInput.setByCircularFace Method

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

This input method is for creating an axis coincident with the axis of a cylindrical, conical or torus face.  

This can result in a parametric or non-parametric construction axis depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionAxisInput_var" is a variable referencing a [ConstructionAxisInput](ConstructionAxisInput.md) object.

```python
returnValue = constructionAxisInput_var.setByCircularFace(circularFace)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionAxisInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| circularFace | [BRepFace](BRepFace.md) | The face from a cylinder, cone, or torus. |

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version August 2014  

