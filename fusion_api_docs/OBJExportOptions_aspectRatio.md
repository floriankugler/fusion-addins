# OBJExportOptions.aspectRatio Property

Parent Object: [OBJExportOptions](OBJExportOptions.md)  

## Description

Gets and sets the minimum aspect ratio for that triangles that are generated for the mesh. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"oBJExportOptions_var" is a variable referencing an OBJExportOptions object.  

```python
# Get the value of the property.
propertyValue = oBJExportOptions_var.aspectRatio

# Set the value of the property.
oBJExportOptions_var.aspectRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version October 2022  

