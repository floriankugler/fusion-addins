# AsBuiltJoint.setAsRevoluteJointMotion Method

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Redefines the relationship between the two joint geometries as a revolute joint.  

To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True)

## Syntax

"asBuiltJoint_var" is a variable referencing an [AsBuiltJoint](AsBuiltJoint.md) object.

```python
# Uses no optional arguments.
returnValue = asBuiltJoint_var.setAsRevoluteJointMotion(rotationAxis)

# Uses optional arguments.
returnValue = asBuiltJoint_var.setAsRevoluteJointMotion(rotationAxis, geometry, customRotationAxisEntity)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| rotationAxis | [JointDirections](JointDirections.md) | Specifies which axis the rotation is around. If this is set to CustomJointDirection then the customRotationAxisEntity argument must also be provided. |
| geometry | [JointGeometry](JointGeometry.md) | Redefines the joint geometry. If not provided, the existing geometry is used. This argument is required if the current joint motion is rigid. This is an optional argument whose default value is null. |
| customRotationAxisEntity | [Base](Base.md) | If the rotationAxis is customAxisEntity this argument is used to specify the entity that defines the custom axis of rotation. This can be several types of entities that an axis can be derived from. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2015  

