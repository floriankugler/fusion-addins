# TemporaryBRepManager.exportToFile Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Exports the input bodies to the specified file.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.exportToFile(bodies, filename)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the export was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| bodies | BRepBody\[\] | An array of BRepBody objects that you want to export. |
| filename | string | The filename to write the BRepBody objects to. The type of file to create is inferred from the extension of the file. The valid extensions are ".sat" and ".smt". |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

