# CAMFolder.createFromCAMTemplate2 Method

Parent Object: [CAMFolder](CAMFolder.md)  

## Description

Create new operations, folders, or patterns from the specified CAMTemplate. They are added to the end of the parent setup.

## Syntax

"cAMFolder_var" is a variable referencing a [CAMFolder](CAMFolder.md) object.

```python
returnValue = cAMFolder_var.createFromCAMTemplate2(input)
```

## Return Value

| Type | Description |
|----|----|
| [OperationBase](OperationBase.md)\[\] | Returns an array containing all of the operations, folders and patterns created from the template. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CreateFromCAMTemplateInput](CreateFromCAMTemplateInput.md) | Input object that contains the template to create from and the generation mode. |

## Version

Introduced in version October 2023  

