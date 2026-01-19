# CAMTemplateLibrary.updateTemplate Method

Parent Object: [CAMTemplateLibrary](CAMTemplateLibrary.md)  

## Description

Update a template in the library. The library substitutes the existing template at the URL by given template. Throws an error if the URL does not already point to an existing template. If the name member of the CAMTemplate doesn't match the name portion of the URL then this will include a rename operation and the returned URL will reflect the new name.

## Syntax

"cAMTemplateLibrary_var" is a variable referencing a [CAMTemplateLibrary](CAMTemplateLibrary.md) object.

```python
returnValue = cAMTemplateLibrary_var.updateTemplate(camTemplate, url)
```

## Return Value

| Type | Description |
|----|----|
| [URL](URL.md) | Returns the URL of the updated template, or null if the update failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| camTemplate | [CAMTemplate](CAMTemplate.md) | The template that should be persisted. |
| url | [URL](URL.md) | The URL to the existing template in the library that should be updated. |

## Version

Introduced in version April 2023  

