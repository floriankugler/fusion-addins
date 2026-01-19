# TimelineGroup.entity Property

Parent Object: [TimelineGroup](TimelineGroup.md)  

## Description

Returns the entity associated with this timeline object. Edit operations can be performed by getting the object representing the associated entity and using the methods and properties on that entity to make changes.  

Returns null if this TimelineObject represents a TimelineGroup object, since it does not have an associated entity.

## Syntax

"timelineGroup_var" is a variable referencing a TimelineGroup object.  

```python
# Get the value of the property.
propertyValue = timelineGroup_var.entity
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

