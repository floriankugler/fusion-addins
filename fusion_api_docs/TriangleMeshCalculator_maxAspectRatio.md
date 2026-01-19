# TriangleMeshCalculator.maxAspectRatio Property

Parent Object: [TriangleMeshCalculator](TriangleMeshCalculator.md)  

## Description

Specifies the maximum length to height ratio that a triangle can have. This helps to avoid long skinny triangles. A value of 0 (the default) indicates that no maximum aspect ratio is specified.

## Syntax

"triangleMeshCalculator_var" is a variable referencing a TriangleMeshCalculator object.  

```python
# Get the value of the property.
propertyValue = triangleMeshCalculator_var.maxAspectRatio

# Set the value of the property.
triangleMeshCalculator_var.maxAspectRatio = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

