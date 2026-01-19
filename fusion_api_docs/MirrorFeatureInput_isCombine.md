# MirrorFeatureInput.isCombine Property

Parent Object: [MirrorFeatureInput](MirrorFeatureInput.md)  

## Description

Gets and sets whether the mirrored bodies should be combined with the original bodies. When true, the mirrored geometry will be Boolean unioned with the original solid or surface body(s) when they connect within the stitch tolerance defined with the stitchTolerance property. If the bodies cannot be unioned or stitched the result will be separate bodies. If any input object is not a body, then this setting is ignored. Default is false.

## Syntax

"mirrorFeatureInput_var" is a variable referencing a MirrorFeatureInput object.  

```python
# Get the value of the property.
propertyValue = mirrorFeatureInput_var.isCombine

# Set the value of the property.
mirrorFeatureInput_var.isCombine = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2020  

