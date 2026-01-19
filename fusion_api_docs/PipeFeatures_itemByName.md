# PipeFeatures.itemByName Method

Parent Object: [PipeFeatures](PipeFeatures.md)  

## Description

Function that returns the specified Pipe feature using the name of the feature.

## Syntax

"pipeFeatures_var" is a variable referencing a [PipeFeatures](PipeFeatures.md) object.

```python
returnValue = pipeFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [PipeFeature](PipeFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

