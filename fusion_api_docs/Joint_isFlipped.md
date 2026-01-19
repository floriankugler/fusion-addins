# Joint.isFlipped Property

Parent Object: [Joint](Joint.md)  

## Description

Gets and sets if the joint direction is flipped or not. This is effectively specifying if the third axis of the two input geometries is facing (false) or opposed (true).  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)  

The value of this property should be ignored in the case where the jointType property returns InferredJointType.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.isFlipped

# Set the value of the property.
joint_var.isFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version July 2015  

