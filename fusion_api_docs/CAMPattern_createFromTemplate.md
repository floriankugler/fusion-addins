# CAMPattern.createFromTemplate Method

Parent Object: [CAMPattern](CAMPattern.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates and adds operations, folders or patterns from the specified template file to the end of this folder.

## Remarks

This property has been retired. Please use createFromCAMTemplate2 in conjunction with a CreateFromCAMTemplateInput to create operations from a template file.

## Syntax

"cAMPattern_var" is a variable referencing a [CAMPattern](CAMPattern.md) object.

```python
returnValue = cAMPattern_var.createFromTemplate(templateFilePath)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns the collection containing all of the operations, folders and patterns created from the template file. |

## Parameters

| Name             | Type   | Description                         |
|------------------|--------|-------------------------------------|
| templateFilePath | string | The full path to the template file. |

## Version

Introduced in version May 2020  
Retired in version July 2024  

