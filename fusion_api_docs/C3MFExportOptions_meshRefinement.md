# C3MFExportOptions.meshRefinement Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Gets and sets the current simple mesh refinement settings. Setting this property will reset the surfaceDeviation, normalDeviation, maximumEdgeLength, and aspectRatio to values that correspond to the specified mesh refinement. The default is MeshRefinementMedium.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.meshRefinement

# Set the value of the property.
c3MFExportOptions_var.meshRefinement = propertyValue
```

## Property Value

This is a read/write property whose value is a [MeshRefinementSettings](MeshRefinementSettings.md).

## Version

Introduced in version September 2021  

