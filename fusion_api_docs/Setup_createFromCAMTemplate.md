# Setup.createFromCAMTemplate Method

Parent Object: [Setup](Setup.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Create new operations, folders, or patterns from the specified CAMTemplate. They are added to the end of the parent setup.

## Remarks

This property has been retired. Please use createFromCAMTemplate2 in conjunction with a CreateFromCAMTemplateInput to create operations from a template file.

## Syntax

"setup_var" is a variable referencing a [Setup](Setup.md) object.

```python
returnValue = setup_var.createFromCAMTemplate(camTemplate)
```

## Return Value

| Type | Description |
|----|----|
| [OperationBase](OperationBase.md)\[\] | Returns an array containing all of the operations, folders and patterns created from the template. |

## Parameters

| Name | Type | Description |
|----|----|----|
| camTemplate | [CAMTemplate](CAMTemplate.md) | The CAMTemplate object to use to create the new operation, folder, or pattern. |

## Version

Introduced in version April 2023  
Retired in version July 2024  

