# PipeFeature.distanceOne Property

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Gets the distance for the pipe created while following the path given as input, in the same order.  

If the path is open, this value returns the length of Pipe relative to the length of the path. If the path is closed, this value returns the length of the Pipe from the start point going along the curves. Ex: Path is made of curves A-B-C-A. The distanceOne returns the length of the pipe going from A-B-C-A.  

This property returns null in the case where the feature is non-parametric.

## Syntax

"pipeFeature_var" is a variable referencing a PipeFeature object.  

```python
# Get the value of the property.
propertyValue = pipeFeature_var.distanceOne
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version October 2023  

