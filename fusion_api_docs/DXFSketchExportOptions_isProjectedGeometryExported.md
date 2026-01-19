# DXFSketchExportOptions.isProjectedGeometryExported Property

Parent Object: [DXFSketchExportOptions](DXFSketchExportOptions.md)  

## Description

Indicates if any projected geometry should be exported. Defaults to true, which will export all projected geometry. If false it will be ignored and not included in the DXF file.

## Syntax

"dXFSketchExportOptions_var" is a variable referencing a DXFSketchExportOptions object.  

```python
# Get the value of the property.
propertyValue = dXFSketchExportOptions_var.isProjectedGeometryExported

# Set the value of the property.
dXFSketchExportOptions_var.isProjectedGeometryExported = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

