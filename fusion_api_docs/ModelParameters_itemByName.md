# ModelParameters.itemByName Method

Parent Object: [ModelParameters](ModelParameters.md)  

## Description

Function that returns the specified Model Parameter using the name of the parameter as it is displayed in the parameters dialog.

## Syntax

"modelParameters_var" is a variable referencing a [ModelParameters](ModelParameters.md) object.

```python
returnValue = modelParameters_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [ModelParameter](ModelParameter.md) | Returns the specified item or null if an invalid name was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the Model Parameter as it is displayed in the parameters dialog |

## Version

Introduced in version August 2014  

