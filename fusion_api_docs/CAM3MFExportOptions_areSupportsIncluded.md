# CAM3MFExportOptions.areSupportsIncluded Property

Parent Object: [CAM3MFExportOptions](CAM3MFExportOptions.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Flag toggling if support information should be included in the exported file. Includes both support structures marked as open or closed support as well as meta data used in Netfabb. This option might not be available for all machine types. The default value is false.

## Remarks

This property has been retired. Please use supportInclusion for setting how to include support.

## Syntax

"cAM3MFExportOptions_var" is a variable referencing a CAM3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = cAM3MFExportOptions_var.areSupportsIncluded

# Set the value of the property.
cAM3MFExportOptions_var.areSupportsIncluded = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2021  
Retired in version January 2024  

