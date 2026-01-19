# OperationBase.deleteMe Method

Parent Object: [OperationBase](OperationBase.md)  

## Description

Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted.

## Syntax

"operationBase_var" is a variable referencing an [OperationBase](OperationBase.md) object.

```python
returnValue = operationBase_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version May 2023  

