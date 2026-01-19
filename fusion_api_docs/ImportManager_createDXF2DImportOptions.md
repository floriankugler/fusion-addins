# ImportManager.createDXF2DImportOptions Method

Parent Object: [ImportManager](ImportManager.md)  

## Description

Creates a DXF2DImportOptions object that is used to import 2D data to create sketches. Creation of the createDXF2DImportOptions object does not perform the import. You must pass this object to the ImportManager.importToTarget method to perform the import. The sketches created as a result of the import are available through the 'results' property of the DXF2DImportOptions.

## Syntax

"importManager_var" is a variable referencing an [ImportManager](ImportManager.md) object.

```python
returnValue = importManager_var.createDXF2DImportOptions(filename, planarEntity)
```

## Return Value

| Type | Description |
|----|----|
| [DXF2DImportOptions](DXF2DImportOptions.md) | The created DXF2DImportOptions object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filename | string | The filename of the DXF file to be imported. |
| planarEntity | [Base](Base.md) | The construction plane or planar face that defines the plane that the resulting sketches will be created on. |

## Samples

| Name | Description |
|----|----|
| [Import Manager API Sample](ImportManager_Sample.md) | Demonstrates how to import different formats to Fusion document |

## Version

Introduced in version November 2015  

