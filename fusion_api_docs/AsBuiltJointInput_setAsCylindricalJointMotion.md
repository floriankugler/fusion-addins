# AsBuiltJointInput.setAsCylindricalJointMotion Method

Parent Object: [AsBuiltJointInput](AsBuiltJointInput.md)  

## Description

Defines the relationship between the two joint geometries as a cylindrical joint.

## Syntax

"asBuiltJointInput_var" is a variable referencing an [AsBuiltJointInput](AsBuiltJointInput.md) object.

```python
# Uses no optional arguments.
returnValue = asBuiltJointInput_var.setAsCylindricalJointMotion(rotationAxis)

# Uses optional arguments.
returnValue = asBuiltJointInput_var.setAsCylindricalJointMotion(rotationAxis, customRotationAxisEntity)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| rotationAxis | [JointDirections](JointDirections.md) | Specifies which axis the rotation is around. If this is set to CustomJointDirection then the customRotationAxisEntity argument must also be provided. |
| customRotationAxisEntity | [Base](Base.md) | If the rotationAxis is customAxisEntity this argument is used to specify the entity that defines the custom axis of rotation. This can be several types of entities that an axis can be derived from. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2015  

