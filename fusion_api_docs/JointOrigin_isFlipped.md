# JointOrigin.isFlipped Property

Parent Object: [JointOrigin](JointOrigin.md)  

## Description

Gets and sets if the joint origin direction is flipped or not.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: joint.timelineObject.rollTo(True)

## Syntax

"jointOrigin_var" is a variable referencing a JointOrigin object.  

```python
# Get the value of the property.
propertyValue = jointOrigin_var.isFlipped

# Set the value of the property.
jointOrigin_var.isFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2015  

