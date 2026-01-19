# StitchFeature.operation Property

Parent Object: [StitchFeature](StitchFeature.md)  

## Description

Gets and sets the feature operation to perform. This property value is ignored if the stitched result does not form a solid body.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"stitchFeature_var" is a variable referencing a StitchFeature object.  

```python
# Get the value of the property.
propertyValue = stitchFeature_var.operation

# Set the value of the property.
stitchFeature_var.operation = propertyValue
```

## Property Value

This is a read/write property whose value is a [FeatureOperations](FeatureOperations.md).

## Version

Introduced in version June 2015  

