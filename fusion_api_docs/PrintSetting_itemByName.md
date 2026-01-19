# PrintSetting.itemByName Method

Parent Object: [PrintSetting](PrintSetting.md)  

## Description

Returns the PrintSetting item of the specified body preset.

## Syntax

"printSetting_var" is a variable referencing a [PrintSetting](PrintSetting.md) object.

```python
returnValue = printSetting_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [PrintSettingItem](PrintSettingItem.md) | Returns the specified parameters or throws exception in the case where there is no parameters with the specified id. |

## Parameters

| Name | Type   | Description                           |
|------|--------|---------------------------------------|
| name | string | The body preset id of the parameters. |

## Version

Introduced in version April 2023  

