# OBJExportOptions.meshRefinement Property

Parent Object: [OBJExportOptions](OBJExportOptions.md)  

## Description

Gets and sets the current simple mesh refinement settings. Setting this property will reset the surfaceDeviation, normalDeviation, maximumEdgeLength, and aspectRatio to values that correspond to the specified mesh refinement. The default is MeshRefinementMedium.

## Syntax

"oBJExportOptions_var" is a variable referencing an OBJExportOptions object.  

```python
# Get the value of the property.
propertyValue = oBJExportOptions_var.meshRefinement

# Set the value of the property.
oBJExportOptions_var.meshRefinement = propertyValue
```

## Property Value

This is a read/write property whose value is a [MeshRefinementSettings](MeshRefinementSettings.md).

## Version

Introduced in version October 2022  

