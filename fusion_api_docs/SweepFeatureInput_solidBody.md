# SweepFeatureInput.solidBody Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the BRepBody object to sweep. It must be a solid body. Setting this property results in the type being a single path sweep, and if the profile, guide path, or surface are set, they are set to null.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.solidBody

# Set the value of the property.
sweepFeatureInput_var.solidBody = propertyValue
```

## Property Value

This is a read/write property whose value is a [BRepBody](BRepBody.md).

## Version

Introduced in version May 2024  

