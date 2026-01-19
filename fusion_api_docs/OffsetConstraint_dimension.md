# OffsetConstraint.dimension Property

Parent Object: [OffsetConstraint](OffsetConstraint.md)  

## Description

Returns the dimension controlling the offset distance. This can return null in the case where the dimension has been deleted. To change the offset distance you can use the parameter property of the returned dimension to get the parameter that controls the value and use properties on the parameter to change the value. This can return either a SketchOffsetCurvesDimension or a SketchOffsetDimension. A SketchOffsetCurvesDimension is created automatically when curves are offset but if it is deleted the offset can also be controlled by a SketchOffsetDimension.

## Syntax

"offsetConstraint_var" is a variable referencing an OffsetConstraint object.  

```python
# Get the value of the property.
propertyValue = offsetConstraint_var.dimension
```

## Property Value

This is a read only property whose value is a [SketchDimension](SketchDimension.md).

## Version

Introduced in version May 2016  

