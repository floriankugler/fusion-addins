# DerivedParameter.expression Property

Parent Object: [DerivedParameter](DerivedParameter.md)  

## Description

Gets and sets the expression used to calculate the value of the parameter. This is the equivalent of the "Expression" column in the Parameters dialog. Numeric parameters can be defined by a simple expression like "6.25", which will be interpreted based on whatever the default units are for the document. For example, if the units are set to millimeters, the value will be 6.25 mm; if the units are inches, it will be 6.25 inches. The expression can also contain the units so "6.25 in" will always be evaluated as inches regardless of the document units.  

An expression can also contain references to other parameters and use equations. For example, the expression "Length / 2" is valid for a numeric parameter as long as there is a numeric parameter named "Length". Expressions can also be used for text parameters, such as concatenating two other text parameters. For example, if there are two existing text parameters named text1 and text2, the expression for another text parameter can be "text1 + text2". More complex equations can also be used with text parameters like "if (Length < 20 mm; 'Short'; 'Long')" where "Length" is a numeric parameter. The resulting string can be obtained using the textValue property.

## Syntax

"derivedParameter_var" is a variable referencing a DerivedParameter object.  

```python
# Get the value of the property.
propertyValue = derivedParameter_var.expression

# Set the value of the property.
derivedParameter_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2026  

