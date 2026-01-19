# Joint.geometryOneTransform Property

Parent Object: [Joint](Joint.md)  

## Description

Returns the position and orientation of the joint geometry associated with the first occurrence. This is returned as a 3D matrix which provides the origin and the X, Y, and Z axis vectors of the coordinate system.  

This property is especially useful in cases where the JointGeometry cannot be obtained. This can happen when the model has been modified in a way where the geometry used to create the joint is no longer available.  

This property will return null in the case where the jointType property returns InferredJointType.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.geometryOneTransform
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version November 2024  

