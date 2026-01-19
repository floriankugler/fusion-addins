# ConstructionPlaneInput.setByThreePoints Method

Parent Object: [ConstructionPlaneInput](ConstructionPlaneInput.md)  

## Description

This input method is for creating a construction plane through three points that define a triangle. This can result in a parametric or non-parametric construction plane depending on whether the parent component is parametric or is a direct edit component.

## Syntax

"constructionPlaneInput_var" is a variable referencing a [ConstructionPlaneInput](ConstructionPlaneInput.md) object.

```python
returnValue = constructionPlaneInput_var.setByThreePoints(pointEntityOne, pointEntityTwo, pointEntityThree)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the creation of the ConstructionPlaneInput is successful. This will fail if the points do not form a triangle (no two points can be coincident and all three cannot be colinear). |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointEntityOne | [Base](Base.md) | The first construction point, sketch point or vertex in the triangle |
| pointEntityTwo | [Base](Base.md) | The second construction point, sketch point or vertex in the triangle |
| pointEntityThree | [Base](Base.md) | The third construction point, sketch point or vertex in the triangle |

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |

## Version

Introduced in version August 2014  

