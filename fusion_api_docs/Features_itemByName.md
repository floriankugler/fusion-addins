# Features.itemByName Method

Parent Object: [Features](Features.md)  

## Description

Function that returns the specified feature using the name of the feature.

## Syntax

"features_var" is a variable referencing a [Features](Features.md) object.

```python
returnValue = features_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [Feature](Feature.md) | Returns the specified item or null if a feature matching the name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the same name seen in the timeline. |

## Version

Introduced in version September 2015  

