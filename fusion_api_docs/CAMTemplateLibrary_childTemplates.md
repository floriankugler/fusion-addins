# CAMTemplateLibrary.childTemplates Method

Parent Object: [CAMTemplateLibrary](CAMTemplateLibrary.md)  

## Description

Get all templates by the given parent folder URL. Returns null if there is no folder at the URL.

## Syntax

"cAMTemplateLibrary_var" is a variable referencing a [CAMTemplateLibrary](CAMTemplateLibrary.md) object.

```python
returnValue = cAMTemplateLibrary_var.childTemplates(url)
```

## Return Value

| Type | Description |
|----|----|
| [CAMTemplate](CAMTemplate.md)\[\] | Returns an array of templates contained within the specified folder URL. Returns null if the URL is not valid. |

## Parameters

| Name | Type           | Description                                      |
|------|----------------|--------------------------------------------------|
| url  | [URL](URL.md) | The URL of the folder to get the templates from. |

## Version

Introduced in version April 2023  

