# DXF2DImportOptions.isViewFit Property

Parent Object: [DXF2DImportOptions](DXF2DImportOptions.md)  

## Description

Specifies if the camera should be adjusted to fit the geometry of the import. This defaults to true, which will cause a change in the current view. Setting this to false will leave the view as-is and just import the geometry.

## Syntax

"dXF2DImportOptions_var" is a variable referencing a DXF2DImportOptions object.  

```python
# Get the value of the property.
propertyValue = dXF2DImportOptions_var.isViewFit

# Set the value of the property.
dXF2DImportOptions_var.isViewFit = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2017  

