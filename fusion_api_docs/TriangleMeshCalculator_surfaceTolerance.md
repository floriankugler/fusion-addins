# TriangleMeshCalculator.surfaceTolerance Property

Parent Object: [TriangleMeshCalculator](TriangleMeshCalculator.md)  

## Description

Specifies the maximum distance that the mesh can deviate from the smooth surface. The value is in centimeters. Smaller values can result in a much greater number of facets being returned and will require more processing time to calculate.

## Syntax

"triangleMeshCalculator_var" is a variable referencing a TriangleMeshCalculator object.  

```python
# Get the value of the property.
propertyValue = triangleMeshCalculator_var.surfaceTolerance

# Set the value of the property.
triangleMeshCalculator_var.surfaceTolerance = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

