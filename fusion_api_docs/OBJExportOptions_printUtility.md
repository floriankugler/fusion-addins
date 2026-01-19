# OBJExportOptions.printUtility Property

Parent Object: [OBJExportOptions](OBJExportOptions.md)  

## Description

Specifies which print utility to use when opening the OBJ file if the sendToPrintUtility property is true. The value of this property can be one of the strings returned by the availalbePrintUtilities property, which will specify one of the known print utilities. You can also specify a custom print utility by specifying the full path to the print utility executable. The default value of this property is the last setting specified in the user-interface.

## Syntax

"oBJExportOptions_var" is a variable referencing an OBJExportOptions object.  

```python
# Get the value of the property.
propertyValue = oBJExportOptions_var.printUtility

# Set the value of the property.
oBJExportOptions_var.printUtility = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version October 2022  

