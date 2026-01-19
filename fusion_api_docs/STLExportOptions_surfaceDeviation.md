# STLExportOptions.surfaceDeviation Property

Parent Object: [STLExportOptions](STLExportOptions.md)  

## Description

Gets and sets the current surface deviation, or the distance the mesh can deviate from the actual surface. This is defined in centimeter. Setting this property will automatically set the meshRefinement to MeshRefinementCustom. The default is the value associated with medium mesh refinement.

## Syntax

"sTLExportOptions_var" is a variable referencing a STLExportOptions object.  

```python
# Get the value of the property.
propertyValue = sTLExportOptions_var.surfaceDeviation

# Set the value of the property.
sTLExportOptions_var.surfaceDeviation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2015  

