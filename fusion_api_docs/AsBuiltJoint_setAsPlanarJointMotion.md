# AsBuiltJoint.setAsPlanarJointMotion Method

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Redefines the relationship between the two joint geometries as a planar joint.  

To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True)

## Syntax

"asBuiltJoint_var" is a variable referencing an [AsBuiltJoint](AsBuiltJoint.md) object.

```python
# Uses no optional arguments.
returnValue = asBuiltJoint_var.setAsPlanarJointMotion(normalDirection)

# Uses optional arguments.
returnValue = asBuiltJoint_var.setAsPlanarJointMotion(normalDirection, geometry, customNormalDirectionEntity, customPrimarySlideDirection)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| normalDirection | [JointDirections](JointDirections.md) | Defines the direction of the normal of the single degree of rotation. This can be set to XAxisJointDirection, YAxisJointDirection, ZAxisJointDirection, or CustomJointDirection. If set to CustomJointDirection then the customNormalDirectionEntity argument must also be provided. |
| geometry | [JointGeometry](JointGeometry.md) | Redefines the joint geometry. If not provided, the existing geometry is used. This argument is required if the current joint motion is rigid. This is an optional argument whose default value is null. |
| customNormalDirectionEntity | [Base](Base.md) | If the normalDirection is CustomJointDirection this argument is used to specify the entity that defines the direction of the normal. This can be several types of entities that can define a direction. This is an optional argument whose default value is null. |
| customPrimarySlideDirection | [Base](Base.md) | This arguments defines the direction of the primary slide direction. A default primary slide direction is automatically chosen and will be used if this argument is not provided or is null. The secondary slide direction is automatically inferred from the normal and primary slide directions. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2015  

