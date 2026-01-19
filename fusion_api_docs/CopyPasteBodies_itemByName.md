# CopyPasteBodies.itemByName Method

Parent Object: [CopyPasteBodies](CopyPasteBodies.md)  

## Description

Function that returns the specified Copy/Paste Body feature using the name of the feature.

## Syntax

"copyPasteBodies_var" is a variable referencing a [CopyPasteBodies](CopyPasteBodies.md) object.

```python
returnValue = copyPasteBodies_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CopyPasteBody](CopyPasteBody.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version June 2017  

