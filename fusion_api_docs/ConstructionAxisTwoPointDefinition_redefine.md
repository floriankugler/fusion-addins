# ConstructionAxisTwoPointDefinition.redefine Method

Parent Object: [ConstructionAxisTwoPointDefinition](ConstructionAxisTwoPointDefinition.md)  

## Description

Redefines the input geometry of the construction axis.

## Syntax

"constructionAxisTwoPointDefinition_var" is a variable referencing a [ConstructionAxisTwoPointDefinition](ConstructionAxisTwoPointDefinition.md) object.

```python
returnValue = constructionAxisTwoPointDefinition_var.redefine(pointEntityOne, pointEntityTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the redefinition of the construction axis is successful. |

## Parameters

| Name           | Type             | Description      |
|----------------|------------------|------------------|
| pointEntityOne | [Base](Base.md) | The first point  |
| pointEntityTwo | [Base](Base.md) | The second point |

## Version

Introduced in version August 2014  

