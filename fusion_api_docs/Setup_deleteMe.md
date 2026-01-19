# Setup.deleteMe Method

Parent Object: [Setup](Setup.md)  

## Description

Deletes the operation from the document. In case of a setup or folder, all containing child operations will be deleted as well. Note: Child classes may overwrite this function and throw an exception if the object cannot be deleted.

## Syntax

"setup_var" is a variable referencing a [Setup](Setup.md) object.

```python
returnValue = setup_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version May 2023  

