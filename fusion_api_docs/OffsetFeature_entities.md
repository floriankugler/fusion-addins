# OffsetFeature.entities Property

Parent Object: [OffsetFeature](OffsetFeature.md)  

## Description

Gets and sets the faces to be offset.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"offsetFeature_var" is a variable referencing an OffsetFeature object.  

```python
# Get the value of the property.
propertyValue = offsetFeature_var.entities

# Set the value of the property.
offsetFeature_var.entities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

