# PipeFeatureInput.distanceOne Property

Parent Object: [PipeFeatureInput](PipeFeatureInput.md)  

## Description

Gets and sets the distance for the pipe created while following the path given as input, in the same order. This value defaults to 1.0 if not set.  

If the path is open, setting this to a value between 0.0 and 1.0 decides the length of the created Pipe. If the path is closed, setting this value should not be higher than 1.0 - distanceTwo. Ex: Path is made of curves A-B-C-A. The distanceOne returns and sets the length of the pipe going from A-B-C-A.  

This property returns null in the case where the feature is non-parametric.

## Syntax

"pipeFeatureInput_var" is a variable referencing a PipeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = pipeFeatureInput_var.distanceOne

# Set the value of the property.
pipeFeatureInput_var.distanceOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version October 2023  

