# C3MFExportOptions.aspectRatio Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Gets and sets the minimum aspect ratio for that triangles that are generated for the mesh. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.aspectRatio

# Set the value of the property.
c3MFExportOptions_var.aspectRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2021  

