# TimelineGroup.reorder Method

Parent Object: [TimelineGroup](TimelineGroup.md)  

## Description

Reorders this object to the position specified. The default value of -1 indicates the end of the timeline.

## Syntax

"timelineGroup_var" is a variable referencing a [TimelineGroup](TimelineGroup.md) object.

```python
# Uses no optional arguments.
returnValue = timelineGroup_var.reorder()

# Uses optional arguments.
returnValue = timelineGroup_var.reorder(beforeIndex)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the reorder operation was successful This method will fail and return false if this is a timelineGroup object and the group is expanded. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| beforeIndex | integer | The index number of the position in the timeline to place this object before This is an optional argument whose default value is -1. |

## Version

Introduced in version August 2014  

