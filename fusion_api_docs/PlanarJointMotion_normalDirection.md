# PlanarJointMotion.normalDirection Property

Parent Object: [PlanarJointMotion](PlanarJointMotion.md)  

## Description

Gets and sets the direction of the normal of the single degree of rotation. This can be set to XAxisJointDirection, YAxisJointDirection, or ZAxisJointDirection. It can return those three directions and CustomJointDirection. If this returns CustomJointDirection then the customNormalDirectionEntity will return an entity that defines the direction. If there is a custom direction defined and this property is set to one of the three standard axes, the custom direction will be removed and customNormalDirectionEntity will return null.

## Syntax

"planarJointMotion_var" is a variable referencing a PlanarJointMotion object.  

```python
# Get the value of the property.
propertyValue = planarJointMotion_var.normalDirection

# Set the value of the property.
planarJointMotion_var.normalDirection = propertyValue
```

## Property Value

This is a read/write property whose value is a [JointDirections](JointDirections.md).

## Version

Introduced in version July 2015  

