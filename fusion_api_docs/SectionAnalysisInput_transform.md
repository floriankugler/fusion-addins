# SectionAnalysisInput.transform Property

Parent Object: [SectionAnalysisInput](SectionAnalysisInput.md)  

## Description

The initial position of the section plane is defined by the specified cut plane entity. Any offsets or rotations are defined by a transformation matrix that is applied to the initial position. This property allows you to get and set the transformation matrix.

## Syntax

"sectionAnalysisInput_var" is a variable referencing a SectionAnalysisInput object.  

```python
# Get the value of the property.
propertyValue = sectionAnalysisInput_var.transform

# Set the value of the property.
sectionAnalysisInput_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version January 2023  

