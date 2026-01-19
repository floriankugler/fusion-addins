# AsBuiltJoints.add Method

Parent Object: [AsBuiltJoints](AsBuiltJoints.md)  

## Description

Creates a new as-built joint.

## Syntax

"asBuiltJoints_var" is a variable referencing an [AsBuiltJoints](AsBuiltJoints.md) object.

```python
returnValue = asBuiltJoints_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [AsBuiltJoint](AsBuiltJoint.md) | Returns the new AsBuiltJoint object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [AsBuiltJointInput](AsBuiltJointInput.md) | An AsBuiltJointInput object that was created using the AsBuiltJoints.createInput method and then fully defined using the properties and methods on the AsBuiltJointInput object. |

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |

## Version

Introduced in version September 2015  

