# FlatPatternProduct.modifyParameters Method

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Modifies the values of many parameters all at once. Changing them all at once is more efficient than modifying them one at a time.

## Syntax

"flatPatternProduct_var" is a variable referencing a [FlatPatternProduct](FlatPatternProduct.md) object.

```python
returnValue = flatPatternProduct_var.modifyParameters(parameters, values)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if setting all of the parameters was successful. Setting multiple parameters is either all or none. If it fails to set any parameters, none of them are updated, and the method will return false. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| parameters | Parameter[] | An array of UserParameter and ModelParameter objects that you want to change the value. The parameters must all exist within the Design object you're calling this method from. They can be in any component but must be local components owned by the Design. |
| values | ValueInput[] | An array of ValueInput objects that defines the new value for each parameter defined by the "parameters" argument. This array must be the same size as the array used for the "parameters" argument, and the items in the arrays are used in the order they exist within the arrays. For example, the parameter at index 0 will use the value at index 0. If you use the createByString method to create the ValueInput, the expression of the parameter will be edited, and the effect is the same as interactively editing the expression.When you set the expression, you can include units, references to other parameters, and math operators and functions.For example, "(Length / 3) * cos(Angle)" is a valid expression for a distance parameter if the parameters "Length" and "Angle" already exist. If you use the createByReal method, the value is assigned directly and is always in the internal units for the unit type associated with the parameter.For example, if the parameter is a length, the value will ALWAYS be used as centimeters. If the parameter is an angle, the value will ALWAYS be used as radians.This is because the default design unit types for length are ignored, and internal units are ALWAYS used. |

## Version

Introduced in version October 2022  

