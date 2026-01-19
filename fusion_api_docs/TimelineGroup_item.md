# TimelineGroup.item Method

Parent Object: [TimelineGroup](TimelineGroup.md)  

## Description

Function that returns the specified timeline object within the group using an index into the collection.

## Syntax

"timelineGroup_var" is a variable referencing a [TimelineGroup](TimelineGroup.md) object.

```python
returnValue = timelineGroup_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [TimelineObject](TimelineObject.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

