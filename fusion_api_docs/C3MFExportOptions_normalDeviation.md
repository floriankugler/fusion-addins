# C3MFExportOptions.normalDeviation Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Gets and sets the current normal deviation, or the angle the mesh normals at the vertices can deviate from the actual surface normals. This is defined in radians. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.normalDeviation

# Set the value of the property.
c3MFExportOptions_var.normalDeviation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2021  

