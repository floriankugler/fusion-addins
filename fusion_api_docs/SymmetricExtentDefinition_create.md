# SymmetricExtentDefinition.create Method

Parent Object: [SymmetricExtentDefinition](SymmetricExtentDefinition.md)  

## Description

Statically creates a new SymmetricExtentDefinition object. This is used as input when create a new feature and defining the starting condition.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.SymmetricExtentDefinition.create(distance, isFullLength)
```

## Return Value

| Type | Description |
|----|----|
| [SymmetricExtentDefinition](SymmetricExtentDefinition.md) | Returns the newly created SymmetricExtentDefinition or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| distance | [ValueInput](ValueInput.md) | An input ValueInput objects that defines either half the extent of the extrude or the full extent, depending on the value of the isFullLength argument. |
| isFullLength | boolean | An input boolean that specifies if the distance specified defines the full or half length of the extrusion. |

## Version

Introduced in version November 2016  

