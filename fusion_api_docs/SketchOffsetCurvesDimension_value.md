# SketchOffsetCurvesDimension.value Property

Parent Object: [SketchOffsetCurvesDimension](SketchOffsetCurvesDimension.md)  

## Description

Gets and sets the current value of the sketch dimension.  

In a parametric modeling design and the isDriving property is True, this is exactly equivalent to getting the parameter associated with the dimension and editing its value. Editing this property will result in the parameter value being changed. If isDriving is False, this acts as a read-only property and attempting to set it will fail.  

In a direct modeling design the parameter property will return null and this property can be used to get and set the value of the dimension because in this case, there isn't an associated parameter.  

The value is always in internal units which means that for dimensions that represent a distance, the value is in Centimeters and for dimensions representing an angle the value is in Radians.

## Syntax

"sketchOffsetCurvesDimension_var" is a variable referencing a SketchOffsetCurvesDimension object.  

```python
# Get the value of the property.
propertyValue = sketchOffsetCurvesDimension_var.value

# Set the value of the property.
sketchOffsetCurvesDimension_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version July 2022  

