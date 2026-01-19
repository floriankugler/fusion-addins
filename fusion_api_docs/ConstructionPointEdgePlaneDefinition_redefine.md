# ConstructionPointEdgePlaneDefinition.redefine Method

Parent Object: [ConstructionPointEdgePlaneDefinition](ConstructionPointEdgePlaneDefinition.md)  

## Description

Redefines the input geometry of the construction point.

## Syntax

"constructionPointEdgePlaneDefinition_var" is a variable referencing a [ConstructionPointEdgePlaneDefinition](ConstructionPointEdgePlaneDefinition.md) object.

```python
returnValue = constructionPointEdgePlaneDefinition_var.redefine(edge, plane)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the redefinition of the Construction Point is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edge | [Base](Base.md) | A linear B-Rep edge, construction axis or sketch line. |
| plane | [Base](Base.md) | A plane, planar B-Rep face or construction plane. |

## Version

Introduced in version August 2014  

