# DXFFlatPatternExportOptions.convertToPolylineTolerance Property

Parent Object: [DXFFlatPatternExportOptions](DXFFlatPatternExportOptions.md)  

## Description

Specifies the tolerance when converting a spline to polylines. This value is only used when the isSplineConvertedToPolyline property is true and otherwise it is ignored. The units for this value are centimeters. Defaults to 0.01 cm.

## Syntax

"dXFFlatPatternExportOptions_var" is a variable referencing a DXFFlatPatternExportOptions object.  

```python
# Get the value of the property.
propertyValue = dXFFlatPatternExportOptions_var.convertToPolylineTolerance

# Set the value of the property.
dXFFlatPatternExportOptions_var.convertToPolylineTolerance = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version November 2022  

