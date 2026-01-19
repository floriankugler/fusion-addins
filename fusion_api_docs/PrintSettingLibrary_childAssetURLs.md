# PrintSettingLibrary.childAssetURLs Method

Parent Object: [PrintSettingLibrary](PrintSettingLibrary.md)  

## Description

Get all assets under given URL.

## Syntax

"printSettingLibrary_var" is a variable referencing a [PrintSettingLibrary](PrintSettingLibrary.md) object.

```python
returnValue = printSettingLibrary_var.childAssetURLs(url)
```

## Return Value

| Type               | Description                                   |
|--------------------|-----------------------------------------------|
| [URL](URL.md)\[\] | Returns list of asset URLs at given location. |

## Parameters

| Name | Type           | Description                   |
|------|----------------|-------------------------------|
| url  | [URL](URL.md) | The URL to the parent folder. |

## Version

Introduced in version April 2023  

