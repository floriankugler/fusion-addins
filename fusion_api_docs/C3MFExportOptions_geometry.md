# C3MFExportOptions.geometry Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Specifies the geometry to export. This can be an Occurrence, or the root Component. For STL, OBJ, and 3MF export, it can be a BRepBody. For DXF export, it can be a sketch of flat pattern.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.geometry

# Set the value of the property.
c3MFExportOptions_var.geometry = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version September 2021  

