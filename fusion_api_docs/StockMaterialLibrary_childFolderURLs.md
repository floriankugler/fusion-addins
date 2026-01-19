# StockMaterialLibrary.childFolderURLs Method

Parent Object: [StockMaterialLibrary](StockMaterialLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get all library folders under given URL.

## Syntax

"stockMaterialLibrary_var" is a variable referencing a [StockMaterialLibrary](StockMaterialLibrary.md) object.

```python
returnValue = stockMaterialLibrary_var.childFolderURLs(url)
```

## Return Value

| Type               | Description                                    |
|--------------------|------------------------------------------------|
| [URL](URL.md)\[\] | Returns list of folder URLs at given location. |

## Parameters

| Name | Type           | Description                   |
|------|----------------|-------------------------------|
| url  | [URL](URL.md) | The URL to the parent folder. |

## Version

Introduced in version September 2024  

