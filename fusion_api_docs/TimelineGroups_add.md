# TimelineGroups.add Method

Parent Object: [TimelineGroups](TimelineGroups.md)  

## Description

Creates a new group within the timeline. The sequential set of items defined by the start and end indices will be included in the group. A group cannot contains another group so none of the items being grouped can be a group of this will fail.

## Syntax

"timelineGroups_var" is a variable referencing a [TimelineGroups](TimelineGroups.md) object.

```python
returnValue = timelineGroups_var.add(startIndex, endIndex)
```

## Return Value

| Type | Description |
|----|----|
| [TimelineGroup](TimelineGroup.md) | Returns the created TimelineGroup object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startIndex | integer | The index of the first item in the timeline that will be added to the group. |
| endIndex | integer | The index of the last item in the timeline that will be added to the group. |

## Version

Introduced in version August 2014  

