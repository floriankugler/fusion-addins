# AsBuiltJoint.setAsRigidJointMotion Method

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Redefines the relationship between the two joint geometries as a rigid joint.  

To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True)

## Syntax

"asBuiltJoint_var" is a variable referencing an [AsBuiltJoint](AsBuiltJoint.md) object.

```python
returnValue = asBuiltJoint_var.setAsRigidJointMotion()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Version

Introduced in version September 2015  

