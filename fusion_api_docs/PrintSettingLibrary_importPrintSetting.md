# PrintSettingLibrary.importPrintSetting Method

Parent Object: [PrintSettingLibrary](PrintSettingLibrary.md)  

## Description

Import a given PrintSetting at a specific location. The PrintSetting will be stored in the library. Throws an error if the given URL is read-only.

## Syntax

"printSettingLibrary_var" is a variable referencing a [PrintSettingLibrary](PrintSettingLibrary.md) object.

```python
returnValue = printSettingLibrary_var.importPrintSetting(printSetting, destinationUrl, printSettingName)
```

## Return Value

| Type | Description |
|----|----|
| [URL](URL.md) | Returns the URL of the newly imported PrintSetting, or null if the import failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| printSetting | [PrintSetting](PrintSetting.md) | The PrintSetting that should be imported. |
| destinationUrl | [URL](URL.md) | The URL to the folder where to save the PrintSetting. |
| printSettingName | string | The name that should be assigned to imported PrintSetting. The name can be extended if there already exists a PrintSetting at given location to ensure a unique name. |

## Version

Introduced in version April 2023  

