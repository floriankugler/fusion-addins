# DocumentStockMaterialLibrary.update Method

Parent Object: [DocumentStockMaterialLibrary](DocumentStockMaterialLibrary.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Update the given StockMaterial in the document StockMaterial library. The update applies all changes to the stockMaterial in the document stockMaterial library and therefore on all setups that use the stockMaterial. Will error if the stockMaterial does not exist in the document stockMaterial library.

## Syntax

"documentStockMaterialLibrary_var" is a variable referencing a [DocumentStockMaterialLibrary](DocumentStockMaterialLibrary.md) object.

```python
returnValue = documentStockMaterialLibrary_var.update(stockMaterial)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the update was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| stockMaterial | [StockMaterial](StockMaterial.md) | The StockMaterial that should be updated. |

## Version

Introduced in version September 2024  

