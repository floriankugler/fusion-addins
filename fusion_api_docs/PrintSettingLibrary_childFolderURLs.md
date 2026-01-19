# PrintSettingLibrary.childFolderURLs Method

Parent Object: [PrintSettingLibrary](PrintSettingLibrary.md)  

## Description

Get all library folders under given URL.

## Syntax

"printSettingLibrary_var" is a variable referencing a [PrintSettingLibrary](PrintSettingLibrary.md) object.

```python
returnValue = printSettingLibrary_var.childFolderURLs(url)
```

## Return Value

| Type               | Description                                    |
|--------------------|------------------------------------------------|
| [URL](URL.md)\[\] | Returns list of folder URLs at given location. |

## Parameters

| Name | Type           | Description                   |
|------|----------------|-------------------------------|
| url  | [URL](URL.md) | The URL to the parent folder. |

## Version

Introduced in version April 2023  

