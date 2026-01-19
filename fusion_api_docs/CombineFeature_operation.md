# CombineFeature.operation Property

Parent Object: [CombineFeature](CombineFeature.md)  

## Description

Gets and sets the type of operation performed by the combine. The valid values are JoinFeatureOperation, CutFeatureOperation and IntersectFeatureOperation.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"combineFeature_var" is a variable referencing a CombineFeature object.  

```python
# Get the value of the property.
propertyValue = combineFeature_var.operation

# Set the value of the property.
combineFeature_var.operation = propertyValue
```

## Property Value

This is a read/write property whose value is a [FeatureOperations](FeatureOperations.md).

## Version

Introduced in version November 2014  

