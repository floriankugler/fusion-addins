# PrintSettingLibrary.printSettingAtURL Method

Parent Object: [PrintSettingLibrary](PrintSettingLibrary.md)  

## Description

Get a specific PrintSetting by the given URL. Returns null if the URL does not exist.

## Syntax

"printSettingLibrary_var" is a variable referencing a [PrintSettingLibrary](PrintSettingLibrary.md) object.

```python
returnValue = printSettingLibrary_var.printSettingAtURL(url)
```

## Return Value

| Type | Description |
|----|----|
| [PrintSetting](PrintSetting.md) | Returns the PrintSetting for a valid URL, returns null otherwise. |

## Parameters

| Name | Type           | Description                               |
|------|----------------|-------------------------------------------|
| url  | [URL](URL.md) | The URL to the PrintSetting to be loaded. |

## Version

Introduced in version April 2023  

