# CAM3MFExportOptions.isMachineInformationIncluded Property

Parent Object: [CAM3MFExportOptions](CAM3MFExportOptions.md)  

## Description

Flag toggling if machine information should be included in the exported file. The machine information is only compatible with Netfabb. This option might not be available for all machine types. The default value is false.

## Syntax

"cAM3MFExportOptions_var" is a variable referencing a CAM3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = cAM3MFExportOptions_var.isMachineInformationIncluded

# Set the value of the property.
cAM3MFExportOptions_var.isMachineInformationIncluded = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2021  

