# TimelineObject.index Property

Parent Object: [TimelineObject](TimelineObject.md)  

## Description

Returns the position of this item within the timeline where the first item has an index of 0.  

This property can return -1 in the two cases where this object is not currently represented in the timeline. The two cases are:  

1. When this is a TimelineGroup object and the group is expanded.  

2. When this object is part of a group and the group is collapsed.

## Syntax

"timelineObject_var" is a variable referencing a TimelineObject object.  

```python
# Get the value of the property.
propertyValue = timelineObject_var.index
```

## Property Value

This is a read only property whose value is an integer.

## Version

Introduced in version August 2014  

