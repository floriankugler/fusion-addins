# ShellFeatures.itemByName Method

Parent Object: [ShellFeatures](ShellFeatures.md)  

## Description

Function that returns the specified shell feature using the name of the feature.

## Syntax

"shellFeatures_var" is a variable referencing a [ShellFeatures](ShellFeatures.md) object.

```python
returnValue = shellFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ShellFeature](ShellFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

