# USDExportOptions.filename Property

Parent Object: [USDExportOptions](USDExportOptions.md)  

## Description

Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor.

## Syntax

"uSDExportOptions_var" is a variable referencing a USDExportOptions object.  

```python
# Get the value of the property.
propertyValue = uSDExportOptions_var.filename

# Set the value of the property.
uSDExportOptions_var.filename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version March 2022  

