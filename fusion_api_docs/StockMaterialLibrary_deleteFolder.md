# StockMaterialLibrary.deleteFolder Method

Parent Object: [StockMaterialLibrary](StockMaterialLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Delete folder by URL from the library. Any content of the folder will also be deleted. Throw an error if given URL does not point to a valid folder or the URL is read-only.

## Syntax

"stockMaterialLibrary_var" is a variable referencing a [StockMaterialLibrary](StockMaterialLibrary.md) object.

```python
returnValue = stockMaterialLibrary_var.deleteFolder(url)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if folder was deleted successfully, false otherwise |

## Parameters

| Name | Type           | Description                                   |
|------|----------------|-----------------------------------------------|
| url  | [URL](URL.md) | The URL to the folder that should be removed. |

## Version

Introduced in version September 2024  

