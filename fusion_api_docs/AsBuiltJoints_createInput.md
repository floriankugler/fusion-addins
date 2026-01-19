# AsBuiltJoints.createInput Method

Parent Object: [AsBuiltJoints](AsBuiltJoints.md)  

## Description

Creates an AsBuiltJointInput object which is used to collect all of the information needed to create an as-built joint. This object is equivalent to the as-built joint dialog in the user-interface in that it doesn't represent an actual joint but just the information needed to create an as-built joint. Once this is fully defined the add method can be called, passing this object in to create the actual joint.

## Syntax

"asBuiltJoints_var" is a variable referencing an [AsBuiltJoints](AsBuiltJoints.md) object.

```python
returnValue = asBuiltJoints_var.createInput(occurrenceOne, occurrenceTwo, geometry)
```

## Return Value

| Type | Description |
|----|----|
| [AsBuiltJointInput](AsBuiltJointInput.md) | Returns the new AsBuiltJointInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrenceOne | [Occurrence](Occurrence.md) | Specifies the first of two occurrences the joint is between. |
| occurrenceTwo | [Occurrence](Occurrence.md) | Specifies the second of two occurrences the joint is between. |
| geometry | [JointGeometry](JointGeometry.md) | Specifies the geometry of where the joint will be positioned. If the as-built joint is a rigid joint, this argument should be null because no geometry is needed. |

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |

## Version

Introduced in version September 2015  

