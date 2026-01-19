# PrintSettingLibrary.updatePrintSetting Method

Parent Object: [PrintSettingLibrary](PrintSettingLibrary.md)  

## Description

Update a PrintSetting in the library. The library overrides the URL by given PrintSetting. Throws an error if the URL does not already point to an existing printSetting.

## Syntax

"printSettingLibrary_var" is a variable referencing a [PrintSettingLibrary](PrintSettingLibrary.md) object.

```python
returnValue = printSettingLibrary_var.updatePrintSetting(url, printSetting)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if asset was updated successfully, false otherwise. |

## Parameters

| Name | Type | Description |
|----|----|----|
| url | [URL](URL.md) | The URL to the existing asset in the library that should be updated. |
| printSetting | [PrintSetting](PrintSetting.md) | The PrintSetting that should be persisted. |

## Version

Introduced in version April 2023  

