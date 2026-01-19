# Joint.setAsRigidJointMotion Method

Parent Object: [Joint](Joint.md)  

## Description

Redefines the relationship between the two joint geometries as a rigid joint.  

This method will fail in the case where the jointType property returns InferredJointType.  

To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True)

## Syntax

"joint_var" is a variable referencing a [Joint](Joint.md) object.

```python
returnValue = joint_var.setAsRigidJointMotion()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Version

Introduced in version July 2015  

