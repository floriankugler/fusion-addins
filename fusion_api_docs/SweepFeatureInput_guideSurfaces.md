# SweepFeatureInput.guideSurfaces Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the guide surfaces to create the sweep. This can be set to an empty array to remove the guide surfaces and have a single path sweep feature. By default connected faces that are tangent to any of the guide faces are set as guide faces. Use the isChainSelection property to disable the use of tangent faces.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.guideSurfaces

# Set the value of the property.
sweepFeatureInput_var.guideSurfaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version January 2024  

