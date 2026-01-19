# ConstructionPlaneThreePointsDefinition.redefine Method

Parent Object: [ConstructionPlaneThreePointsDefinition](ConstructionPlaneThreePointsDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneThreePointsDefinition_var" is a variable referencing a [ConstructionPlaneThreePointsDefinition](ConstructionPlaneThreePointsDefinition.md) object.

```python
returnValue = constructionPlaneThreePointsDefinition_var.redefine(pointEntityOne, pointEntityTwo, pointEntityThree)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if the redefinition of the plane is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointEntityOne | [Base](Base.md) | Gets the first construction point, sketch point or vertex. |
| pointEntityTwo | [Base](Base.md) | Gets the second construction point, sketch point or vertex. |
| pointEntityThree | [Base](Base.md) | Gets the third construction point, sketch point or vertex. |

## Version

Introduced in version August 2014  

