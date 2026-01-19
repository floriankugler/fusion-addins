# C3MFExportOptions.printUtility Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Specifies which print utility to use when opening the 3MF file if the sendToPrintUtility property is true. The value of this property can be one of the strings returned by the availalbePrintUtilities property, which will specify one of the know print utilities. You can also specify a custom print utility by specifying the full path to the print utility executable. The default value of this property is the last setting specified in the user-interface.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.printUtility

# Set the value of the property.
c3MFExportOptions_var.printUtility = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2021  

