# RevolveFeature.operation Property

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Gets and sets the type of operation performed by the revolve.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"revolveFeature_var" is a variable referencing a RevolveFeature object.  

```python
# Get the value of the property.
propertyValue = revolveFeature_var.operation

# Set the value of the property.
revolveFeature_var.operation = propertyValue
```

## Property Value

This is a read/write property whose value is a [FeatureOperations](FeatureOperations.md).

## Version

Introduced in version August 2014  

