# FlatPatternProduct.deleteEntities Method

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Deletes the specified set of entities that are associated with this product.

## Syntax

"flatPatternProduct_var" is a variable referencing a [FlatPatternProduct](FlatPatternProduct.md) object.

```python
returnValue = flatPatternProduct_var.deleteEntities(entities)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns True if any of the entities provided in the list were deleted. If entities were specified that can't be deleted or aren't owned by this product, they are ignored. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | [ObjectCollection](ObjectCollection.md) | An ObjectCollection containing the list of entities to delete. |

## Version

Introduced in version October 2022  

