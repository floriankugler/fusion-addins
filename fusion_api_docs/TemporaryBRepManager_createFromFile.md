# TemporaryBRepManager.createFromFile Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Creates new BRepBody objects based on the contents of the specified file.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createFromFile(filename)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBodies](BRepBodies.md) | A BRepBodies collection object is returned which can contain multiple BRepBody objects. null is returned in the case where it was unable to read the file. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The full path and name of the file to read in. This can be a SMT, SMB, SAT, or SAB file. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

