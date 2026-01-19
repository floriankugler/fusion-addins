# ArrangeComponent.isDirectionFlipped Property

Parent Object: [ArrangeComponent](ArrangeComponent.md)  

## Description

Specifies if the direction is flipped from it's default direction.  

For a component defined by a face the default direction is defined by the selected face and the isGlobalDirectionFaceUp property of the Arrange2DDefinition associated with the parent ArrangeFeature object.  

For a component defined by an occurrence, the default direction orients the occurrence such that the largest face points downward.  

For a 3D arrange, this property is ignored and the orientation of the part is the same as it exists in the original assembly.

## Syntax

"arrangeComponent_var" is a variable referencing an ArrangeComponent object.  

```python
# Get the value of the property.
propertyValue = arrangeComponent_var.isDirectionFlipped

# Set the value of the property.
arrangeComponent_var.isDirectionFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

