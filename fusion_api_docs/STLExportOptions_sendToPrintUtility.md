# STLExportOptions.sendToPrintUtility Property

Parent Object: [STLExportOptions](STLExportOptions.md)  

## Description

Gets and sets whether the created STL file will be sent to the print utility specified by the printUtility property. If this is false a filename must be defined.

## Syntax

"sTLExportOptions_var" is a variable referencing a STLExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTLExportOptions_var.sendToPrintUtility

# Set the value of the property.
sTLExportOptions_var.sendToPrintUtility = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [STLExport API Sample](STLExport_Sample.md) | Demonstrates how to export f3d to STL format. |

## Version

Introduced in version March 2015  

