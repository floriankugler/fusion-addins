# ConstructionPlaneMidplaneDefinition.redefine Method

Parent Object: [ConstructionPlaneMidplaneDefinition](ConstructionPlaneMidplaneDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneMidplaneDefinition_var" is a variable referencing a [ConstructionPlaneMidplaneDefinition](ConstructionPlaneMidplaneDefinition.md) object.

```python
returnValue = constructionPlaneMidplaneDefinition_var.redefine(planarEntityOne, planarEntityTwo)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if the redefinition of the plane is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntityOne | [Base](Base.md) | The first planar face or construction plane that defines this ConstructionPlane. |
| planarEntityTwo | [Base](Base.md) | The second planar face or construction plane that defines this ConstructionPlane. |

## Version

Introduced in version August 2014  

