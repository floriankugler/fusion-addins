# TimelineGroup.name Property

Parent Object: [TimelineGroup](TimelineGroup.md)  

## Description

Gets and sets the name of this timeline object. This name is shared by the object the timeline object represents. For example, if the TimelineObject represents a Sketch and you change the name using the TimelineObject, the name of the sketch in the browser is also changed. The reverse is also true. Setting the name of an object; sketch, feature construction geometry, etc, will also change the name of the associated node in the timeline.

## Syntax

"timelineGroup_var" is a variable referencing a TimelineGroup object.  

```python
# Get the value of the property.
propertyValue = timelineGroup_var.name

# Set the value of the property.
timelineGroup_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2016  

