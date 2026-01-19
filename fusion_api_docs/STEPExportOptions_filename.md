# STEPExportOptions.filename Property

Parent Object: [STEPExportOptions](STEPExportOptions.md)  

## Description

Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor.

## Syntax

"sTEPExportOptions_var" is a variable referencing a STEPExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTEPExportOptions_var.filename

# Set the value of the property.
sTEPExportOptions_var.filename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2015  

