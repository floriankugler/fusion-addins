# OBJExportOptions.surfaceDeviation Property

Parent Object: [OBJExportOptions](OBJExportOptions.md)  

## Description

Gets and sets the current surface deviation, or the distance the mesh can deviate from the actual surface. This is defined in centimeter. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"oBJExportOptions_var" is a variable referencing an OBJExportOptions object.  

```python
# Get the value of the property.
propertyValue = oBJExportOptions_var.surfaceDeviation

# Set the value of the property.
oBJExportOptions_var.surfaceDeviation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version October 2022  

