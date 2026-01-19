# StockMaterialLibrary.createFolder Method

Parent Object: [StockMaterialLibrary](StockMaterialLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Create a new folder in the library. Create the folder under given parent URL with given folder name. Add counting suffix, in case a folder with given name already exists. Throw an error if given URL does not point to a valid folder or the URL is read-only. Also throws an error if given folder name is empty.

## Syntax

"stockMaterialLibrary_var" is a variable referencing a [StockMaterialLibrary](StockMaterialLibrary.md) object.

```python
returnValue = stockMaterialLibrary_var.createFolder(parentUrl, folderName)
```

## Return Value

| Type           | Description                                 |
|----------------|---------------------------------------------|
| [URL](URL.md) | Returns the URL to the newly created folder |

## Parameters

| Name | Type | Description |
|----|----|----|
| parentUrl | [URL](URL.md) | The parent URL for the folder to be created. |
| folderName | string | Name of the new folder to be created. Must not be empty. |

## Version

Introduced in version September 2024  

