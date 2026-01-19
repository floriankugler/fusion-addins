# TimelineObject.canReorder Method

Parent Object: [TimelineObject](TimelineObject.md)  

## Description

Checks to see if this object can be reordered to the specified position. The default value of -1 indicates the end of the timeline.  

This method will fail if this is a timelineGroup object and the group is expanded.

## Syntax

"timelineObject_var" is a variable referencing a [TimelineObject](TimelineObject.md) object.

```python
# Uses no optional arguments.
returnValue = timelineObject_var.canReorder()

# Uses optional arguments.
returnValue = timelineObject_var.canReorder(beforeIndex)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the object can be reordered to the specified position |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| beforeIndex | integer | The index number of the position in the timeline to check This is an optional argument whose default value is -1. |

## Version

Introduced in version August 2014  

