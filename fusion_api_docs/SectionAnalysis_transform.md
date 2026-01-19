# SectionAnalysis.transform Property

Parent Object: [SectionAnalysis](SectionAnalysis.md)  

## Description

The initial position of the section plane is defined by the specified cut plane entity. Any offsets or rotations are defined by a transformation matrix that is applied to the initial position. This property allows you to get and set the transformation matrix.

## Syntax

"sectionAnalysis_var" is a variable referencing a SectionAnalysis object.  

```python
# Get the value of the property.
propertyValue = sectionAnalysis_var.transform

# Set the value of the property.
sectionAnalysis_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version April 2023  

