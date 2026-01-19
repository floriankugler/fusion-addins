# MirrorFeature.patternComputeOption Property

Parent Object: [MirrorFeature](MirrorFeature.md)  

## Description

Gets and sets the compute option for this mirror feature. This property only applies when mirroring features and is ignored in the direct modeling environment.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"mirrorFeature_var" is a variable referencing a MirrorFeature object.  

```python
# Get the value of the property.
propertyValue = mirrorFeature_var.patternComputeOption

# Set the value of the property.
mirrorFeature_var.patternComputeOption = propertyValue
```

## Property Value

This is a read/write property whose value is a [PatternComputeOptions](PatternComputeOptions.md).

## Version

Introduced in version November 2015  

