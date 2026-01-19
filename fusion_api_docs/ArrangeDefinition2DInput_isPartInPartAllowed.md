# ArrangeDefinition2DInput.isPartInPartAllowed Property

Parent Object: [ArrangeDefinition2DInput](ArrangeDefinition2DInput.md)  

## Description

Gets and sets if parts can be nested within void areas of other parts. This defaults to true.  

This is only used when the solver type is 2D True Shape and is ignored for 2D Rectangular solutions.

## Syntax

"arrangeDefinition2DInput_var" is a variable referencing an ArrangeDefinition2DInput object.  

```python
# Get the value of the property.
propertyValue = arrangeDefinition2DInput_var.isPartInPartAllowed

# Set the value of the property.
arrangeDefinition2DInput_var.isPartInPartAllowed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

