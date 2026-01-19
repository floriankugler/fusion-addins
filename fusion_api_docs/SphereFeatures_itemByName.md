# SphereFeatures.itemByName Method

Parent Object: [SphereFeatures](SphereFeatures.md)  

## Description

Function that returns the specified sphere feature using the name of the feature.

## Syntax

"sphereFeatures_var" is a variable referencing a [SphereFeatures](SphereFeatures.md) object.

```python
returnValue = sphereFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [SphereFeature](SphereFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

