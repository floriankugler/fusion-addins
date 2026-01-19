# CAMTemplateLibrary.childFolderURLs Method

Parent Object: [CAMTemplateLibrary](CAMTemplateLibrary.md)  

## Description

Get all library folders under given URL.

## Syntax

"cAMTemplateLibrary_var" is a variable referencing a [CAMTemplateLibrary](CAMTemplateLibrary.md) object.

```python
returnValue = cAMTemplateLibrary_var.childFolderURLs(url)
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

