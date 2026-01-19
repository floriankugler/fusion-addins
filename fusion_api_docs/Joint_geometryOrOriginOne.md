# Joint.geometryOrOriginOne Property

Parent Object: [Joint](Joint.md)  

## Description

Gets and sets the first JointGeometry or JointOrigin for this joint.  

If the JointType is InferredJointType, this property will return null when queried and will fail if it set.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.geometryOrOriginOne

# Set the value of the property.
joint_var.geometryOrOriginOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

