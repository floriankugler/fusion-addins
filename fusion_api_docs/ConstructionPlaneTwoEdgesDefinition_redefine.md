# ConstructionPlaneTwoEdgesDefinition.redefine Method

Parent Object: [ConstructionPlaneTwoEdgesDefinition](ConstructionPlaneTwoEdgesDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneTwoEdgesDefinition_var" is a variable referencing a [ConstructionPlaneTwoEdgesDefinition](ConstructionPlaneTwoEdgesDefinition.md) object.

```python
returnValue = constructionPlaneTwoEdgesDefinition_var.redefine(linearEntityOne, linearEntityTwo)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| linearEntityOne | [Base](Base.md) | The first linear edge, construction line, or sketch line that defines the construction plane. |
| linearEntityTwo | [Base](Base.md) | The second linear edge, construction line, or sketch line that defines the construction plane. |

## Version

Introduced in version August 2014  

