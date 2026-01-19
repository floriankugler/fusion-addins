# Joints.createInferredJointInput Method

Parent Object: [Joints](Joints.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a joint input to define an inferred joint. Use functionality on the returned InferredJointInput to define the input needed to infer a joint.

## Syntax

"joints_var" is a variable referencing a [Joints](Joints.md) object.

```python
returnValue = joints_var.createInferredJointInput()
```

## Return Value

| Type | Description |
|----|----|
| [InferredJointInput](InferredJointInput.md) | Returns an InferredJointInput. |

## Version

Introduced in version September 2025  

