# ImportManager.createSATImportOptions Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Creates an SATImportOptions object that's used to import a design from SAT format. Creation of the SATImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The SATImportOptions supports any available options when importing from SAT format.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.createSATImportOptions(filename)
```

## Return Value

| Type | Description |
|----|----|
| [SATImportOptions](SATImportOptions.md) | The created SATImportOptions object or null if the creation failed. |

## Parameters

| Name     | Type   | Description                                         |
|----------|--------|-----------------------------------------------------|
| filename | string | The filename or URL of the SAT file to be imported. |

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

