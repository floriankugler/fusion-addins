# ReplaceFaceFeature.targetFaces Property

Parent Object: [ReplaceFaceFeature](ReplaceFaceFeature.md)  

## Description

Gets and sets the entities that define the target faces. The new faces must completely intersect the part. The collection can contain the surface faces, surface bodies and construction planes.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"replaceFaceFeature_var" is a variable referencing a ReplaceFaceFeature object.  

```python
# Get the value of the property.
propertyValue = replaceFaceFeature_var.targetFaces

# Set the value of the property.
replaceFaceFeature_var.targetFaces = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version March 2015  

