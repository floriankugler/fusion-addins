# CAMPattern.createFromCAMTemplate Method

Parent Object: [CAMPattern](CAMPattern.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates and adds operations, folders or patterns from the specified CAMTemplate to the end of this folder.

## Remarks

This property has been retired. Please use createFromCAMTemplate2 in conjunction with a CreateFromCAMTemplateInput to create operations from a template file.

## Syntax

"cAMPattern_var" is a variable referencing a [CAMPattern](CAMPattern.md) object.

```python
returnValue = cAMPattern_var.createFromCAMTemplate(camTemplate)
```

## Return Value

| Type | Description |
|----|----|
| [OperationBase](OperationBase.md)\[\] | Returns an array containing all of the operations, folders and patterns created from the template. |

## Parameters

| Name        | Type                           | Description                     |
|-------------|--------------------------------|---------------------------------|
| camTemplate | [CAMTemplate](CAMTemplate.md) | The CAMTemplate object to apply |

## Version

Introduced in version April 2023  
Retired in version July 2024  

