# RevoluteJointMotion.customRotationAxisEntity Property

Parent Object: [RevoluteJointMotion](RevoluteJointMotion.md)  

## Description

This property can be set using various types of entities that can infer an axis. For example, a linear edge, sketch line, planar face, and cylindrical face. This property is only valid in the case where the rotationAxis property returns CustomJointDirection. Setting this property will automatically set the rotationAxis property to CustomJointDirection.

## Syntax

"revoluteJointMotion_var" is a variable referencing a RevoluteJointMotion object.  

```python
# Get the value of the property.
propertyValue = revoluteJointMotion_var.customRotationAxisEntity

# Set the value of the property.
revoluteJointMotion_var.customRotationAxisEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2015  

