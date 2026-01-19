# SectionAnalysisInput.initialPosition Property

Parent Object: [SectionAnalysisInput](SectionAnalysisInput.md)  

## Description

Returns the matrix that describes the initial position and orientation of the specified cut plane entity. Any additional offsets or rotations are defined by a transformation matrix that is applied to this initial position matrix. That matrix is obtained and set using the transform property.

## Syntax

"sectionAnalysisInput_var" is a variable referencing a SectionAnalysisInput object.  

```python
# Get the value of the property.
propertyValue = sectionAnalysisInput_var.initialPosition
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version January 2023  

