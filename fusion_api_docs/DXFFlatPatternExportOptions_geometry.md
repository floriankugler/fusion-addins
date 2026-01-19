# DXFFlatPatternExportOptions.geometry Property

Parent Object: [DXFFlatPatternExportOptions](DXFFlatPatternExportOptions.md)  

## Description

Specifies the geometry to export. This can be an Occurrence, or the root Component. For STL, OBJ, and 3MF export, it can be a BRepBody. For DXF export, it can be a sketch of flat pattern.

## Syntax

"dXFFlatPatternExportOptions_var" is a variable referencing a DXFFlatPatternExportOptions object.  

```python
# Get the value of the property.
propertyValue = dXFFlatPatternExportOptions_var.geometry

# Set the value of the property.
dXFFlatPatternExportOptions_var.geometry = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2022  

