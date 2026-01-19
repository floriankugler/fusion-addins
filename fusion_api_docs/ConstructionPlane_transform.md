# ConstructionPlane.transform Property

Parent Object: [ConstructionPlane](ConstructionPlane.md)  

## Description

Returns the current position and orientation of the construction plane as a matrix. For a parametric construction plane, this property is read-only. For a construction plane in a direct modeling model or in a base feature, this is read-write and can be used to reposition the constructions plane.

## Syntax

"constructionPlane_var" is a variable referencing a ConstructionPlane object.  

```python
# Get the value of the property.
propertyValue = constructionPlane_var.transform

# Set the value of the property.
constructionPlane_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version August 2016  

