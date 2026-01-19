# ConstructionPlaneTangentAtPointDefinition.redefine Method

Parent Object: [ConstructionPlaneTangentAtPointDefinition](ConstructionPlaneTangentAtPointDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneTangentAtPointDefinition_var" is a variable referencing a [ConstructionPlaneTangentAtPointDefinition](ConstructionPlaneTangentAtPointDefinition.md) object.

```python
returnValue = constructionPlaneTangentAtPointDefinition_var.redefine(tangentFace, pointEntity)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if the redefinition of the plane is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tangentFace | [Base](Base.md) | The face to create the plane tangent to |
| pointEntity | [Base](Base.md) | The point (sketch point, vertex, construction point) used to align the plane. |

## Version

Introduced in version August 2014  

