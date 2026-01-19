# C3MFExportOptions.isOneFilePerBody Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

If the input is an Occurrence or the root Component, this specifies if a single file should be created containing all of the bodies within that occurrence or component or if multiple files should be created; one for each body. If multiple files are created, the body name is appended to the filename. The default is false.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.isOneFilePerBody

# Set the value of the property.
c3MFExportOptions_var.isOneFilePerBody = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2021  

