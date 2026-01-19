# RuledSurfaceFeatureInput.direction Property

Parent Object: [RuledSurfaceFeatureInput](RuledSurfaceFeatureInput.md)  

## Description

Gets and sets the entity that defines the direction when the ruled surface type is DirectionRuledSurfaceType. The direction is specified by providing a linear or planar entity. For example, a linear edge, construction axis, planar face, or construction plane can be used as input.  

If this property is set when the ruledSurfaceType is not DirectionRuledSurfaceType, the type will automatically be changed to DirectionRuledSurfaceType. If you get this property when the direction is not DirectionRuledSurfaceType, it will return null.

## Syntax

"ruledSurfaceFeatureInput_var" is a variable referencing a RuledSurfaceFeatureInput object.  

```python
# Get the value of the property.
propertyValue = ruledSurfaceFeatureInput_var.direction

# Set the value of the property.
ruledSurfaceFeatureInput_var.direction = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version September 2020  

