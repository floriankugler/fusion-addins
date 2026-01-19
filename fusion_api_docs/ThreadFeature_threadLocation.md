# ThreadFeature.threadLocation Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets and sets where the thread length is measured from. This property is only used in the case where the isFullLength property is false.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

If the thread feature is associated with a hole (the hole property is not null), this property will always return null and will always return LowEndThreadLocation and will fail if set.

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.threadLocation

# Set the value of the property.
threadFeature_var.threadLocation = propertyValue
```

## Property Value

This is a read/write property whose value is a [ThreadLocations](ThreadLocations.md).

## Version

Introduced in version January 2015  

