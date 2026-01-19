# ImportManager.createFusionArchiveImportOptions Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Creates a FusionArchiveImportOptions object that imports a design from a Fusion archive format. The creation of the FusionArchiveImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The FusionArchiveImportOptions object supports the available options when importing from a Fusion archive format. This method only supports f3d files. For f3z files, you should use the DataFolder.uploadFile method.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.createFusionArchiveImportOptions(filename)
```

## Return Value

| Type | Description |
|----|----|
| [FusionArchiveImportOptions](FusionArchiveImportOptions.md) | The created FusionArchiveImportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The filename or URL of the Fusion archive file to be imported. Only f3d files can be imported. For f3z files, you should use the DataFolder.uploadFile method. |

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

