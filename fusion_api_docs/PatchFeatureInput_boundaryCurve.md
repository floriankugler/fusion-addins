# PatchFeatureInput.boundaryCurve Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

Gets and sets the input geometry that will be used to define the boundary. This can be a sketch profile, a single sketch curve, a single B-Rep edge, an ObjectCollection, or a Path object.  

If a single open sketch curve or B-Rep edge is input, Fusion will automatically find connected sketch curves or B-Rep edges to define a closed loop.  

If an ObjectCollection is used as input, it must be a set of curves that define a closed shape.  

If a Path is used as input, it must define a closed shape.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.boundaryCurve

# Set the value of the property.
patchFeatureInput_var.boundaryCurve = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2016  

