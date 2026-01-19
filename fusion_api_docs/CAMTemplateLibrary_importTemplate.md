# CAMTemplateLibrary.importTemplate Method

Parent Object: [CAMTemplateLibrary](CAMTemplateLibrary.md)  

## Description

Import a given template at a specific location. The template will be stored in the library. Throws an error if the given URL is read-only.

## Syntax

"cAMTemplateLibrary_var" is a variable referencing a [CAMTemplateLibrary](CAMTemplateLibrary.md) object.

```python
returnValue = cAMTemplateLibrary_var.importTemplate(camTemplate, destinationUrl)
```

## Return Value

| Type | Description |
|----|----|
| [URL](URL.md) | Returns the URL of the newly imported template, or null if the import failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| camTemplate | [CAMTemplate](CAMTemplate.md) | The template that should be imported. |
| destinationUrl | [URL](URL.md) | The URL to the folder where to save the template. |

## Version

Introduced in version April 2023  

