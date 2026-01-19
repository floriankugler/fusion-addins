# PrintSetting.duplicatePrintSettingItem Method

Parent Object: [PrintSetting](PrintSetting.md)  

## Description

Duplicates the PrintSetting item of the specified body preset.

## Syntax

"printSetting_var" is a variable referencing a [PrintSetting](PrintSetting.md) object.

```python
returnValue = printSetting_var.duplicatePrintSettingItem(name)
```

## Return Value

| Type | Description |
|----|----|
| [PrintSettingItem](PrintSettingItem.md) | Returns the specified parameters or throws exception in the case where there is no parameters with the specified id. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The body preset id of the parameters that has to be duplicated. |

## Version

Introduced in version April 2023  

