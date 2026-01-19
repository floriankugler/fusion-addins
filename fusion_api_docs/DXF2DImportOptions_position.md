# DXF2DImportOptions.position Property

Parent Object: [DXF2DImportOptions](DXF2DImportOptions.md)  

## Description

Gets and sets the X,Y offset position for the origin of the imported DXF data relative to the sketch origin. This defaults to (0,0) in a newly created DXF2DImportOptions object.

## Syntax

"dXF2DImportOptions_var" is a variable referencing a DXF2DImportOptions object.  

```python
# Get the value of the property.
propertyValue = dXF2DImportOptions_var.position

# Set the value of the property.
dXF2DImportOptions_var.position = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point2D](Point2D.md).

## Version

Introduced in version November 2015  

