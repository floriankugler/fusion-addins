# Design.unitsManager Property

Parent Object: [Design](Design.md)  

## Description

Returns the UnitsManager object associated with this product.

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.unitsManager
```

## Property Value

This is a read only property whose value is a [UnitsManager](UnitsManager.md).

## Samples

| Name | Description |
|----|----|
| [Use inputBox to get value and evaluateExpression to validate it](InputBox_Sample.md) | Uses the UserInterface.inputBox function to get a string from the user and then validates that the strinng entered is a valid expression by using the UnitsManager.evaluateExpression function. |

## Version

Introduced in version August 2014  

