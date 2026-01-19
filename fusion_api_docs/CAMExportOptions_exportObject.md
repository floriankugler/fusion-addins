# CAMExportOptions.exportObject Property

Parent Object: [CAMExportOptions](CAMExportOptions.md)  

## Description

The export object we want to export. Depending on the actual export option, this might be geometry, an operation or a setup.

## Syntax

"cAMExportOptions_var" is a variable referencing a CAMExportOptions object.  

```python
# Get the value of the property.
propertyValue = cAMExportOptions_var.exportObject

# Set the value of the property.
cAMExportOptions_var.exportObject = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2021  

