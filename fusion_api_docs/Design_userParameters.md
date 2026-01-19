# Design.userParameters Property

Parent Object: [Design](Design.md)  

## Description

Returns the collection of User Parameters in a design

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.userParameters
```

## Property Value

This is a read only property whose value is a [UserParameters](UserParameters.md).

## Samples

| Name | Description |
|----|----|
| [Set parameters from a csv file and export to STEP](SetParametersFromACsvFileAndExportToSTEP_Sample.md) | Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model. |

## Version

Introduced in version August 2014  

