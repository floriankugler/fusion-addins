# TimelineObject.isRolledBack Property

Parent Object: [TimelineObject](TimelineObject.md)  

## Description

Indicates if this item is currently not being computed because it has been rolled back.  

If this is a timelineGroup object and the group is expanded the value of this property should be ignored.

## Syntax

"timelineObject_var" is a variable referencing a TimelineObject object.  

```python
# Get the value of the property.
propertyValue = timelineObject_var.isRolledBack
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version August 2014  

