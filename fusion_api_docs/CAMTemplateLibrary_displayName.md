# CAMTemplateLibrary.displayName Method

Parent Object: [CAMTemplateLibrary](CAMTemplateLibrary.md)  

## Description

Get the localized display name for a given URL. The URL must point to a folder.

## Syntax

"cAMTemplateLibrary_var" is a variable referencing a [CAMTemplateLibrary](CAMTemplateLibrary.md) object.

```python
returnValue = cAMTemplateLibrary_var.displayName(url)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns localized display name for the folder. Returns empty string for invalid URL. |

## Parameters

| Name | Type           | Description                                |
|------|----------------|--------------------------------------------|
| url  | [URL](URL.md) | The URL that defines the path to a folder. |

## Version

Introduced in version April 2023  

