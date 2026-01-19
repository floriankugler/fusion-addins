# ExportOptions.filename Property

Parent Object: [ExportOptions](ExportOptions.md)  

## Description

Gets and sets the filename that the exported file will be written to. This can be empty in the case of STL export and sending the result to the mesh editor.

## Syntax

"exportOptions_var" is a variable referencing an ExportOptions object.  

```python
# Get the value of the property.
propertyValue = exportOptions_var.filename

# Set the value of the property.
exportOptions_var.filename = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2015  

