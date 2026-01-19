# ConstructionAxisNormalToFaceAtPointDefinition.redefine Method

Parent Object: [ConstructionAxisNormalToFaceAtPointDefinition](ConstructionAxisNormalToFaceAtPointDefinition.md)  

## Description

Redefines the input geometry of the construction axis.

## Syntax

"constructionAxisNormalToFaceAtPointDefinition_var" is a variable referencing a [ConstructionAxisNormalToFaceAtPointDefinition](ConstructionAxisNormalToFaceAtPointDefinition.md) object.

```python
returnValue = constructionAxisNormalToFaceAtPointDefinition_var.redefine(face, pointEntity)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the redefinition of the construction axis is successful. |

## Parameters

| Name        | Type             | Description                       |
|-------------|------------------|-----------------------------------|
| face        | [Base](Base.md) | The face the axis is normal to    |
| pointEntity | [Base](Base.md) | The point that positions the axis |

## Version

Introduced in version August 2014  

