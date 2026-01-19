# LoftFeature.operation Property

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Gets and sets the type of operation performed by the extrusion.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftFeature_var" is a variable referencing a LoftFeature object.  

```python
# Get the value of the property.
propertyValue = loftFeature_var.operation

# Set the value of the property.
loftFeature_var.operation = propertyValue
```

## Property Value

This is a read/write property whose value is a [FeatureOperations](FeatureOperations.md).

## Version

Introduced in version August 2016  

