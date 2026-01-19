# CutPasteBodies.itemByName Method

Parent Object: [CutPasteBodies](CutPasteBodies.md)  

## Description

Function that returns the specified Cut/Paste Body feature using the name of the feature.

## Syntax

"cutPasteBodies_var" is a variable referencing a [CutPasteBodies](CutPasteBodies.md) object.

```python
returnValue = cutPasteBodies_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CutPasteBody](CutPasteBody.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version June 2017  

