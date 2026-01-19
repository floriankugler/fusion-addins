# ImportManager.importToNewDocument Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Executes the import operation to import a file (of the format specified by the input ImportOptions object) to a new document.  

This method does not support the DXF2DImportOptions or SVGImportOptions objects. Use ImportToTarget or ImportToTarget2 for those types.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.importToNewDocument(importOptions)
```

## Return Value

| Type | Description |
|----|----|
| [Document](Document.md) | Returns the newly created Document object or null if the creation failed. A new unnamed, unsaved document will be opened in Fusion 360 as a result. |

## Parameters

| Name | Type | Description |
|----|----|----|
| importOptions | [ImportOptions](ImportOptions.md) | An ImportOptions object that is created using one of the create methods on the ImportManager object. This defines the type of file and any available options supported for that file type. |

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

