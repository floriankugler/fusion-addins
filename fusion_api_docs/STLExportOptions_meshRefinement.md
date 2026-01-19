# STLExportOptions.meshRefinement Property

Parent Object: [STLExportOptions](STLExportOptions.md)  

## Description

Gets and sets the current simple mesh refinement settings. Setting this property will reset the surfaceDeviation, normalDeviation, maximumEdgeLength, and aspectRatio to values that correspond to the specified mesh refinement. The default is MeshRefinementMedium.

## Syntax

"sTLExportOptions_var" is a variable referencing a STLExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTLExportOptions_var.meshRefinement

# Set the value of the property.
sTLExportOptions_var.meshRefinement = propertyValue
```

## Property Value

This is a read/write property whose value is a [MeshRefinementSettings](MeshRefinementSettings.md).

## Samples

| Name | Description |
|----|----|
| [Export to other formats API Sample](ExportToOtherFormats_Sample.md) | Demonstrates exporting the active design to IGES, STEP, SAT, SMT, F3D and STL formats. To run this sample, have a design open and run the script. It will write out the translated files to a temp directory, which will it show in a message box. |

## Version

Introduced in version January 2015  

