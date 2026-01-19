# Arrange2DDefinition.isPartInPartAllowed Property

Parent Object: [Arrange2DDefinition](Arrange2DDefinition.md)  

## Description

Gets and sets if parts can be nested within void areas of other parts.  

This is only used when the solver type is 2D True Shape and is ignored for 2D Rectangular solutions.

## Syntax

"arrange2DDefinition_var" is a variable referencing an Arrange2DDefinition object.  

```python
# Get the value of the property.
propertyValue = arrange2DDefinition_var.isPartInPartAllowed

# Set the value of the property.
arrange2DDefinition_var.isPartInPartAllowed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

