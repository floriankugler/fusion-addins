# MoveFeatureInput.transform Property

Parent Object: [MoveFeatureInput](MoveFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the transform to apply to the input entities. This can describe a move (translation) or a rotation. The matrix must define an orthogonal transform. That is the axes remain perpendicular to each other and there isn't any scale or mirror defined.

## Remarks

This property is obsolete. You should now use the setToFreeMove for the equivalent functionality.

## Syntax

"moveFeatureInput_var" is a variable referencing a MoveFeatureInput object.  

```python
# Get the value of the property.
propertyValue = moveFeatureInput_var.transform

# Set the value of the property.
moveFeatureInput_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version March 2015  
Retired in version January 2023  

