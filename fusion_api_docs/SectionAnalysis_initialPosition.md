# SectionAnalysis.initialPosition Property

Parent Object: [SectionAnalysis](SectionAnalysis.md)  

## Description

Returns the matrix that describes the initial position and orientation of the specified cut plane entity. Any additional offsets or rotations are defined by a transformation matrix that is applied to this initial position. That matrix can be obtained and set using the transform property.

## Syntax

"sectionAnalysis_var" is a variable referencing a SectionAnalysis object.  

```python
# Get the value of the property.
propertyValue = sectionAnalysis_var.initialPosition
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version April 2023  

