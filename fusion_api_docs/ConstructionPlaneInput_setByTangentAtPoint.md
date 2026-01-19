# ConstructionPlaneInput.setByTangentAtPoint Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a construction plane tangent to a face and aligned to a point. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByTangentAtPoint(tangentFace, pointEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPlaneInput is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tangentFace | [BRepFace](BRepFace.md) | A face to create the plane tangent to |
| pointEntity | [Base](Base.md) | A construction point, sketch point or vertex the tangent plane aligns to. This point need not lie on the tangent face. |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |

## Version

Introduced in version August 2014  

