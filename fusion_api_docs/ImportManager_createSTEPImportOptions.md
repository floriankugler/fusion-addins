# ImportManager.createSTEPImportOptions Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Creates an STEPImportOptions object that's used to import a design from STEP format. Creation of the STEPImportOptions object does not perform the import. You must pass this object to one of the ImportManager import methods to perform the import. The STEPImportOptions supports any available options when importing from STEP format.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.createSTEPImportOptions(filename)
```

## Return Value

| Type | Description |
|----|----|
| [STEPImportOptions](STEPImportOptions.md) | The created STEPImportOptions object or null if the creation failed. |

## Parameters

| Name     | Type   | Description                                          |
|----------|--------|------------------------------------------------------|
| filename | string | The filename or URL of the STEP file to be imported. |

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version September 2015  

