# DocumentStockMaterialLibrary.item Method

Parent Object: [DocumentStockMaterialLibrary](DocumentStockMaterialLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Get StockMaterial by index in DocumentStockMaterialLibrary.

## Syntax

"documentStockMaterialLibrary_var" is a variable referencing a [DocumentStockMaterialLibrary](DocumentStockMaterialLibrary.md) object.

```python
returnValue = documentStockMaterialLibrary_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [StockMaterial](StockMaterial.md) | Returns the StockMaterial in the DocumentStockMaterialLibrary by given index. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | Index of the StockMaterial in the DocumentStockMaterialLibrary. |

## Version

Introduced in version September 2024  

