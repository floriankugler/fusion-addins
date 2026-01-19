# Occurrence.replace Method

Parent Object: [Occurrence](Occurrence.md)  

## Description

Replaces this occurrence or all occurrences that reference the same external component with a new component.  

This method will fail if the occurrence is not referencing an external component.

## Syntax

"occurrence_var" is a variable referencing an [Occurrence](Occurrence.md) object.

```python
returnValue = occurrence_var.replace(newFile, replaceAll)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the replacement was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| newFile | [DataFile](DataFile.md) | Specifies the DataFile you want to use as the replacement. The DataFile specified must exist in the same hub as the parent assembly. |
| replaceAll | boolean | Indicates if you want to replace only this single occurrence or all occurrences that reference the same external design. |

## Version

Introduced in version October 2023  

