# PatternElement.transform Property

Parent Object: [PatternElement](PatternElement.md)  

## Description

Get the transform that describes this elements relative position to the parent object(s). The transform returned for the first element in a pattern will be an identity matrix.

## Syntax

"patternElement_var" is a variable referencing a PatternElement object.  

```python
# Get the value of the property.
propertyValue = patternElement_var.transform
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version November 2014  

