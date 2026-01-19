# Arrange2DDefinition.grainDirection Property

Parent Object: [Arrange2DDefinition](Arrange2DDefinition.md)  

## Description

Defines the angle of the grain direction of the envelope. An angle of 0 is in the X direction of the envelope. You can modify the value by using the properties on the returned ModelParameter object.  

This is only valid when the solver type is True Shape and it returns null in all other cases.

## Syntax

"arrange2DDefinition_var" is a variable referencing an Arrange2DDefinition object.  

```python
# Get the value of the property.
propertyValue = arrange2DDefinition_var.grainDirection
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2025  

