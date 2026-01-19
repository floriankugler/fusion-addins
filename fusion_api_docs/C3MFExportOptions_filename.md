# C3MFExportOptions.filename Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.filename

# Set the value of the property.
c3MFExportOptions_var.filename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2021  

