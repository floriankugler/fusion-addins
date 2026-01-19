# Data.findFolderById Method

Parent Object: [Data](Data.md)  

## Description

Returns the DataFolder identified by the input id. This can fail if there isn't a DataFolder identified with the specified id or if the current user doesn't have privileges to access the folder.

## Syntax

"data_var" is a variable referencing a [Data](Data.md) object.

```python
returnValue = data_var.findFolderById(id)
```

## Return Value

| Type | Description |
|----|----|
| [DataFolder](DataFolder.md) | Returns a DataFolder if one is found matching the input id or null if one is not found or you don't have privileges to access it. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full id of the folder will be something similar to that shown below. urn:adsk.wipprod:fs.folder:co.BdMZ64GqTAie4w3NShw23C This is also the same id that you'll obtain if you use the APS Data Management API. |

## Version

Introduced in version May 2024  

