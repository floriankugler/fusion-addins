# ConstructionPointThreePlanesDefinition.redefine Method

Parent Object: [ConstructionPointThreePlanesDefinition](ConstructionPointThreePlanesDefinition.md)  

## Description

Redefines the input geometry of the construction point.

## Syntax

"constructionPointThreePlanesDefinition_var" is a variable referencing a [ConstructionPointThreePlanesDefinition](ConstructionPointThreePlanesDefinition.md) object.

```python
returnValue = constructionPointThreePlanesDefinition_var.redefine(planeOne, planeTwo, planeThree)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the redefinition of the Construction Point is successful. |

## Parameters

| Name       | Type             | Description                                  |
|------------|------------------|----------------------------------------------|
| planeOne   | [Base](Base.md) | The first plane or planar face to intersect  |
| planeTwo   | [Base](Base.md) | The second plane or planar face to intersect |
| planeThree | [Base](Base.md) | The third plane or planar face to intersect  |

## Version

Introduced in version August 2014  

