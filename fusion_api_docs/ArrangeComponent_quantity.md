# ArrangeComponent.quantity Property

Parent Object: [ArrangeComponent](ArrangeComponent.md)  

## Description

Specifies the quantity of this component to use in the arrange. This defaults to -1, which indicates that the global quantity is to be used.  

For a 3D arrange, this property is ignored and the quantity is always one.

## Syntax

"arrangeComponent_var" is a variable referencing an ArrangeComponent object.  

```python
# Get the value of the property.
propertyValue = arrangeComponent_var.quantity

# Set the value of the property.
arrangeComponent_var.quantity = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version January 2025  

