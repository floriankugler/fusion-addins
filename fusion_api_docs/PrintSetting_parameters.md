# PrintSetting.parameters Method

Parent Object: [PrintSetting](PrintSetting.md)  

## Description

Function that returns the specified parameterTable using an enum into the collection.

## Syntax

"printSetting_var" is a variable referencing a [PrintSetting](PrintSetting.md) object.

```python
returnValue = printSetting_var.parameters(type)
```

## Return Value

| Type | Description |
|----|----|
| [CAMParameters](CAMParameters.md) | Returns the specified type of parameters or null if an invalid type was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| type | [PrintSettingItemTypes](PrintSettingItemTypes.md) | The type of the item within the collection to return. |

## Version

Introduced in version April 2023  

