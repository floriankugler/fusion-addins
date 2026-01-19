# CylinderFeatures.item Method

Parent Object: [CylinderFeatures](CylinderFeatures.md)  

## Description

Function that returns the specified cylinder feature using an index into the collection.

## Syntax

"cylinderFeatures_var" is a variable referencing a [CylinderFeatures](CylinderFeatures.md) object.

```python
returnValue = cylinderFeatures_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [CylinderFeature](CylinderFeature.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version September 2015  

