# STLExportOptions.aspectRatio Property

Parent Object: [STLExportOptions](STLExportOptions.md)  

## Description

Gets and sets the minimum aspect ratio for that triangles that are generated for the mesh. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"sTLExportOptions_var" is a variable referencing a STLExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTLExportOptions_var.aspectRatio

# Set the value of the property.
sTLExportOptions_var.aspectRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2015  

