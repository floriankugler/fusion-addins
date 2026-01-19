# ConstructionPlaneInput.setByAngle Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a construction plane through an edge, axis or line at a specified angle. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByAngle(linearEntity, angle, planarEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPlaneInput is successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| linearEntity | [Base](Base.md) | The axis about which to rotate the plane |
| angle | [ValueInput](ValueInput.md) | The angle at which to create the plane |
| planarEntity | [Base](Base.md) | The planar face or construction plane the angle is measured from. |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |

## Version

Introduced in version August 2014  

