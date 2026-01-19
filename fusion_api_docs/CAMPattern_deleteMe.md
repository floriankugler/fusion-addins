# CAMPattern.deleteMe Method

Parent Object: [CAMPattern](CAMPattern.md)  

## Description

Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted.

## Syntax

"cAMPattern_var" is a variable referencing a [CAMPattern](CAMPattern.md) object.

```python
returnValue = cAMPattern_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version May 2023  

