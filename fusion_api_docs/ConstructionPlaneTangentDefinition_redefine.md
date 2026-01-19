# ConstructionPlaneTangentDefinition.redefine Method

Parent Object: [ConstructionPlaneTangentDefinition](ConstructionPlaneTangentDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneTangentDefinition_var" is a variable referencing a [ConstructionPlaneTangentDefinition](ConstructionPlaneTangentDefinition.md) object.

```python
returnValue = constructionPlaneTangentDefinition_var.redefine(angle, tangentFace, planarEntity)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if the redefinition of the plane is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| angle | [ValueInput](ValueInput.md) | A Value object that defines the angle of the construction plane |
| tangentFace | [Base](Base.md) | The cylindrical or conical face that the construction plane is tangent to. |
| planarEntity | [Base](Base.md) | The planar face or construction plane the angle for this construction plane is measured from |

## Version

Introduced in version August 2014  

