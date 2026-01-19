# DocumentStockMaterialLibrary.setupsByStockMaterial Method

Parent Object: [DocumentStockMaterialLibrary](DocumentStockMaterialLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns all setups that use the given StockMaterial. The StockMaterial must exist in the document StockMaterial library. Raises an error if the StockMaterial is not in the document.

## Syntax

"documentStockMaterialLibrary_var" is a variable referencing a [DocumentStockMaterialLibrary](DocumentStockMaterialLibrary.md) object.

```python
returnValue = documentStockMaterialLibrary_var.setupsByStockMaterial(stockMaterial)
```

## Return Value

| Type                   | Description                                    |
|------------------------|------------------------------------------------|
| [Setup](Setup.md)\[\] | Returns setups using a specific StockMaterial. |

## Parameters

| Name | Type | Description |
|----|----|----|
| stockMaterial | [StockMaterial](StockMaterial.md) | The StockMaterial to search for setups. The StockMaterial must exist in the document. |

## Version

Introduced in version September 2024  

