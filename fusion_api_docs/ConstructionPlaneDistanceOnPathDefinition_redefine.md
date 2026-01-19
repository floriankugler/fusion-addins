# ConstructionPlaneDistanceOnPathDefinition.redefine Method

Parent Object: [ConstructionPlaneDistanceOnPathDefinition](ConstructionPlaneDistanceOnPathDefinition.md)  

## Description

Redefines the input defining the construction plane.

## Syntax

"constructionPlaneDistanceOnPathDefinition_var" is a variable referencing a [ConstructionPlaneDistanceOnPathDefinition](ConstructionPlaneDistanceOnPathDefinition.md) object.

```python
returnValue = constructionPlaneDistanceOnPathDefinition_var.redefine(pathEntity, distance)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if the redefinition of the plane is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pathEntity | [Base](Base.md) | The sketch curve, edge, or a profile object |
| distance | [ValueInput](ValueInput.md) | The ValueInput object that defines the distance along the path |

## Version

Introduced in version August 2014  

