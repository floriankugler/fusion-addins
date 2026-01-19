# STLExportOptions.isBinaryFormat Property

Parent Object: [STLExportOptions](STLExportOptions.md)  

## Description

Indicates if the STL file is to be an ASCII or binary STL format. The default is true.

## Syntax

"sTLExportOptions_var" is a variable referencing a STLExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTLExportOptions_var.isBinaryFormat

# Set the value of the property.
sTLExportOptions_var.isBinaryFormat = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |

## Version

Introduced in version January 2015  

