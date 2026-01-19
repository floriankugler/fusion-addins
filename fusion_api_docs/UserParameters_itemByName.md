# UserParameters.itemByName Method

Parent Object: [UserParameters](UserParameters.md)  

## Description

Function that returns the specified User Parameter using the name of the parameter as it is displayed in the parameters dialog.

## Syntax

"userParameters_var" is a variable referencing a [UserParameters](UserParameters.md) object.

```python
returnValue = userParameters_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [UserParameter](UserParameter.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the User Parameter as it is displayed in the parameters dialog |

## Samples

| Name | Description |
|----|----|
| [Set parameters from a csv file and export to STEP](SetParametersFromACsvFileAndExportToSTEP_Sample.md) | Reads data from a .csv file and sets user parameters in the model and then exports the model to STEP. When setting parameters be aware that this sample is setting user parameters. It's also possible to set model parameters but that's not demonstrated here. Also when accessing parameters, it is case sensitive so the names you use in your program much exactly match the names in the model. |

## Version

Introduced in version August 2014  

