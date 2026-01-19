# PipeFeatureInput.distanceTwo Property

Parent Object: [PipeFeatureInput](PipeFeatureInput.md)  

## Description

Gets and sets the distance for the pipe created while following the reversed path given as input. Before setting this value, distanceOne must be set.  

If the path is open, getting this value returns null, and setting the value is ignored. If the path is closed, setting this value should not be higher than 1.0 - distanceOne. Ex: Path is made of curves A-B-C-A. The distanceTwo returns and sets the length of the pipe going from A-C-B-A.  

This property returns null in the case where the feature is non-parametric.

## Syntax

"pipeFeatureInput_var" is a variable referencing a PipeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = pipeFeatureInput_var.distanceTwo

# Set the value of the property.
pipeFeatureInput_var.distanceTwo = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version October 2023  

