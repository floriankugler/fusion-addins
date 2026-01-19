# JointOrigin.xAxisEntity Property

Parent Object: [JointOrigin](JointOrigin.md)  

## Description

Gets and sets the entity that defines the X axis direction. This defaults to null meaning the X axis is inferred from the input geometry.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: joint.timelineObject.rollTo(True)

## Syntax

"jointOrigin_var" is a variable referencing a JointOrigin object.  

```python
# Get the value of the property.
propertyValue = jointOrigin_var.xAxisEntity

# Set the value of the property.
jointOrigin_var.xAxisEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version September 2015  

