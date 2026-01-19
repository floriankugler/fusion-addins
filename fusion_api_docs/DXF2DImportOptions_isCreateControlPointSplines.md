# DXF2DImportOptions.isCreateControlPointSplines Property

Parent Object: [DXF2DImportOptions](DXF2DImportOptions.md)  

## Description

When set to true, if there are any splines in the DXF they will be created as control point splines. Otherwise they will be created as fixed splines that cannot be edited. The default for this property is false, to create fixed splines.

## Syntax

"dXF2DImportOptions_var" is a variable referencing a DXF2DImportOptions object.  

```python
# Get the value of the property.
propertyValue = dXF2DImportOptions_var.isCreateControlPointSplines

# Set the value of the property.
dXF2DImportOptions_var.isCreateControlPointSplines = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2022  

