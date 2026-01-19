# ImportManager.createIGESImportOptions Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Creates an IGESImportOptions object that is used to import a design from IGES format. Creation of the IGESImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The IGESImportOptions supports any available options when importing from IGES format.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.createIGESImportOptions(filename)
```

## Return Value

| Type | Description |
|----|----|
| [IGESImportOptions](IGESImportOptions.md) | The created IGESImportOptions object or null if the creation failed. |

## Parameters

| Name     | Type   | Description                                          |
|----------|--------|------------------------------------------------------|
| filename | string | The filename or URL of the IGES file to be imported. |

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

