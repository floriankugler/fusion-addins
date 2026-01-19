# Joints.addInferredJoint Method

Parent Object: [Joints](Joints.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new inferred joint.

## Syntax

"joints_var" is a variable referencing a [Joints](Joints.md) object.

```python
returnValue = joints_var.addInferredJoint(input)
```

## Return Value

| Type | Description |
|----|----|
| [Joint](Joint.md) | Returns the newly created Joint or fails if there is bad input. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [InferredJointInput](InferredJointInput.md) | The InferredJointInput object that defines the pairs of geometry and other settings that Fusion will use to infer a joint from. An InferredJointInput object is created using the Joints.createInferredJointInput method. |

## Version

Introduced in version September 2025  

