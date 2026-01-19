# TriangleMeshCalculator.maxNormalDeviation Property

Parent Object: [TriangleMeshCalculator](TriangleMeshCalculator.md)  

## Description

Specifies the maximum deviation between adjacent vertex normals. This value is the maximum angle allowed between normals and is specified in radians. A value of 0 (the default) indicates that no normal deviation is specified.

## Syntax

"triangleMeshCalculator_var" is a variable referencing a TriangleMeshCalculator object.  

```python
# Get the value of the property.
propertyValue = triangleMeshCalculator_var.maxNormalDeviation

# Set the value of the property.
triangleMeshCalculator_var.maxNormalDeviation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

