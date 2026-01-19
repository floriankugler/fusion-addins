# ConstructionPlaneOffsetDefinition.redefine Method

Parent Object: [ConstructionPlaneOffsetDefinition](ConstructionPlaneOffsetDefinition.md)  

## Description

Redefines the input geometry of the construction plane.

## Syntax

"constructionPlaneOffsetDefinition_var" is a variable referencing a [ConstructionPlaneOffsetDefinition](ConstructionPlaneOffsetDefinition.md) object.

```python
returnValue = constructionPlaneOffsetDefinition_var.redefine(offset, planarEntity)
```

## Return Value

| Type    | Description                                 |
|---------|---------------------------------------------|
| boolean | Returns true is the operation is successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| offset | [ValueInput](ValueInput.md) | ValueInput object that specifies the offset distance |
| planarEntity | [Base](Base.md) | A plane, planar face or construction plane from which to measure the offset from |

## Version

Introduced in version August 2014  

