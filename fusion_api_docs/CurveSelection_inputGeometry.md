# CurveSelection.inputGeometry Property

Parent Object: [CurveSelection](CurveSelection.md)  

## Description

Get or set the value of the input geometry. If the value originates from a component instead of an occurrence, or an occurrence outside of the CAM environment, then the subpath is checked against the CAM model tree. For some child classes, this may be the same as the value property, but might also consist of fewer elements. Valid elements depend on the capabilities of the derived class. An exception is thrown if the matching fails or the given entity does not match the expected type.

## Syntax

"curveSelection_var" is a variable referencing a CurveSelection object.  

```python
# Get the value of the property.
propertyValue = curveSelection_var.inputGeometry

# Set the value of the property.
curveSelection_var.inputGeometry = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Version

Introduced in version April 2023  

