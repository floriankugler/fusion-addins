# ArrangeComponent.rotation Property

Parent Object: [ArrangeComponent](ArrangeComponent.md)  

## Description

Gets and sets the rotation angle of this ArrangeComponent. The value is defined in Radians, is relative to the zero direction vector returned by the zeroDirectionVector property, and is in a counterclockwise direction.  

This is only valid for 2D True Shape arrangements and is ignored for 2D rectangular and 3D arrangements.

## Syntax

"arrangeComponent_var" is a variable referencing an ArrangeComponent object.  

```python
# Get the value of the property.
propertyValue = arrangeComponent_var.rotation

# Set the value of the property.
arrangeComponent_var.rotation = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2025  

