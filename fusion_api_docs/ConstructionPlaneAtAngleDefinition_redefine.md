# ConstructionPlaneAtAngleDefinition.redefine Method

Parent Object: [ConstructionPlaneAtAngleDefinition](ConstructionPlaneAtAngleDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneAtAngleDefinition_var" is a variable referencing a [ConstructionPlaneAtAngleDefinition](ConstructionPlaneAtAngleDefinition.md) object.

```python
returnValue = constructionPlaneAtAngleDefinition_var.redefine(angle, linearEntity, planarEntity)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if the redefinition of the plane is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| angle | [ValueInput](ValueInput.md) | A ValueInput object that defines the angle at which to create the construction plane |
| linearEntity | [Base](Base.md) | The linear edge, construction line, or sketch line that defines the axis of rotation to measure the angle about |
| planarEntity | [Base](Base.md) | A plane, planar face or construction plane the angle of the construction plane is measured from |

## Version

Introduced in version August 2014  

