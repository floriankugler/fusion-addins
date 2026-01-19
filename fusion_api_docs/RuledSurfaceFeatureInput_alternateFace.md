# RuledSurfaceFeatureInput.alternateFace Property

Parent Object: [RuledSurfaceFeatureInput](RuledSurfaceFeatureInput.md)  

## Description

Gets and sets if the other face is used for creation of the Ruled Surface. When creating a ruled surface using the edges of a solid or the interior edges of a surface the angle of the ruled surface is measured with respect to the face the selected edge is bounding. For a solid, or an interior edge on a surface, the edge connects to two faces. This setting toggles which of the two faces will be used for measuring the angle.

## Syntax

"ruledSurfaceFeatureInput_var" is a variable referencing a RuledSurfaceFeatureInput object.  

```python
# Get the value of the property.
propertyValue = ruledSurfaceFeatureInput_var.alternateFace

# Set the value of the property.
ruledSurfaceFeatureInput_var.alternateFace = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2020  

