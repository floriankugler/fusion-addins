# ConstructionPointTwoEdgesDefinition.redefine Method

Parent Object: [ConstructionPointTwoEdgesDefinition](ConstructionPointTwoEdgesDefinition.md)  

## Description

Redefines the input geometry of the construction point.

## Syntax

"constructionPointTwoEdgesDefinition_var" is a variable referencing a [ConstructionPointTwoEdgesDefinition](ConstructionPointTwoEdgesDefinition.md) object.

```python
returnValue = constructionPointTwoEdgesDefinition_var.redefine(edgeOne, edgeTwo)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the redefinition of the Construction Point is successful. |

## Parameters

| Name    | Type             | Description                          |
|---------|------------------|--------------------------------------|
| edgeOne | [Base](Base.md) | The first B-Rep edge or sketch line  |
| edgeTwo | [Base](Base.md) | The second B-Rep edge or sketch line |

## Version

Introduced in version August 2014  

