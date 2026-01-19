# STLExportOptions.normalDeviation Property

Parent Object: [STLExportOptions](STLExportOptions.md)  

## Description

Gets and sets the current normal deviation, or the angle the mesh normals at the vertices can deviate from the actual surface normals. This is defined in radians. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"sTLExportOptions_var" is a variable referencing a STLExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTLExportOptions_var.normalDeviation

# Set the value of the property.
sTLExportOptions_var.normalDeviation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2015  

