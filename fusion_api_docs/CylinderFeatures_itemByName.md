# CylinderFeatures.itemByName Method

Parent Object: [CylinderFeatures](CylinderFeatures.md)  

## Description

Function that returns the specified cylinder feature using the name of the feature.

## Syntax

"cylinderFeatures_var" is a variable referencing a [CylinderFeatures](CylinderFeatures.md) object.

```python
returnValue = cylinderFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CylinderFeature](CylinderFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

