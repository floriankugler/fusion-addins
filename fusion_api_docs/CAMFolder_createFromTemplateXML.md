# CAMFolder.createFromTemplateXML Method

Parent Object: [CAMFolder](CAMFolder.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates and adds operations, folders or patterns from the specified template content XML to the end of this folder.

## Remarks

This property has been retired. Please use createFromCAMTemplate2 in conjunction with a CreateFromCAMTemplateInput to create operations from a template file.

## Syntax

"cAMFolder_var" is a variable referencing a [CAMFolder](CAMFolder.md) object.

```python
returnValue = cAMFolder_var.createFromTemplateXML(templateXML)
```

## Return Value

| Type | Description |
|----|----|
| [OperationBase](OperationBase.md)\[\] | Returns an array containing all of the operations, folders and patterns created from the template. |

## Parameters

| Name        | Type   | Description                           |
|-------------|--------|---------------------------------------|
| templateXML | string | The full XML content of the template. |

## Version

Introduced in version April 2023  
Retired in version July 2024  

