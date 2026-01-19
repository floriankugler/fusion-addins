# C3MFExportOptions.surfaceDeviation Property

Parent Object: [C3MFExportOptions](C3MFExportOptions.md)  

## Description

Gets and sets the current surface deviation, or the distance the mesh can deviate from the actual surface. This is defined in centimeter. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"c3MFExportOptions_var" is a variable referencing a C3MFExportOptions object.  

```python
# Get the value of the property.
propertyValue = c3MFExportOptions_var.surfaceDeviation

# Set the value of the property.
c3MFExportOptions_var.surfaceDeviation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version September 2021  

