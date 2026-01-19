# RemoveFeatures.add Method

Parent Object: [RemoveFeatures](RemoveFeatures.md)  

## Description

Creates a new Remove feature.

## Syntax

"removeFeatures_var" is a variable referencing a [RemoveFeatures](RemoveFeatures.md) object.

```python
returnValue = removeFeatures_var.add(itemToRemove)
```

## Return Value

| Type | Description |
|----|----|
| [RemoveFeature](RemoveFeature.md) | Returns the newly created RemoveFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| itemToRemove | [Base](Base.md) | A single body (solid or surface) or component occurrence to remove. |

## Samples

| Name | Description |
|----|----|
| [removeFeatures.add](removeFeatures_add_Sample.md) | Demonstrate the removeFeatures.add method. The Remove feature is the same as selecting a body in the browser and selecting "Remove" in the context menu. |
| [Remove Feature](RemoveFeatureSample_Sample.md) | Demonstrates creating a new remove feature. |

## Version

Introduced in version September 2015  

