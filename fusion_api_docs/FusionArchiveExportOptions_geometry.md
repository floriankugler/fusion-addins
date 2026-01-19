# FusionArchiveExportOptions.geometry Property

Parent Object: [FusionArchiveExportOptions](FusionArchiveExportOptions.md)  

## Description

Specifies the geometry to export. This can be an Occurrence, or the root Component. For STL, OBJ, and 3MF export, it can be a BRepBody. For DXF export, it can be a sketch of flat pattern.

## Syntax

"fusionArchiveExportOptions_var" is a variable referencing a FusionArchiveExportOptions object.  

```python
# Get the value of the property.
propertyValue = fusionArchiveExportOptions_var.geometry

# Set the value of the property.
fusionArchiveExportOptions_var.geometry = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version June 2015  

