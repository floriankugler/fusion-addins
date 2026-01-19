# JointOrigin.geometry Property

Parent Object: [JointOrigin](JointOrigin.md)  

## Description

Gets and sets the joint geometry for this joint origin input. This defines the location of the joint origin.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: joint.timelineObject.rollTo(True)

## Syntax

"jointOrigin_var" is a variable referencing a JointOrigin object.  

```python
# Get the value of the property.
propertyValue = jointOrigin_var.geometry

# Set the value of the property.
jointOrigin_var.geometry = propertyValue
```

## Property Value

This is a read/write property whose value is a [JointGeometry](JointGeometry.md).

## Version

Introduced in version September 2015  

