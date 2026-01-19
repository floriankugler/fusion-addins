# CAMHoleRecognition.deleteMe Method

Parent Object: [CAMHoleRecognition](CAMHoleRecognition.md)  

## Description

Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted.

## Syntax

"cAMHoleRecognition_var" is a variable referencing a [CAMHoleRecognition](CAMHoleRecognition.md) object.

```python
returnValue = cAMHoleRecognition_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version May 2023  

