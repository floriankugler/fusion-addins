# RuledSurfaceFeature.profile Property

Parent Object: [RuledSurfaceFeature](RuledSurfaceFeature.md)  

## Description

Gets and sets the Profile object that defines the sketch geometry or edges that define the shape of the ruled surface. The Component.createBRepEdgeProfile method is useful to create a profile defined from edges.  

In many cases the RuledSurface operation results in the profile being consumed so it is no longer available after the feature is created. In this case, you need to reposition the timeline marker to just before this feature, when the profile still exists.

## Syntax

"ruledSurfaceFeature_var" is a variable referencing a RuledSurfaceFeature object.  

```python
# Get the value of the property.
propertyValue = ruledSurfaceFeature_var.profile

# Set the value of the property.
ruledSurfaceFeature_var.profile = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version September 2020  

