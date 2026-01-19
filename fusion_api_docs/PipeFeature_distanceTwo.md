# PipeFeature.distanceTwo Property

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Gets the distance for the pipe created while following the reversed path given as input.  

If the path is open, getting this value returns null, and setting the value is ignored. If the path is closed, this value returns the length of the Pipe from the start point going in the reverse order of the path. Ex: Path is made of curves A-B-C-A. The distanceTwo returns the length of the pipe going from A-C-B-A.  

This property returns null in the case where the feature is non-parametric.

## Syntax

"pipeFeature_var" is a variable referencing a PipeFeature object.  

```python
# Get the value of the property.
propertyValue = pipeFeature_var.distanceTwo
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version October 2023  

