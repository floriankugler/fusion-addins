# SweepFeature.guideSurfaces Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the guide surfaces to create the sweep. This can be set to an empty array to remove the guide surfaces and have a single path sweep feature. The isChainSelection property controls whether tangentially connected faces to the guide surfaces are also made guide surfaces.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.guideSurfaces

# Set the value of the property.
sweepFeature_var.guideSurfaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version January 2024  

