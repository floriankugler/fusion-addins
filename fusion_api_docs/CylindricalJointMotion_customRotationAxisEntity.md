# CylindricalJointMotion.customRotationAxisEntity Property

Parent Object: [CylindricalJointMotion](CylindricalJointMotion.md)  

## Description

This property can be set using various types of entities that can infer an axis. For example, a linear edge, sketch line, planar face, and cylindrical face. This property is only valid in the case where the rotationAxis property returns CustomJointDirection. Setting this property will automatically set the rotationAxis property to CustomJointDirection.  

To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"cylindricalJointMotion_var" is a variable referencing a CylindricalJointMotion object.  

```python
# Get the value of the property.
propertyValue = cylindricalJointMotion_var.customRotationAxisEntity

# Set the value of the property.
cylindricalJointMotion_var.customRotationAxisEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

