# CAM3MFExportOptions.isSliceDataIncluded Property

Parent Object: [CAM3MFExportOptions](CAM3MFExportOptions.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Flag toggling if slice data which has been generated beforehand by generating the entire setup or the additive toolpath object should be included in the exported file. The default value is false.

## Syntax

"cAM3MFExportOptions_var" is a variable referencing a CAM3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = cAM3MFExportOptions_var.isSliceDataIncluded

# Set the value of the property.
cAM3MFExportOptions_var.isSliceDataIncluded = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2026  

