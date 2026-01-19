# PipeFeature.path Property

Parent Object: [PipeFeature](PipeFeature.md)  

## Description

Gets and sets the path to create the Pipe. This property returns null in the case where the feature is non-parametric. The path can be either closed (you can reach again the starting point by following the curves) or open (the starting point and end point are different in the path).  

The starting point of the Pipe will be the starting point of the first curve in the Path, regardless of it being open or closed. When the desired Pipe has a section that includes the starting point and the path is closed, the curves should be shifted in a circular pattern.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"pipeFeature_var" is a variable referencing a PipeFeature object.  

```python
# Get the value of the property.
propertyValue = pipeFeature_var.path

# Set the value of the property.
pipeFeature_var.path = propertyValue
```

## Property Value

This is a read/write property whose value is a [Path](Path.md).

## Version

Introduced in version October 2023  

