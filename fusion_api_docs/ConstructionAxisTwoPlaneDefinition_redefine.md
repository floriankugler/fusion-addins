# ConstructionAxisTwoPlaneDefinition.redefine Method

Parent Object: [ConstructionAxisTwoPlaneDefinition](ConstructionAxisTwoPlaneDefinition.md)  

## Description

Redefines the input geometry of the construction axis.

## Syntax

"constructionAxisTwoPlaneDefinition_var" is a variable referencing a [ConstructionAxisTwoPlaneDefinition](ConstructionAxisTwoPlaneDefinition.md) object.

```python
returnValue = constructionAxisTwoPlaneDefinition_var.redefine(planarEntityOne, planarEntityTwo)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the redefinition of the axis is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| planarEntityOne | [Base](Base.md) | The first planar face or construction plane |
| planarEntityTwo | [Base](Base.md) | The second planar face or construction plane |

## Version

Introduced in version August 2014  

