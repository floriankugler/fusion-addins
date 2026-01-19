# PrintSetting.deletePrintSettingItem Method

Parent Object: [PrintSetting](PrintSetting.md)  

## Description

Deletes the PrintSettingItem of the specified body preset. Throws an exception when the name does not match any available PrintSettingItems or when trying to delete the default PrintSettingItem.

## Syntax

"printSetting_var" is a variable referencing a [PrintSetting](PrintSetting.md) object.

```python
returnValue = printSetting_var.deletePrintSettingItem(name)
```

## Parameters

| Name | Type   | Description                                                  |
|------|--------|--------------------------------------------------------------|
| name | string | The body preset id of the parameters that has to be deleted. |

## Version

Introduced in version April 2023  

