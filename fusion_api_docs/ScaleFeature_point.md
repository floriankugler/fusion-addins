# ScaleFeature.point Property

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Gets and sets the point as reference to scale. This can be a BRepVertex, a SketchPoint or a ConstructionPoint.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"scaleFeature_var" is a variable referencing a ScaleFeature object.  

```python
# Get the value of the property.
propertyValue = scaleFeature_var.point

# Set the value of the property.
scaleFeature_var.point = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version January 2015  

