# CAMTemplateLibrary.templateAtURL Method

Parent Object: [CAMTemplateLibrary](CAMTemplateLibrary.md)  

## Description

Gets a specific template specified by the given URL. Returns null if the specified template does not exist.

## Syntax

"cAMTemplateLibrary_var" is a variable referencing a [CAMTemplateLibrary](CAMTemplateLibrary.md) object.

```python
returnValue = cAMTemplateLibrary_var.templateAtURL(url)
```

## Return Value

| Type | Description |
|----|----|
| [CAMTemplate](CAMTemplate.md) | Returns the template for a valid URL, returns null otherwise. |

## Parameters

| Name | Type           | Description                            |
|------|----------------|----------------------------------------|
| url  | [URL](URL.md) | The URL to the template to be fetched. |

## Version

Introduced in version April 2023  

