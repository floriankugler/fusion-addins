# DataFile.deleteMe Method

Parent Object: [DataFile](DataFile.md)  

## Description

Deletes this DataFile. This can fail if this file is referenced by another file or is currently open.

## Syntax

"dataFile_var" is a variable referencing a [DataFile](DataFile.md) object.

```python
returnValue = dataFile_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version September 2016  

