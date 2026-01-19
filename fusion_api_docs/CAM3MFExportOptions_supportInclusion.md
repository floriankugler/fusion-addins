# CAM3MFExportOptions.supportInclusion Property

Parent Object: [CAM3MFExportOptions](CAM3MFExportOptions.md)  

## Description

Flag setting if support information should be included in the exported file. Includes both support structures marked as open or closed support as well as meta data used in Netfabb. This option might not be available for all machine types. The default value is NotIncluded.

## Syntax

"cAM3MFExportOptions_var" is a variable referencing a CAM3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = cAM3MFExportOptions_var.supportInclusion

# Set the value of the property.
cAM3MFExportOptions_var.supportInclusion = propertyValue
```

## Property Value

This is a read/write property whose value is a [CAM3MFSupportInclusionType](CAM3MFSupportInclusionType.md).

## Version

Introduced in version January 2024  

