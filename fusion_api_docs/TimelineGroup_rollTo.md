# TimelineGroup.rollTo Method

Parent Object: [TimelineGroup](TimelineGroup.md)  

## Description

Rolls the timeline by repositioning the marker to either before or after this object. This method will fail if this is a timelineGroup object and the group is expanded.

## Syntax

"timelineGroup_var" is a variable referencing a [TimelineGroup](TimelineGroup.md) object.

```python
returnValue = timelineGroup_var.rollTo(rollBefore)
```

## Return Value

| Type    | Description                             |
|---------|-----------------------------------------|
| boolean | Returns true if the move was successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| rollBefore | boolean | Set rollBefore to true to reposition the marker before this object or to false to reposition the marker after this object |

## Version

Introduced in version August 2014  

